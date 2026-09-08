"""全量扫描:处理目录内全部支持格式(pdf/docx/xlsx)文件,输出报告与人工检查提示。

用法:
    python full_scan.py [目录]
输出:
    scan_report_2020.json   — 逐文件明细(状态/项目数/错误)
    控制台                  — 需要人工检查的文件提示
"""

import asyncio
import json
import sys
from pathlib import Path
import os
from main import process_file
from parser.notice_parser import is_notice_file
from util.db_util import AsyncDB
from util.file_config import skpFilePath
from util.log_util import get_logger

logger = get_logger(__file__)

# SUPPORTED_EXT = {'.pdf', '.docx', '.xlsx'}
SUPPORTED_EXT = { '.xlsx'}


async def main(directory: str) -> None:
    base = Path(directory)
    files = sorted(
        p for p in base.rglob('*')
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXT and not p.name.startswith('~$')
    )
    logger.info(f"扫描目录: {directory},支持格式文件 {len(files)} 个")
    for f in files:
        if str(f).endswith('xlsx'):
            size_bytes = os.path.getsize(f)
            if size_bytes>3*1024*1024:
                print(size_bytes/1024/1024,'MB,',f)
    report = []
    async with AsyncDB() as db:
        for fp in files:
            result = await process_file(db, base, fp)
            item = {
                'status': result.status,          # ok | skipped_existing | failed
                'file': fp.name,
                'path': str(fp.relative_to(base)),
                'projects': result.project_count,
                'error': result.error,
                'notice': is_notice_file(fp.name),
            }
            report.append(item)
            logger.info(f"[{result.status}] {fp.name} | 项目 {result.project_count} | {result.error}")

    out = Path(__file__).parent / 'analy' / 'scan_report.json'
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    logger.info(f"报告已写入: {out}")

    print("\n" + "=" * 50)
    print("=== 需要人工检查的文件 ===")
    checked = 0
    for r in report:
        if r['status'] == 'failed':
            print(f"  [解析失败] {r['path']}: {r['error']}")
            checked += 1
        elif r['status'] == 'ok' and r['projects'] == 0 and not r['notice']:
            print(f"  [0条项目] {r['path']}(可能为扫描件/无清单/排版异常)")
            checked += 1
    if checked == 0:
        print("  (无)")
    ok = sum(1 for r in report if r['status'] == 'ok')
    skip = sum(1 for r in report if r['status'] == 'skipped_existing')
    total_projects = sum(r['projects'] for r in report)
    print(f"共 {len(report)} 个文件:成功 {ok},已存在跳过 {skip},失败 {len(report) - ok - skip}")
    print(f"项目总数: {total_projects}")


if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) > 1 else skpFilePath
    asyncio.run(main(directory))
