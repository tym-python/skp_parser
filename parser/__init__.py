"""解析器统一入口:按文件扩展名分发到具体解析器。

用法:
    from parser import parse_file
    projects = parse_file(r"E:\\...\\2023年重点项目.xlsx")
"""

import os
from typing import Dict, List, Type

from parser.base_parser import BaseParser
from parser.docx_parser import DocxParser
from parser.pdf_parser import PdfParser
from parser.xls_parser import XlsParser
from parser.xlsx_parser import XlsxParser

PARSER_REGISTRY: Dict[str, Type[BaseParser]] = {
    '.pdf': PdfParser,
    '.docx': DocxParser,
    '.xlsx': XlsxParser,
    '.xls': XlsParser,
}


def get_parser(ext: str) -> BaseParser:
    """按扩展名(含点,大小写不敏感)返回解析器实例。"""
    parser_cls = PARSER_REGISTRY.get(ext.lower())
    if parser_cls is None:
        hint = ' (疑似压缩包/伪装文件,不做解析)' if ext == '.zip' else ''
        raise ValueError(f"不支持的扩展名: {ext},仅支持 {list(PARSER_REGISTRY)}{hint}")
    return parser_cls()


def detect_real_ext(file_path: str) -> str:
    """按文件头探测真实格式,覆盖 扩展名与内容不符 的情况(如 .xlsx 实为旧版 xls)。

    - OLE2 魔数(D0CF11E0)→ 按流名区分 .doc(WordDocument 流)/ .xls(旧版 Excel)
    - ZIP 魔数(PK)→ .xlsx
    - 其他 → 按扩展名
    """
    try:
        with open(file_path, 'rb') as f:
            head = f.read(8)
        if head.startswith(b'\xd0\xcf\x11\xe0'):
            # 目录扇区(流名 UTF-16LE)位置不定(常见于文件尾部)→ 整文件扫 WordDocument 流
            with open(file_path, 'rb') as f:
                return '.doc' if 'WordDocument'.encode('utf-16le') in f.read() \
                    else '.xls'
        if head.startswith(b'PK'):
            # docx/xlsx/pptx 同为 ZIP(PK 魔数):按 zip 内容区分——
            # 不能按魔数一刀切,否则 .docx 会被误判给 openpyxl 报
            # "openpyxl does not support .docx file format"
            return detect_zip_type(file_path)
        # 压缩包(改名伪装成 pdf/docx/xlsx 的 rar/7z/gzip 等)→ 不解析,统一标记 .zip
        if head.startswith((b'Rar!\x1a\x07', b'7z\xbc\xaf\x27\x1c', b'\x1f\x8b\x08')):
            return '.zip'
    except OSError:
        pass
    return os.path.splitext(file_path)[1].lower()


def detect_zip_type(file_path: str) -> str:
    """ZIP 容器(OOXML)按内部部件区分真实格式:xlsx 含 xl/,docx 含 word/。

    非 OOXML 的 ZIP(普通压缩包改名伪装)→ 返回 '.zip',不按扩展名兜底尝试
    用 openpyxl/python-docx 解析(避免 "openpyxl does not support .docx" 类误报)。
    """
    try:
        import zipfile
        with zipfile.ZipFile(file_path) as zf:
            names = zf.namelist()
    except Exception:
        return '.zip'  # 打不开的 ZIP(如加密/损坏)→ 按压缩包处理,不做 OOXML 猜测
    if any(n.startswith('xl/') for n in names):
        return '.xlsx'
    if any(n.startswith('word/') for n in names):
        return '.docx'
    if any(n.startswith('ppt/') for n in names):
        return '.pptx'
    return '.zip'


def parse_file(file_path: str) -> List[Dict]:
    """解析单个文件(按文件头探测真实格式),返回项目记录列表。"""
    return get_parser(detect_real_ext(file_path)).parse(file_path)


__all__ = ['parse_file', 'get_parser', 'detect_real_ext', 'detect_zip_type',
           'BaseParser', 'PARSER_REGISTRY']
