"""统一文本清洗管道(高内聚、一次解析多处复用)。

各处零散的 `str.strip()` / `re.sub(r'\\s+', …)` / 全角转半角 收敛到本模块,
按固定顺序串联:去首尾空白 → 全角数字/字母转半角 → 折叠内部空白 → 截断。
各解析器(xlsx/docx/pdf/通知)与字段清洗统一调用,避免实现漂移。
"""

import re
from typing import Optional

# 全角 → 半角(数字/拉丁字母;中文标点不动,防 "（"→"(" 影响全角括号识别)
_FULLWIDTH_CHARS = '０１２３４５６７８９'
_HALFWIDTH_CHARS = '0123456789'
_FULLWIDTH_LETTERS = ('ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ'
                      'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ')
_HALFWIDTH_LETTERS = ('abcdefghijklmnopqrstuvwxyz'
                      'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
_HALFWIDTH_TABLE = str.maketrans(
    _FULLWIDTH_CHARS + _FULLWIDTH_LETTERS,
    _HALFWIDTH_CHARS + _HALFWIDTH_LETTERS)

_WS_RE = re.compile(r'\s+')


def halfwidth(text: str) -> str:
    """全角数字/字母转半角(如 山东 等文件用全角序号 "１、")。"""
    return str(text).translate(_HALFWIDTH_TABLE)


def collapse(text: str) -> str:
    """去首尾空白 + 折叠内部连续空白为单个空格(含换行/制表,如 "联  系  人")。"""
    return _WS_RE.sub(' ', str(text).strip())


def clean_text(text: Optional[object], max_len: Optional[int] = None) -> str:
    """统一清洗管道:去首尾空白 → 全角数字/字母转半角 → 折叠内部空白。

    用于单元格/段落文本进入解析前的通用前置清洗;
    需要保留内部空白的语义判断(如 去空格后缀匹配)可在之后另做去空格处理。
    """
    cleaned = halfwidth(str(text if text is not None else ''))
    cleaned = collapse(cleaned)
    if max_len is not None and len(cleaned) > max_len:
        cleaned = cleaned[:max_len]
    return cleaned
