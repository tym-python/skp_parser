"""PDF 解析器:pdfplumber 提取,优先表格结构,无表格时退化行级文本兜底。"""

from typing import Any, Dict, List, Optional

import pdfplumber

from parser.base_parser import BaseParser
from parser.field_mapping import extract_file_year
from util.log_util import get_logger

logger = get_logger(__file__)


class PdfParser(BaseParser):
    """PDF 重点清单解析:逐页提取表格与文本。"""

    SUPPORTED_EXT = ('.pdf',)

    # 表格提取产出少于该值 → 判定表格质量差(单元格跨行截断等),改用列式/文本提取
    MIN_TABLE_PROJECTS = 50
    # 列式提取产出少于该值 → 判定列对齐失败,改用文本兜底
    MIN_COLUMN_PROJECTS = 30

    @staticmethod
    def _to_halfwidth(text: str) -> str:
        """全角数字转半角(山东等文件用全角序号)。"""
        return text.translate(str.maketrans('０１２３４５６７８９', '0123456789'))

    @classmethod
    def _cluster_columns(cls, page: Any) -> List[Dict[str, Any]]:
        """把页内单词按 x 坐标聚类为列(同列单词 x0 相邻)。"""
        words = sorted(page.extract_words(), key=lambda w: w['x0'])
        cols: List[Dict[str, Any]] = []
        for w in words:
            if cols and w['x0'] - cols[-1]['x'] < 15:
                cols[-1]['words'].append(w)
                xs = [x['x0'] for x in cols[-1]['words']]
                cols[-1]['x'] = sum(xs) / len(xs)
            else:
                cols.append({'x': w['x0'], 'words': [w]})
        return cols

    def _parse_column_layout(self, file_path: str,
                             context: Dict[str, str]) -> List[Dict[str, Any]]:
        """列式排版提取:处理 "序号 | 项目名称 | 项目描述" 三列式 PDF(如 山东名单)。

        按 x 坐标聚类列 → 以序号列单词为行锚 → 其余列单词按 top 落入行区间 →
        行内按列顺序拼接。空名称行(调度表等空白表单)自动过滤。
        """
        projects: List[Dict[str, Any]] = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                cols = self._cluster_columns(page)
                if len(cols) < 2:
                    continue
                # 序号列:最左的、以数字为主的列
                seq_col = None
                for c in cols:
                    digits = sum(1 for w in c['words']
                                 if self._to_halfwidth(w['text']).isdigit())
                    if digits / max(len(c['words']), 1) > 0.7:
                        seq_col = c
                        break
                if seq_col is None:
                    continue
                anchors = sorted(
                    (w for w in seq_col['words'] if self._to_halfwidth(w['text']).isdigit()),
                    key=lambda w: w['top'])
                if not anchors:
                    continue
                other_cols = [c for c in cols if c['x'] > seq_col['x']]

                for i, a in enumerate(anchors):
                    top_start = a['top']
                    top_end = anchors[i + 1]['top'] if i + 1 < len(anchors) else float('inf')
                    cells: List[str] = []
                    for c in other_cols:  # 按列 x 顺序
                        cell_words = sorted(c['words'], key=lambda w: w['top'])
                        cells.append(''.join(
                            w['text'] for w in cell_words if top_start <= w['top'] < top_end))
                    cells = [t.strip() for t in cells]
                    # 空名称行(空白表单/调度表)过滤
                    if not cells or not cells[0]:
                        continue
                    project: Dict[str, Any] = {
                        'project_name': cells[0][:255],
                        'construction_content': ' '.join(c for c in cells[1:] if c)[:2000],
                        'category': context.get('category', ''),
                        'project_type': context.get('project_type', ''),
                    }
                    projects.append(project)
        return projects

    def parse(self, file_path: str) -> List[Dict[str, Any]]:
        self.file_year = extract_file_year(file_path)
        projects: List[Dict[str, Any]] = []
        text_found = False
        context: Dict[str, str] = {}  # 跨页/跨路径共享分类上下文

        with pdfplumber.open(file_path) as pdf:
            # 1. 先全量尝试表格提取(重点项目清单多为表格排版,比文本流更可靠)
            prev_header: Optional[Dict[int, str]] = None  # 跨页表格共享表头(湖北等多页表)
            for page in pdf.pages:
                for table in page.extract_tables():
                    page_projects, prev_header = self.extract_rows_from_table(
                        table, context, file_year=self.file_year, prev_header_map=prev_header)
                    projects.extend(page_projects)

            # 2. 文件级判定:表格产出充足 → 直接返回,不再文本兜底
            #    (文本流在复杂表格 PDF 中常逐行截断错乱,混用会产生垃圾行)
            if len(projects) >= self.MIN_TABLE_PROJECTS:
                return self.filter_blank_projects(projects)
            if projects:
                logger.warning(f"{file_path}: 表格提取仅 {len(projects)} 条(疑似单元格截断),改用列式提取")
                projects = []

            # 3. 列式排版提取(序号|名称|描述,如 山东名单类 PDF)
            column_projects = self._parse_column_layout(file_path, context)
            if len(column_projects) >= self.MIN_COLUMN_PROJECTS:
                return self.filter_blank_projects(column_projects)
            if column_projects:
                logger.warning(f"{file_path}: 列式提取仅 {len(column_projects)} 条,改用文本兜底")
                projects = []

            # 3. 全无有效表格时,行级文本兜底(扫描件除外)
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_found = True
                    projects.extend(self.parse_lines(text.splitlines(), context))

        # 4. 质量门:文本兜底结果中项目名大量含空格(多列碎片交叉) → 文本流错乱,弃用
        #    (此类文件多为排版差的表格 PDF,行级解析无法可靠恢复)
        if projects:
            spaced = sum(1 for p in projects if ' ' in (p.get('project_name') or ''))
            if spaced / len(projects) > 0.3:
                logger.warning(
                    f"{file_path}: 文本流错乱(碎片行占 {spaced}/{len(projects)}),解析结果弃用")
                return []

        if not projects and not text_found:
            logger.warning(f"{file_path}: 未提取到任何文本,疑似扫描件(需 OCR 支持)")
        return self.filter_blank_projects(projects)
