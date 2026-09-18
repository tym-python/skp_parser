"""DOCX 解析器:按"表格优先、段落兜底"两条路径解析:

- **有表格**:通知/计划文件的项目清单在表格中——表格(可多张)逐张走公共
  `extract_rows_from_table`(与 xlsx/pdf 共用 装饰行/窄化分组/性质标题/分类上下文);
  表格前的通知正文、标题段落不参与解析(避免标题/导语被当项目或拼入项目名),
  表格后的落款/说明同样忽略。
- **无表格**:纯文本清单(段落式 序号行/分类行/条目)→ 全部段落走公共
  `parse_lines`(装饰行/概况句/备注 过滤已内置)。

内容读取走共享 docx_reader(损坏包自动 lxml 兜底)。python-docx 特有处理:
- 合并单元格文本会**跨列重复**(如 分类行 "一、基础设施" 出现于两列)→ 相邻去重,
  否则双份文本拼进 joined 会污染分类名("基础设施 一、基础设施");
- 单元格文本统一走 text_clean 清洗管道(去空白/全角转半角/折叠)。

通知类文件(docx)的元信息(标题/文号/发文单位/正文)由 NoticeParser 解析入库
(skp_notice),本类只负责其中的项目清单部分。
"""

from typing import Any, Dict, List, Optional

from parser.base_parser import BaseParser
from parser.docx_reader import iter_blocks
from parser.field_mapping import extract_file_year
from parser.text_clean import clean_text
from util.log_util import get_logger

logger = get_logger(__file__)


class DocxParser(BaseParser):
    """DOCX 重点清单解析:表格优先;纯文本清单走段落兜底。"""

    SUPPORTED_EXT = ('.docx',)

    # ---------- 清洗 ----------

    @staticmethod
    def _dedupe_row_cells(cells: List[str]) -> List[str]:
        """python-docx 合并单元格跨列去重:同一文本在相邻多列重复 → 保留首格。

        例:分类行 ["一、基础设施", "一、基础设施"] → ["一、基础设施", ""],
        否则 joined="一、基础设施 一、基础设施" 会被当作分类名整体入库。
        仅**索引相邻**(i == prev_i + 1)的相同值才视为合并跨列重复;中间隔列的
        相同值(如 宿迁 文件 资金来源/计划投资 两处 "92300" 落在不同资金明细列、
        中间夹空列)是真实数据,不清零——否则 年度计划投资 被误清为空。
        """
        out: List[str] = []
        prev = ''
        prev_i = -1
        for i, c in enumerate(cells):
            t = str(c).strip()
            if t and t == prev and i == prev_i + 1:
                out.append('')  # 相邻重复(合并跨列)→ 清零
            else:
                out.append(t)
                if t:
                    prev, prev_i = t, i
        return out

    @staticmethod
    def _clean_row(row: List[Any]) -> List[Any]:
        """单行清洗管道:clean_text 统一清洗 + 合并单元格相邻去重。"""
        return DocxParser._dedupe_row_cells([clean_text(c) for c in row])

    # ---------- 解析 ----------

    def parse(self, file_path: str) -> List[Dict[str, Any]]:
        self.file_year = extract_file_year(file_path)
        projects: List[Dict[str, Any]] = []
        context: Dict[str, str] = {}  # 分类上下文在表格间共享
        prev_header: Optional[Dict[int, str]] = None
        paragraph_lines: List[str] = []
        has_table = False
        project_list_title = False

        for kind, payload in iter_blocks(file_path, with_grid=True):
            if kind == 'tbl':
                has_table = True
                # 表格 = 项目清单主体:表前通知正文/标题段落、表后落款说明一律
                # 不参与解析(见类注释),段落路径仅保留"整文档无表格"的纯文本清单
                rows, grid = payload  # with_grid:附各逻辑格 (offset, span) 网格坐标
                rows = [self._clean_row(row) for row in rows]
                page_projects, prev_header = self.extract_rows_from_table(
                    (rows, grid), context, file_year=self.file_year,
                    prev_header_map=prev_header, project_list_title=project_list_title)
                projects.extend(page_projects)
            else:
                # 表格前的段落(标题/通知导语/概况句)——仅在尚未出现表格时收集,
                # 供"无表格纯文本清单"走段落兜底;有表格时表后段落不再收集
                if not projects and not prev_header:
                    text = clean_text(payload)
                    if text:
                        paragraph_lines.append(payload)
                        if BaseParser.POSITIONAL_TITLE_RE.search(payload) and len(payload)<36:
                            project_list_title = True   # tbl 前一行满足 项目清单
                        else:
                            project_list_title = False

        if has_table:
            # 表格 = 项目清单主体,段落不参与解析(见类注释)
            pass
        else:
            # 无表格:先纯文本清单兜底(bare:段落式逐行项目条目,如 甘肃 名单
            # "续建项目：…（一）农业水利项目 → 项目名" 逐行)
            if paragraph_lines:
                projects.extend(self.parse_lines(paragraph_lines, context, bare=True))
            # 段落路径 0 条(纯图片清单 docx,正文仅引言/概况段,项目为截图,
            # 如 天津西青/临港/松江/湖南 2023)→ 按 body 顺序逐图 OCR 行级兜底,
            # 与单独图片文件共用 ocr_parser 逻辑;有产出的常规 docx 不触发
            if not projects:
                from parser.ocr_parser import docx_image_blocks, ocr_image_bytes
                for img in docx_image_blocks(file_path):
                    ocr_lines,_ = ocr_image_bytes(img)
                    if ocr_lines and _ == 'lines':
                        projects.extend(self.parse_lines(ocr_lines, context))
                    elif ocr_lines and _ == 'table':
                        projects.extend(self.extract_rows_from_table(ocr_lines, context)[0])
                if projects:
                    logger.info(f"{file_path}: 纯图片 docx,OCR 解析 {len(projects)} 条")
                else:
                    logger.warning(f"{file_path}: 无表格且段落/OCR 均未解析到项目")

        return self.filter_blank_projects(projects)
