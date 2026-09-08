"""红头文件(计划通知类)解析:提取标题、文件编号、发文单位、发文时间、正文、附件名。

典型文件:XX办公室关于下达2020年第N批重点项目计划的通知.pdf
通知正文中若含重点项目清单,项目由各文件类型解析器照常解析进 skp_project,
本模块只负责通知自身的元信息(存 skp_notice 表)。
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import pdfplumber

from util.log_util import get_logger

logger = get_logger(__file__)

NOTICE_KEYWORDS = ('通知', '印发', '下达')

# 文件编号:如 〔2020〕4号、(2020)4号
NOTICE_NO_RE = re.compile(r'[〔(（]\s*\d{4}\s*[〕)）]\s*\d+\s*号')


def is_notice_file(file_name: str) -> bool:
    """判定通知类文件:文件名含 通知/印发/下达,或为文号命名(如 云发改投资〔2020〕210号)。"""
    return any(kw in file_name for kw in NOTICE_KEYWORDS) or bool(NOTICE_NO_RE.search(file_name))
# 发文时间:如 2020年6月18日
ISSUE_DATE_RE = re.compile(r'(20\d{2})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日')
# 附件行:如 "附件1:XXX"、"附件:XXX"(行首)
ATTACHMENT_RE = re.compile(r'^附件\s*\d*\s*[:：]?\s*(.+)$', re.MULTILINE)


class NoticeParser:
    """通知类 PDF 解析器:从文件与正文中提取通知元信息。"""

    def parse(self, file_path: str) -> Dict[str, Any]:
        text = self._extract_text(file_path)
        title = Path(file_path).stem
        return {
            'title': title[:255],
            'notice_no': self._extract_no(text),
            'issuer': self._extract_issuer(title),
            'issue_date': self._extract_date(text),
            'content': self._clean_text(text),
            'attachment_names': '、'.join(self._extract_attachments(text))[:1024],
        }

    @staticmethod
    def _extract_text(file_path: str) -> str:
        """按真实格式提取全文:docx 用共享 docx_reader(段落 + 表格行文本,
        损坏包自动 lxml 兜底),pdf 用 pdfplumber 逐页拼接。"""
        from parser.docx_reader import iter_blocks, is_docx
        from parser.text_clean import clean_text
        if is_docx(file_path):
            lines: List[str] = []
            for kind, payload in iter_blocks(file_path):
                if kind == 'p':
                    text = clean_text(payload)
                    if text:
                        lines.append(text)
                else:
                    # 表格行文本:单元格 清洗 + 合并跨列去重,行内 ' | ' 连接
                    for row in payload:
                        prev = ''
                        cells = []
                        for c in row:
                            t = clean_text(c)
                            if t and t == prev:
                                cells.append('')
                            else:
                                cells.append(t)
                            if t:
                                prev = t
                        joined = ' | '.join(x for x in cells if x)
                        if joined:
                            lines.append(joined)
            return "\n".join(lines)
        parts: List[str] = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    parts.append(text)
        return "\n".join(parts)

    @staticmethod
    def _clean_text(text: str) -> str:
        """压缩空白与空行,截断到 MEDIUMTEXT 安全长度。"""
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        return "\n".join(lines)[:65500]

    @staticmethod
    def _extract_no(text: str) -> str:
        """提取文件编号:优先取含编号的整行(如 "桂重大办〔2020〕4号"),否则仅编号。"""
        m = NOTICE_NO_RE.search(text)
        if not m:
            return ''
        line_start = text.rfind('\n', 0, m.start()) + 1
        line_end = text.find('\n', m.end())
        line = text[line_start:line_end if line_end != -1 else None].strip()
        return line[:128]

    @staticmethod
    def _extract_issuer(title: str) -> str:
        """发文单位:取标题中"关于"之前的部分(如 "XX办公室关于…的通知")。"""
        m = re.search(r'^(.*?)\s*关于', title)
        return m.group(1).strip()[:255] if m else ''

    @staticmethod
    def _extract_date(text: str) -> Optional[str]:
        """发文时间:正文中第一个 "YYYY年M月D日",返回 'YYYY-MM-DD'。"""
        m = ISSUE_DATE_RE.search(text)
        if not m:
            return None
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"

    @staticmethod
    def _extract_attachments(text: str) -> List[str]:
        """文末附件名称列表(如 "附件1:XXX责任表")。"""
        return [m.group(1).strip() for m in ATTACHMENT_RE.finditer(text) if m.group(1).strip()]
