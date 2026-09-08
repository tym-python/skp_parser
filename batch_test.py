"""批量测试:按文件类型扫描目录下全部该类文件,每个文件先清除旧入库数据,再重新解析入库。

用法:
    python batch_test.py xlsx                # 扫描 skpFilePath 下全部 xlsx
    python batch_test.py docx                # 扫描 skpFilePath 下全部 docx
    python batch_test.py pdf --no-upload     # 调试模式,跳过 GoFast 上传
    python batch_test.py xlsx 2022年重点项目 # 仅扫描 skpFilePath 下的子目录
    python batch_test.py docx
"""

import asyncio
import hashlib
import sys
from pathlib import Path
from typing import Dict, List, Tuple

from main import collect_files, process_file, resolve_upload
from util.db_util import AsyncDB
from util.file_config import skpFilePath
from util.log_util import get_logger

logger = get_logger(__file__)

SUPPORTED_EXT = {'.pdf', '.docx', '.xlsx', 'xls'}


async def batch_test(file_type: str, sub_dir: str, upload: bool) -> None:
    ext = '.' + file_type.lower().lstrip('.')
    if ext not in SUPPORTED_EXT:
        raise ValueError(f"不支持的格式: {file_type}(仅支持 {sorted(SUPPORTED_EXT)})")

    base = Path(skpFilePath)
    if sub_dir:
        base = base / sub_dir
        if not base.is_dir():
            raise NotADirectoryError(f"子目录不存在: {base}")

    files = [p for p in collect_files(base) if p.suffix.lower() == ext]
    logger.info(f"批量测试: {base} 下 {file_type} 文件 {len(files)} 个(上传 GoFast: {upload})")

    ok = failed = skipped = project_total = 0
    failed_list: List[Tuple[str, str]] = []
    async with AsyncDB() as db:
        await db.init_db()
        import gc
        for fp in files:
            # 每文件后主动回收,防 openpyxl 对象滞留导致进程内存随文件数累积
            gc.collect()
            try:
                # 1. 清除该文件在数据库中的全部关联数据(SHA-256 定位,单事务)
                bs = await asyncio.to_thread(fp.read_bytes)
                file_hash = hashlib.sha256(bs).hexdigest()
                deleted = await db.delete_file_data(file_hash)
                if any(deleted.values()):
                    logger.info(
                        f"清除旧数据: {fp.name}(文件 {deleted['file']} 条, 项目 {deleted['project']} 条, "
                        f"特有信息 {deleted['extra']} 条, 通知 {deleted['notice']} 条, "
                        f"分类声明 {deleted['category_declared']} 条)")

                # 2. 重新解析入库(与主流程一致:解析 → 上传 → 单事务入库)
                result = await process_file(db, base, fp, upload=upload)
                if result.status == 'ok':
                    ok += 1
                    project_total += result.project_count
                    logger.info(f"OK: {result.file_name} (file_id={result.file_id}, 项目 {result.project_count} 条)")
                elif result.status == 'skipped_existing':
                    skipped += 1
                    logger.warning(f"跳过(已入库): {result.file_name}")
                else:
                    failed += 1
                    failed_list.append((result.file_name, result.error))
                    logger.error(f"FAIL: {result.file_name} - {result.error}")
            except Exception as ex:
                failed += 1
                failed_list.append((fp.name, f"未预期异常: {ex}"))
                logger.error(f"处理异常 {fp}: {ex}", exc_info=True)

    # 汇总报告
    logger.info("=" * 40)
    logger.info(f"批量测试完成: {file_type} 共 {len(files)} 个")
    logger.info(f"成功: {ok} 个, 入库项目 {project_total} 条 | 失败: {failed} 个 | 跳过: {skipped} 个")
    for name, reason in failed_list:
        logger.error(f"  - {name}: {reason}")
    logger.info("=" * 40)


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    flags = set(a for a in sys.argv[1:] if a.startswith('--'))
    if not args:
        print(__doc__)
        sys.exit(1)
    file_type = args[0]
    sub_dir = args[1] if len(args) > 1 else ''

    if '--upload' in flags:
        upload = True
    elif '--no-upload' in flags:
        upload = False
    else:
        upload = resolve_upload()

    asyncio.run(batch_test(file_type, sub_dir, upload=upload))


if __name__ == "__main__":
    main()
