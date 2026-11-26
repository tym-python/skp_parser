"""将 skp_project.extra_info 中指定字段提取到对应表字段并回填。

逻辑:
1. 查询 extra_info 中存在 FIELD_TO_COLUMN 任一 key 的行;
2. 目标字段为空或 0 时,将 extra_info 中的值提取到目标字段,并从 extra_info 删除该 key;
3. 目标字段已有非零值时跳过,不动数据;
4. 按行输出日志: 数据id / 字段extra_info: 原-->现 / 字段xxx: 原-->现。

用法: python -m util.extract_extra_fields
"""
import json
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, Optional

from util.db_util import AsyncDB
from util.log_util import get_logger

logger = get_logger(__name__)



def to_number(value: Any) -> Optional[Decimal]:
    """尽量转 Decimal;转不了返回 None。"""
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return Decimal(str(value))
    s = str(value).strip().replace(',', '')
    if not s:
        return None
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


def build_filter_sql() -> str:
    """构造 extra_info 命中任一 key 的 WHERE 条件(JSON 路径 key 加引号)。"""
    parts = []
    for key in FIELD_TO_COLUMN:
        path = '$."' + key.replace('"', '\\"') + '"'
        parts.append(f"JSON_CONTAINS_PATH(extra_info, 'one', {json.dumps(path, ensure_ascii=False)})")
    return " OR ".join(parts)


async def extract_extra_fields(con_id=0,dbkey='') -> None:
    if con_id > 0:
        conditions = f'and file_id = {con_id}'
    else:
        conditions = ''
    sql = (
        "SELECT id, extra_info, " + ", ".join(FIELD_TO_COLUMN.values()) +
        f" FROM skp_project WHERE extra_info IS NOT NULL AND {build_filter_sql()} {conditions}"
    )
    async with AsyncDB(dbkey=dbkey) as db:
        rows = await db.query(sql)
        logger.info(f"命中 {len(rows)} 行待提取")
        for row in rows:
            extra = json.loads(row['extra_info']) if isinstance(row['extra_info'], str) else row['extra_info']
            if not isinstance(extra, dict):
                continue
            old_extra = json.dumps(extra, ensure_ascii=False)
            updates: Dict[str, Any] = {}
            changed = False
            for key, col in FIELD_TO_COLUMN.items():
                if key not in extra:
                    continue
                cur_val = row.get(col)
                if cur_val not in (None, '', 0, Decimal(0)):
                    logger.info(f"数据id={row['id']} 字段{col}已有值{cur_val},跳过{key}")
                    continue
                if col in STRING_COLUMNS:
                    new_val = str(extra[key]).strip()
                    if not new_val:
                        continue
                else:
                    new_val = to_number(extra[key])
                    if new_val is None:
                        logger.warning(f"数据id={row['id']} {key}值无法转数值: {extra[key]!r},跳过")
                        continue
                extra.pop(key)
                updates[col] = new_val
                changed = True
            if not changed:
                continue
            # 逐字段日志: extra_info 整体 原-->现, 各目标字段 原-->现
            new_extra = json.dumps(extra, ensure_ascii=False) if extra else None
            logger.info(f"数据id={row['id']} 字段extra_info: {old_extra} --> {new_extra}")
            set_parts, params = [], [new_extra]
            for col, val in updates.items():
                set_parts.append(f"{col} = %s")
                params.append(val)
                logger.info(f"数据id={row['id']} 字段{col}: {row.get(col) if row.get(col) is not None else ''} --> {val}")
            params.append(row['id'])
            await db.execute(
                f"UPDATE skp_project SET extra_info = %s, {', '.join(set_parts)} WHERE id = %s",
                tuple(params),
            )
        logger.info("提取完成")


if __name__ == '__main__':
    import asyncio

    # extra_info 中的 key -> skp_project 列名(同时作为列名白名单,防注入)
    FIELD_TO_COLUMN: Dict[str, str] = {
        # '年度投资计划（万元）': 'annual_investment',
        # '2021年主要前期工作内容': 'annual_goal',
        '2022年计划达到的工程形象进度': 'annual_goal',
    }

    # 字符串类型目标列:值无需转数值,原样写入
    STRING_COLUMNS = {'annual_goal'}

    con_id = 73
    dbkey = 'db220'
    # dbkey = ''
    asyncio.run(extract_extra_fields(con_id,dbkey))
