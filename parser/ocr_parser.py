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
logger = get_logger(__file__)

# PaddleOCR 懒加载单例(初始化约数秒,首个图片文件时触发)
_OCR_ENGINE: Optional[Any] = None
_rapid_engine = None

def _ocr_engine() -> Any:
    global _OCR_ENGINE
    if _OCR_ENGINE is None:
        from paddleocr import PaddleOCR
        _OCR_ENGINE = PaddleOCR(lang='ch', use_doc_orientation_classify=False,
                                use_doc_unwarping=False,
                                use_textline_orientation=False)
    return _OCR_ENGINE

def _get_engine() -> Any:
    """延迟初始化 RapidOCR 引擎（全局单例）。"""
    global _rapid_engine
    if _rapid_engine is None:
        from rapidocr import (
            RapidOCR,
            ModelType,
            EngineType,
            LangDet,
            LangRec,
            OCRVersion,
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

def ocr_image_bytes_paddleocr(data: bytes) -> List[str]:
    """图片字节 → 文本行列表(按 y 分组成行、行内按 x 排序,空格连接)。

    失败(解码不了/OCR 异常/无文本)返回空列表,不抛异常。
    """
    if not data:
        return []
    try:
        import cv2
        import numpy as np
        img = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is None or img.size < 1000:
            return []
        result = _ocr_engine().predict(img)
        page = result[0]
        polys = [list(map(list, poly)) for poly in page['rec_polys']]
        items = sorted(zip(polys, page['rec_texts']),
                       key=lambda it: (it[0][0][1], it[0][0][0]))
        lines: List[List[Any]] = []  # [y中心, 行高, [(x0, 文本)...]]
        for poly, text in items:
            yc = sum(p[1] for p in poly) / 4
            x0 = min(p[0] for p in poly)
            h = max(p[1] for p in poly) - min(p[1] for p in poly)
            if lines and abs(yc - lines[-1][0]) < max(8, lines[-1][1] * 0.6):
                lines[-1][2].append((x0, text))
                lines[-1][0] = yc
            else:
                lines.append([yc, h, [(x0, text)]])
        return [' '.join(t for _, t in sorted(cells)) for _, _, cells in lines]
    except Exception as ex:
        logger.warning(f"图片 OCR 失败: {type(ex).__name__}: {ex}")
        return []

def ocr_image_bytes(data: bytes) -> List[str]:
    """图片字节 → 文本行列表(按 y 分组成行、行内按 x 排序,空格连接)。

    失败(解码不了/OCR 异常/无文本)返回空列表,不抛异常。
    """
    if not data:
        return []
    try:
        img = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is None or img.size < 1000:
            return []

        result = _get_engine()(img)
        if result.boxes is None or result.txts is None or len(result.txts) == 0:
            return []

        # 1. 整理所有检测框信息
        items = []
        for poly, text in zip(result.boxes, result.txts):
            xs = [float(p[0]) for p in poly]
            ys = [float(p[1]) for p in poly]
            items.append({
                'text': text,
                'x0': min(xs), 'y0': min(ys),
                'x1': max(xs), 'y1': max(ys),
                'xc': sum(xs) / 4.0, 'yc': sum(ys) / 4.0,
                'h': max(ys) - min(ys)
            })

        # 2. 按 y0 粗排，保证后续遍历顺序稳定
        items.sort(key=lambda it: (it['y0'], it['x0']))

        # 3. 行分组：使用更宽松的动态阈值
        lines = []
        for it in items:
            placed = False
            for line in lines:
                line_yc = sum(x['yc'] for x in line) / len(line)
                line_h = sum(x['h'] for x in line) / len(line)

                # 动态放宽阈值，允许换行文本和垂直居中的序号合并到同一行
                threshold = max(20, 1.2 * max(it['h'], line_h))
                if abs(it['yc'] - line_yc) < threshold:
                    line.append(it)
                    placed = True
                    break
            if not placed:
                lines.append([it])

        # 4. 按行的平均 Y 中心点排序
        lines.sort(key=lambda line: sum(x['yc'] for x in line) / len(line))

        # 5. 行内按 X 排序，空格连接
        res = []
        for line in lines:
            line.sort(key=lambda x: x['x0'])
            res.append(' '.join(x['text'] for x in line))
        return res

    except Exception as ex:
        logger.warning(f"图片 OCR 失败: {type(ex).__name__}: {ex}")
        return []

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
        lines = ocr_image_bytes(data)
        if not lines:
            logger.warning(f"{file_path}: 图片未识别到文本(疑似非清单图片)")
            return []
        context: Dict[str, str] = {}
        return self.filter_blank_projects(self.parse_lines(lines, context))
