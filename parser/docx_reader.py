"""DOCX 内容读取层(一次读取、多处复用):按 body 顺序产出 段落/表格 块。

- python-docx 优先(单元格保留 python-docx 的合并跨列重复文本,由调用方去重);
- 损坏/WPS 畸形包(python-docx 报 "no item named 'NULL'" 等)→ lxml 直接读
  word/document.xml 兜底(lxml 版合并单元格只出现在首格,天然无跨列重复)。
两者输出同一结构,docx 解析器与通知解析共用:
    iter_blocks(path) -> ('p', text) | ('tbl', rows[][])
"""

import re
from typing import Any, Iterator, List, Tuple

from util.log_util import get_logger

logger = get_logger(__file__)

_W_NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


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


def iter_blocks(file_path: str) -> Iterator[Tuple[str, Any]]:
    """按 body 顺序读取 docx 的段落/表格块。损坏包自动降级 lxml 读取。"""
    import docx
    try:
        document = docx.Document(file_path)
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
            yield 'tbl', [[_Cell(tc, table).text for tc in row._tr.tc_lst]
                          for row in table.rows]


def is_docx(file_path: str) -> bool:
    """docx 判定(ZIP 含 word/):供通知解析等按真实格式分派。"""
    import os
    import zipfile
    try:
        with zipfile.ZipFile(file_path) as zf:
            return any(n.startswith('word/') for n in zf.namelist())
    except Exception:
        return os.path.splitext(file_path)[1].lower() == '.docx'
