"""
表格 OCR 解析模块

整体流程：
  1. RapidOCR 识别图片 → items（text + 坐标）
  2. 清除顶部标题行 / 金额单位行
  3. 检测横线（定位表头）与竖线（定义列）
  4. 无足够表格线 → 降级为段落模式
  5. 横线定表头 → 竖线定列 → body items 落列
  6. 横线硬边界切分单元格 → 锚点列（项目名称）分行
  7. 渲染为 (result, mode)

返回约定：
  - mode='table'：result 为 List[List[str]]，第一行是表头
  - mode='lines'：result 为 List[str]，每行一段纯文本
"""

import re
import traceback
from bisect import bisect_right
from typing import List, Dict, Any, Tuple, Optional

import cv2
import numpy as np

_rapid_engine = None

# ============================================================
# 0. 引擎：延迟初始化 RapidOCR
# ============================================================
def _get_engine():
    """RapidOCR 引擎全局单例（首次调用时加载模型）。"""
    global _rapid_engine
    if _rapid_engine is None:
        from rapidocr import RapidOCR
        _rapid_engine = RapidOCR()
    return _rapid_engine

# ============================================================
# 1. OCR 结果 → items
# ============================================================
def parse_items(result) -> List[Dict[str, Any]]:
    """RapidOCR 输出 → 统一 items 列表。

    每个 item 含文本 + 边界框 + 中心点 + 宽高。
    文本会做清洗：去页码、去 "- N -"、去水印。
    """
    if result.boxes is None or result.txts is None:
        return []

    items = []
    for poly, text in zip(result.boxes, result.txts):
        # 文本清洗：页码 / 页脚 / 水印
        text = re.sub(r'第?\s*\d+\s*页\s*[，,、/]?\s*共\s*\d+\s*页', ' ', text).strip()
        text = re.sub(r'^\s*-\s*\d+\s*-\s*$', ' ', text).strip()
        watermark = re.fullmatch(r'基建通|建通', text)
        if not text:
            continue
        if watermark:
            continue

        xs = [float(p[0]) for p in poly]
        ys = [float(p[1]) for p in poly]
        items.append({
            'text': text,
            'x0': min(xs), 'x1': max(xs),
            'y0': min(ys), 'y1': max(ys),
            'xc': sum(xs) / 4.0,
            'yc': sum(ys) / 4.0,
            'h':  max(ys) - min(ys),
            'w':  max(xs) - min(xs),
        })
    return items


# ============================================================
# 2. 顶部标题行 / 金额单位行识别与剔除
# ============================================================
# 标题关键字：命中即判为标题
TITLE_KEYWORDS = (
    '项目清单', '清单汇总', '项目分布', '重点项目', '项目计划表',
    '建设项目清单', '项目表', '项目一览', '项目汇总','项目名单',
)
# 金额单位行正则，如"金额单位：万元"、"单位：亿元"
UNIT_LINE_RE = re.compile(r'(?:金额)?单位\s*[:：]\s*[万亿]元')


def _detect_title_rows(
    phys_rows: List[List[Dict]],
    avg_h: float,
    img_width: int,
) :
    """检测顶部标题占据的物理行数（不含表头）。

    标题特征（满足任一即判为标题）：
      1. 命中标题关键字
      2. 命中金额单位行正则
      3. 大字 + 横跨（h > 1.2*avg_h 且 w > 40% 图宽）
      4. 大字 + 单 item（h > 1.2*avg_h 且该行只 1 个 item）

    只检查最上面 5 行，遇到第一个不满足的行立即停止，避免吃掉表头。
    """
    if not phys_rows:
        return 0

    title_count = 0
    HEADER_UNIT_itme = []
    for row in phys_rows[:5]:
        tallest = max(row, key=lambda x: x['h'])
        text = ''.join(x['text'] for x in row)
        text_clean = text.replace(' ', '').replace('\u3000', '')

        if any(kw in text for kw in TITLE_KEYWORDS):
            title_count += 1
            continue
        if UNIT_LINE_RE.search(text_clean):
            HEADER_UNIT_itme.append(text_clean)
            title_count += 1
            continue
        if tallest['h'] > avg_h * 1.2 and tallest['w'] > img_width * 0.4:
            title_count += 1
            continue
        if tallest['h'] > avg_h * 1.2 and len(row) == 1:
            title_count += 1
            continue

        break

    return title_count,HEADER_UNIT_itme


def _remove_title_and_unit_rows(
    items: List[Dict],
    avg_h: float,
    img_width: int,
) -> List[Dict]:
    """从 items 顶部剔除标题行和金额单位行。

    用 id() 做排除，避免 dict 不可哈希。
    """
    if not items:
        return items

    phys_rows = _split_physical_rows(items, avg_h)
    title_n,HEADER_UNIT_itme = _detect_title_rows(phys_rows, avg_h, img_width)
    if title_n <= 0:
        return items

    to_exclude = {id(it) for row in phys_rows[:title_n] for it in row}
    # print(f'移除顶部 {title_n} 行（标题/单位），共 {len(to_exclude)} 个 items')
    return [it for it in items if id(it) not in to_exclude]


# ============================================================
# 3. 物理行切分（仅用于标题检测与文本方案）
# ============================================================
def _split_physical_rows(items: List[Dict], avg_h: float) -> List[List[Dict]]:
    """按 y 中心把 items 聚成物理行。

    相邻 item 的 yc 与当前行均值差距 < 0.8*avg_h → 归入同一行。
    维护 running sum，避免每轮重算均值（O(n²) → O(n)）。
    """
    if not items:
        return []

    items_sorted = sorted(items, key=lambda x: x['yc'])
    rows: List[List[Dict]] = []
    curr: List[Dict] = [items_sorted[0]]
    curr_sum = items_sorted[0]['yc']

    for it in items_sorted[1:]:
        curr_yc = curr_sum / len(curr)
        if abs(it['yc'] - curr_yc) < avg_h * 0.8:
            curr.append(it)
            curr_sum += it['yc']
        else:
            rows.append(curr)
            curr = [it]
            curr_sum = it['yc']

    rows.append(curr)
    return rows


# ============================================================
# 4. 表格线检测（横 / 竖 通用）
# ============================================================
# ============================================================
# 公共工具：合并相邻的线
# ============================================================
def _merge_adjacent_lines(indices: np.ndarray, gap: int = 3) -> List[float]:
    """把升序的坐标索引合并为若干条线。

    相邻索引差 <= gap 视为同一条粗线，取均值作为该线的坐标。
    """
    if len(indices) == 0:
        return []

    lines: List[float] = []
    group = [int(indices[0])]
    for i in indices[1:]:
        i = int(i)
        if i - group[-1] <= gap:
            group.append(i)
        else:
            lines.append(float(np.mean(group)))
            group = [i]
    lines.append(float(np.mean(group)))
    return lines


# ============================================================
# 横线检测：形态学开运算
# ============================================================
def _detect_horizontal_lines(
    img: np.ndarray,
    min_width_ratio: float = 0.5,
    min_px: int = 20,
    threshold_val: int = 200,
) -> List[float]:
    """检测长横线，返回 y 坐标升序列表。

    思路：形态学开运算只保留长度 >= max(min_px, 图宽 * min_width_ratio) 的横线。
    相邻 3px 内的横线会合并为一条。

    参数：
        min_width_ratio: 横线最小长度 / 图宽
        min_px:          横线最小像素长度（保底，防止小图 ratio 失效）
        threshold_val:   二值化阈值
    """
    if img is None or img.size == 0:
        return []

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, threshold_val, 255, cv2.THRESH_BINARY_INV)

    kw = max(min_px, int(img.shape[1] * min_width_ratio))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kw, 1))
    horizontal = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    # 每一行是否有横线
    proj = horizontal.sum(axis=1) // 255
    idxs = np.where(proj > 0)[0]
    return _merge_adjacent_lines(idxs)


# ============================================================
# 竖线检测：暗像素总量 + 最长连续段 双条件
# ============================================================
def _compute_max_run_per_column(binary_01: np.ndarray) -> np.ndarray:
    """计算每一列的最长连续 1 段长度。

    参数：
        binary_01: 0/1 二值矩阵，shape (H, W)
    返回：
        长度 W 的数组，第 x 项是第 x 列最长的连续 1 段长度
    """
    H, W = binary_01.shape

    # runs[y, x] = 以 (y, x) 结尾的连续 1 长度
    runs = np.zeros_like(binary_01)
    runs[0] = binary_01[0]
    for y in range(1, H):
        runs[y] = (runs[y - 1] + 1) * binary_01[y]

    return runs.max(axis=0)


def _detect_vertical_lines(
    img: np.ndarray,
    min_total_ratio: float = 0.3,        # 总暗像素至少占图高 30%
    min_continuous_ratio: float = 0.15,  # 最长连续段至少占图高 15%
    threshold_val: int = 180,
) -> List[float]:
    """竖线检测：暗像素总量 + 最长连续段 双条件。

    不要求竖线贯穿整图（表格中常有汇总行横跨，打断竖线），
    但要求同时满足：
      1. 该列暗像素总数 >= 图高 * min_total_ratio
      2. 该列最长连续暗像素段 >= 图高 * min_continuous_ratio

    条件 1 过滤稀疏的笔画；
    条件 2 过滤文字竖笔画（它们连续段很短）。
    两者都满足的才判为真实表格竖线。

    参数：
        min_total_ratio:      总暗像素占比下限
        min_continuous_ratio: 最长连续段占比下限
        threshold_val:        二值化阈值
    """
    if img is None or img.size == 0:
        return []

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, threshold_val, 255, cv2.THRESH_BINARY_INV)

    H, W = binary.shape
    b = (binary > 0).astype(np.int32)

    # 条件 1：每列暗像素总数
    col_total = b.sum(axis=0)

    # 条件 2：每列最长连续暗像素段
    col_max_run = _compute_max_run_per_column(b)

    # 阈值
    min_total = int(H * min_total_ratio)
    min_cont = int(H * min_continuous_ratio)

    # 同时满足两个条件才算竖线
    mask = (col_total >= min_total) & (col_max_run >= min_cont)
    cols = np.where(mask)[0]

    return _merge_adjacent_lines(cols)
# ============================================================
# 5. 按横线硬边界切分单元格
# ============================================================
def _split_by_hard_boundaries(
    col_items: List[Dict],
    boundaries: List[float],
) -> List[List[Dict]]:
    """按横线 y 坐标把某列的 items 切成单元格组。

    boundaries 升序，代表该列内的单元格分隔线 y。
    每个 item 按 yc 落入哪个区间归组。
    用 bisect 定位区间，复杂度 O(n log m)。
    """
    if not col_items:
        return []
    if len(boundaries) < 2:
        return [col_items]

    cells: List[List[Dict]] = []
    curr: List[Dict] = []
    curr_band = None

    for it in sorted(col_items, key=lambda x: x['y0']):
        it_yc = (it['y0'] + it['y1']) / 2.0
        # 落入哪个区间
        band = bisect_right(boundaries, it_yc) - 1
        band = max(0, min(band, len(boundaries) - 2))

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


# ============================================================
# 6. 表头定位 —— 横线方案
# ============================================================
def _detect_header_by_lines(
    items: List[Dict],
    horizontal_lines: List[float],
    avg_h: float,
) -> Tuple[List[Dict], List[Dict]]:
    """用横线定位表头。

    思路：
      在 horizontal_lines[0..3] 中选一条线作为表头下边界，
      使得该线"上方 items 数"和"下方 items 数"都 >= 2，
      并且上方 items 的 y 范围最紧凑（即最像表头）。

    返回 (header_items, body_items)；不可靠时返回 ([], items)。
    """
    if not horizontal_lines or not items:
        return [], items

    # 收集候选线：前 4 条（含 lines[0]）
    candidates = horizontal_lines[:4]

    best_score = -1.0
    best_bottom = None

    for bottom in candidates:
        above = [it for it in items if (it['y0'] + it['y1']) / 2 < bottom]
        below = [it for it in items if (it['y0'] + it['y1']) / 2 >= bottom]

        # 上方和下方都必须有足够 items
        if len(above) < 2 or len(below) < 2:
            continue

        # 打分：上方 items 的 y 跨度越小越像表头（表头通常 1~3 行）
        y_min = min(it['y0'] for it in above)
        y_max = max(it['y1'] for it in above)
        span = y_max - y_min
        rows_est = span / avg_h if avg_h > 0 else 0

        # 只接受 0.8~3.5 行的跨度
        if not (0.8 <= rows_est <= 3.5):
            continue

        # 越接近 1 行越好
        score = 1.0 / (1.0 + abs(rows_est - 1.0))
        if score > best_score:
            best_score = score
            best_bottom = bottom

    if best_bottom is None:
        return [], items

    header_items = [it for it in items
                    if (it['y0'] + it['y1']) / 2 < best_bottom
                    and (it.get('text') or '').strip()]
    body_items = [it for it in items
                  if (it['y0'] + it['y1']) / 2 >= best_bottom
                  and (it.get('text') or '').strip()]

    if len(header_items) < 2 or len(body_items) < 2:
        return [], items

    return header_items, body_items

# ============================================================
# 7. 表头定列 —— 竖线硬边界
# ============================================================
def _fill_column_headers(col_defs: List[Dict], header_items: List[Dict]) -> None:
    """把表头 items 按 x 落入各列，拼接成该列的 header 文本（原地修改）。"""
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


def _build_columns_from_vertical_lines(
    vertical_lines: List[float],
    img_width: int,
    header_items: Optional[List[Dict]] = None,
    avg_h: float = 20.0,
) -> List[Dict]:
    """用竖线硬边界构造列定义。

    边界补充策略：
      - 仅当竖线外侧"确有表头 items"时才补 0 / img_width
      - 补充的边界与最近竖线间距必须 > avg_h * 0.5，防止造出窄空列

    列数校验：竖线分出的列数与表头 items 数比值必须在 [0.5, 2.5] 内。

    返回 [{x0, x1, xc, header}, ...]；不可靠时返回 []。
    """
    if len(vertical_lines) < 2:
        return []

    lines = sorted(vertical_lines)
    min_gap = avg_h * 0.5

    # 补左边界：竖线左侧有表头内容
    if lines[0] > min_gap and header_items:
        if any(it['xc'] < lines[0] for it in header_items):
            lines = [0.0] + lines

    # 补右边界：竖线右侧有表头内容
    if img_width - lines[-1] > min_gap and header_items:
        if any(it['xc'] > lines[-1] for it in header_items):
            lines = lines + [float(img_width)]

    n_cols = len(lines) - 1
    if n_cols < 2:
        return []

    # 列数校验：表头 items 数与列数不应悬殊
    if header_items:
        n_headers = len(header_items)
        if n_headers < n_cols * 0.5 or n_headers > n_cols * 2.5:
            # print(f'竖线列数与表头 items 数不匹配: n_cols={n_cols}, n_headers={n_headers}')
            return []

    col_defs = [
        {
            'x0': lines[i], 'x1': lines[i + 1],
            'xc': (lines[i] + lines[i + 1]) / 2.0,
            'header': '',
        }
        for i in range(n_cols)
    ]

    if header_items:
        _fill_column_headers(col_defs, header_items)

    return col_defs


def _validate_vertical_columns(
    col_defs: List[Dict],
    header_items: List[Dict],
) -> bool:
    """校验竖线列定义是否合理。

    判据：
      1. 列数 >= 2
      2. 每列宽度 >= 15px（过滤误检的窄列）
      3. 表头 items 至少覆盖一半的列
    """
    if len(col_defs) < 2:
        return False

    if any((c['x1'] - c['x0']) < 15 for c in col_defs):
        return False

    hit_cols = set()
    for it in header_items:
        for i, c in enumerate(col_defs):
            if c['x0'] <= it['xc'] < c['x1']:
                hit_cols.add(i)
                break

    if len(hit_cols) < max(2, len(col_defs) // 2):
        return False

    return True


# ============================================================
# 8. 把 item 分配到某一列
# ============================================================
def _assign_column(xc: float, col_defs: List[Dict]) -> int:
    """按列定义的 x 区间把 xc 分配到列索引。

    落在某列区间内 → 该列；否则按 xc 大小就近落到首列 / 末列。
    """
    for i, c in enumerate(col_defs):
        if c['x0'] <= xc < c['x1']:
            return i

    if col_defs and xc < col_defs[0]['x0']:
        return 0
    return max(0, len(col_defs) - 1)


# ============================================================
# 9. 单元格内文字拼接
# ============================================================
def _cell_text(cell_items: List[Dict], avg_h: float) -> str:
    """把一个单元格内的 items 按阅读顺序拼接。

    先按 y 分行（行间用空格连接），行内按 x 排序（直接拼接）。
    """
    if not cell_items:
        return ""

    cell_items = sorted(cell_items, key=lambda x: (x['y0'], x['x0']))

    text_lines: List[str] = []
    currline = [cell_items[0]]

    for it in cell_items[1:]:
        max_y1 = max(x['y1'] for x in currline)
        if max_y1 <= it['y0'] + it['h'] * 0.25:   # 换行
            currline.sort(key=lambda x: x['x0'])
            text_lines.append(''.join(x['text'] for x in currline))
            currline = [it]
        else:                                      # 同行
            currline.append(it)

    text_lines.append(''.join(x['text'] for x in currline))
    return ' '.join(text_lines)


# ============================================================
# 10. 锚点列：以"项目名称"列为骨架分行
# ============================================================
def _find_anchor_col_idx(col_defs: List[Dict], keyword: str = "项目名称") -> int:
    """在 col_defs 里找表头含关键字的列索引，找不到返回 -1。"""
    for i, c in enumerate(col_defs):
        if keyword in c.get('header', ''):
            return i
    return -1


def group_cells_into_rows_with_anchor(
    all_cells: List[Dict],
    anchor_col_idx: int,
    avg_h: float,
) -> List[List[Dict]]:
    """以锚点列的 cells 为行骨架，其他列的 cells 按 y 重叠挂靠。

    - 锚点列：每个 cell 独立成一行骨架
    - 其他列：优先按 y 重叠最大挂靠；无重叠时按 y 中心距离最近挂靠
    """
    if not all_cells:
        return []

    # 1) 锚点列 cells 定义骨架
    anchor_cells = [c for c in all_cells if c['col_idx'] == anchor_col_idx]
    anchor_cells.sort(key=lambda x: x['y0'])
    anchor_rows = [
        {'y0': ac['y0'], 'y1': ac['y1'], 'cells': [ac]}
        for ac in anchor_cells
    ]

    # 2) 其他列 cells 挂靠
    for c in all_cells:
        if c['col_idx'] == anchor_col_idx:
            continue

        best_row, best_ov = None, 0.0
        for row in anchor_rows:
            ov = min(row['y1'], c['y1']) - max(row['y0'], c['y0'])
            if ov > best_ov:
                best_ov, best_row = ov, row

        if best_row is not None and best_ov > 0.3:
            best_row['cells'].append(c)
        else:
            c_yc = (c['y0'] + c['y1']) / 2.0
            best_row = min(
                anchor_rows,
                key=lambda r: abs((r['y0'] + r['y1']) / 2.0 - c_yc),
            )
            best_row['cells'].append(c)

    # 3) 行内按 col_idx 排序
    for row in anchor_rows:
        row['cells'].sort(key=lambda x: x['col_idx'])
    return [row['cells'] for row in anchor_rows]


# ============================================================
# 11. 主函数：按表头定列重建表格
# ============================================================
def reconstruct_table_by_header(
    items: List[Dict],
    img: np.ndarray = None,
) -> Tuple[Any, str]:
    """按表头定列重建表格。

    返回 (result, mode)：
      mode='table' → result 是 List[List[str]]，第一行为表头
      mode='lines' → result 是 List[str]，每行一段文本（由 _fallback_paragraph 产出）
    """
    if not items:
        return [], 'lines'

    img_width = img.shape[1] if img is not None else 0

    # ------------------------------------------------------------
    # 步骤 0：清除标题行 / 金额单位行（前置，对所有方案统一）
    # ------------------------------------------------------------
    avg_h = sum(it['h'] for it in items) / len(items)
    items = _remove_title_and_unit_rows(items, avg_h, img_width)
    if not items:
        return [], 'lines'
    # 清除标题后重算 avg_h（排除大字标题干扰）
    avg_h = sum(it['h'] for it in items) / len(items)

    # ------------------------------------------------------------
    # 步骤 1：检测横竖线
    # ------------------------------------------------------------
    horizontal_lines = _detect_horizontal_lines(img) if img is not None else []
    vertical_lines = _detect_vertical_lines(img) if img is not None else []
    # print(f'检测到 {len(horizontal_lines)} 条横线, {len(vertical_lines)} 条竖线')

    # ------------------------------------------------------------
    # 步骤 2：表格线不足 → 降级段落
    # ------------------------------------------------------------
    if len(horizontal_lines) < 3 or len(vertical_lines) < 2:
        # print('表格线不足，降级为段落模式')
        return _fallback_paragraph(items), 'lines'

    # ------------------------------------------------------------
    # 步骤 3：横线定表头
    # ------------------------------------------------------------
    header_items, body_items = _detect_header_by_lines(
        items, horizontal_lines, avg_h,
    )
    if not header_items or not body_items:
        # print('表格线定表头失败，降级为段落模式')
        return _fallback_paragraph(items), 'lines'

    # ------------------------------------------------------------
    # 步骤 4：竖线定列 + 校验
    # ------------------------------------------------------------
    col_defs = _build_columns_from_vertical_lines(
        vertical_lines, img_width, header_items, avg_h,
    )
    if not col_defs or not _validate_vertical_columns(col_defs, header_items):
        return _fallback_paragraph(items), 'lines'


    # ------------------------------------------------------------
    # 步骤 5：找锚点列（项目名称）
    # ------------------------------------------------------------
    anchor_col_idx = _find_anchor_col_idx(col_defs, keyword="项目名称")
    if anchor_col_idx < 0:
        anchor_col_idx = 1   # 兜底：默认第 1 列

    # ------------------------------------------------------------
    # 步骤 6：body items 按列落位
    # ------------------------------------------------------------
    col_items_list: List[List[Dict]] = [[] for _ in col_defs]
    for it in body_items:
        col_items_list[_assign_column(it['xc'], col_defs)].append(it)

    # ------------------------------------------------------------
    # 步骤 7：横线硬边界切分单元格
    # ------------------------------------------------------------
    body_y1 = max(it['y1'] for it in body_items)
    boundaries = list(horizontal_lines)
    if boundaries[-1] < body_y1:
        boundaries.append(body_y1)   # 补下边界，确保覆盖所有数据行

    all_cells: List[Dict] = []
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

    # ------------------------------------------------------------
    # 步骤 8：锚点列分行
    # ------------------------------------------------------------
    rows = group_cells_into_rows_with_anchor(all_cells, anchor_col_idx, avg_h)

    # ------------------------------------------------------------
    # 步骤 9：渲染为 List[List[str]]（第一行为表头）
    # ------------------------------------------------------------
    result: List[List[str]] = [[c['header'] for c in col_defs]]
    for row in rows:
        cells = [""] * len(col_defs)
        for c in row:
            idx = c['col_idx']
            cells[idx] = (cells[idx] + " " + c['text']) if cells[idx] else c['text']
        if any(c.strip() for c in cells):
            result.append(cells)

    return result, 'table'


# ============================================================
# 12. 降级：段落模式
# ============================================================
def _fallback_paragraph(items: List[Dict]) -> List[str]:
    """无法识别为表格时，按 y 分行输出纯文本行。

    每行内 items 按 x 排序，空格拼接。
    """
    if not items:
        return []

    avg_h = sum(it['h'] for it in items) / len(items)
    items_sorted = sorted(items, key=lambda x: (x['y0'], x['x0']))

    lines: List[List[Dict]] = []
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


# ============================================================
# 13. 统一入口
# ============================================================
def ocr_image_bytes(data: bytes) -> Tuple[Any, Optional[str]]:
    """图片字节 → (result, mode)。

    mode='table' → result 是 List[List[str]]，第一行为表头
    mode='lines' → result 是 List[str]，每行一段文本
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
        print(f"OCR 失败: {type(ex).__name__}: {ex}")
        return [], None


# ============================================================
# 14. 批量遍历脚本
# ============================================================
#!/usr/bin/env python3
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
    """
    生成器：每遍历到一个含图片的文件夹，产出一个 (文件夹路径, 图片路径)。
    """
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
                images.sort()          # 按文件名排序，取第一张
            yield Path(dirpath), Path(dirpath) / images[0]


def main(root_path):
    count = 0
    for folder, image in iter_one_image_per_folder(root_path):
        print(f"[文件夹] {folder}")
        print(f"[图片]   {image}\n")
        count += 1
        with open(image, 'rb') as f:
            data = f.read()

        lines,_ = ocr_image_bytes(data)
        for ln in lines:
            print(ln)
        print('='*30,len(lines))

        # 这里可以对 image 做你想做的事，比如：
        # shutil.copy(image, "output/")        # 复制
        # Image.open(image).thumbnail((256,256))  # 缩略图

    print(f"共在 {count} 个文件夹中各找到 1 张图片。")


if __name__ == "__main__":
    batch_flag = False

    if batch_flag:
        main(r'E:\STangWork\STangFiles\各省重点项目：2020年起')
    else:
        # file_path= r"2023年重点项目\04重庆市2023年重点项目清单\2023年开州区\15.jpg"
        # file_path= r"2023年重点项目\14贵州省2023年重点项目清单\2023年黔东南州\5.jpg"
        # full_path = r'E:\STangWork\STangFiles\各省重点项目：2020年起' +'\\'+ file_path
        # full_path = r'E:\STangWork\STangFiles\各省重点项目：2020年起\2023年重点项目\19湖北省2023年重点项目清单\2023年十堰市\十堰市2023年省级重点项目清单1.png'
        # full_path = r'E:\STangWork\STangFiles\各省重点项目：2020年起\2026年重点项目\19湖北省2026年重点项目清单\2026年荆州市\荆州市2026年省级重点项目清单.png'
        full_path = r'E:\STangWork\STangFiles\各省重点项目：2020年起\2023年重点项目\19湖北省2023年重点项目清单\2023年十堰市\十堰市2023年省级重点项目清单1.png'
        full_path = r'E:\STangWork\STangFiles\各省重点项目：2020年起\2023年重点项目\19湖北省2023年重点项目清单\2023年十堰市\十堰市2023年省级重点项目清单1.png'
        full_path = r'E:\STangWork\STangFiles\各省重点项目：2020年起\2023年重点项目\19湖北省2023年重点项目清单\2023年十堰市\十堰市2023年省级重点项目清单1.png'
        full_path = r'E:\STangWork\STangFiles\各省重点项目：2020年起\2023年重点项目\20湖南省2023年重点项目清单\湖南1.png'
        # full_path = r'E:\STangWork\STangFiles\各省重点项目：2020年起\2024年重点项目\11福建省2024年重点项目清单\厦门市2024年\ilovepdf_pages-to-jpg\2024年厦门市重点项目名单（简版）_page-0001.jpg'
        # t = r'''E:\STangWork\STangFiles\各省重点项目：2020年起\2023年重点项目\19湖北省2023年重点项目清单\2023年十堰市\十堰市2023年省级重点项目清单1.png
        # E:\STangWork\STangFiles\各省重点项目：2020年起\2023年重点项目\19湖北省2023年重点项目清单\2023年荆州市\荆州市2023年省级重点项目清单.png
        # E:\STangWork\STangFiles\各省重点项目：2020年起\2024年重点项目\02上海市2024年重点项目清单\金山区2024年\金山2024年重大工程（新开）一览表.png
        # E:\STangWork\STangFiles\各省重点项目：2020年起\2024年重点项目\19湖北省2024年重点项目清单\荆州市2024年\荆州市2024年省级重点项目清单.png'''
        # for file in t.split('\n'):
        #     if not file:
        #         continue
        #     print(file)
        with open(full_path, 'rb') as f:
            data = f.read()

        lines,_ = ocr_image_bytes(data)
        for ln in lines:
            print(ln)
        print('='*30,len(lines))