"""主入口:扫描给定目录,逐文件执行 解析 → 上传 GoFast → 入库 MySQL。

用法:
    python main.py                  # 使用 util/file_config.py 中的默认目录
    python main.py <目录路径>        # 指定目录

每个文件的处理:
    读取字节 + SHA-256 → (已存在则跳过) → 解析项目 → 上传 GoFast → 单事务入库
"""

import asyncio
import hashlib
import platform
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple

from parser import detect_real_ext, get_parser
from parser.notice_parser import NoticeParser, is_notice_file
from util import area_id, file_config
from util.db_util import AsyncDB
from util.file_config import skpFilePath
from util.go_fast import GoFast
from util.log_util import get_logger

logger = get_logger(__file__)

SUPPORTED_EXT = {'.pdf', '.docx', '.xlsx', '.png', '.jpg', '.jpeg'}

# 省份关键词 → area_id(与 util/area_id.py 对应,长词优先匹配)
PROVINCE_KEYWORDS: Dict[str, int] = {
    '黑龙江': area_id.HEILONGJIANG, '内蒙古': area_id.NEIMENGGU,
    '北京': area_id.BEIJING, '天津': area_id.TIANJIN, '河北': area_id.HEBEI,
    '山西': area_id.SHANXI_1, '辽宁': area_id.LIAONING, '吉林': area_id.JILIN,
    '上海': area_id.SHANGHAI, '江苏': area_id.JIANGSU, '浙江': area_id.ZHEJIANG,
    '安徽': area_id.ANHUI, '福建': area_id.FUJIAN, '江西': area_id.JIANGXI,
    '山东': area_id.SHANDONG, '河南': area_id.HENAN, '湖北': area_id.HUBEI,
    '湖南': area_id.HUNAN, '广东': area_id.GUANGDONG, '广西': area_id.GUANGXI,
    '海南': area_id.HAINAN, '重庆': area_id.CHONGQING, '四川': area_id.SICHUAN,
    '贵州': area_id.GUIZHOU, '云南': area_id.YUNNAN, '西藏': area_id.XIZANG,
    '陕西': area_id.SHANXI_3, '甘肃': area_id.GANSU, '青海': area_id.QINGHAI,
    '宁夏': area_id.NINGXIA, '新疆': area_id.XINJIANG,
    '香港': area_id.XIANGGANG, '澳门': area_id.AOMEN, '台湾': area_id.TAIWAN,
}

YEAR_RE = re.compile(r'(20\d{2})')


@dataclass
class FileResult:
    file_name: str
    file_path: str
    status: str  # ok | skipped_existing | failed
    project_count: int = 0
    file_id: int = 0
    error: str = ''


@dataclass
class SummaryReport:
    total: int = 0
    ok: int = 0
    skipped: int = 0
    failed: int = 0
    project_total: int = 0
    failed_files: List[Tuple[str, str]] = field(default_factory=list)


def detect_area(path: Path) -> Tuple[int, int]:
    """从路径/文件名判断省份与年份,返回 (area_id, year);无法判断返回 (0, 0)。"""
    text = str(path).replace('\\', '/')
    area = 0
    for keyword, area_id_ in PROVINCE_KEYWORDS.items():
        if keyword in text:
            area = area_id_
            break

    # 年份:优先文件名;否则取路径中最后一个年份(离文件最近的目录)
    years = YEAR_RE.findall(path.name) or YEAR_RE.findall(text)
    year = int(years[-1]) if years else 0
    return area, year


async def process_file(db: AsyncDB, base_dir: Path, file_path: Path,
                       upload: bool = True) -> FileResult:
    """处理单个文件:去重 → 解析 → 上传 GoFast → 单事务入库。

    Args:
        upload: False 表示调试模式,跳过 GoFast 上传(解析重点调试时使用)
    """
    file_name = file_path.name
    rel_path = str(file_path.relative_to(base_dir))
    ext = file_path.suffix.lower()

    bs = await asyncio.to_thread(file_path.read_bytes)
    file_hash = hashlib.sha256(bs).hexdigest()

    if await db.get_file_by_hash(file_hash):
        return FileResult(file_name, rel_path, 'skipped_existing')

    area, year = detect_area(file_path)

    # 1. 解析项目记录(解析库为同步实现,放入线程避免阻塞事件循环)
    declared_sum: Dict[str, int] = {}
    actual_by_cat: Dict[str, int] = {}
    try:
        # 按文件头探测真实格式(覆盖 .xlsx 实为旧版 xls 的情况)
        parser = get_parser(detect_real_ext(str(file_path)))
        projects = await asyncio.to_thread(parser.parse, str(file_path))
        # 分类声明校验:标题 "（共N项）" 与实际解析条数对比(解析检验手段,同分类声明累加)
        if parser.declared_categories:
            for project in projects:
                cat = project.get('category', '')
                if cat:
                    actual_by_cat[cat] = actual_by_cat.get(cat, 0) + 1
            for cat, declared in parser.declared_categories:
                declared_sum[cat] = declared_sum.get(cat, 0) + declared
            for cat, declared in declared_sum.items():
                # 子分类项目计入父分类(如 "重大产业项目-工业" 计入 "重大产业项目")
                got = sum(n for c, n in actual_by_cat.items()
                          if c == cat or c.startswith(cat + '-'))
                if got != declared:
                    logger.warning(
                        f"分类校验[{file_name}] {cat}: 标题声明 {declared} 项,解析 {got} 项")
    except Exception as ex:
        logger.error(f"解析失败 {file_name}: {ex}", exc_info=True)
        return FileResult(file_name, rel_path, 'failed', error=f"解析失败: {ex}")

    # 项目记录注入省份 ID(解析器不感知文件归属)
    for project in projects:
        project['area_id'] = area

    # 2. 通知类文件(红头文件):额外解析通知元信息
    notice = None
    if is_notice_file(file_name):
        try:
            notice = await asyncio.to_thread(NoticeParser().parse, str(file_path))
        except Exception as ex:
            logger.warning(f"通知信息解析失败 {file_name}: {ex}")

    # 3. 上传 GoFast(调试模式跳过;上传失败不阻塞入库,status 记为 0)
    gofast_url = ""
    if upload:
        gofast_url = await GoFast.upload(bs, ext.lstrip('.'))

    # 4. 单事务入库:文件 + 项目(失败自动回滚)
    file_data = {
        'file_name': file_name,
        'file_path': rel_path,
        'file_type': ext.lstrip('.'),
        'gofast_url': gofast_url,
        'area_id': area,
        'year': year,
        'file_size': len(bs),
        'file_hash': file_hash,
        'status': 1 if (gofast_url or not upload) else 0,
    }
    file_id = await db.save_file_with_projects(file_data, projects)
    if file_id is None:
        return FileResult(file_name, rel_path, 'failed', error="入库失败(已回滚)")

    # 5. 通知信息入库(失败不影响主流程)
    if notice is not None:
        notice['file_id'] = file_id
        notice['has_project_list'] = 1 if projects else 0
        await db.save_notice(notice)

    # 6. 分类标题声明项数与实际解析数入库(供统计校验)
    if declared_sum:
        await db.save_category_declared(file_id, declared_sum, actual_by_cat)

    return FileResult(file_name, rel_path, 'ok', project_count=len(projects), file_id=file_id)


def collect_files(base: Path) -> List[Path]:
    """递归收集支持的文档文件,跳过:
    - Office 临时文件(~$ 开头)
    - 文件名或所在文件夹名含"跳过解析"标记的文件
    """
    return sorted(
        p for p in base.rglob('*')
        if p.is_file()
        and p.suffix.lower() in SUPPORTED_EXT
        and not p.name.startswith('~$')
        and '跳过解析' not in str(p)
    )


def resolve_upload() -> bool:
    """是否上传 GoFast:手动配置 UPLOAD_ENABLED 优先,否则按平台自动。

    Windows 为开发机 → 不上传;Linux 为生产 → 上传。
    """
    if file_config.UPLOAD_ENABLED is not None:
        return bool(file_config.UPLOAD_ENABLED)
    return platform.system() != 'Windows'


async def scan_and_process(db: AsyncDB, directory: str, upload: bool = True) -> SummaryReport:
    """递归扫描目录内 pdf/docx/xlsx,逐个处理并汇总。"""
    base = Path(directory)
    if not base.is_dir():
        raise NotADirectoryError(f"目录不存在: {directory}")

    files = collect_files(base)
    report = SummaryReport(total=len(files))

    for fp in files:
        try:
            result = await process_file(db, base, fp, upload=upload)
        except Exception as ex:
            result = FileResult(fp.name, str(fp), 'failed', error=f"未预期异常: {ex}")
            logger.error(f"处理文件异常 {fp}: {ex}", exc_info=True)

        if result.status == 'ok':
            report.ok += 1
            report.project_total += result.project_count
            logger.info(f"OK: {result.file_name} (项目 {result.project_count} 条)")
        elif result.status == 'skipped_existing':
            report.skipped += 1
            logger.info(f"跳过(已入库): {result.file_name}")
        else:
            report.failed += 1
            report.failed_files.append((result.file_name, result.error))
            logger.error(f"FAIL: {result.file_name} - {result.error}")

    return report


def print_summary(report: SummaryReport) -> None:
    """输出汇总报告。"""
    logger.info("=" * 40)
    logger.info(f"共扫描 {report.total} 个文件")
    logger.info(f"成功处理: {report.ok} 个,入库项目 {report.project_total} 条")
    logger.info(f"已存在跳过: {report.skipped} 个")
    logger.info(f"失败: {report.failed} 个")
    for name, reason in report.failed_files:
        logger.error(f"  - {name}: {reason}")
    logger.info("=" * 40)


async def run(directory: str, upload: bool = True, dbkey:str='local') -> None:
    async with AsyncDB(dbkey=dbkey) as db:
        await db.init_db()
        report = await scan_and_process(db, directory, upload=upload)
        print_summary(report)


def main() -> None:
    directory = sys.argv[1] if len(sys.argv) > 1 else skpFilePath
    upload = resolve_upload()
    argv = sys.argv[1:]
    dbkey = argv[argv.index('--dbkey')+1] if '--dbkey' in argv else 'local'
    logger.info(f"开始处理目录: {directory}(上传 GoFast: {upload})")
    asyncio.run(run(directory, upload=upload, dbkey=dbkey))


if __name__ == "__main__":
    main()
