"""单文件调试运行:先删除数据库中该文件的旧数据,再重新 解析 → 上传 GoFast → 入库。

删除按 SHA-256(file_hash)定位 —— 与主流程去重键一致:凡是会导致
"已存在跳过" 的记录都会被清掉,保证本文件必然重新解析入库。

用法:
    python run_single.py <文件路径>              # 按平台规则决定是否上传(Windows 不上传)
    python run_single.py <文件路径> --upload     # 强制上传 GoFast
    python run_single.py <文件路径> --no-upload  # 调试模式,跳过上传
"""

import asyncio
import hashlib
import sys
from pathlib import Path
from util.file_config import skpFilePath
from main import process_file, resolve_upload
from util.db_util import AsyncDB
from util.log_util import get_logger

logger = get_logger(__file__)

SUPPORTED_EXT = {'.pdf', '.docx', '.xlsx', '.png', '.jpg', '.jpeg'}


async def run_single(file_path: Path, upload: bool, dbkey:str='local') -> None:
    """删除旧数据 → 重新解析入库(file_path.parent 作为相对路径基准)。"""
    if not file_path.is_file():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    if file_path.suffix.lower() not in SUPPORTED_EXT:
        raise ValueError(f"不支持的格式: {file_path.suffix}(仅支持 {sorted(SUPPORTED_EXT)})")

    # 根据 skp_file 中的 file_path 删除数据
    db_file_path = str(file_path).replace(skpFilePath+'\\','')

    bs = await asyncio.to_thread(file_path.read_bytes)
    file_hash = hashlib.sha256(bs).hexdigest()

    async with AsyncDB(dbkey=dbkey) as db:
        await db.init_db()

        # 1. 删除该文件在数据库中的全部关联数据(单事务)
        deleted = await db.delete_file_data(file_hash)
        logger.info(
            f"删除旧数据: 文件 {deleted['file']} 条, 项目 {deleted['project']} 条, "
            f"通知 {deleted['notice']} 条, 分类声明 {deleted['category_declared']} 条")

        # 2. 调用主流程单文件处理(解析 → 上传 → 入库)
        result = await process_file(db, skpFilePath, file_path, upload=upload)
        if result.status == 'ok':
            logger.info(
                f"OK: {result.file_name} (file_id={result.file_id}, 项目 {result.project_count} 条)")
        elif result.status == 'skipped_existing':
            logger.warning(f"跳过(已入库): {result.file_name}")
        else:
            logger.error(f"FAIL: {result.file_name} - {result.error}")


def main(file_path,upload=False,dbkey:str='local') -> None:

    logger.info(f"单文件处理: {file_path}(上传 GoFast: {upload})")
    asyncio.run(run_single(file_path, upload=upload, dbkey=dbkey))


if __name__ == "__main__":
    # file_path= r'2020年重点项目\2020年各省市重点项目清单汇总：51.63万亿\07宁夏古自治区2020年重点项目清单\2020年宁夏全区重大项目清单（最新）.xlsx'
    # file_path= r'2022年重点项目\05广西自治区2022年重点项目清单\附件 2022年上半年自治区层面统筹推进重大项目退出项目清单.xlsx'
    # file_path= r'2024年重点项目\29四川省2024年重点项目清单\阿坝州2024年\2024年阿坝州重点项目名单.xlsx'
    # file_path= r'2023年重点项目\04重庆市2023年重点项目清单\2023年奉节县\奉节委办发〔2023〕1号附件.xlsx'
    # file_path= r'2026年重点项目\04重庆市2026年重点项目清单\2026年垫江县\重庆市垫江县2026年重点前期项目清单.xlsx'
    # file_path= r'2021年重点项目\02上海市2021年重点项目清单\2021年上海市重大建设项目清单.xlsx'
    file_path= r'2023年重点项目\26山东省2023年重点项目清单\附件：2023年山东省重点项目名单.docx'  # 没表格
    file_path= r"2022年重点项目\20湖南省2022年重点项目清单\2022年湖南省重点建设项目名单.docx"
    file_path= r"2022年重点项目\06内蒙古自治区2022年重点项目清单\4_副本.jpg"
    file_path= r"2022年重点项目\22江苏省2022年重点项目清单\2022年宿迁市\宿政发〔2022〕2号 2022年度中心城市建设重点工程计划的通知表格.docx"
    file_path= r"2021年重点项目\2021年各省市重点项目清单汇总（截止3月12日，持续更新中）.docx"
    file_path= r"2023年重点项目\11福建省2023年重点项目清单\附件：2023年度福建省重点项目名单(1580个).docx"
    file_path= r"2026年重点项目\文章发布表格.xlsx"
    # file_path= r"2026年重点项目\12甘肃省2026年重点项目清单\2026年张掖市\张掖市2026年重大建设项目清单.docx"
    # file_path= r"2026年重点项目\12甘肃省2026年重点项目清单\2026年庆阳市\庆阳市2026年省列重大建设项目名单.docx"
    # file_path= r"2026年重点项目\12甘肃省2026年重点项目清单\2026年庆阳市\庆阳市2026年市列重大建设项目名单.docx"
    # file_path= r"2025年重点项目\12甘肃省2025年重点项目清单\2025年甘肃省省列重大建设项目名单.docx"
    # file_path= r"2026年重点项目\12甘肃省2026年重点项目清单\2026年甘肃省列重大建设项目名单.docx"
    file_path= r"2023年重点项目\11福建省2023年重点项目清单\2023年龙岩市\附件1：龙岩市2023年重点项目及分级管理单位名单.docx"
    # file_path = file_path.replace(r'E:\STangWork\STangFiles\各省重点项目：2020年起\', '')
    print('文件地址：',skpFilePath+'\\'+file_path)

    full_path = skpFilePath +'\\'+ file_path
    main(Path(full_path))
    # main(Path(full_path),True,dbkey='db220')
