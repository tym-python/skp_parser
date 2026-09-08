"""XLS 解析器(xlrd):兼容 Excel 97-2003 旧格式,解析逻辑与 XlsxParser 一致。

注:xlrd 2.x 仅支持 .xls(旧二进制格式),不支持 .xlsx。
"""

import re
from typing import Any, Dict, List, Optional

import xlrd

from parser.base_parser import BaseParser
from parser.field_mapping import extract_file_year, map_row
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
        for i, cells in enumerate(self._sheet_rows(sheet), start=1):
            first = str(cells[0] or '').strip() if cells else ''
            second = str(cells[1] or '').strip() if len(cells) > 1 else ''
            if first and not second:
                # 大段说明文本(如 "第四批-.0 河北省 703个 1.5万亿元…")→ 忽略
                if len(first) > 20:
                    continue
                # 分类/性质标题行(如 "铁路"、"新开工项目")
                if self.classify_single_row(first, context) or self.apply_category(first, context):
                    continue
                context['category'] = first[:128]
                continue
            if not second:
                continue
            if first:
                # 新分类 + 项目名同行;纯数字/单字符(如 序号 "1")不是分类,跳过沿用上下文
                if not first.isdigit() and len(first) > 1 \
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

    def _sheet_rows(self, sheet: Any, max_row: Optional[int] = None) -> List[List[Any]]:
        """按行取 sheet 单元格值(xlrd 无迭代器,手动构造)。"""
        n = sheet.nrows if max_row is None else min(max_row, sheet.nrows)
        return [[sheet.cell_value(i, j) for j in range(sheet.ncols)] for i in range(n)]

    def _parse_sheet(self, file_path: str, sheet: Any) -> List[Dict[str, Any]]:
        header_rows = self._sheet_rows(sheet, HEADER_SCAN_ROWS)
        header_map, header_idx = self.find_header(header_rows, max_scan=HEADER_SCAN_ROWS)
        # 省份汇总表检测(如 "第一批(截止2025.01.24)":数据第 2 列为省份名)→ 干扰,记录名单
        is_summary, sample = self._is_province_summary(sheet)
        if is_summary:
            record_noise(file_path, sheet.name, sample)
            logger.warning(f"{file_path}[{sheet.name}]: 判定为各省汇总表干扰数据,已跳过并记录名单")
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
        all_rows = self._sheet_rows(sheet)
        # 用于数字过滤，不过滤小于最大项目数的整型
        max_project_num = len(all_rows)
        normal_cols = BaseParser._normal_cols(all_rows,header_map)
        # 表头列错位修正:合并表头检查优先,数字列检测兜底
        header_map = BaseParser._fix_merged_header(header_map, sheet.merged_cells, header_idx)
        header_map = BaseParser._fix_numeric_project_col(header_map, all_rows, header_idx)
        # 表头之前的行:分类标题计入上下文;装饰行(备注/正文标签/清单概况·总数
        # 描述,同 xlsx is_decor_text)→ 跳过且不设任何 category
        for row in header_rows[:header_idx]:
            joined = " ".join(
                str(c).strip() for c in row if c is not None and str(c).strip())
            if BaseParser.is_decor_text(joined):
                continue
            self.apply_category(joined, context)

        data_rows = all_rows[header_idx + 2:]
        # 目录+正文 单行表头 sheet 预扫描(同 xlsx):正文区 = ≥5 编号行后出现 ≥3 个
        # 连续无序号行且其后不再有编号行 → 正文区起始行起不入库
        prose_start = -1
        minimal_numbered = 0  # 极简 sheet 含纯数字序号的行数(供窄化分组 allow_city 用)
        if len(header_map) <= 1:
            numbered_cnt = 0
            unnum_run = 0
            run_start = -1
            for j in range(len(data_rows)):
                cells_j = data_rows[j]
                if not self.is_data_row(cells_j) or self.skip_summary_row(cells_j):
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
                           for cells_k in data_rows[j + 1:] for c in cells_k):
                        continue
                    prose_start = run_start
                    break
            minimal_numbered = numbered_cnt
        for i, cells in enumerate(data_rows, start=header_idx + 2):
            if not self.is_data_row(cells) or self.skip_summary_row(cells):
                continue
            # 装饰行统一判定(同 xlsx,is_prose_row):备注/注记说明行、招商简介正文、
            # 清单概况/总结句 → 不产生项目
            if BaseParser.is_prose_row(cells):
                continue
            # 正文区行(预扫描 prose_start 起,同 xlsx):不入库、不参与分组/分类判断
            if prose_start >= 0 and (i - header_idx - 2) >= prose_start:
                continue
            # 极简清单(仅 序号+名称/目录,header_map ≤1 列)窄化分组识别(同 xlsx:
            # 城市分组短名如 "南宁市" 跳过,单格真项目名如 "汉中综合保税区" 不误弃);
            # 多列映射表 → 责任单位/地区分组行检测(如 "['','南宁市人民政府','16',…]")
            if len(header_map) <= 1:
                # allow_city:sheet 完全无编号行(纯名称单列清单)→ 关闭 市/区 短名分组
                # 判定,避免 "xx小区/园区" 短名真项目被当城市分组丢弃(同 xlsx)
                if BaseParser.is_group_row_minimal(
                        cells, allow_city=minimal_numbered > 0):
                    continue
            else:
                if self.is_group_row(cells):
                    continue
                if BaseParser.is_group_header_row(cells, header_map, normal_cols):
                    continue
            # 建设性质标题行(合并 is_build_type_row + _group_type_title 后的统一入口;
            # 单格纯词,如 安徽"续建"/"计划开工")→ 更新 project_type 上下文
            build_type = BaseParser.group_type_title(cells, header_map)
            if build_type:
                context['project_type'] = build_type
                continue
            # 单格分类行(分类独立一行,如 "1、合肥市(915个)"、"续建项目(597个)")→ 分类上下文
            non_empty = [str(c).strip() for c in cells if c is not None and str(c).strip()]
            if len(non_empty) == 1 and len(header_map) > 1:
                if self.classify_single_row(non_empty[0], context):
                    continue
            joined = " ".join(str(c).strip() for c in cells if c is not None and str(c).strip())
            if self.apply_category(joined, context):
                continue
            project = map_row(header_map, cells, headers=headers, file_year=self.file_year)
            name = project.get('project_name')
            if not name:
                continue
            # 分类名过滤仅对少列行(≤2 个非空);多列数据行即使项目名以"(1)"开头也保留
            if len(non_empty) <= 2 and self.is_category_name(name):
                continue
            # 上下文分类仅补充,不覆盖 项目类别/产业类别 列的映射值
            if context.get('category') and not project.get('category'):
                project['category'] = context['category']
            if not project.get('project_type'):
                project['project_type'] = context.get('project_type', '')
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

    def _is_province_summary(self, sheet: Any) -> tuple[bool, str]:
        """省份汇总表检测:数据行第 2 列多为省份名(如 "1|北京市|500个…")。

        表头可能被误识别(子表头行含"总投资额"等),此时解析产出为 0,
        需按原始行判断。判定条件:省份名行占比 ≥80%(覆盖各省汇总表与省→地级市对照表)。
        返回 (是否汇总表, 示例省份名)。
        """
        from util.province_names import PROVINCE_NAMES
        checked = 0
        prov = 0
        sample = ''
        for cells in self._sheet_rows(sheet):
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
        cleaned = re.sub(r'^(sheet|table)\s*\d*$', '', cleaned, flags=re.IGNORECASE)
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
