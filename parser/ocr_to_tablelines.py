from typing import List, Dict, Any
import logging
import cv2
import numpy as np
logger = logging.getLogger(__name__)

_rapid_engine = None

def _get_engine():
    global _rapid_engine
    if _rapid_engine is None:
        from rapidocr import RapidOCR
        _rapid_engine = RapidOCR()
    return _rapid_engine

# ============================================================
# 一、OCR 结果 → items
# ============================================================
def parse_items(result) -> List[Dict[str, Any]]:
    if result.boxes is None or result.txts is None:
        return []
    items = []
    for poly, text in zip(result.boxes, result.txts):
        text = text.strip()
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
            'h':  max(ys) - min(ys),
            'w':  max(xs) - min(xs),
        })
    return items

# ============================================================
# 二、自适应阈值（替换固定行高阈值）
# ============================================================
def _auto_threshold_gap(gaps: List[float], avg_h: float) -> float:
    """自适应阈值 + 字高绝对边界约束。"""
    if not gaps:
        return avg_h * 0.5

    lower = avg_h * 0.3   # 低于此值 → 一定同格
    upper = avg_h * 1.2   # 高于此值 → 一定跨格

    sorted_g = sorted(gaps)
    if len(sorted_g) == 1:
        g = sorted_g[0]
        return max(lower, min(upper, g))

    # 找最大跳变
    max_jump = 0.0
    split = 0
    for i in range(1, len(sorted_g)):
        jump = sorted_g[i] - sorted_g[i - 1]
        if jump > max_jump:
            max_jump = jump
            split = i

    # 跳变太小 → 分布可能多峰或无显著分界 → 用字高兜底
    if max_jump < avg_h * 0.3:
        return avg_h * 0.6

    candidate = (sorted_g[split - 1] + sorted_g[split]) / 2.0
    # 用绝对边界夹住
    return max(lower, min(upper, candidate))

# ============================================================
# 三、表头识别（保留，因为表头行通常均匀）
# ============================================================
def _split_physical_rows(items: List[Dict], avg_h: float) -> List[List[Dict]]:
    """仅用于表头识别的物理行切分。"""
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

# ============================================================
# 三、识别表头区域（第一行 + 后续紧贴的行）
# ============================================================
def _detect_header_rows(rows: List[List[Dict]], avg_h: float) -> int:
    """返回表头占用的物理行数（至少为 1）。

    判定：从第一行开始，如果下一行的 y0 与当前表头区域底部的间距
    明显小于数据行的正常行距，则视为表头的延续。
    """
    if not rows:
        return 0
    if len(rows) == 1:
        return 1

    header_count = 1
    for i in range(1, len(rows)):
        prev_y1 = max(it['y1'] for row in rows[:header_count] for it in row)
        next_y0 = min(it['y0'] for it in rows[i])
        gap = next_y0 - prev_y1

        # 参考行距：用接下来的两行之间的间距
        if i + 1 < len(rows):
            next_next_y0 = min(it['y0'] for it in rows[i + 1])
            curr_y1 = max(it['y1'] for it in rows[i])
            ref_gap = next_next_y0 - curr_y1
        else:
            ref_gap = avg_h * 1.5

        # 若与表头间距 < 参考行距的 60%，判为表头延续
        if gap < ref_gap * 0.6:
            header_count += 1
        else:
            break

    return header_count


# ============================================================
# 四、从表头 items 推断列定义
# ============================================================
def _build_columns_from_header(header_items: List[Dict]) -> List[Dict]:
    """把表头里的 items 按 x 范围重叠聚类成列。"""
    header_sorted = sorted(header_items, key=lambda x: x['xc'])
    columns: List[List[Dict]] = []
    for it in header_sorted:
        placed = False
        for col in columns:
            col_x0 = min(x['x0'] for x in col)
            col_x1 = max(x['x1'] for x in col)
            if it['xc'] >= col_x0 and it['xc'] <= col_x1:
                col.append(it)
                placed = True
                break
        if not placed:
            columns.append([it])

    col_defs = []
    for col in columns:
        x0 = min(x['x0'] for x in col)
        x1 = max(x['x1'] for x in col)
        col_sorted = sorted(col, key=lambda x: (x['y0'], x['x0']))
        header_text = ''.join(x['text'] for x in col_sorted)
        col_defs.append({
            'x0': x0, 'x1': x1,
            'xc': (x0 + x1) / 2.0,
            'header': header_text,
        })
    col_defs.sort(key=lambda c: c['xc'])
    return col_defs


# ============================================================
# 五、把 item 分配到某一列
# ============================================================
def _assign_column(it: Dict, col_defs: List[Dict]) -> int:
    """按 xc 最近的策略把 item 分配到某列。"""
    best_idx = 0
    best_dist = float('inf')
    for i, c in enumerate(col_defs):
        # 完全落在列范围内
        if c['x0'] <= it['xc'] <= c['x1']:
            return i
        # 否则取最近
        d = min(abs(it['xc'] - c['x0']), abs(it['xc'] - c['x1']))
        if d < best_dist:
            best_dist = d
            best_idx = i
    return best_idx


# ============================================================
# 六、拼单元格文本（同格子里的多个 items 按 y 分行、行内按 x 排序）
# ============================================================
def _cell_text(cell_items: List[Dict], avg_h: float) -> str:
    if not cell_items:
        return ""
    cell_items = sorted(cell_items, key=lambda x: (x['y0'], x['x0']))

    text_lines = []
    currline = [cell_items[0]]
    for idx, it in enumerate(cell_items[1:],start=1):
        if cell_items[idx-1]['y1'] <= it['y0'] + it['h'] * 0.25:   # 换行
            text_lines.append(''.join(x['text'] for x in currline))
            currline = [it]  # 赋新行
        else:       # 同行
            currline.append(it)
    text_lines.append(''.join(x['text'] for x in currline))

    return ' '.join(text_lines)

# ============================================================
# 六、列内合并单元格（用自适应阈值替换固定阈值）
# ============================================================
def _merge_cells_in_column(col_items: List[Dict], avg_h: float) -> List[List[Dict]]:
    """列内按 y 合并成单元格组。阈值完全由该列的 y 间距分布自适应。"""
    if not col_items:
        return []
    if len(col_items) == 1:
        return [col_items]

    col_sorted = sorted(col_items, key=lambda x: x['y0'])

    # 计算相邻 items 的 y 间距
    gaps = []
    for i in range(1, len(col_sorted)):
        prev_max_y1 = max(x['y1'] for x in col_sorted[:i])
        gaps.append(max(0.0, col_sorted[i]['y0'] - prev_max_y1))

    threshold = _auto_threshold_gap(gaps, avg_h)

    cells = []
    curr = [col_sorted[0]]
    for i in range(1, len(col_sorted)):
        if gaps[i - 1] < threshold:
            curr.append(col_sorted[i])
        else:
            cells.append(curr)
            curr = [col_sorted[i]]
    cells.append(curr)
    return cells

# ============================================================
# 分列并合并text之后，y 范围重叠贪心聚类 分行
# ============================================================
def group_cells_into_rows(all_cells: List[Dict], n_cols: int, avg_h: float) -> List[List[Dict]]:
    """把 all_cells 按 y 范围重叠聚成逻辑行。

    返回 List[List[Dict]]，每一行内的 cell 按 col_idx 排序。
    允许某些行某些列缺失（空单元格）。
    """
    if not all_cells:
        return []

    # 按 y0 排序，从上到下处理
    all_cells = sorted(all_cells, key=lambda x: (x['y0'], x['col_idx']))

    rows: List[Dict] = []  # {'y0', 'y1', 'cells': List[Dict]}

    for c in all_cells:
        best_row = None
        best_overlap = 0.0

        for row in rows:
            # 计算当前 cell 与这一行的 y 范围重叠量
            ov = min(row['y1'], c['y1']) - max(row['y0'], c['y0'])
            if ov <= 0:
                continue
            # 归一化到较矮的那个
            h_min = min(row['y1'] - row['y0'], c['y1'] - c['y0'])
            ratio = ov / max(1.0, h_min)
            if ratio > best_overlap:
                best_overlap = ratio
                best_row = row

        # 找到归属行且重叠够大
        if best_row is not None and best_overlap > 0.3:
            best_row['cells'].append(c)
            # 更新行的 y 范围（取并集）
            best_row['y0'] = min(best_row['y0'], c['y0'])
            best_row['y1'] = max(best_row['y1'], c['y1'])
        else:
            rows.append({
                'y0': c['y0'],
                'y1': c['y1'],
                'cells': [c],
            })

    # 输出：转成 List[List[Dict]]，行内按 col_idx 排序
    result = []
    for row in rows:
        row['cells'].sort(key=lambda x: x['col_idx'])
        result.append(row['cells'])
    return result

# ============================================================
# 寻找锚点列：锚点行的 y 范围直接来自项目名称列的 cell 的 y 范围
# ============================================================
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

    # ---------- 1) 取出锚点列的 cells ----------
    if anchor_col_idx < 0:
        # 没找到锚点列 → 退回无锚点的通用方案
        return group_cells_into_rows(all_cells, avg_h)

    anchor_cells = [c for c in all_cells if c['col_idx'] == anchor_col_idx]
    if not anchor_cells:
        return group_cells_into_rows(all_cells, avg_h)

    anchor_cells.sort(key=lambda x: x['y0'])

    # 每个锚点 cell 定义一行骨架
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

        if best_row is not None and best_ov > 0:
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

# ============================================================
# 七、主函数：按表头定列重建表格
# ============================================================
def reconstruct_table_by_header(items: List[Dict]) -> List[str]:
    if not items:
        return []

    avg_h = sum(it['h'] for it in items) / len(items)

    # 1) 只在「找表头」时用物理行切分
    phys_rows = _split_physical_rows(items, avg_h)
    if len(phys_rows) < 2:
        # 没有数据行，退回段落
        return _fallback_paragraph(items),'lines'

    # 2) 表头行数 + 表头 items / 数据 items
    header_n = _detect_header_rows(phys_rows, avg_h)
    header_items = [it for r in phys_rows[:header_n] for it in r]
    body_items = [it for r in phys_rows[header_n:] for it in r]

    if not body_items:
        return _fallback_paragraph(items),'lines'

    # 3) 表头定列
    col_defs = _build_columns_from_header(header_items)
    if len(col_defs) < 2:
        return _fallback_paragraph(items),'lines'

    # 4) 数据 items 按 x0 分列
    col_items_list: List[List[Dict]] = [[] for _ in col_defs]
    for it in body_items:
        idx = _assign_column(it, col_defs)
        col_items_list[idx].append(it)

    # 5) ★ 每列独立合并单元格（这是替换点：不再按全局物理行）
    all_cells: List[Dict] = []
    for col_idx, col_items in enumerate(col_items_list):
        if col_idx == 6:
            pass
        for cell in _merge_cells_in_column(col_items, avg_h):
            all_cells.append({
                'col_idx': col_idx,
                'x0': min(x['x0'] for x in cell),
                'x1': max(x['x1'] for x in cell),
                'y0': min(x['y0'] for x in cell),
                'y1': max(x['y1'] for x in cell),
                'text': _cell_text(cell, avg_h),
            })

    if not all_cells:
        return _fallback_paragraph(items),'lines'

    # 2. 找锚点列
    anchor_col_idx = _find_anchor_col_idx(col_defs, keyword="项目名称")
    if anchor_col_idx < 0:
        anchor_col_idx = 1  # 兜底：默认第 1 列

    # 3. 用锚点分行
    rows = group_cells_into_rows_with_anchor(all_cells, anchor_col_idx, avg_h)

    # 4. 输出
    # result = [' | '.join(c['header'] for c in col_defs)]
    # for row in rows:
    #     cells = [""] * len(col_defs)
    #     for c in row:
    #         if cells[c['col_idx']]:
    #             cells[c['col_idx']] += " " + c['text']
    #         else:
    #             cells[c['col_idx']] = c['text']
    #     if any(c.strip() for c in cells):
    #         result.append(' | '.join(cells))
    # 输出，构造List[List[Any]]   ————> base_parser.py extract_rows_from_table
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

    return result,'table'


# ============================================================
# 八、降级：段落
# ============================================================
def _fallback_paragraph(items: List[Dict]) -> List[str]:
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
    return [' '.join(x['text'] for x in sorted(l, key=lambda y: y['x0'])) for l in lines]

# ============================================================
# 九、统一入口
# ============================================================
def ocr_image_bytes(data: bytes) -> List[str]:
    if not data:
        return []
    try:
        img = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is None or img.size < 1000:
            return []

        result = _get_engine()(img)
        items = parse_items(result)
        if not items:
            return []

        return reconstruct_table_by_header(items)

    except Exception as ex:
        logger.warning(f"OCR 失败: {type(ex).__name__}: {ex}")
        return []

if __name__ == '__main__':

    file_path= r"2023年重点项目\04重庆市2023年重点项目清单\2023年开州区\15.jpg"
    # file_path= r"2023年重点项目\14贵州省2023年重点项目清单\2023年黔东南州\5.jpg"
    full_path = r'E:\STangWork\STangFiles\各省重点项目：2020年起' +'\\'+ file_path
    with open(full_path, 'rb') as f:
        data = f.read()

    lines,_ = ocr_image_bytes(data)
    for ln in lines:
        print(ln)


