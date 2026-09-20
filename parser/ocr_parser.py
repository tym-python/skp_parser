"""图片解析:OCR 提取项目清单,供 两类入口 共用同一套逻辑——

- **单独图片文件**(.png/.jpg/.jpeg):ImageOcrParser,整图 OCR → 行级解析;
- **纯图片 docx**(无表格、无正文段落,项目清单以截图形式嵌入,如 天津西青/
  湖南 2023 等):docx_parser 按 body 顺序抽出全部内嵌图 → 逐张走同一 OCR 行提取。

OCR 引擎为 PaddleOCR(懒加载单例);文本行按 行(y 分组)+ x 排序 重组后,
走行级兜底 parse_lines(序号行/分类行/续行拼接 规则与 docx 段落清单一致),
不新增解析规则。OCR 失败/无文本 → 返回空列表(记 warning,不中断)。
"""

import re
import zipfile
from typing import Any, Dict, List, Optional
from parser.base_parser import BaseParser
from util.log_util import get_logger
import cv2
import numpy as np
from parser.ocr_to_tablelines import reconstruct_table_by_header,parse_items
logger = get_logger(__file__)

# PaddleOCR 懒加载单例(初始化约数秒,首个图片文件时触发)
_OCR_ENGINE: Optional[Any] = None
_rapid_engine = None

def _get_engine() -> Any:
    """延迟初始化 RapidOCR 引擎（全局单例）。"""
    global _rapid_engine
    if _rapid_engine is None:
        from rapidocr import (
            RapidOCR,
        )
        _rapid_engine = RapidOCR(
            # params={
            #     # 检测模型：使用 server 高精度版
            #     "Det.engine_type": EngineType.ONNXRUNTIME,
            #     "Det.lang_type": LangDet.CH,
            #     "Det.model_type": ModelType.SERVER,
            #     "Det.ocr_version": OCRVersion.PPOCRV5,
            #     # 识别模型：同样使用 server 高精度版
            #     "Rec.engine_type": EngineType.ONNXRUNTIME,
            #     "Rec.lang_type": LangRec.CH,
            #     "Rec.model_type": ModelType.SERVER,
            #     "Rec.ocr_version": OCRVersion.PPOCRV5,
            # }
        )
    return _rapid_engine

def ocr_image_bytes(data: bytes) -> List[str]:
    """图片字节 → 文本行列表(按 y 分组成行、行内按 x 排序,空格连接)。

    失败(解码不了/OCR 异常/无文本)返回空列表,不抛异常。
    """
    if not data:
        return [],None
    try:
        img = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is None or img.size < 1000:
            return [],None

        result = _get_engine()(img)
        items = parse_items(result)
        if not items:
            return [],None

        return reconstruct_table_by_header(items)

    except Exception as ex:
        logger.warning(f"图片 OCR 失败: {type(ex).__name__}: {ex}")
        return [],None

def docx_image_blocks(file_path: str) -> List[bytes]:
    """按 body(正文)顺序提取 docx 内嵌图字节列表(r:embed 引用顺序)。"""
    out: List[bytes] = []
    try:
        with zipfile.ZipFile(file_path) as zf:
            doc = zf.read('word/document.xml').decode('utf-8', errors='replace')
            rels = zf.read('word/_rels/document.xml.rels').decode('utf-8', errors='replace')
        rid2target = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels))
        for rid in re.findall(r'r:embed="([^"]+)"', doc):
            target = rid2target.get(rid)
            if not target:
                continue
            target = target.lstrip('/')
            if not target.startswith('word/'):
                target = 'word/' + target
            with zipfile.ZipFile(file_path) as zf:
                out.append(zf.read(target))
    except Exception as ex:
        logger.warning(f"{file_path}: 提取内嵌图片失败: {ex}")
    return out


class ImageOcrParser(BaseParser):
    """单独图片文件(.png/.jpg/.jpeg)的项目清单解析:整图 OCR → 行级兜底。"""

    SUPPORTED_EXT = ('.png', '.jpg', '.jpeg')

    def parse(self, file_path: str) -> List[Dict[str, Any]]:
        with open(file_path, 'rb') as f:
            data = f.read()
        lines,_ = ocr_image_bytes(data)
        if not lines:
            logger.warning(f"{file_path}: 图片未识别到文本(疑似非清单图片)")
            return []
        context: Dict[str, str] = {}
        if _ == 'lines':
            return self.filter_blank_projects(self.parse_lines(lines, context))
        elif _ == 'table':
            return self.extract_rows_from_table(lines, context)[0]
