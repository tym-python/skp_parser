"""DOCX 内容读取层(一次读取、多处复用):按 body 顺序产出 段落/表格 块。

- python-docx 优先(单元格保留 python-docx 的合并跨列重复文本,由调用方去重);
- 损坏/WPS 畸形包(python-docx 报 "no item named 'NULL'" 等)→ lxml 直接读
  word/document.xml 兜底(lxml 版合并单元格只出现在首格,天然无跨列重复)。
两者输出同一结构,docx 解析器与通知解析共用:
    iter_blocks(path) -> ('p', text) | ('tbl', rows[][])
with_grid=True 时 tbl 块附带各逻辑格的 (offset, span) 网格信息(第 3 元素),
供 两行表头按网格偏移 补父标题(docx_parser);默认关闭,通知解析等零变化。
"""

from typing import Any, Iterator, List, Tuple
import os
import shutil
import subprocess
import tempfile
from util.log_util import get_logger

logger = get_logger(__file__)

_W_NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

def transpose(rows, grid=None):
    """转置 iter_blocks(with_grid=True) 拿到的 tbl 块。

    rows: List[List[str]]          每行各逻辑格的文本
    grid: List[List[(off, span)]]  与 rows 等长
    返回: List[List[str]]          转置后的行
    """
    if not rows:
        return []

    if grid is None:                      # 退化情形
        w = max(len(r) for r in rows)
        padded = [list(r) + [None] * (w - len(r)) for r in rows]
        return [list(col) for col in zip(*padded)]

    n_rows = len(rows)
    n_cols = max(off + span for row_g in grid for off, span in row_g)

    # 1) 铺平：合并格覆盖到的每一列都填同一个值
    full = [[None] * n_cols for _ in range(n_rows)]
    for i, (vals, row_g) in enumerate(zip(rows, grid)):
        for v, (off, span) in zip(vals, row_g):
            for c in range(off, off + span):
                full[i][c] = v

    # 2) 转置
    return [[full[i][c] for i in range(n_rows)] for c in range(n_cols)]

_OLE2_MAGIC = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"

def _is_ole2(file_path: str) -> bool:
    """读文件头 8 字节判断是否为 OLE2(旧版 .doc/.xls/.ppt)。"""
    try:
        with open(file_path, "rb") as f:
            return f.read(8) == _OLE2_MAGIC
    except OSError:
        return False

# doc转docx
def _convert_doc_to_docx_libreoffice(doc_path: str, out_dir: str) -> str:
    """用 LibreOffice 把 OLE2 .doc 转成 .docx,返回生成的 docx 路径。"""
    # 复制成 .doc 后缀,避免 LibreOffice 因后缀与实际内容不符而拒绝转换
    src_copy = os.path.join(out_dir, "source.doc")
    shutil.copy(doc_path, src_copy)

    last_err = None
    for cmd in ("libreoffice", "soffice"):
        try:
            subprocess.run(
                [cmd, "--headless", "--convert-to", "docx",
                 "--outdir", out_dir, src_copy],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            break
        except FileNotFoundError as e:
            last_err = e
            continue
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"LibreOffice 转换失败: {e.stderr.decode(errors='ignore')}"
            ) from e
    else:
        raise RuntimeError("未找到 libreoffice / soffice 命令,无法转换 .doc") from last_err

    out_path = os.path.join(out_dir, "source.docx")
    if not os.path.exists(out_path):
        raise RuntimeError(f"转换后未生成 docx: {out_dir}")
    return out_path

def _convert_doc_to_docx(doc_path: str) -> str:
    """把 OLE2 .doc 转成 .docx。返回临时 docx 路径,调用方负责删父目录。
    优先 LibreOffice,失败再尝试 Word COM(Windows)。
    """
    out_dir = tempfile.mkdtemp(prefix="doc_conv_")
    try:
        return _convert_doc_to_docx_libreoffice(doc_path, out_dir)
    except Exception as lo_err:
        shutil.rmtree(out_dir, ignore_errors=True)
        raise RuntimeError(
            f"LibreOffice 失败({lo_err})"
        ) from lo_err

def _lxml_text(el: Any) -> str:
    """取元素下全部 w:t 文本(含 行内 tab 转空格,忽略分隔符 run)。"""
    parts: List[str] = []
    for t in el.iter(_W_NS + 't'):
        parts.append(t.text or '')
    return ''.join(parts)


def _lxml_blocks(document_xml_root: Any) -> Iterator[Tuple[str, Any]]:
    """按 body 子元素顺序产出块:('p', 文本) / ('tbl', rows 列表)。"""
    body = document_xml_root.find(_W_NS + 'body')
    if body is None:
        return
    for child in body.iterchildren():
        if child.tag == _W_NS + 'p':
            yield 'p', _lxml_text(child)
        elif child.tag == _W_NS + 'tbl':
            rows: List[List[str]] = []
            for tr in child.findall(_W_NS + 'tr'):
                cells = []
                for tc in tr.findall(_W_NS + 'tc'):
                    # 单元格内多段落以换行分隔(与 python-docx cell.text 口径一致)
                    paras = [_lxml_text(p).strip()
                             for p in tc.findall(_W_NS + 'p')]
                    cells.append('\n'.join(x for x in paras if x))
                rows.append(cells)
            yield 'tbl', rows


def iter_blocks(file_path: str, with_grid: bool = False) -> Iterator[Tuple[str, Any]]:
    """按 body 顺序读取 docx 的段落/表格块。损坏包自动降级 lxml 读取。

    with_grid: True 时 tbl 块 = (rows, grid),grid 与 rows 等长,每行为该
    行各逻辑格的 (offset, span) 网格坐标(合并格 span>1,见 w:gridSpan)。
    """
    import docx
    tmp_dir = None          # 转换产生的临时目录,finally 清理
    real_path = file_path   # 实际拿去读的路径
    if _is_ole2(file_path):
        logger.warning(f"{file_path}: 检测为 OLE2 旧版 .doc,先转换为 docx")
        real_path = _convert_doc_to_docx(file_path)
        tmp_dir = os.path.dirname(real_path)
    try:
        try:
            document = docx.Document(real_path)
        except Exception as ex:
            logger.warning(f"{file_path}: python-docx 读取失败({ex}),降级 lxml 直接读 document.xml")
            try:
                import zipfile
                from lxml import etree
                with zipfile.ZipFile(file_path) as zf:
                    xml = zf.read('word/document.xml')
                yield from _lxml_blocks(etree.fromstring(xml))
                return
            except Exception as lex:
                raise RuntimeError(f"docx 损坏且 lxml 兜底失败: {lex}") from ex

        # python-docx 正常路径:还原 body 子元素顺序
        from docx.table import Table, _Cell
        from docx.text.paragraph import Paragraph
        for child in document.element.body.iterchildren():
            if child.tag.endswith('}p'):
                yield 'p', Paragraph(child, document).text
            elif child.tag.endswith('}tbl'):
                table = Table(child, document)
                # 按逻辑格(tc)读取而非网格展开(row.cells):后者按最大列 span 展开、
                # 合并值跨列重复,表头行与数据行 span 不同时(如 南京 2022 表头 10 逻辑列、
                # 数据行"序号"占 2 网格列)逻辑列错位、字段映射取空。逻辑格与 lxml 兜底
                # 路径口径一致,合并值只出现一次,表头/数据天然对齐
                rows = [[_Cell(tc, table).text for tc in row._tr.tc_lst]
                        for row in table.rows]
                if not with_grid:
                    yield 'tbl', rows
                    continue
                # 各逻辑格 (offset, span) 网格坐标:横向合并格 gridSpan>1,
                # offset 为该格在表网格中的起始列(供两行表头按网格补父标题)
                grid = []
                for row in table.rows:
                    off = 0
                    spans = []
                    for tc in row._tr.tc_lst:
                        sp = tc.tcPr.grid_span if tc.tcPr is not None else 1
                        spans.append((off, sp))
                        off += sp
                    grid.append(spans)
                yield 'tbl', (rows, grid)
    finally:
        # 3) 清理临时转换目录
        if tmp_dir and os.path.isdir(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)

def is_docx(file_path: str) -> bool:
    """docx 判定(ZIP 含 word/):供通知解析等按真实格式分派。"""
    import os
    import zipfile
    try:
        with zipfile.ZipFile(file_path) as zf:
            return any(n.startswith('word/') for n in zf.namelist())
    except Exception:
        return os.path.splitext(file_path)[1].lower() == '.docx'
