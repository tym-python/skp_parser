"""XLS 解析器(xlrd):兼容 Excel 97-2003 旧格式,解析逻辑与 XlsxParser 一致。

注:xlrd 2.x 仅支持 .xls(旧二进制格式),不支持 .xlsx。
"""

import re
from typing import Any, Dict, List, Optional

import xlrd

from parser.base_parser import BaseParser
from parser.field_mapping import extract_file_year, map_row, process_total_investment_header
from util.log_util import get_logger
from util.noise_filter import is_noise_sheet, record_noise

logger = get_logger(__file__)

HEADER_SCAN_ROWS = 20  # 只在前 N 行内查找表头行


class XlsParser(BaseParser):
    """XLS 重点清单解析:遍历全部 sheet,定位表头后逐数据行映射。"""

    SUPPORTED_EXT = ('.xls',)

    def parse(self, file_path: str) -> List[Dict[str, Any]]:
        self.file_year = extract_file_year(file_path)
        workbook = xlrd.open_workbook(file_path, on_demand=True)
        try:
            projects: List[Dict[str, Any]] = []
            for sheet in workbook.sheets():
                if sheet.visibility != 0:
                    continue
                projects.extend(self._parse_sheet(file_path, sheet))
            return self.filter_blank_projects(projects)
        finally:
            workbook.release_resources()

    def _parse_two_column(self, sheet: Any) -> List[Dict[str, Any]]:
        """两列式清单退化解析:第一列为分类/性质、第二列为项目名(无表头)。

        如 2025年各省市重大项目汇总 的 "['铁路','京唐城际铁路北京隧道段']" / "['','市郊铁路东北环线']"。
        """
        projects: List[Dict[str, Any]] = []
        context: Dict[str, str] = {}
        for i, cells in enumerate(self._sheet_rows(sheet)[0], start=1):
            if i== 262-1:
                pass
            if BaseParser.is_decor_text(''.join(map(str,cells))):
                continue
            first = str(cells[0] or '').strip() if cells else ''
            second = str(cells[1] or '').strip() if len(cells) > 1 else ''
            if (first and not second) or (not first and second):
                # 大段说明文本(如 "第四批-.0 河北省 703个 1.5万亿元…")→ 忽略
                if len(first) > 20 or len(second) > 20:
                    continue
                # 分类/性质标题行(如 "铁路"、"新开工项目")
                if self.classify_single_row(first if first else second, context) or self.apply_category(first if first else second, context):
                    continue
                # context['category'] = first[:128]
                # continue
            # if not second:
            #     continue
            if first:
                # 新分类 + 项目名同行;纯数字/单字符(如 序号 "1")不是分类,跳过沿用上下文
                if not BaseParser._is_number(first) and len(first) > 1 \
                        and not self.classify_single_row(first, context) \
                        and BaseParser._looks_like_category(first):
                    context['category'] = first[:128]
            projects.append({
                'project_name': second[:255],
                'category': context.get('category', ''),
                'project_type': context.get('project_type', ''),
                'source_row': i,  # 1-based 文件行号
            })
        return self.filter_blank_projects(projects)

    def _sheet_rows(self, sheet: Any, max_row: Optional[int] = None, valid_len: Optional[int] = 0): #  -> List[List[Any]]
        """按行取 sheet 单元格值(xlrd 无迭代器,手动构造)。"""
        n = sheet.nrows if max_row is None else min(max_row, sheet.nrows)
        if n == 0:
            return [],0

        MAX_COL_LIMIT = 50

        if valid_len == 0:
            # 1. 嗅探真实的有效列数（只扫前 20 行，速度极快）
            scan_limit = min(20, n)
            # 从右向左反向扫描，寻找第一列有数据的列
            for j in range(min(sheet.ncols - 1,MAX_COL_LIMIT), -1, -1):
                has_data = False
                for i in range(scan_limit):
                    val = sheet.cell_value(i, j)
                    if val is not None and str(val).strip() != "":
                        has_data = True
                        break
                if has_data:
                    valid_len = j + 1
                    break

        # 如果整张表前 20 行全是空的，valid_len 为 0，直接返回
        if valid_len == 0:
            return [],valid_len

        # 2. 根据真实列数读取数据（将原本的 range(sheet.ncols) 替换为 range(valid_len)）
        return [sheet.row_values(i)[:valid_len] for i in range(n)],valid_len
        # return [[sheet.cell_value(i, j) for j in range(sheet.ncols)] for i in range(n)]

    def _parse_sheet(self, file_path: str, sheet: Any) -> List[Dict[str, Any]]:
        header_rows,valid_len = self._sheet_rows(sheet, HEADER_SCAN_ROWS)
        header_map, header_idx = self.find_header(header_rows, max_scan=HEADER_SCAN_ROWS)
        # 省份汇总表检测(如 "第一批(截止2025.01.24)":数据第 2 列为省份名)→ 干扰,记录名单
        is_summary, sample = self._is_province_summary(sheet,valid_len)
        if is_summary:
            record_noise(file_path, sheet.name, sample)
            logger.warning(f"{file_path}[{sheet.name}]: 判定为各省汇总表干扰数据,已跳过并记录名单")
            return []
        if not header_map and sheet.name == '行业类别' and sheet.name in ' ' .join(map(str,header_rows[0])):
            logger.warning(f"{file_path}[{sheet.name}]: 判定为行业类别干扰数据,已跳过并记录名单")
            return []
        if header_map is None:
            # 两列式退化解析:各省摘要清单(分类|项目名,无表头,如 2025年各省市重大项目汇总)
            two_col = self._parse_two_column(sheet)
            if two_col:
                return self._filter_noise(file_path, sheet.name, two_col)
            logger.warning(f"{file_path}[{sheet.name}]: 前 {HEADER_SCAN_ROWS} 行未找到表头,跳过")
            return []

        projects: List[Dict[str, Any]] = []
        context: Dict[str, str] = {}  # 分类上下文:category 行业分类 / project_type 建设性质

        # sheet 名:行业分类 → 初始 category;建设性质(如"重点预备"/"续建项目")→ 初始 project_type;
        # 性质类 sheet 名(如 "续建项目")不再作为 category;记录供"未纳入 project 时存 extra"判定
        sheet_type = self._sheet_type(sheet.name)
        sheet_category = self._sheet_category(sheet.name)
        if sheet_type:
            context['project_type'] = sheet_type
            context['sheet_type'] = sheet_type
            if sheet_category in (sheet_type, sheet_type + '项目'):
                sheet_category = ''
        if sheet_category:
            context['category'] = sheet_category
            context['sheet_category'] = sheet_category

        headers, header_idx = self._build_headers(header_rows, header_idx)
        # 合并后的表头重建列映射(子表头行可能带来新字段,如 "2020年计划-计划投资")
        from parser.field_mapping import build_header_map
        header_map = build_header_map(headers)
        # 普遍数据行非空列数(分组行判定的动态基准)
        all_rows = self._sheet_rows(sheet,valid_len=valid_len)[0]
        # 表头列错位修正:合并表头检查优先,数字列检测兜底
        header_map = BaseParser._fix_merged_header(header_map, sheet.merged_cells, header_idx)
        header_map = BaseParser._fix_numeric_project_col(header_map, all_rows, header_idx)
        header_map = process_total_investment_header(header_map, headers)
        # 表头之前的行:分类标题计入上下文;装饰行(备注/正文标签/清单概况·总数
        # 描述,同 xlsx is_decor_text)→ 跳过且不设任何 category
        for row in header_rows[:header_idx]:
            joined = " ".join(
                str(c).strip() for c in row if c is not None and str(c).strip())
            if BaseParser.is_decor_text(joined):
                continue
            self.apply_category(joined, context)

        # 目录+正文 单行表头 sheet 预扫描(同 xlsx):正文区 = ≥5 编号行后出现 ≥3 个
        # 连续无序号行且其后不再有编号行 → 正文区起始行起不入库
        prose_start = -1
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
                              and BaseParser._is_number(str(c).strip()) for c in cells_j)
                if has_num:
                    numbered_cnt += 1
                    unnum_run = 0
                    run_start = -1
                    continue
                if unnum_run == 0:
                    run_start = j
                unnum_run += 1
                if numbered_cnt >= 5 and unnum_run >= 3:
                    if any(c is not None and str(c).strip()
                           and BaseParser._is_number(str(c).strip())
                           for row_k in all_rows[j + 1:] for c in row_k):
                        continue
                    prose_start = run_start
                    break
            minimal_numbered = numbered_cnt
        # 用于数字过滤，不过滤小于最大项目数的整型
        # max_project_num = len(all_rows)
        if 'project_name' not in header_map.values():
            logger.info('未匹配到有效header_map')
            return []
        normal_cols = BaseParser._normal_cols(all_rows[header_idx + 1:],header_map)
        # 金额单位
        investment_unit = BaseParser._get_investment_unit(all_rows[:header_idx],headers,header_map)
        for i, cells in enumerate(all_rows[header_idx + 1:], start=header_idx + 1):
            if i== 136-1:
                pass
            if not self.is_data_row(cells) or self.skip_summary_row(cells):
                continue
            # 装饰行统一判定(同 xlsx,is_prose_row):备注/注记说明行、招商简介正文、
            # 清单概况/总结句 → 不产生项目
            if BaseParser.is_prose_row(cells):
                continue
            # 说明行(如 开州附件2 "下列12个子项目"):不产生项目、不参与分类判断
            if any(re.match(r'^(下列|详见|见下表|附后|备注)', str(c).strip())
                   for c in cells if c is not None and str(c).strip()
                   and not self._is_placeholder(str(c).strip())):
                continue
            # 正文区行(预扫描 prose_start 起,同 xlsx):不入库、不参与分组/分类判断
            if prose_start >= 0 and (i - header_idx - 1) >= prose_start:
                continue
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
                    if BaseParser.is_group_row(cells):
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
            # 数据行(业务字段列含非纯数字文本,如 责任单位/建设性质/建设年限/项目业主)→
            # 不参与分类判断:干扰源(建设内容/项目名中的 "（N个）")在名称/内容列,
            # 由 header_map 的列语义识别数据行,避免兜底误判为分类
            # (与上方 group 检测共用同一先排除业务数据行的判定)
            suspect_row = not is_biz_row
            # 业务文本
            valid_num = len([
                cells[i] for i in header_map
                if cells[i] is not None
                   and str(cells[i]).strip()
                   and not self._is_number(cells[i])
                   and not self._is_placeholder(cells[i])
            ])
            non_empty = [str(c).strip() for c in cells if c is not None and str(c).strip() and not BaseParser._is_number(c) and not BaseParser._is_placeholder(c)]
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
                # 单格分类行(分类独立一行,如 "1、合肥市(915个)"、"续建项目(597个)")→ 分类上下文
                if len(non_empty) == 1 and len(header_map) > 1:
                    if not normal_cols == 1 or not BaseParser._check_sortNum(cells, header_map):
                        if self.classify_single_row(non_empty[0], context, header_map):
                            continue
                joined = " ".join(non_empty)
                if self.apply_category(joined, context):
                    continue
                if re.search(r'[（(]\s*共?\s*\d+\s*[)）]\s*$', joined) and len(non_empty) >= normal_cols:
                    pass
                # 原本直接map_row，增加判断：valid_num / normal_cols <= 0.2，如果上一个项目有效文本占比低于20%，怀疑是续行
                elif valid_num / normal_cols <= 0.2 and projects:
                    project = map_row(header_map, cells, headers=headers, file_year=self.file_year,
                                      investment_unit=investment_unit)
                    name = project.get('project_name')
                    if not name:
                        continue
                    last = projects[-1]
                    if i+1 in range(last['source_row']+1,last['source_row']+3):
                        if not re.findall('项目|项日|项曰|页目|顶日|顶目', last['project_name'], re.DOTALL):
                            last['project_name'] = fr"{last['project_name']} \n {name}".strip()[:255]
                            continue
            project = map_row(header_map, cells, headers=headers, file_year=self.file_year,investment_unit=investment_unit)
            name = project.get('project_name')
            if not name:
                continue
            if valid_num / normal_cols <= 0.8 and projects:
                last = projects[-1]
                if i+1 in range(last['source_row']+1,last['source_row']+3) and (
                        re.search('^[(（][^()（）]*?[)）]$', name)
                        or BaseParser.is_continuation(last['project_name'],name)
                        or BaseParser._is_seconde_name(name)
                ):
                    last['project_name'] = fr"{last['project_name']} \n {name}".strip()[:255]
                    continue
            # 分类名过滤仅对少列行(≤2 个非空);多列数据行即使项目名以"(1)"开头也保留
            if len(non_empty) <= 2 and self.is_category_name(name):
                continue
            # 上下文分类仅补充,不覆盖 项目类别/产业类别 列的映射值
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
        return self._filter_noise(file_path, sheet.name, projects)

    @staticmethod
    def _filter_noise(file_path: str, sheet_name: str,
                      projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """干扰 sheet 识别(各省汇总表):数据不入库,记录到 noise_sheets.json。"""
        if is_noise_sheet(projects):
            record_noise(file_path, sheet_name, projects[0].get('project_name', ''))
            logger.warning(f"{file_path}[{sheet_name}]: 判定为各省汇总表干扰数据,已跳过并记录名单")
            return []
        return projects

    def _is_province_summary(self, sheet: Any, valid_len:int=0) -> tuple[bool, str]:
        """省份汇总表检测:数据行第 2 列多为省份名(如 "1|北京市|500个…")。

        表头可能被误识别(子表头行含"总投资额"等),此时解析产出为 0,
        需按原始行判断。判定条件:省份名行占比 ≥80%(覆盖各省汇总表与省→地级市对照表)。
        返回 (是否汇总表, 示例省份名)。
        """
        from util.province_names import PROVINCE_NAMES
        checked = 0
        prov = 0
        sample = ''
        for cells in self._sheet_rows(sheet,valid_len=valid_len)[0]:
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
        # 默认 sheet 名(Excel 导出/复制常见)非行业分类:Sheet/Table 后可带空格与编号
        cleaned = re.sub(r'^(sheet|table|责任分解)\s*\d*$', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'[（(].*?[)）]', '', cleaned).strip()
        # 清洗结果 ≤1 字符(如 sheet 名"总表"→"总")或超长 → 视为无意义
        if not cleaned or len(cleaned) > 20 or len(cleaned) <= 1:
            return ''
        return cleaned[:128]

    @staticmethod
    def _sheet_type(sheet_name: str) -> str:
        """从 sheet 名提取建设性质(如 "重点预备" → 预备、"重点前期" → 前期),无则空。"""
        for word in ('竣工投产', '新开工', '预备', '前期', '续建', '新建', '储备', '投产'):
            if word in str(sheet_name):
                return word
        return ''

    @staticmethod
    def _build_headers(header_rows: List[List[Any]], header_idx: int
                       ) -> tuple[List[Any], int]:
        """构造表头行并定位数据起始行(委托 base_parser.merge_header_rows)。"""
        return BaseParser.merge_header_rows(header_rows, header_idx)
