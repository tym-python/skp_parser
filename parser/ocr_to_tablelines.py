"""
表格 OCR 解析模块

整体流程：
  1. RapidOCR 识别图片 → items（text + 坐标）
  2. 表头定位（优先表格线，回退文本方案）
  3. 表头定列 → 数据 items 按 x 落列
  4. 每列合并单元格（表格线硬边界 / 自适应阈值）
  5. 以锚点列（项目名称）分行
  6. 渲染为 List[List[str]]
"""
import traceback
import re
from typing import List, Dict, Any, Tuple, Optional
import logging

import cv2
import numpy as np

from parser.field_mapping import HEADER_ALIASES

logger = logging.getLogger(__name__)

_rapid_engine = None

# 0. 引擎：延迟初始化 RapidOCR
def _get_engine():
    global _rapid_engine
    if _rapid_engine is None:
        from rapidocr import RapidOCR
        _rapid_engine = RapidOCR()
    return _rapid_engine

# 1. OCR 结果 → items
def parse_items(result) -> List[Dict[str, Any]]:
    """把 RapidOCR 输出转换为统一的 items 列表。

    每个 item 包含文本 + 边界框 + 中心点 + 宽高。
    OCR 文本会做一些清洗：去页码、去 "- N -"、去水印。
    """
    if result.boxes is None or result.txts is None:
        return []

    items = []
    for poly, text in zip(result.boxes, result.txts):
        # 文本清洗：页码 / 页脚 / 水印
        text = re.sub(r'第?\s*\d+\s*页\s*[，,、/]?\s*共\s*\d+\s*页', ' ', text).strip()
        text = re.sub(r'^\s*-\s*\d+\s*-\s*$', ' ', text).strip()
        text = re.sub(r'基建通', '', text).strip()
        if not text:
            continue

        xs = [float(p[0]) for p in poly]
        ys = [float(p[1]) for p in poly]
        items.append({
            'text': text,
            'x0': min(xs), 'x1': max(xs),
            'y0': min(ys), 'y1': max(ys),
            'xc': sum(xs) / 4.0,
            'yc': sum(ys) / 4.0,
            'h': max(ys) - min(ys),
            'w': max(xs) - min(xs),
        })
    return items


# 2. 顶部标题行识别（含金额单位行）

# 标题关键字：命中则判为标题
TITLE_KEYWORDS = (
    '项目清单', '清单汇总', '项目分布', '重点项目', '项目计划表',
    '建设项目清单', '项目表', '项目一览', '项目汇总',
)

# 金额单位行正则，如"金额单位：万元"、"单位：亿元"
UNIT_LINE_RE = re.compile(r'(?:金额)?单位\s*[:：]\s*[万亿]元')


def _detect_title_rows(
        phys_rows: List[List[Dict]],
        avg_h: float,
        img_width: int,
) -> int:
    """检测图片顶部标题占据的物理行数（不含表头）。

    标题特征（满足任一即判为标题）：
      1. 包含标题关键字
      2. 字高 > 1.2 * avg_h，且横向跨度 > 40% 图宽
      3. 字高 > 1.2 * avg_h，且该行只有一个 item
    只检查最上面 5 行，避免误伤表头。
    """
    if not phys_rows:
        return 0

    title_count = 0
    for row in phys_rows[:5]:
        # 这一行取最高的 item 作为判断依据
        tallest = max(row, key=lambda x: x['h'])
        text = ''.join(x['text'] for x in row)
        text_clean = text.replace(' ', '').replace('\u3000', '')

        # 条件 1：关键字命中
        if any(kw in text for kw in TITLE_KEYWORDS):
            title_count += 1
            continue

        # 条件 2：金额单位行
        if UNIT_LINE_RE.search(text_clean):
            title_count += 1
            continue

        # 条件 3：大字 + 横跨
        if tallest['h'] > avg_h * 1.2 and tallest['w'] > img_width * 0.4:
            title_count += 1
            continue

        # 条件 4：大字 + 单 item
        if tallest['h'] > avg_h * 1.2 and len(row) == 1:
            title_count += 1
            continue

        # 一旦不满足就停，避免把表头也吃掉
        break

    return title_count


def _remove_title_and_unit_rows(
        items: List[Dict],
        avg_h: float,
        img_width: int,
) -> List[Dict]:
    """从 items 顶部移除标题行和金额单位行。

    返回移除后的 items 列表。
    若未检出标题行，原样返回。
    """
    if not items:
        return items

    phys_rows = _split_physical_rows(items, avg_h)
    title_n = _detect_title_rows(phys_rows, avg_h, img_width)
    if title_n <= 0:
        return items

    # 收集要排除的 items（用 id 避免 dict 不可哈希问题）
    to_exclude = set()
    for row in phys_rows[:title_n]:
        for it in row:
            to_exclude.add(id(it))

    print(f'移除顶部 {title_n} 行（标题/单位），共 {len(to_exclude)} 个 items')
    return [it for it in items if id(it) not in to_exclude]


# 4. 物理行切分（仅用于表头识别的文本方案）

def _split_physical_rows(items: List[Dict], avg_h: float) -> List[List[Dict]]:
    """按 y 中心把 items 聚成物理行。"""
    if not items:
        return []

    items_sorted = sorted(items, key=lambda x: x['yc'])
    rows = []
    curr = [items_sorted[0]]
    for it in items_sorted[1:]:
        curr_yc = sum(x['yc'] for x in curr) / len(curr)
        if abs(it['yc'] - curr_yc) < avg_h * 0.8:
            curr.append(it)
        else:
            rows.append(curr)
            curr = [it]
    rows.append(curr)
    return rows


# 6. 表格线检测

def _detect_horizontal_lines(img: np.ndarray, min_width_ratio: float = 0.5) -> List[float]:
    """检测图像中的长横线，返回它们的 y 坐标列表（升序，已合并粗线）。

    参数：
        img: BGR 图像
        min_width_ratio: 横线最小长度 / 图像宽度，用于过滤文字笔画
    返回：
        横线 y 坐标列表
    """
    if img is None or img.size == 0:
        return []

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # 横向形态学：只保留长横线
    kernel_w = max(20, int(img.shape[1] * min_width_ratio))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_w, 1))
    horizontal = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    # 每一行是否有横线
    row_sum = horizontal.sum(axis=1) // 255
    rows_with_line = np.where(row_sum > 0)[0]
    if len(rows_with_line) == 0:
        return []

    # 相邻 3 px 内的合并为一条线（避免粗线被拆成多条）
    lines = []
    curr_group = [int(rows_with_line[0])]
    for r in rows_with_line[1:]:
        r = int(r)
        if r - curr_group[-1] <= 3:
            curr_group.append(r)
        else:
            lines.append(float(np.mean(curr_group)))
            curr_group = [r]
    lines.append(float(np.mean(curr_group)))
    return lines


def _detect_vertical_lines(
        img: np.ndarray,
        min_height_ratio: float = 0.3,
        min_length_px: int = 30,
) -> List[float]:
    """检测图像中的长竖线，返回它们的 x 坐标列表（升序，已合并粗线）。

    参数：
        img: BGR 图像
        min_height_ratio: 竖线最小长度 / 图像高度
        min_length_px: 竖线最小像素长度（保底，防止小图 ratio 失效）
    返回：
        竖线 x 坐标列表
    """
    if img is None or img.size == 0:
        return []

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # 竖向形态学：只保留长竖线
    kernel_h = max(min_length_px, int(img.shape[0] * min_height_ratio))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_h))
    vertical = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    # 每一列是否有竖线
    col_sum = vertical.sum(axis=0) // 255
    cols_with_line = np.where(col_sum > 0)[0]
    if len(cols_with_line) == 0:
        return []

    # 相邻 3 px 内的合并为一条线
    lines = []
    curr_group = [int(cols_with_line[0])]
    for c in cols_with_line[1:]:
        c = int(c)
        if c - curr_group[-1] <= 3:
            curr_group.append(c)
        else:
            lines.append(float(np.mean(curr_group)))
            curr_group = [c]
    lines.append(float(np.mean(curr_group)))
    return lines


def _split_by_hard_boundaries(col_items: List[Dict], boundaries: List[float]) -> List[List[Dict]]:
    """按硬边界（横线 y 坐标）把 col_items 切分成单元格组。

    boundaries 已升序排列，且第一个是表格上边界、最后一个是下边界。
    每个 item 按其 y 中心落入哪条带，就归到对应单元格。
    """
    if not col_items:
        return []
    if len(boundaries) < 2:
        return [col_items]

    def which_band(yc):
        for i in range(len(boundaries) - 1):
            if boundaries[i] <= yc < boundaries[i + 1]:
                return i
        return -1 if yc < boundaries[0] else len(boundaries) - 2

    cells = []
    curr = []
    curr_band = None
    for it in sorted(col_items, key=lambda x: x['y0']):
        it_yc = (it['y0'] + it['y1']) / 2.0
        band = which_band(it_yc)
        if curr_band is None:
            curr_band = band
            curr = [it]
        elif band == curr_band:
            curr.append(it)
        else:
            if curr:
                cells.append(curr)
            curr = [it]
            curr_band = band
    if curr:
        cells.append(curr)
    return cells


# 7. 表头定位 —— 表格线方案（优先）

def _detect_header_by_lines(
        items: List[Dict],
        horizontal_lines: List[float],
        avg_h: float,
) -> Tuple[List[Dict], List[Dict]]:
    """用表格线定位表头。
    直接取第一根长横线作为表头下边界（表格第一条分隔线）
    返回 (header_items, body_items)。
    若无法可靠定位，返回 ([], items)，由调用方回退文本方案。
    """
    if not horizontal_lines:
        return [], items

    top = horizontal_lines[0]

    # 从 lines[1] 开始，找第一条"到 top 的高度能容纳 1~3 行文字"的线
    header_bottom = None
    for i in range(1, min(4, len(horizontal_lines))):
        h = horizontal_lines[i] - top
        rows_est = h / avg_h if avg_h > 0 else 0
        if 0.8 <= rows_est <= 3.5:
            header_bottom = horizontal_lines[i]
            break

    if header_bottom is None:
        return [], items  # 定位失败，交给调用方兜底

    # 按表头下边框切分 items
    header_items = []
    body_items = []
    for it in items:
        text = (it.get('text') or '').strip()
        if not text:
            continue
        it_yc = (it['y0'] + it['y1']) / 2.0
        if it_yc < header_bottom:
            header_items.append(it)
        else:
            body_items.append(it)

    # 校验：表头至少要能凑出 2 列
    if len(header_items) < 2:
        return [], items

    return header_items, body_items


# 9. 表头定列


def _build_columns_from_vertical_lines(
        vertical_lines: List[float],
        img_width: int,
        header_items: Optional[List[Dict]] = None,
        avg_h: float = 20.0,
) -> List[Dict]:
    """用竖线硬边界构造列定义。

    返回 [{x0, x1, xc, header}, ...]
    header 从表头 items 里按 x 区间抽取。

    若竖线数量 < 2，返回空列表（调用方回退表头聚类方案）。
    """
    if len(vertical_lines) < 2:
        return []

    lines = sorted(vertical_lines)
    min_gap = avg_h * 0.5

    # 1) 判断是否补左边界：竖线左侧"确有表头 items"

    if lines[0] > min_gap and header_items:
        has_left_content = any(it['xc'] < lines[0] for it in header_items)
        if has_left_content:
            lines = [0.0] + lines

    # 2) 判断是否补右边界：竖线右侧"确有表头 items"

    if img_width - lines[-1] > min_gap and header_items:
        has_right_content = any(it['xc'] > lines[-1] for it in header_items)
        if has_right_content:
            lines = lines + [float(img_width)]

    n_cols = len(lines) - 1
    if n_cols < 2:
        return []

    # 3) 用 header_items 数量校验列数

    if header_items:
        n_headers = len(header_items)
        # 表头可能有多行（header_items > 列数），
        # 也可能有合并单元格（header_items < 列数）。
        # 允许的比值区间：[0.5, 2.5]。
        if n_headers < n_cols * 0.5 or n_headers > n_cols * 2.5:
            logger.info(
                f'竖线列数与表头 items 数不匹配: '
                f'n_cols={n_cols}, n_headers={n_headers}，放弃'
            )
            return []

    col_defs = []
    for i in range(len(lines) - 1):
        x0, x1 = lines[i], lines[i + 1]
        col_defs.append({
            'x0': x0,
            'x1': x1,
            'xc': (x0 + x1) / 2.0,
            'header': '',  # 后面用表头 items 回填
        })

    # 用表头 items 回填每列的 header 文本
    if header_items:
        buckets: List[List[Dict]] = [[] for _ in col_defs]
        for it in header_items:
            xc = it['xc']
            for i, c in enumerate(col_defs):
                if c['x0'] <= xc < c['x1']:
                    buckets[i].append(it)
                    break
        for i, col in enumerate(col_defs):
            col_sorted = sorted(buckets[i], key=lambda x: (x['y0'], x['x0']))
            col['header'] = ''.join(x['text'] for x in col_sorted)

    return col_defs


def _validate_vertical_columns(
        col_defs: List[Dict],
        header_items: List[Dict],
) -> bool:
    """校验竖线列定义是否合理。

    判据：
      1. 列数 >= 2
      2. 每列宽度不能过窄（< 15px 基本是误检）
      3. 表头 items 应该能落满大部分列
    """
    if len(col_defs) < 2:
        return False

    # 宽度检查
    widths = [c['x1'] - c['x0'] for c in col_defs]
    if any(w < 15 for w in widths):
        return False

    # 覆盖率检查：表头 items 至少落到一半以上的列
    hit_cols = set()
    for it in header_items:
        for i, c in enumerate(col_defs):
            if c['x0'] <= it['xc'] < c['x1']:
                hit_cols.add(i)
                break
    if len(hit_cols) < max(2, len(col_defs) // 2):
        return False

    return True


# 10. 把 item 分配到某一列

def _assign_column(xc: float, col_defs: List[Dict]) -> int:
    """按竖线边界把 xc 分配到某列索引。
    vertical_lines 已升序，且首尾已补齐到 [0, img_width]。
    """
    for i, c in enumerate(col_defs):
        if c['x0'] <= xc < c['x1']:
            return i
    # 越界：左侧 → 0，右侧 → 最后一列
    if col_defs and xc < col_defs[0]['x0']:
        return 0
    return max(0, len(col_defs) - 1)


# 11. 单元格内文字拼接

def _cell_text(cell_items: List[Dict], avg_h: float) -> str:
    """把一个单元格内的多个 items 按阅读顺序拼接：
       先按 y 分行，行内按 x 排序，行间用空格连接。
    """
    if not cell_items:
        return ""
    cell_items = sorted(cell_items, key=lambda x: (x['y0'], x['x0']))

    text_lines = []
    currline = [cell_items[0]]
    for idx, it in enumerate(cell_items[1:], start=1):
        max_y1 = max(x['y1'] for x in currline)
        if max_y1 <= it['y0'] + it['h'] * 0.25:  # 换行
            currline.sort(key=lambda x: x['x0'])
            text_lines.append(''.join(x['text'] for x in currline))
            currline = [it]  # 赋新行
        else:  # 同行
            currline.append(it)
    text_lines.append(''.join(x['text'] for x in currline))

    return ' '.join(text_lines)


# 12. 列内合并单元格（自适应阈值）

# 13. 锚点列：以"项目名称"列为骨架分行

def _find_anchor_col_idx(col_defs: List[Dict], keyword: str = "项目名称") -> int:
    """在表头列定义里找到包含关键字的列索引。"""
    for i, c in enumerate(col_defs):
        if keyword in c.get('header', ''):
            return i
    return -1  # 没找到


def group_cells_into_rows_with_anchor(
        all_cells: List[Dict],
        anchor_col_idx: int,
        avg_h: float,
) -> List[List[Dict]]:
    """以项目名称列为锚点分行。

    - 项目名称列：独立合并出的每个 cell = 一个逻辑行
    - 其他列：按 y 重叠挂到某个锚点行上，绝不跨两个锚点
    """
    if not all_cells:
        return []

    # ---------- 1) 取出锚点列的 cells，定义行骨架 ----------
    anchor_cells = [c for c in all_cells if c['col_idx'] == anchor_col_idx]
    anchor_cells.sort(key=lambda x: x['y0'])

    anchor_rows = []
    for ac in anchor_cells:
        anchor_rows.append({
            'y0': ac['y0'],
            'y1': ac['y1'],
            'cells': [ac],
        })

    # ---------- 2) 其他列的 cells 挂靠到锚点行 ----------
    for c in all_cells:
        if c['col_idx'] == anchor_col_idx:
            continue

        # 找 y 重叠最大的锚点行
        best_row = None
        best_ov = 0.0
        for row in anchor_rows:
            ov = min(row['y1'], c['y1']) - max(row['y0'], c['y0'])
            if ov > best_ov:
                best_ov = ov
                best_row = row

        if best_row is not None and best_ov > 0.3:
            # 有重叠 → 挂到该行
            best_row['cells'].append(c)
        else:
            # 无重叠 → 取 y 中心最近的锚点行
            c_yc = (c['y0'] + c['y1']) / 2.0
            best_row = min(
                anchor_rows,
                key=lambda r: abs((r['y0'] + r['y1']) / 2.0 - c_yc),
            )
            best_row['cells'].append(c)

    # ---------- 3) 行内按 col_idx 排序 ----------
    result = []
    for row in anchor_rows:
        row['cells'].sort(key=lambda x: x['col_idx'])
        result.append(row['cells'])
    return result


# 14. 主函数：按表头定列重建表格

def reconstruct_table_by_header(items: List[Dict], img: np.ndarray = None) -> Tuple[List[List[str]], str]:
    if not items:
        return [], 'lines'

    img_width = img.shape[1] if img is not None else 0

    # 步骤 0：清除标题行和金额单位行

    avg_h = sum(it['h'] for it in items) / len(items)
    items = _remove_title_and_unit_rows(items, avg_h, img_width)
    if not items:
        return [], 'lines'

    avg_h = sum(it['h'] for it in items) / len(items)

    # 1) 检测表格线（横 + 竖）

    horizontal_lines = _detect_horizontal_lines(img) if img is not None else []
    vertical_lines = _detect_vertical_lines(img) if img is not None else []
    logger.info(f'检测到 {len(horizontal_lines)} 条横线, {len(vertical_lines)} 条竖线')

    # 2) 无表格线 → 直接降级为段落

    if len(horizontal_lines) < 3 or len(vertical_lines) < 2:
        logger.info('表格线不足，降级为段落模式')
        return _fallback_paragraph(items), 'lines'

    # 3) 用横线定位表头

    header_items, body_items = _detect_header_by_lines(
        items, horizontal_lines, avg_h,
    )
    if not header_items:
        logger.info('表格线定表头失败，降级为段落模式')
        return _fallback_paragraph(items), 'lines'

    if not body_items:
        logger.info('无数据行，降级为段落模式')
        return _fallback_paragraph(items), 'lines'

    # 4) 用竖线定列

    candidate = _build_columns_from_vertical_lines(
        vertical_lines, img_width, header_items, avg_h,
    )
    if not candidate or not _validate_vertical_columns(candidate, header_items):
        logger.info('竖线定列失败，降级为段落模式')
        return _fallback_paragraph(items), 'lines'

    col_defs = candidate
    logger.info(f'用竖线定列，共 {len(col_defs)} 列')

    if len(col_defs) < 2:
        return _fallback_paragraph(items), 'lines'

    # 5) 找锚点列

    project_name_col_idx = _find_anchor_col_idx(col_defs, keyword="项目名称")
    if project_name_col_idx < 0:
        project_name_col_idx = 1

    # 6) 数据 items 按列落位

    col_items_list: List[List[Dict]] = [[] for _ in col_defs]
    for it in body_items:
        idx = _assign_column(it['xc'], col_defs)
        col_items_list[idx].append(it)

    # 7) 用横线硬边界合并单元格

    all_cells: List[Dict] = []
    print('使用表格线方案')

    body_y0 = min(it['y0'] for it in body_items)
    body_y1 = max(it['y1'] for it in body_items)
    boundaries = list(horizontal_lines)
    if boundaries[-1] < body_y1:
        boundaries = boundaries + [body_y1]

    for col_idx, col_items in enumerate(col_items_list):
        for cell in _split_by_hard_boundaries(col_items, boundaries):
            all_cells.append({
                'col_idx': col_idx,
                'x0': min(x['x0'] for x in cell),
                'x1': max(x['x1'] for x in cell),
                'y0': min(x['y0'] for x in cell),
                'y1': max(x['y1'] for x in cell),
                'text': _cell_text(cell, avg_h),
            })

    if not all_cells:
        return _fallback_paragraph(items), 'lines'

    # 8) 用锚点分行

    rows = group_cells_into_rows_with_anchor(all_cells, project_name_col_idx, avg_h)

    # 9) 输出

    result: List[List[Any]] = []
    result.append([c['header'] for c in col_defs])
    for row in rows:
        cells = [""] * len(col_defs)
        for c in row:
            idx = c['col_idx']
            if cells[idx]:
                cells[idx] += " " + c['text']
            else:
                cells[idx] = c['text']
        if any(c.strip() for c in cells):
            result.append(cells)

    return result, 'table'


# 15. 降级：段落模式

def _fallback_paragraph(items: List[Dict]) -> List[str]:
    """无法识别为表格时，退回按行输出纯文本。"""
    if not items:
        return []

    avg_h = sum(it['h'] for it in items) / len(items)
    items_sorted = sorted(items, key=lambda x: (x['y0'], x['x0']))

    lines = []
    for it in items_sorted:
        placed = False
        for line in lines:
            line_yc = sum(x['yc'] for x in line) / len(line)
            if abs(it['yc'] - line_yc) < avg_h * 1.2:
                line.append(it)
                placed = True
                break
        if not placed:
            lines.append([it])

    lines.sort(key=lambda l: sum(x['yc'] for x in l) / len(l))
    return [
        ' '.join(x['text'] for x in sorted(l, key=lambda y: y['x0']))
        for l in lines
    ]


# 16. 统一入口
def ocr_image_bytes(data: bytes) -> List[str]:
    """图片字节 → (result, mode)。

    mode = 'table'：result 是 List[List[str]]，第一行为表头
    mode = 'lines'：result 是 List[str]，每行一段文本
    """
    if not data:
        return [], None
    try:
        img = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is None or img.size < 1000:
            return [], None

        result = _get_engine()(img)
        items = parse_items(result)
        if not items:
            return [], None

        return reconstruct_table_by_header(items, img=img)

    except Exception as ex:
        traceback.print_exc()
        logger.warning(f"OCR 失败: {type(ex).__name__}: {ex}")
        return [], None


# 17. 批量遍历脚本

# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
遍历指定目录及其所有子目录，每个文件夹取一张图片。
"""

import os
from pathlib import Path

# 支持的图片扩展名
IMAGE_EXTS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp',
    '.tif', '.tiff', '.ico', '.jfif', '.avif', '.heic',
}


def iter_one_image_per_folder(root, exts=IMAGE_EXTS, sort=True):
    """生成器：每遍历到一个含图片的文件夹，产出一个 (文件夹路径, 图片路径)。"""
    root = Path(root)
    if not root.is_dir():
        raise NotADirectoryError(f"不是有效目录: {root}")

    for dirpath, dirnames, filenames in os.walk(root):
        # 跳过隐藏文件夹（不需要可删掉这一行）
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]

        images = [
            f for f in filenames
            if not f.startswith('.') and Path(f).suffix.lower() in exts
        ]

        if images:
            if sort:
                images.sort()  # 按文件名排序，取第一张
            yield Path(dirpath), Path(dirpath) / images[0]


def main(root_path):
    count = 0
    for folder, image in iter_one_image_per_folder(root_path):
        print(f"[文件夹] {folder}")
        print(f"[图片]   {image}\n")
        count += 1

        with open(image, 'rb') as f:
            data = f.read()

        lines, _ = ocr_image_bytes(data)
        for ln in lines:
            print(ln)
        print('=' * 30, len(lines))

        # 这里可以对 image 做你想做的事，比如：
        # shutil.copy(image, "output/")        # 复制
        # Image.open(image).thumbnail((256,256))  # 缩略图

    print(f"共在 {count} 个文件夹中各找到 1 张图片。")


if __name__ == "__main__":
    batch_flag = False

    if batch_flag:
        main(r'E:\STangWork\STangFiles\各省重点项目：2020年起')
    else:
        # file_path = r"2023年重点项目\04重庆市2023年重点项目清单\2023年开州区\15.jpg"
        file_path = r"2023年重点项目\14贵州省2023年重点项目清单\2023年黔东南州\5.jpg"
        full_path = r'E:\STangWork\STangFiles\各省重点项目：2020年起' + '\\' + file_path
        # full_path = r'E:\STangWork\STangFiles\各省重点项目：2020年起\2023年重点项目\19湖北省2023年重点项目清单\2023年十堰市\十堰市2023年省级重点项目清单1.png'
        # full_path = r'E:\STangWork\STangFiles\各省重点项目：2020年起\2026年重点项目\19湖北省2026年重点项目清单\2026年荆州市\荆州市2026年省级重点项目清单.png'

        with open(full_path, 'rb') as f:
            data = f.read()

        lines, _ = ocr_image_bytes(data)
        for ln in lines:
            print(ln)
        print('=' * 30, len(lines))
