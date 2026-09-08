"""干扰数据识别与名单记录。

干扰 sheet 两类不入库,记录到 analy/noise_sheets.json(备注原因与示例):
1. 各省汇总表(项目名=省份名称,如 2025年各省重点重大项目清单 的汇总 sheet)
2. 统计汇总表(表头含 合计/个数 等且无 项目名称/建设内容,如 泸州 汇总 sheet)
"""

import json
from pathlib import Path
from typing import Dict, List

from util.province_names import PROVINCE_NAMES

NOISE_FILE = Path(__file__).resolve().parent.parent / 'analy' / 'noise_sheets.json'
NOISE_RATIO = 0.8   # 省份名项目占比 ≥80% 判定为干扰
MIN_PROJECTS = 3    # 少于 3 条不做判定(数据太少无法判断)


def is_noise_sheet(projects: List[Dict]) -> bool:
    """判断 sheet 解析结果是否为干扰:项目名绝大多数为省份名称。

    覆盖两类干扰:各省汇总表(每省一行)与 省→地级市对照表(每省多行),
    两者均无有效项目。
    """
    if len(projects) < MIN_PROJECTS:
        return False
    prov_count = sum(1 for p in projects
                     if str(p.get('project_name', '')).strip() in PROVINCE_NAMES)
    return prov_count / len(projects) >= NOISE_RATIO


def record_noise(file_path: str, sheet_name: str, sample: str,
                 reason: str = '项目名均为省份名称(各省汇总表),有效数据无') -> None:
    """记录干扰 sheet 到名单文件(追加,按 文件+sheet 去重)。

    reason 可指定干扰类型(省份汇总表 / 统计汇总表 等)。
    """
    key = Path(file_path).name
    data: Dict = {}
    if NOISE_FILE.exists():
        try:
            data = json.loads(NOISE_FILE.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, OSError):
            data = {}
    entry = {
        'sheet': sheet_name,
        'reason': reason,
        'sample': str(sample)[:60],
    }
    lst = data.setdefault(key, [])
    if not any(e.get('sheet') == sheet_name for e in lst):
        lst.append(entry)
        NOISE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
