"""XLSX 解析器:openpyxl 读取,先定位表头行再逐数据行映射,支持合并单元格表头拼接。"""

import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import openpyxl

from parser.base_parser import BaseParser
from parser.field_mapping import extract_file_year, map_row
from util.log_util import get_logger
from util.noise_filter import is_noise_sheet, record_noise
logger = get_logger(__file__)

HEADER_SCAN_ROWS = 20  # 只在前 N 行内查找表头行(真实文件常有多行封面/标题),避免数据行被误判
MAX_XLSX_SIZE = 5 * 1024 * 1024  # xlsx 超过该大小 → 提示并跳过解析(人工优化大文件)

# 分析产物目录:表头诊断/噪声名单/扫描报告(供人工分析,完善表头信号)
ANALY_DIR = Path(__file__).resolve().parent.parent / 'analy'
HEADER_DIAGNOSE_FILE = ANALY_DIR / 'sheet_headers_diagnose.txt'
# 统计汇总表判定:表头命中汇总特征 且 不含项目特征 → 无项目 sheet,不入库
STAT_SUMMARY_RE = re.compile(r'合计|总计|个数|总数|小计')
STAT_PROJECT_RE = re.compile(r'项目名称|项目名|建设内容|建设规模|项目清单')


class XlsxParser(BaseParser):
    """XLSX 重点清单解析:表头行(前 10 行内)之后的数据行逐行映射。"""

    SUPPORTED_EXT = ('.xlsx',)

    def parse(self, file_path: str) -> List[Dict[str, Any]]:
        """遍历工作簿的全部 sheet(每 sheet 一个行业分类,如 内蒙古文件 11 个 sheet)。

        超过 MAX_XLSX_SIZE 的文件跳过解析(提示人工优化);
        小文件非 read_only 加载以读取合并单元格(二级表头拼接、表头列错位检查)。
        """
        if os.path.getsize(file_path) > MAX_XLSX_SIZE:
            logger.warning(
                f"{file_path}: xlsx 文件超过 {MAX_XLSX_SIZE // 1024 // 1024}MB,"
                f"跳过解析(建议人工拆分/优化后重跑)")
            return []
        self.file_year = extract_file_year(file_path)
        workbook = openpyxl.load_workbook(file_path, data_only=True, read_only=False)
        try:
            projects: List[Dict[str, Any]] = []
            for sheet in workbook.worksheets:
                try:
                    projects.extend(self._parse_sheet(file_path, sheet))
                except Exception as ex:
                    # 单 sheet 失败(如 文件内部 XML 损坏)不影响其他 sheet
                    logger.warning(f"{file_path}[{sheet.title}] 解析跳过: {ex}")
            return self.filter_blank_projects(projects)
        finally:
            workbook.close()

    def _parse_sheet(self, file_path: str, sheet: Any) -> List[Dict[str, Any]]:
        """解析单个 sheet:定位表头 → 数据行映射,维护分类上下文。"""
        header_map, header_idx, header_rows,valid_len = self._locate_header(sheet)
        # 统计汇总表检测(无项目,如 泸州 "政府投资前期单位汇总"):
        # 表头命中 合计/个数/总数 且不含 项目名称/建设内容 → 不入库,记入 noise 名单
        if self._is_statistics_sheet(header_rows):
            record_noise(file_path, sheet.title,
                         " ".join(str(c).strip() for row in header_rows[:3]
                                  for c in row if c is not None and str(c).strip())[:60],
                         reason='统计汇总表(表头含合计/个数/总数,无项目名称/建设内容),不入库')
            logger.warning(f"{file_path}[{sheet.title}]: 判定为统计汇总表(无项目),已跳过并记录名单")
            return []
        # 省份汇总表检测(如 "第一批(截止2025.01.24)":数据第 2 列为省份名)→ 干扰,记录名单
        is_summary, sample = self._is_province_summary(sheet,valid_len=valid_len)
        if is_summary:
            record_noise(file_path, sheet.title, sample)
            logger.warning(f"{file_path}[{sheet.title}]: 判定为各省汇总表干扰数据,已跳过并记录名单")
            return []
        if header_map is None:
            # 有表头但字段未匹配(FIELD_ALIASES 未覆盖)→ 记录表头到诊断文件,日志输出供查看;
            # 本 sheet 暂走两列式退化解析,待人工完善表头信号后自动修正
            self._record_unknown_header(file_path, sheet.title, header_rows)
            # 两列式退化解析:各省摘要清单(分类|项目名,无表头)
            two_col = self._parse_two_column(sheet,valid_len=valid_len)
            if two_col:
                return self._filter_noise(file_path, sheet.title, two_col)
            logger.warning(f"{file_path}[{sheet.title}]: 前 {HEADER_SCAN_ROWS} 行未找到表头,跳过")
            return []

        projects: List[Dict[str, Any]] = []
        context: Dict[str, str] = {}  # 分类上下文:category 行业分类 / project_type 建设性质

        # sheet 名:行业分类 → 初始 category;建设性质(如"重点预备"/"续建项目")→ 初始 project_type;
        # 性质类 sheet 名(如 "续建项目")不再作为 category;记录供"未纳入 project 时存 extra"判定
        sheet_project_type = self._sheet_project_type(sheet.title)  # project_type
        sheet_category = self._sheet_category(sheet.title)
        if sheet_project_type:
            context['project_type'] = sheet_project_type
            context['sheet_type'] = sheet_project_type
            if sheet_category in (sheet_project_type, sheet_project_type + '项目'):
                sheet_category = ''
        if sheet_category:
            context['category'] = sheet_category
            context['sheet_category'] = sheet_category

        # 合并单元格(0-based):表头构造(父标题合并化)与表头列错位修正共用
        merged = [(r.min_row - 1, r.max_row - 1, r.min_col - 1, r.max_col - 1)
                  for r in sheet.merged_cells.ranges]
        # 表头行自身是否横向合并(父标题,如 "2020年计划" 合并跨列)→ 子表头合并的前提
        header_merged = any(chi > clo and rlo <= header_idx <= rhi
                            for rlo, rhi, clo, chi in merged)
        # merged_ranges:父标题仅认横向合并单元格(上方非合并短文本不再作父标题)
        headers, header_idx = self._build_headers(header_rows, header_idx,
                                                  header_merged, merged)
        # 合并后的表头重建列映射(子表头行可能带来新字段,如 "2020年计划-计划投资")
        from parser.field_mapping import build_header_map
        header_map = build_header_map(headers)
        # 普遍数据行非空列数(分组行判定的动态基准)
        all_rows = [list(r) for r in sheet.iter_rows(max_col=valid_len if valid_len>0 else 50, values_only=True)]
        # 统计普遍有效数据项，1. 不过滤小于最大有效项的数据行，2. 有效项/普遍有效项<0.2，为分类行。（暂定）
        max_project_num = len(all_rows)
        normal_cols = BaseParser._normal_cols(all_rows, header_map)
        # project_name 候选列:修正前后的原始列 + 数据行合并单元格覆盖的相邻列——
        # 数据行名称可能落在任一列(合并单元格只首格有值,如 芜湖 B:C 合并名称在左格、
        # 宁夏 表头修正后主列反而为空),主列取空时回退候选列
        orig_pname = next((c for c, f in header_map.items() if f == 'project_name'), None)
        header_map = BaseParser._fix_merged_header(header_map, merged, header_idx)
        header_map = BaseParser._fix_numeric_project_col(header_map, all_rows, header_idx)
        cur_pname = next((c for c, f in header_map.items() if f == 'project_name'), None)
        pname_candidates = sorted({c for c in (cur_pname, orig_pname) if c is not None})
        if cur_pname is not None and cur_pname >= 1 \
                and header_map.get(cur_pname - 1) is None:
            # 数据行横向合并覆盖 project_name 及左邻列(如 芜湖 "B14:C14")
            # → 名称可能落在左格,左邻列作候选;仅限相邻一列,防止宽合并
            # (如 "A:K")把远处未映射列误当候选
            # 仅数据行区域的横向合并(rlo > header_idx),排除文件标题行合并(如 A1:D1)
            if any(rlo > header_idx and clo <= cur_pname - 1 and cur_pname <= chi and chi > clo
                   for rlo, rhi, clo, chi in merged):
                pname_candidates.append(cur_pname - 1)
            pname_candidates = sorted(set(pname_candidates))
        # 表头之前的行:分类标题(如 "一、基础设施项目(100项)")计入上下文;
        # 装饰行(备注/正文标签/清单概况·总数描述,如 "项目总数246个(新开工73个…)",
        # 项目概述 前言)→ 跳过且**不设任何 category**(与数据区 is_prose_row 同口径,
        # 防止概况句带括号统计等 hint 被当分类行污染后续项目 category)
        for row in header_rows[:header_idx]:
            joined = " ".join(
                str(c).strip() for c in row if c is not None and str(c).strip())
            if BaseParser.is_decor_text(joined):
                continue
            self.apply_category(joined, context)
        # 宽松规则文件级统计:数据行 ≥80% 有业务文本 + 潜在分类行多数无暗示条件
        full_field_sheet, plain_category_file = self._calc_full_field_stats(
            header_map, all_rows, header_idx, pname_candidates)
        # 目录+正文 单行表头 sheet 预扫描(招商手册,如 广西(第一批) 目录后的正文区):
        # 正文区 = 已见 ≥5 个编号行后、出现 ≥3 个连续无序号行,且**该 run 之后不再有
        # 编号行**——目录/清单编号行居多的极简 sheet(如 汉中)不会命中;正文区行全为
        # 单列排版噪声(城市短名/目录名重排/字段标签/续段碎片/落款行),整体不入库。
        # 仅 header_map ≤1 列(纯 序号+名称 类)启用,多列表不参与。
        prose_start = -1  # 正文区起始行(0-based all_rows 下标),-1 = 无正文区
        minimal_numbered = 0  # 极简 sheet 含纯数字序号的行数(供窄化分组 allow_city 用)
        if len(header_map) <= 1:
            numbered_cnt = 0
            unnum_run = 0
            run_start = -1
            for j in range(header_idx + 1, len(all_rows)):
                row_j = all_rows[j]
                if not self.is_data_row(row_j) or self.skip_summary_row(row_j):
                    continue
                has_num = any(c is not None and str(c).strip()
                              and self._is_number(str(c).strip()) for c in row_j)
                if has_num:
                    numbered_cnt += 1
                    unnum_run = 0
                    run_start = -1
                    continue
                if unnum_run == 0:
                    run_start = j
                unnum_run += 1
                if numbered_cnt >= 5 and unnum_run >= 3:
                    # run 之后仍出现编号行(层级分类标题夹在编号清单中)→ 非正文区
                    if any(c is not None and str(c).strip()
                           and self._is_number(str(c).strip())
                           for row_k in all_rows[j + 1:] for c in row_k):
                        continue
                    prose_start = run_start
                    break
            minimal_numbered = numbered_cnt
        # header_idx 为 0-based,数据行从表头下一行(1-based header_idx + 2)开始
        # 金额单位
        investment_unit = BaseParser._get_investment_unit(all_rows[:header_idx],headers,header_map)
        for i, row in enumerate(all_rows[header_idx + 1:], start=header_idx + 1):
            cells = list(row)
            if i == 15-1:
                pass
            # 跳过空行，跳过汇总行
            if not self.is_data_row(cells) or self.skip_summary_row(cells):
                continue
            # 说明行(如 开州附件2 "下列12个子项目"):不产生项目、不参与分类判断
            if any(re.match(r'^(下列|详见|见下表|附后|备注)', str(c).strip())
                   for c in cells if c is not None and str(c).strip()
                   and not self._is_placeholder(str(c).strip())):
                continue
            # 正文区行(预扫描 prose_start 起,见上):不入库、不参与分组/分类判断
            if prose_start >= 0 and i >= prose_start:
                continue
            # 数据行(业务字段列含非纯数字文本,header_map 列语义)→ 直接映射为项目,
            # 不参与 group/性质标题/分类判断;
            # group 判断与分类检测同路径:先排除业务数据行,非业务行再依次识别
            # 分组行 → 性质标题行 → 分类行(分类行见下方 suspect_row 分支)
            is_biz_row = BaseParser.is_business_data_row(cells, header_map)
            if not is_biz_row:
                # 装饰行统一判定(is_prose_row):备注/注记说明行、招商简介正文
                # (字段标签/超长段落)、清单概况/总结句(如 "重大前期项目92个,
                # 总投资494亿元。其中,政府投资项目54个…")→ 直接跳过
                if BaseParser.is_prose_row(cells):
                    continue
                # 极简清单(仅 序号+名称/目录 结构,header_map ≤1 列)无多列分组行形态,
                # 但城市/地区分组行以单格短名出现(如 广西目录 "南宁市"、正文对齐变体
                # "南 宁 市")→ 窄化分组检测(县州盟省/机构后缀 + 短名 市/区);
                # 单格真项目名(如 汉中 "206|汉中综合保税区" 尾"区")超出短名长度不误弃。
                # 多列映射表(有 单位/责任/投资 等列结构)→ 责任单位/地区分组行检测
                # (组名行 = 组名+计数+金额,如 "['','南宁市人民政府','16',...,金额]")
                if len(header_map) <= 1:
                    # allow_city:sheet 完全无编号行(纯名称单列清单)→ 关闭 市/区 短名
                    # 分组判定,避免 "xx小区/园区" 短名真项目被当城市分组丢弃
                    if BaseParser.is_group_row_minimal(
                            cells, allow_city=minimal_numbered > 0):
                        continue
                else:
                    if self.is_group_row(cells):
                        continue
                    if BaseParser.is_group_header_row(cells, header_map, normal_cols):
                        continue
                # 建设性质标题行:单格纯词(如 安徽 "续建"/"计划开工")或性质分组行
                # (如 贵港 "计划新开工项目|19|金额",序号列空;该文件无建设性质列,
                # 性质由分组行提供)→ 更新 project_type 上下文
                build_type = BaseParser.group_type_title(cells, header_map)
                if build_type:
                    context['project_type'] = build_type
                    continue
            # 合并单元格分类列识别:前提是 header_map 存在 category 映射列
            # (表头命中 category 别名,如 "项目类型"/"领域分类"),且该列有数据行合并
            # 单元格(分类信息存于合并首格,如 内蒙古 col0"项目类型" / col1"（一）xxx")。
            # 识别范围 = 覆盖 category 列或其相邻未映射列的合并块所占列;
            # 不再无差别处理所有 col0/col1(序号/子序号列不误走分类判断)
            cat_cols = [c for c, f in header_map.items() if f == 'category']
            if cat_cols:
                cat_scope = set()
                for rlo, rhi, clo, chi in merged:
                    if rlo <= header_idx:
                        continue  # 表头及之前的合并(文件标题行等)不算
                    cols = range(clo, chi + 1)
                    if any(c in cat_cols for c in cols) or any(
                            abs(c - cc) == 1 and header_map.get(c) is None
                            for c in cols for cc in cat_cols):
                        cat_scope.update(cols)
                if cat_scope:
                    for cat_col in sorted(cat_scope):
                        v = str(cells[cat_col] or '').strip()
                        if v:
                            self.apply_category(v, context)
            # 数字过滤:分类行的项目数(如 昆明 "一|农林水利|14|None|金额|金额")
            # 紧随文字之后、整型、小于 max_project_num、后一单元格为空 → 保留(不过滤),
            # 分类识别成功时作为声明项目数;其余数字(金额/序号等)照常过滤
            non_empty: List[str] = []
            cat_count: Optional[int] = None
            for ci, c in enumerate(cells):
                s = str(c).strip() if c is not None else ''
                if not s:
                    continue
                if self._is_number(s) or self._is_placeholder(s):
                    if self._is_project_count(cells, ci, s, max_project_num):
                        non_empty.append(s)
                        if cat_count is None:
                            cat_count = int(s)
                    continue
                non_empty.append(s)
            # 数据行(业务字段列含非纯数字文本,如 责任单位/建设性质/建设年限/项目业主)→
            # 不参与分类判断:干扰源(建设内容/项目名中的 "（N个）")在名称/内容列,
            # 由 header_map 的列语义识别数据行,避免兜底误判为分类
            # (与上方 group 检测共用同一先排除业务数据行的判定)
            suspect_row = not is_biz_row
            if suspect_row:
                # 清单概况/统计说明行(文本级统一判定 _is_overview_sentence,如 奉节
                # row7 "2023年续建项目共85个,总投资338…"、重庆/各区 "重大前期项目
                # 92个,总投资494亿元。其中,政府投资项目54个…" 前言)——多文本格/带
                # 序号的概况句也在此拦截(单文本格已在 is_prose_row 拦):
                # → 跳过,不产生项目、不设分类(仅在非业务行路径,不误伤数据行)
                if BaseParser._is_overview_sentence(
                        " ".join(str(c).strip() for c in cells
                                 if c is not None and str(c).strip())):
                    continue
                # 词表外分类行宽松标志:文件级(数据行 ≥80% 有业务文本 + 潜在分类行
                # 多数无统计暗示)+ 行级无业务文本 → m2/m3/单格行 词表失败时放宽判分类
                valid_num = len([
                    cells[i] for i in header_map
                    if cells[i] is not None
                       and str(cells[i]).strip()
                       and not self._is_number(cells[i])
                       and not self._is_placeholder(cells[i])
                ])
                # print(f'匹配后有效数据：{valid_num}个，有效比例：{round(valid_num/normal_cols*100, 2)}%')
                relax_ok = full_field_sheet and plain_category_file \
                    and not self._has_biz_text(cells, header_map)
                if relax_ok:
                    context['_relax'] = True
                # 单格分类行(分类独立一行,如 "1、合肥市(915个)"、"续建项目(597个)")→ 分类上下文
                if len(non_empty) == 1 and len(header_map) > 1:
                    if self.classify_single_row(non_empty[0], context, header_map):
                        if relax_ok:
                            context.pop('_relax', None)
                        continue
                joined = " ".join(non_empty)
                # 行尾括号整数统计格式(如 "城镇（含园区）基础设施类（52）"/"合计(2617)"):
                # 有效数据项少于 normal_cols 才记入分类;数据行(有效项 ≥ normal_cols,
                # 如 "某项目（2）" 多列行)不参与分类判断
                if re.search(r'[（(]\s*共?\s*\d+\s*[)）]\s*$', joined) and len(non_empty) >= normal_cols:
                    pass
                elif valid_num/normal_cols <= 0.2:
                    # 潜在分类行有效匹配数据占比普遍有效匹配数据
                    if cat_count is not None:
                        context['declared_count'] = cat_count
                    # 分类
                    if self.apply_category(joined, context, type='valid_normal_ratio'):
                        if relax_ok:
                            context.pop('_relax', None)
                        continue
                else:
                    # 分类行项目数(紧随文字后的整型,如 昆明 "一|农林水利|14|None|…"):
                    # 分类识别成功时作为声明项目数;识别后清理,防残留到下一行
                    if cat_count is not None:
                        context['declared_count'] = cat_count
                    if self.apply_category(joined, context, type='joined_non_empty'):  # 分类行，跳过
                        if relax_ok:
                            context.pop('_relax', None)
                        continue
                    context.pop('declared_count', None)
                    if relax_ok:
                        context.pop('_relax', None)
            project = self._map_cells(header_map, cells, headers, pname_candidates, investment_unit)
            name = project.get('project_name')
            if not name:
                continue
            # 疑似分类/分组行:该文件数据行普遍有业务文本(full_field_sheet),而本行
            # 六字段(含建设内容)全空,分类判断也未识别 → 成项目大概率是漏网的
            # 分类/单位行(如 责任单位 "自治区消防救援总队")→ 备注标记供人工核查。
            # 用 _has_biz_text(含 construction_content)判定,避免"名称+内容"型
            # 文件(数据行无 单位/地点 等映射字段)被整体误标
            if full_field_sheet and not self._has_biz_text(cells, header_map) \
                    and not project.get('category') and not project.get('project_type'):
                project['remark'] = '疑似分类/单位字段行(无业务字段),请人工核查'
            # 分类名过滤仅对少列行(≤2 个非空);多列数据行即使项目名以"(1)"开头也保留
            # (如 宁夏 "(1)宁夏泽恺三道山风电项目" 是光伏/风电分类下的子序号项目)
            if len(non_empty) <= 2 and self.is_category_name(name):
                continue
            # context.get('category') and project.get('category') 互补
            self._resolve_row_context(project,context,' '.join(map(str, cells)))
            # sheet 名未纳入 project(category/project_type 均未体现)→ 存入 extra
            sheet_cat = context.get('sheet_category')
            sheet_type = context.get('sheet_type')
            cat_used = sheet_cat and (project.get('category') == sheet_cat
                                      or str(project.get('category', '')).startswith(sheet_cat + '-'))
            type_used = sheet_type and project.get('project_type') == sheet_type
            if not cat_used and not type_used and (sheet_cat or sheet_type):
                project.setdefault('extra_fields', {})['sheet'] = sheet_cat or sheet_type
            project['source_row'] = i + 1  # 1-based 文件行号
            projects.append(project)
        return self._filter_noise(file_path, sheet.title, projects)

    @staticmethod
    def _filter_noise(file_path: str, sheet_name: str,
                      projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """干扰 sheet 识别(各省汇总表):数据不入库,记录到 noise_sheets.json。"""
        if is_noise_sheet(projects):
            record_noise(file_path, sheet_name, projects[0].get('project_name', ''))
            logger.warning(f"{file_path}[{sheet_name}]: 判定为各省汇总表干扰数据,已跳过并记录名单")
            return []
        return projects

    @staticmethod
    def _is_statistics_sheet(header_rows: List[List[Any]]) -> bool:
        """统计汇总表判定(无项目,如 泸州 "政府投资前期单位汇总" 等):

        表头区(前 20 行)命中汇总特征(合计/总计/个数/总数/小计)
        且不含项目特征(项目名称/项目名/建设内容/建设规模/项目清单)。
        """
        text = " ".join(str(c).strip() for row in header_rows
                        for c in row if c is not None and str(c).strip())
        if not STAT_SUMMARY_RE.search(text):
            return False
        # 项目特征用去空格文本匹配(表头如 "项 目 名 称" 带空格,如 宁夏)
        return not STAT_PROJECT_RE.search(re.sub(r'\s+', '', text))

    def _record_unknown_header(self, file_path: str, sheet_name: str,
                               header_rows: List[List[Any]]) -> None:
        """表头诊断:有表头信号(≥2 个非空单元格)但 find_header 未匹配字段
        (FIELD_ALIASES 未覆盖)→ 追加记录到 analy/sheet_headers_diagnose.txt,
        日志输出表头文本供查看;无表头信号(封面/描述等)不记录。"""
        lines = []
        for row in header_rows[:8]:
            texts = [str(c).strip() for c in row
                     if c is not None and str(c).strip()
                     and not self._is_placeholder(str(c).strip())]
            if len(texts) >= 2:
                lines.append("|".join(texts))
        if not lines:
            return
        sample = " / ".join(lines[:2])[:120]
        logger.warning(f"[{sheet_name}] 有表头但字段未匹配(两列式兜底): {sample}")
        try:
            ANALY_DIR.mkdir(parents=True, exist_ok=True)
            block = f"=== {Path(file_path).name} | {sheet_name} ===\n{sample}\n"
            existing = HEADER_DIAGNOSE_FILE.read_text(encoding='utf-8') \
                if HEADER_DIAGNOSE_FILE.exists() else ""
            if f"| {sheet_name} ===" not in existing:  # 按 sheet 去重
                with open(HEADER_DIAGNOSE_FILE, 'a', encoding='utf-8') as f:
                    f.write(block)
        except OSError as ex:
            logger.warning(f"表头诊断记录失败: {ex}")

    @staticmethod
    def _is_province_summary(sheet: Any,valid_len:int=0) -> tuple[bool, str]:
        """省份汇总表检测:数据行第 2 列多为省份名(如 "1|北京市|500个…")。

        判定条件:省份名行占比 ≥80%(覆盖各省汇总表与省→地级市对照表)。
        """
        from util.province_names import PROVINCE_NAMES
        checked = 0
        prov = 0
        sample = ''
        for row in sheet.iter_rows(max_col=valid_len if valid_len>0 else 50,values_only=True):
            cells = list(row)
            if len(cells) < 2:
                continue
            v1 = str(cells[1] or '').strip()
            if not v1:
                continue
            checked += 1
            if v1 in PROVINCE_NAMES:
                prov += 1
                if not sample:
                    sample = v1
        if checked >= 3 and prov / checked >= 0.8:
            return True, sample
        return False, ''

    @staticmethod
    def _sheet_category(sheet_name: str) -> str:
        """从 sheet 名提取行业分类(如 "装备制造"、"Sheet1" → 空)。"""
        cleaned = re.sub(r'^(20\d{2}\s*年?\s*)?', '', str(sheet_name))
        cleaned = re.sub(r'(【打印】|重点项目|项目清单|清单|计划|进度表|表|名单|汇总|总表|附件\d*|详情)$', '', cleaned)
        # 报告性 sheet 名(如 "2021年城市建设重点项目统计表")是文件标题,非行业分类
        if re.search(r'统计|情况|台账', cleaned):
            return ''
        # 默认 sheet 名(Excel 导出/复制常见)非行业分类:Sheet/Table 后可带空格与编号
        cleaned = re.sub(r'^(sheet|table)\s*\d*$', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'[（(].*?[)）]', '', cleaned).strip()
        # 清洗结果 ≤1 字符(如 sheet 名"总表"→"总")或超长 → 视为无意义
        if not cleaned or len(cleaned) > 20 or len(cleaned) <= 1:
            return ''
        return cleaned[:128]

    @staticmethod
    def _sheet_project_type(sheet_name: str) -> str:
        """从 sheet 名提取建设性质(如 "重点预备" → 预备、"重点前期" → 前期),无则空。"""
        for word in ('竣工投产', '新开工', '预备', '前期', '续建', '新建', '储备', '投产'):
            if word in str(sheet_name):
                return word
        return ''

    @staticmethod
    def _build_headers(header_rows: List[List[Any]], header_idx: int,
                       header_merged: bool = False,
                       merged_ranges: Optional[List[tuple]] = None
                       ) -> tuple[List[Any], int]:
        """构造表头行并定位数据起始行(委托 base_parser.merge_header_rows)。

        header_merged: 表头行自身是否横向合并(父标题)→ 子表头向下合并的前提。
        merged_ranges: 0-based 合并范围,父标题仅认横向合并单元格。
        """
        return BaseParser.merge_header_rows(header_rows, header_idx,
                                            header_merged, merged_ranges)

    def _parse_two_column(self, sheet: Any, valid_len:int=0) -> List[Dict[str, Any]]:
        """两列式清单退化解析:第一列为分类/性质、第二列为项目名(无表头)。"""
        projects: List[Dict[str, Any]] = []
        context: Dict[str, str] = {}
        for i, row in enumerate(sheet.iter_rows(max_col=valid_len if valid_len>0 else 50,y=True), start=1):
            cells = list(row)
            first = str(cells[0] or '').strip() if cells else ''
            second = str(cells[1] or '').strip() if len(cells) > 1 else ''
            if (first and not second) or (not first and second):
                # 大段说明文本(如 "第四批-.0 河北省 703个 1.5万亿元…")→ 忽略
                text = first if first else second
                if len(text) > 20:
                    continue
                if self.classify_single_row(text, context) or self.apply_category(text, context):
                    continue
                # context['category'] = text[:128]
                # continue
            # if not second:
            #     continue
            if first:
                # 纯数字/单字符(如 序号 "1")不是分类,跳过沿用上下文分类
                if not first.isdigit() and len(first) > 1 \
                        and not self.classify_single_row(first, context) \
                        and BaseParser._looks_like_category(first):
                    context['category'] = first[:128]
            projects.append({
                'project_name': second[:255],
                'category': context.get('category', '').split('-')[-1],
                'project_type': context.get('project_type', ''),
                'source_row': i,  # 1-based 文件行号
            })
        return self.filter_blank_projects(projects)

    def _locate_header(self, sheet: Any) -> tuple[Optional[Dict[int, str]], int, List[List[Any]]]:
        """读取前 HEADER_SCAN_ROWS 行定位表头行,返回 (列映射, 表头行索引, 扫描到的行)。"""
        MAX_COL_LIMIT = 50
        header_rows: List[List[Any]] = []
        valid_len = 0
        # 1. 源头限流：防止读取 1.6w 列
        for row in sheet.iter_rows(max_row=HEADER_SCAN_ROWS, max_col=MAX_COL_LIMIT, values_only=True):
            header_rows.append(list(row))
        # 2. 纯 Python 极速截断：从右向左，找最后一个有值的列
        if header_rows and len(header_rows[0]) > 0:
            # 利用 zip(*header_rows) 转置，按列生成 Tuple，比按行遍历快得多
            cols = list(zip(*header_rows))
            valid_len = len(cols)
            for i in range(len(cols) - 1, -1, -1):
                # 只要这一列有任何非空字符串/None，就认为有效
                if any(v is not None and str(v).strip() != "" for v in cols[i]):
                    valid_len = i + 1
                    break
            # 统一截断
            if valid_len < len(header_rows[0]):
                header_rows = [row[:valid_len] for row in header_rows]

        header_map, header_idx = self.find_header(header_rows, max_scan=HEADER_SCAN_ROWS)
        return header_map, header_idx, header_rows,valid_len

    def _map_cells(self, header_map: Dict[int, str], cells: List[Any],
                   headers: Optional[List[Any]] = None,
                   pname_candidates: Optional[List[int]] = None,
                   investment_unit:Dict[Any, str]={}) -> Dict[str, Any]:
        """按列映射生成项目 dict(project_name 候选列回退见 map_row)。"""
        return map_row(header_map, cells, headers=headers, file_year=self.file_year,
                       pname_candidates=pname_candidates,investment_unit=investment_unit)

    def _is_number(self, s):
        """纯数字单元格(含千分位逗号,如 "1,584,946.56");金额/数量列不参与文本判断。

        是否保留(不过滤)由 _is_project_count 判定(需要 cells 上下文:紧随文字、
        后一单元格为空等),本方法只判断是否为数字。
        广东省2021年重点项目计划表.xlsx： -1 国铁干线项目，-1 分类。正数不被排除。
        """
        try:
            num = float(str(s).replace(',', ''))
            if num<0:
                return False
            return True
        except ValueError:
            return False

    def _is_placeholder(self, s):
        """占位符单元格(如 "——" / "--"):无意义,视为空,不参与文本/分类判断。"""
        return BaseParser._is_placeholder(s)
