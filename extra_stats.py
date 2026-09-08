"""extra 字段统计与提列:统计 skp_file_extra 中各字段出现率,超过半数项目者并入 skp_project。

用法:
    python extra_stats.py [--apply]   # 默认仅统计;--apply 执行提列(ALTER + 回填)

字段名 → 列名映射(新字段需在此登记):
"""

import asyncio
import json
import sys
from typing import Dict, List

from util.db_util import AsyncDB
from util.log_util import get_logger

logger = get_logger(__file__)

# extra 字段名 → skp_project 列名(超半数时提列用)
FIELD_TO_COLUMN: Dict[str, str] = {
    '合作方式': 'cooperation_mode',
    '联系方式': 'contact_info',
}


async def stats(db: AsyncDB) -> None:
    """统计各 extra 字段的出现次数与占比。"""
    total = (await db.query("SELECT COUNT(*) n FROM skp_project"))[0]['n']
    if total == 0:
        logger.warning("skp_project 为空,先运行全量扫描")
        return

    rows = await db.query("""
        SELECT j.field_name, COUNT(DISTINCT e.project_id) AS n
        FROM skp_file_extra e
        JOIN JSON_TABLE(JSON_KEYS(e.extra_info), '$[*]'
             COLUMNS (field_name VARCHAR(64) PATH '$')) j
        GROUP BY j.field_name
        ORDER BY n DESC
    """)
    half = total / 2
    print(f"项目总数: {total} | 超半数阈值: >{half:.0f}")
    print(f"{'字段名':<24} {'项目数':>6} {'占比':>7}  建议")
    print("-" * 60)
    promote: List[str] = []
    for r in rows:
        name = r['field_name']
        ratio = r['n'] / total
        is_majority = r['n'] > half
        col = FIELD_TO_COLUMN.get(name)
        suggestion = ""
        if is_majority:
            suggestion = f"→ 提列 {col or '(未登记映射,需补充)'}"
            if col:
                promote.append(name)
        print(f"{name:<24} {r['n']:>6} {ratio:>6.1%}  {suggestion}")
    return promote


async def promote_fields(db: AsyncDB, fields: List[str]) -> None:
    """将超半数字段从 extra 提为 skp_project 列并回填数据。"""
    for name in fields:
        col = FIELD_TO_COLUMN.get(name)
        if not col:
            logger.warning(f"字段 [{name}] 未登记列名映射,跳过提列")
            continue
        ddl = "VARCHAR(512) NOT NULL DEFAULT '' COMMENT '从extra提列(原字段:{}),原文为JSON时存JSON文本'".format(name)
        # 加列(幂等)
        async def _run(conn):
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT COUNT(*) n FROM information_schema.COLUMNS "
                    "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME='skp_project' AND COLUMN_NAME=%s",
                    (col,))
                row = await cur.fetchone()
                if row and int(row['n']) == 0:
                    await cur.execute(f"ALTER TABLE skp_project ADD COLUMN `{col}` {ddl}")
                    logger.info(f"skp_project 已新增列 {col}")
        await db._with_conn(_run, commit=True)

        # 回填:从 extra_info 取该字段
        await db.execute(
            f"""UPDATE skp_project p
                JOIN skp_file_extra e ON e.project_id = p.id
                SET p.`{col}` = JSON_UNQUOTE(JSON_EXTRACT(e.extra_info, %s))
                WHERE JSON_CONTAINS_PATH(e.extra_info, 'one', %s)""",
            (f'$.{name}', f'$.{name}'))
        filled = (await db.query(
            f"SELECT COUNT(*) n FROM skp_project WHERE `{col}` <> ''"))[0]['n']
        logger.info(f"字段 [{name}] → {col} 回填 {filled} 条")

    # 回填完成后移除 skp_file_extra 中已提列字段
    for name in fields:
        await db.execute(
            "UPDATE skp_file_extra SET extra_info = JSON_REMOVE(extra_info, %s) "
            "WHERE JSON_CONTAINS_PATH(extra_info, 'one', %s)",
            (f'$.{name}', f'$.{name}'))
    logger.info("extra 中已提列字段已移除")


async def main() -> None:
    apply = '--apply' in sys.argv[1:]
    async with AsyncDB() as db:
        promote = await stats(db)
        if promote and apply:
            logger.info("执行提列(--apply)")
            await promote_fields(db, promote)
            print("\n=== 提列后重新统计 ===")
            await stats(db)
        elif promote and not apply:
            print("\n(提示:加 --apply 参数执行提列与回填)")


if __name__ == "__main__":
    asyncio.run(main())
