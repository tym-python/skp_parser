"""DOCX 解析器:按"表格优先、段落兜底"两条路径解析:

- **有表格**:通知/计划文件的项目清单在表格中——表格(可多张)逐张走公共
  `extract_rows_from_table`(与 xlsx/pdf 共用 装饰行/窄化分组/性质标题/分类上下文);
  表格前的通知正文、标题段落不参与解析(避免标题/导语被当项目或拼入项目名),
  表格后的落款/说明同样忽略。
- **单项目纵排卡片表**(每表一个项目,3 列 序号|标签|内容,如 西藏招商引资):
  不转置会把标签列当项目名逐行产垃圾;识别后先并续行、转置(docx_reader.transpose)
  为 序号/标签/值 三行横表,再走公共 `extract_rows_from_table`(标签行自动识别为表头)。
- **无表格**:纯文本清单(段落式 序号行/分类行/条目)→ 全部段落走公共
  `parse_lines`(装饰行/概况句/备注 过滤已内置)。

内容读取走共享 docx_reader(损坏包自动 lxml 兜底)。python-docx 特有处理:
- 合并单元格文本会**跨列重复**(如 分类行 "一、基础设施" 出现于两列)→ 相邻去重,
  否则双份文本拼进 joined 会污染分类名("基础设施 一、基础设施");
- 单元格文本统一走 text_clean 清洗管道(去空白/全角转半角/折叠)。

通知类文件(docx)的元信息(标题/文号/发文单位/正文)由 NoticeParser 解析入库
(skp_notice),本类只负责其中的项目清单部分。
"""

import re
from typing import Any, Dict, List, Optional

from parser.base_parser import BaseParser
from parser.docx_reader import iter_blocks, transpose
from parser.field_mapping import extract_file_year
from parser.text_clean import clean_text
from util.log_util import get_logger

logger = get_logger(__file__)


class DocxParser(BaseParser):
    """DOCX 重点清单解析:表格优先;纯文本清单走段落兜底。"""

    SUPPORTED_EXT = ('.docx','.doc')

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

    # ---------- 单项目纵排卡片表(序号|标签|内容,每表一个项目) ----------

    # 卡片表标签词根:col1 每个非空标签须命中其一(如 "用地规模和建设内容" 含
    # 两个词根,归一为同一标签);词根带"招商"限定,避免 投资/前期工作 等常见词
    # 误伤普通横排清单表(其表头首行为 序号,不在词根集)
    PROFILE_LABELS = ('项目名称', '招商单位', '项目简介', '用地规模', '建设内容',
                      '前期工作', '投资', '合作方式', '招商联系')
    _PROFILE_NAME_MAX_LEN = 60  # 表前回溯项目名的长度护栏(项目名行 2-60 字)

    @classmethod
    def _is_profile_table(cls, rows: List[List[Any]]) -> bool:
        """单项目纵排卡片表识别(西藏招商引资:每表一个项目,3 列 序号|标签|内容)。

        不转置时表头识别只命中 project_name 列,标签列文字逐行当项目名产垃圾;
        转置后(3 行:序号/标签/值)标签行自然成为表头,走公共 extract_rows_from_table。
        护栏(从严,任一不满足即不转置、保持原逐行逻辑):
        - 行数 ≥7 且每行恰好 3 格(纵排卡片形态);
        - col0 全为空或纯数字(序号);col1 每个非空标签命中 PROFILE_LABELS,
          去重后 ≥3 个且含 项目名称/项目简介 之一(防 投资/前期工作 等常见词误伤)。
        """
        if len(rows) < 7 or any(len(r) != 3 for r in rows):
            return False
        labels = set()
        for r in rows:
            c0 = str(r[0] or '').strip()
            if c0 and not re.fullmatch(r'\d+', c0):
                return False
            c1 = re.sub(r'[\s（）()亿万元]', '', str(r[1] or ''))
            if not c1:
                continue
            if not any(word in c1 for word in cls.PROFILE_LABELS):
                return False
            labels.add(c1)
        if len(labels) < 3 or not (labels & {'项目名称', '项目简介'}):
            return False
        return True

    @staticmethod
    def _merge_profile_rows(rows: List[List[Any]]) -> List[List[str]]:
        """卡片表跨行续写合并:空序号+空标签+非空内容 → 并入上一行内容(换行分隔);
        整行空的行删除。返回新列表,不改入参。"""
        merged: List[List[str]] = []
        for r in rows:
            cells = [str(c or '').strip() for c in r[:3]]
            c0, c1, c2 = cells
            if not c0 and not c1 and c2 and merged:
                merged[-1][2] = (merged[-1][2] + '\n' + c2).strip()
            elif c0 or c1 or c2:
                merged.append(cells)
        return merged

    @classmethod
    def _profile_name_from_paras(cls, paragraph_lines: List[str]) -> Optional[str]:
        """卡片表缺 项目名称 行时(如 西藏 某 7 行表),从表前最近段落回溯项目名:
        跳过 地点/行业类别 标签段、无汉字段(逗号碎片),取首个 ≤60 字短段(名称行
        与 项目地点行 成对出现,名称在前);找不到返回 None(该项目整条丢弃)。"""
        for line in reversed(paragraph_lines[-4:]):
            text = clean_text(line)
            if not text or len(text) > cls._PROFILE_NAME_MAX_LEN or len(text) < 2:
                continue
            if '项目地点' in text or '行业类别' in text or '项目单位' in text:
                continue
            if not re.search(r'[一-鿿]', text):
                continue
            return text
        return None

    # ---------- 解析 ----------

    def parse(self, file_path: str) -> List[Dict[str, Any]]:
        self.file_year = extract_file_year(file_path)
        projects: List[Dict[str, Any]] = []
        context: Dict[str, str] = {}  # 分类上下文在表格间共享
        prev_header: Optional[Dict[int, str]] = None
        paragraph_lines: List[str] = []
        last_paras: List[str] = []  # 最近段落环形缓冲(卡片表缺项目名时回溯,见 _profile_name_from_paras)
        has_table = False
        project_list_title = False
        profile_count = 0  # 单项目纵排卡片表计数(汇总日志用)

        for kind, payload in iter_blocks(file_path, with_grid=True):
            if kind == 'tbl':
                has_table = True
                rows, grid = payload  # with_grid:附各逻辑格 (offset, span) 网格坐标
                rows = [self._clean_row(row) for row in rows]
                if self._is_profile_table(rows):
                    # 单项目纵排卡片表(每表一个项目):不转置会把标签列当项目名逐行
                    # 产垃圾。并续行 → 转置为 序号/标签/值 三行横表,标签行自动被
                    # find_header 识别为表头,再走公共 extract_rows_from_table。每表用
                    # 独立 context(长简介不污染共享分类上下文);转置表自包含,重置
                    # prev_header 切断向后续表(如文末联络人名录表)的表头串味。
                    merged = self._merge_profile_rows(rows)
                    has_name = any(
                        re.sub(r'[\s（）()亿万元]', '', str(r[1] or '')) == '项目名称'
                        for r in merged)
                    transposed = transpose(merged)  # grid=None:卡片表无横向合并,3 列对齐
                    if not has_name:
                        name = self._profile_name_from_paras(last_paras)
                        if name:
                            # 前置 项目名称 列:转置表首列补 序号'1'/表头'项目名称'/值 name,
                            # 使 find_header 命中 project_name(否则该表无项目名列,整条丢弃)
                            seq, hdr, val = '1', '项目名称', name
                            for i, row in enumerate(transposed):
                                row.insert(0, (seq, hdr, val)[i])
                            logger.warning(f"{file_path}: 卡片表缺项目名称行,回溯段落补名: {name}")
                        else:
                            logger.warning(f"{file_path}: 卡片表缺项目名称行且回溯未找到,该项目跳过")
                    page_projects, _ = self.extract_rows_from_table(
                        transposed, {}, file_year=self.file_year)
                    projects.extend(page_projects)
                    prev_header = None
                    profile_count += 1
                else:
                    page_projects, prev_header = self.extract_rows_from_table(
                        (rows, grid), context, file_year=self.file_year,
                        prev_header_map=prev_header, project_list_title=project_list_title)
                    projects.extend(page_projects)
            else:
                text = clean_text(payload)
                if text:
                    # 最近段落环形缓冲(始终更新):卡片表缺项目名时回溯取名
                    last_paras.append(payload)
                    if len(last_paras) > 4:
                        last_paras.pop(0)
                    # 表格前的段落(标题/通知导语/概况句)——仅在尚未出现表格时收集,
                    # 供"无表格纯文本清单"走段落兜底;有表格时表后段落不再收集
                    if not projects and not prev_header:
                        paragraph_lines.append(payload)
                        if BaseParser.POSITIONAL_TITLE_RE.search(payload) and len(payload) < 36:
                            project_list_title = True   # tbl 前一行满足 项目清单
                        else:
                            project_list_title = False

        if has_table:
            # 表格 = 项目清单主体,段落不参与解析(见类注释)
            if profile_count:
                logger.info(f"{file_path}: 单项目卡片表 {profile_count} 张")
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
