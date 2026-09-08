"""异步数据库工具类(aiomysql):按运行平台选择 MySQL 连接,提供建表、入库、查询、更新。

平台选择规则:
- Windows → local(127.0.0.1)
- Linux → db252(192.168.1.252)

连接配置见 util/db_config.py,表结构与 skillDraft.md 中定义一致。
用法:
    async with AsyncDB() as db:
        await db.init_db()
        file_id = await db.save_file_with_projects(file_data, projects)
"""

import json
import platform
from typing import Any, Callable, Dict, List, Optional, Tuple

import aiomysql

from util.db_config import mysql
from util.log_util import get_logger

logger = get_logger(__file__)

# ---------- 建表语句 ----------

CREATE_TABLE_SKP_FILE = """
CREATE TABLE IF NOT EXISTS skp_file (
  id            BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  file_name     VARCHAR(255)  NOT NULL                COMMENT '原始文件名',
  file_path     VARCHAR(512)  DEFAULT ''              COMMENT '目录内相对路径',
  file_type     VARCHAR(10)   DEFAULT ''              COMMENT '扩展名 pdf/docx/xlsx',
  gofast_url    VARCHAR(512)  DEFAULT ''              COMMENT 'GoFast 上传后 URL',
  area_id       INT           DEFAULT 0               COMMENT '省份ID,见 util/area_id.py',
  year          INT           DEFAULT 0               COMMENT '文件对应年份,0=未知',
  file_size     BIGINT        DEFAULT 0               COMMENT '文件字节数',
  file_hash     CHAR(64)      DEFAULT ''              COMMENT 'SHA-256,用于去重',
  status        TINYINT       DEFAULT 1               COMMENT '0=失败 1=成功',
  created_at    DATETIME      DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uk_hash (file_hash),
  KEY idx_area_year (area_id, year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='重点项目源文件(含 GoFast 关联)'
"""

CREATE_TABLE_SKP_PROJECT = """
CREATE TABLE IF NOT EXISTS skp_project (
  id                    BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  file_id               BIGINT UNSIGNED NOT NULL      COMMENT '关联 skp_file.id',
  area_id               INT           DEFAULT 0       COMMENT '省份ID',
  project_name          VARCHAR(255)  NOT NULL        COMMENT '项目名称',
  construction_unit     VARCHAR(255)  DEFAULT ''      COMMENT '建设单位',
  location              VARCHAR(255)  DEFAULT ''      COMMENT '建设地点',
  total_investment      DECIMAL(20,2) DEFAULT 0       COMMENT '总投资(万元)',
  annual_investment     DECIMAL(20,2) DEFAULT 0       COMMENT '年度计划投资(万元)',
  start_year            INT           DEFAULT 0       COMMENT '开工年份',
  end_year              INT           DEFAULT 0       COMMENT '竣工年份',
  construction_content  TEXT                          COMMENT '建设内容',
  responsible_unit      VARCHAR(255)  DEFAULT ''      COMMENT '责任单位',
  project_owner         VARCHAR(255)  DEFAULT ''      COMMENT '项目业主/业主单位(业主方)',
  source_row            INT           DEFAULT 0       COMMENT '源文件中的行号(调试用)',
  project_type          VARCHAR(32)   DEFAULT ''      COMMENT '建设性质:新建/续建/竣工投产/预备/储备',
  category              VARCHAR(128)  DEFAULT ''      COMMENT '行业分类(如 工业-电子信息)',
  annual_goal           VARCHAR(512)  DEFAULT ''      COMMENT '年度工作目标(前期研究阶段项目)',
  raw_fields            JSON                          COMMENT '未映射字段的原始数据',
  created_at            DATETIME      DEFAULT CURRENT_TIMESTAMP,
  KEY idx_file (file_id),
  KEY idx_name (project_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='省重点项目明细'
"""

CREATE_TABLE_SKP_FILE_EXTRA = """
CREATE TABLE IF NOT EXISTS skp_file_extra (
  id           BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  file_id      BIGINT UNSIGNED NOT NULL              COMMENT '关联 skp_file.id',
  project_id   BIGINT UNSIGNED NOT NULL              COMMENT '关联 skp_project.id(该行项目)',
  extra_info   JSON                                  COMMENT '文件特有信息(如 {"合作方式":"合资","联系方式":"xxx"})',
  created_at   DATETIME      DEFAULT CURRENT_TIMESTAMP,
  KEY idx_file (file_id),
  KEY idx_project (project_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文件特有信息(非共性字段,每项目一行 JSON)'
"""

CREATE_TABLE_SKP_NOTICE = """
CREATE TABLE IF NOT EXISTS skp_notice (
  id               BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  file_id          BIGINT UNSIGNED NOT NULL          COMMENT '关联 skp_file.id',
  title            VARCHAR(255)  DEFAULT ''          COMMENT '通知标题',
  notice_no        VARCHAR(128)  DEFAULT ''          COMMENT '文件编号(如 桂重大办〔2020〕4号)',
  issuer           VARCHAR(255)  DEFAULT ''          COMMENT '发文单位',
  issue_date       DATE NULL                         COMMENT '发文时间',
  content          MEDIUMTEXT                        COMMENT '通知正文',
  attachment_names VARCHAR(1024) DEFAULT ''          COMMENT '文末附件名称(逗号/顿号分隔)',
  has_project_list TINYINT       DEFAULT 0           COMMENT '是否含重点项目清单(0=否 1=是)',
  created_at       DATETIME      DEFAULT CURRENT_TIMESTAMP,
  KEY idx_file (file_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='红头文件(计划通知类)信息'
"""

CREATE_TABLE_SKP_CATEGORY_DECLARED = """
CREATE TABLE IF NOT EXISTS skp_category_declared (
  id             BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  file_id        BIGINT UNSIGNED NOT NULL          COMMENT '关联 skp_file.id',
  category       VARCHAR(128)   NOT NULL           COMMENT '分类名(如 重大产业项目-光伏发电项目)',
  declared_count INT            NOT NULL           COMMENT '标题声明项数(如 "光伏发电项目(16项)" → 16)',
  actual_count   INT            NOT NULL DEFAULT 0 COMMENT '实际解析项目数(含子分类)',
  created_at     DATETIME       DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uk_file_cat (file_id, category),
  KEY idx_file (file_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='分类标题声明项数与实际解析数(解析校验统计)'
"""

INSERT_FILE_SQL = """
INSERT INTO skp_file
    (file_name, file_path, file_type, gofast_url, area_id, year,
     file_size, file_hash, status, full_field_status)
VALUES
    (%(file_name)s, %(file_path)s, %(file_type)s, %(gofast_url)s, %(area_id)s, %(year)s,
     %(file_size)s, %(file_hash)s, %(status)s, %(full_field_status)s)
"""

INSERT_PROJECT_SQL = """
INSERT INTO skp_project
    (file_id, area_id, project_name, construction_unit, location,
     total_investment, annual_investment, start_year, end_year,
     construction_content, responsible_unit, project_owner, source_row,
     project_type, category, annual_goal, raw_fields, remark)
VALUES
    (%(file_id)s, %(area_id)s, %(project_name)s, %(construction_unit)s, %(location)s,
     %(total_investment)s, %(annual_investment)s, %(start_year)s, %(end_year)s,
     %(construction_content)s, %(responsible_unit)s, %(project_owner)s, %(source_row)s,
     %(project_type)s, %(category)s, %(annual_goal)s, %(raw_fields)s, %(remark)s)
"""

INSERT_EXTRA_SQL = """
INSERT INTO skp_file_extra (file_id, project_id, extra_info)
VALUES (%(file_id)s, %(project_id)s, %(extra_info)s)
"""

INSERT_NOTICE_SQL = """
INSERT INTO skp_notice
    (file_id, title, notice_no, issuer, issue_date, content, attachment_names, has_project_list)
VALUES
    (%(file_id)s, %(title)s, %(notice_no)s, %(issuer)s, %(issue_date)s,
     %(content)s, %(attachment_names)s, %(has_project_list)s)
"""

INSERT_CATEGORY_DECLARED_SQL = """
INSERT INTO skp_category_declared (file_id, category, declared_count, actual_count)
VALUES (%(file_id)s, %(category)s, %(declared_count)s, %(actual_count)s)
ON DUPLICATE KEY UPDATE declared_count = VALUES(declared_count), actual_count = VALUES(actual_count)
"""

# 表结构演进时对已有表补充的列(DDL 为代码内常量,无注入风险)
PROJECT_EXTRA_COLUMNS = [
    ("project_type", "VARCHAR(32) NOT NULL DEFAULT '' COMMENT '建设性质:新建/续建/竣工投产/预备/储备'"),
    ("category", "VARCHAR(128) NOT NULL DEFAULT '' COMMENT '行业分类(如 工业-电子信息)'"),
    ("annual_goal", "VARCHAR(512) NOT NULL DEFAULT '' COMMENT '年度工作目标(前期研究阶段项目)'"),
    ("project_owner", "VARCHAR(255) NOT NULL DEFAULT '' COMMENT '项目业主/业主单位(业主方)'"),
    ("remark", "VARCHAR(255) NOT NULL DEFAULT '' COMMENT '备注(疑似分类/单位字段行标记,人工核查)'"),
]
FILE_EXTRA_COLUMNS = [
    ("full_field_status", "JSON NULL COMMENT 'full_field 宽松规则统计(按 sheet):relax/full/total/hinted/plain/biz_fields,供人工分析'"),
]

_MAX_VARCHAR = 255
_FILE_UPDATE_FIELDS = {
    'file_name', 'file_path', 'file_type', 'gofast_url',
    'area_id', 'year', 'file_size', 'file_hash', 'status', 'full_field_status',
}


class AsyncDB:
    """异步 MySQL 工具类:平台选库 + 建表/入库/查询/更新。"""

    def __init__(self, minsize: int = 1, maxsize: int = 5) -> None:
        self._pool: Optional[aiomysql.Pool] = None
        self.minsize = minsize
        self.maxsize = maxsize

    # ---------- 生命周期 ----------

    @staticmethod
    def get_db_config() -> Dict[str, Any]:
        """根据当前操作系统返回数据库配置:Windows → local,Linux 等 → db252。"""
        system = platform.system()
        key = 'local' if system == 'Windows' else 'db252'
        if key not in mysql:
            raise ValueError(f"未找到数据库配置: {key}")
        return mysql[key]

    async def connect(self) -> "AsyncDB":
        """创建连接池(幂等),返回自身便于链式调用。"""
        if self._pool is not None:
            return self
        cfg = self.get_db_config()
        self._pool = await aiomysql.create_pool(
            host=cfg['host'],
            port=cfg['port'],
            user=cfg['user'],
            password=cfg['password'],
            db=cfg['database'],
            charset=cfg.get('charset', 'utf8mb4'),
            minsize=self.minsize,
            maxsize=self.maxsize,
            autocommit=False,
            cursorclass=aiomysql.DictCursor,
        )
        logger.info(f"数据库连接池已创建: {cfg['host']}:{cfg['port']}/{cfg['database']}")
        return self

    async def close(self) -> None:
        """关闭连接池,释放全部连接。"""
        if self._pool is not None:
            self._pool.close()
            await self._pool.wait_closed()
            self._pool = None
            logger.info("数据库连接池已关闭")

    async def __aenter__(self) -> "AsyncDB":
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()

    # ---------- 内部:连接池内执行 ----------

    async def _with_conn(self, work: Callable[[Any], Any], *, commit: bool = False) -> Any:
        """在池化连接上执行 work(conn);commit=True 提交,异常回滚后抛出。"""
        if self._pool is None:
            raise RuntimeError("AsyncDB 未连接,请先 await db.connect()")
        async with self._pool.acquire() as conn:
            try:
                result = await work(conn)
            except Exception:
                await conn.rollback()
                raise
            if commit:
                await conn.commit()
            return result

    # ---------- 通用执行 ----------

    async def query(self, sql: str, params: Tuple[Any, ...] = ()) -> List[Dict[str, Any]]:
        """执行查询语句,返回 dict 列表。SQL 必须使用 %s 占位符。"""

        async def _run(conn: Any) -> List[Dict[str, Any]]:
            async with conn.cursor() as cur:
                await cur.execute(sql, params)
                return list(await cur.fetchall())

        return await self._with_conn(_run)

    async def execute(self, sql: str, params: Tuple[Any, ...] = ()) -> int:
        """执行写语句(INSERT/UPDATE/DELETE),自动提交,返回影响行数。"""

        async def _run(conn: Any) -> int:
            async with conn.cursor() as cur:
                return await cur.execute(sql, params)

        return await self._with_conn(_run, commit=True)

    # ---------- 建表 ----------

    async def init_db(self) -> None:
        """创建 skp_file、skp_project 表(IF NOT EXISTS,可重复执行),并迁移补充新增列。"""

        async def _run(conn: Any) -> None:
            async with conn.cursor() as cur:
                await cur.execute(CREATE_TABLE_SKP_FILE)
                await cur.execute(CREATE_TABLE_SKP_PROJECT)
                await cur.execute(CREATE_TABLE_SKP_FILE_EXTRA)
                await cur.execute(CREATE_TABLE_SKP_NOTICE)
                await cur.execute(CREATE_TABLE_SKP_CATEGORY_DECLARED)
                for column, ddl in PROJECT_EXTRA_COLUMNS:
                    await self._ensure_column(cur, 'skp_project', column, ddl)
                for column, ddl in FILE_EXTRA_COLUMNS:
                    await self._ensure_column(cur, 'skp_file', column, ddl)

        await self._with_conn(_run, commit=True)
        logger.info("数据库表初始化完成(skp_file/skp_project/skp_file_extra/skp_notice/skp_category_declared)")

    @staticmethod
    async def _ensure_column(cur: Any, table: str, column: str, ddl: str) -> None:
        """检查列是否存在,不存在则 ALTER 补充(用于表结构演进)。"""
        await cur.execute(
            "SELECT COUNT(*) AS n FROM information_schema.COLUMNS "
            "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s AND COLUMN_NAME = %s",
            (table, column))
        row = await cur.fetchone()
        if row and int(row['n']) == 0:
            await cur.execute(f"ALTER TABLE `{table}` ADD COLUMN `{column}` {ddl}")
            logger.info(f"表 {table} 已新增列 {column}")

    # ---------- 入库 ----------

    async def insert_file(self, file_data: Dict[str, Any]) -> int:
        """插入一条文件记录,返回自增 file_id。"""

        async def _run(conn: Any) -> int:
            async with conn.cursor() as cur:
                await cur.execute(INSERT_FILE_SQL, _normalize_file(file_data))
                return int(cur.lastrowid)

        return await self._with_conn(_run, commit=True)

    async def insert_projects(self, file_id: int, projects: List[Dict[str, Any]]) -> int:
        """插入项目记录(同一 file_id)及其文件特有信息,返回插入条数。

        逐条插入以获取各项目 id,供 skp_file_extra 关联;无项目名称的行自动跳过。
        """
        count = 0

        async def _run(conn: Any) -> int:
            nonlocal count
            async with conn.cursor() as cur:
                for project in projects:
                    if not (project.get('project_name') or '').strip():
                        logger.warning(f"file_id={file_id} 存在无项目名称的行,已跳过")
                        continue
                    await cur.execute(INSERT_PROJECT_SQL, _normalize_project(file_id, project))
                    project_id = int(cur.lastrowid)
                    extra = _normalize_extra(file_id, project_id, project.get('extra_fields'))
                    if extra:
                        await cur.execute(INSERT_EXTRA_SQL, extra)
                    count += 1
            return count

        return await self._with_conn(_run, commit=True)

    async def save_file_with_projects(self, file_data: Dict[str, Any],
                                      projects: List[Dict[str, Any]]) -> Optional[int]:
        """单文件一个事务:先插入文件记录,再逐条插入项目记录及其特有信息。

        成功返回 file_id;失败回滚并返回 None。
        """
        file_id: Optional[int] = None

        async def _run(conn: Any) -> int:
            nonlocal file_id
            async with conn.cursor() as cur:
                await cur.execute(INSERT_FILE_SQL, _normalize_file(file_data))
                file_id = int(cur.lastrowid)
                for project in projects:
                    if not (project.get('project_name') or '').strip():
                        logger.warning(f"file_id={file_id} 存在无项目名称的行,已跳过")
                        continue
                    await cur.execute(INSERT_PROJECT_SQL, _normalize_project(file_id, project))
                    project_id = int(cur.lastrowid)
                    extra = _normalize_extra(file_id, project_id, project.get('extra_fields'))
                    if extra:
                        await cur.execute(INSERT_EXTRA_SQL, extra)
            return file_id

        try:
            return await self._with_conn(_run, commit=True)
        except Exception as ex:
            logger.error(f"文件 {file_data.get('file_name', '')} 入库失败,已回滚: {ex}",
                         exc_info=True)
            return None

    async def save_category_declared(self, file_id: int,
                                     declared_sum: Dict[str, int],
                                     actual: Dict[str, int]) -> None:
        """保存分类标题声明项数与实际解析数(解析校验统计)。

        declared_sum: 分类 → 标题声明项数(同分类累加)
        actual: 分类 → 实际解析项目数;子分类项目计入父分类
        """
        rows: List[Dict[str, Any]] = []
        for cat, declared in declared_sum.items():
            got = sum(n for c, n in actual.items() if c == cat or c.startswith(cat + '-'))
            rows.append({
                'file_id': int(file_id),
                'category': str(cat)[:128],
                'declared_count': int(declared),
                'actual_count': int(got),
            })
        if not rows:
            return

        async def _run(conn: Any) -> None:
            async with conn.cursor() as cur:
                await cur.executemany(INSERT_CATEGORY_DECLARED_SQL, rows)

        await self._with_conn(_run, commit=True)

    async def save_notice(self, notice: Dict[str, Any]) -> Optional[int]:
        """保存红头文件(计划通知)信息,返回 notice id;失败返回 None(不影响主流程)。"""

        async def _run(conn: Any) -> int:
            async with conn.cursor() as cur:
                await cur.execute(INSERT_NOTICE_SQL, _normalize_notice(notice))
                return int(cur.lastrowid)

        try:
            return await self._with_conn(_run, commit=True)
        except Exception as ex:
            logger.error(f"通知信息入库失败(file_id={notice.get('file_id', '')}): {ex}",
                         exc_info=True)
            return None

    # ---------- 查询 ----------

    async def get_file_by_hash(self, file_hash: str) -> Optional[Dict[str, Any]]:
        """按 SHA-256 查询文件记录(用于去重),不存在返回 None。"""
        if not file_hash:
            return None
        rows = await self.query("SELECT * FROM skp_file WHERE file_hash = %s", (file_hash,))
        return rows[0] if rows else None

    async def get_file_by_id(self, file_id: int) -> Optional[Dict[str, Any]]:
        """按主键查询文件记录。"""
        rows = await self.query("SELECT * FROM skp_file WHERE id = %s", (int(file_id),))
        return rows[0] if rows else None

    async def get_projects_by_file(self, file_id: int) -> List[Dict[str, Any]]:
        """查询某文件下的全部项目记录。"""
        return await self.query(
            "SELECT * FROM skp_project WHERE file_id = %s ORDER BY id", (int(file_id),))

    async def count_projects(self) -> int:
        """查询项目总数。"""
        rows = await self.query("SELECT COUNT(*) AS total FROM skp_project")
        return int(rows[0]['total']) if rows else 0

    # ---------- 更新 ----------

    async def update_file(self, file_id: int, **fields: Any) -> bool:
        """按 file_id 更新文件记录,仅允许白名单字段,返回是否更新成功。

        示例:
            await db.update_file(1, gofast_url="http://.../x.pdf", status=0)
        """
        allowed = {k: v for k, v in fields.items() if k in _FILE_UPDATE_FIELDS}
        if not allowed:
            logger.warning(f"update_file 没有可更新的白名单字段: {fields}")
            return False
        # 列名来自白名单集合,无注入风险
        set_clause = ", ".join(f"{col} = %s" for col in allowed)
        sql = f"UPDATE skp_file SET {set_clause} WHERE id = %s"
        params = tuple(allowed.values()) + (int(file_id),)
        return await self.execute(sql, params) > 0

    async def update_file_status(self, file_id: int, status: int) -> bool:
        """更新文件处理状态(0=失败 1=成功)。"""
        return await self.update_file(file_id, status=int(status))

    # ---------- 删除 ----------

    async def delete_file_data(self, file_hash: str) -> Dict[str, int]:
        """按文件 SHA-256 删除该文件及其全部关联数据(单事务,失败自动回滚)。

        删除顺序:先子表(skp_file_extra/skp_project/skp_notice/skp_category_declared),
        后父表 skp_file。返回各表删除行数 {'file','project','extra','notice','category_declared'};
        文件不存在时各表均为 0。
        """

        async def _run(conn: Any) -> Dict[str, int]:
            async with conn.cursor() as cur:
                await cur.execute("SELECT id FROM skp_file WHERE file_hash = %s", (file_hash,))
                # await cur.execute("SELECT id FROM skp_file WHERE file_path = %s", (file_hash,))
                row = await cur.fetchone()
                if not row:
                    return {'file': 0, 'project': 0, 'extra': 0, 'notice': 0, 'category_declared': 0}
                file_id = int(row['id'])
                deleted: Dict[str, int] = {}
                # 表名均为代码内常量,无注入风险
                for table, key in (('skp_file_extra', 'extra'), ('skp_project', 'project'),
                                   ('skp_notice', 'notice'), ('skp_category_declared', 'category_declared')):
                    await cur.execute(f"DELETE FROM {table} WHERE file_id = %s", (file_id,))
                    deleted[key] = cur.rowcount
                await cur.execute("DELETE FROM skp_file WHERE id = %s", (file_id,))
                deleted['file'] = cur.rowcount
                return deleted

        return await self._with_conn(_run, commit=True)


# ---------- 数据清洗(模块级,供各方法复用) ----------


def _normalize_file(data: Dict[str, Any]) -> Dict[str, Any]:
    """清洗文件记录字段,补齐默认值。"""
    return {
        'file_name': (data.get('file_name') or '')[:255],
        'file_path': (data.get('file_path') or '')[:512],
        'file_type': (data.get('file_type') or '').lstrip('.').lower()[:10],
        'gofast_url': (data.get('gofast_url') or '')[:512],
        'area_id': int(data.get('area_id') or 0),
        'year': int(data.get('year') or 0),
        'file_size': int(data.get('file_size') or 0),
        'file_hash': data.get('file_hash') or '',
        'status': int(data.get('status', 1)),
        # full_field 统计(JSON 字符串,如 {"sheets": {...}});None → 不入列
        'full_field_status': data.get('full_field_status'),
    }


def _normalize_project(file_id: int, project: Dict[str, Any]) -> Dict[str, Any]:
    """清洗项目记录字段,补齐默认值;raw_fields(dict)序列化为 JSON。"""
    raw = project.get('raw_fields')
    if raw:
        try:
            raw_json = json.dumps(raw, ensure_ascii=False)
        except (TypeError, ValueError):
            raw_json = json.dumps(str(raw), ensure_ascii=False)
    else:
        raw_json = None
    return {
        'file_id': int(file_id),
        'area_id': int(project.get('area_id') or 0),
        'project_name': (project.get('project_name') or '').strip()[:_MAX_VARCHAR],
        'construction_unit': (project.get('construction_unit') or '')[:255],
        'location': (project.get('location') or '')[:255],
        'total_investment': float(project.get('total_investment') or 0),
        'annual_investment': float(project.get('annual_investment') or 0),
        'start_year': int(project.get('start_year') or 0),
        'end_year': int(project.get('end_year') or 0),
        'construction_content': project.get('construction_content') or '',
        'responsible_unit': (project.get('responsible_unit') or '')[:255],
        'project_owner': (project.get('project_owner') or '')[:255],
        'source_row': int(project.get('source_row') or 0),
        'project_type': (project.get('project_type') or '')[:32],
        'category': (project.get('category') or '')[:128],
        'annual_goal': (project.get('annual_goal') or '')[:512],
        'raw_fields': raw_json,
        'remark': (project.get('remark') or '')[:255],
    }


def _normalize_extra(file_id: int, project_id: int,
                     extra_fields: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """把项目行的文件特有信息组装为 skp_file_extra 单行(extra_info 为 JSON)。

    空字段过滤;无特有信息返回 None(不产生 extra 行)。
    """
    cleaned = {}
    for name, value in (extra_fields or {}).items():
        field_name = str(name).strip()[:64]
        field_value = str(value or '').replace('\n', ' ').strip()[:512]
        if field_name and field_value:
            cleaned[field_name] = field_value
    if not cleaned:
        return None
    return {
        'file_id': int(file_id),
        'project_id': int(project_id),
        'extra_info': json.dumps(cleaned, ensure_ascii=False),
    }


def _normalize_notice(notice: Dict[str, Any]) -> Dict[str, Any]:
    """清洗通知信息字段。"""
    return {
        'file_id': int(notice.get('file_id') or 0),
        'title': (notice.get('title') or '')[:255],
        'notice_no': (notice.get('notice_no') or '')[:128],
        'issuer': (notice.get('issuer') or '')[:255],
        'issue_date': notice.get('issue_date') or None,
        'content': notice.get('content') or '',
        'attachment_names': (notice.get('attachment_names') or '')[:1024],
        'has_project_list': int(notice.get('has_project_list') or 0),
    }


def _build_project_rows(file_id: int, projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """清洗并过滤项目行;无项目名称的行跳过。"""
    rows = []
    for project in projects:
        if not (project.get('project_name') or '').strip():
            logger.warning(f"file_id={file_id} 存在无项目名称的行,已跳过")
            continue
        rows.append(_normalize_project(file_id, project))
    return rows


if __name__ == "__main__":
    import asyncio


    async def _test() -> None:
        # 测试:初始化表结构(可重复执行,不会重复建表)
        async with AsyncDB() as db:
            await db.init_db()
        logger.info("init_db 执行完成")


    asyncio.run(_test())
