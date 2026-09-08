"""数据查看脚本:按 beizhu.md 的检查口径 + category/机构名等维度审计库内解析结果。

用于发现"该是分类/分组/备注却被当项目"、"名称/分类被污染"等解析问题,
输出逐项报告作为后续解析优化的依据(如发现新的 表头别名/分类词/装饰行 场景)。

用法:
    python check_data.py                      # 检查全部文件类型的解析结果
    python check_data.py --type xlsx          # 仅检查 xlsx 文件(按 skp_file.file_type)
    python check_data.py --type docx          # 仅 docx;--type pdf / xls 同理
    python check_data.py --type all --exclude xlsx   # 排除 xlsx,检查其余类型
    python check_data.py --top 20             # 每项明细行数上限(默认 10)
    python check_data.py --db db252           # 换库(默认 local,见 util/db_config.py)
    python check_data.py --out report.txt     # 结果同时写入文件(utf-8)

检查项(来源 beizhu.md 1~6 + category 污染):
  1 project_name 过短(<10 字)
  2 project_name 末尾残留 "（N个/项/件）" 统计后缀
  3 category 过长(>30 字,疑似未清洗干净)
  3b category 含空格拼接/序号残留(如 "基础设施 一、基础设施" 合并单元格污染)
  4 单文件解析条数过少(<= --min,疑似漏解析;阈值默认 3)
  5 同文件"无详情"项目(地点/内容/年限全空)与总数不一致(部分/全部无详情)
  6 机构/地区名称被识别为项目(尾 市/区/县/州/盟/省/政府/厅/局/委/办/管委会/集团/公司)
    ——注意:园区/小区/校区/灌区 等"区"结尾可能是真项目名,需结合上下文人工判断
"""

import argparse
import os
import sys
from typing import Any, Dict, List, Tuple

import pymysql

from util.db_config import mysql

# 类型参数 → skp_file.file_type 取值(文件类型为入库时记录的后缀)
TYPE_CHOICES = ('xlsx', 'docx', 'pdf', 'xls')


def connect(db_name: str):
    cfg = mysql.get(db_name)
    if cfg is None:
        raise SystemExit(f"未知库名: {db_name}(可选 {list(mysql)})")
    return pymysql.connect(host=cfg['host'], port=cfg['port'], user=cfg['user'],
                           password=cfg['password'], database=cfg['database'],
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


class Check:
    """单个检查项:sql(占位符 %(ftype)s)与展示方式。"""

    def __init__(self, title: str, desc: str, sql: str,
                 kind: str = 'detail', note: str = ''):
        self.title = title
        self.desc = desc
        self.sql = sql
        self.kind = kind          # detail:明细列; agg:已聚合列
        self.note = note


def build_checks(min_count: int, ftypes_sql: str, limit: int) -> List[Check]:
    # ftypes_sql/limit/min_count 均来自白名单枚举与 int 参数,可安全内插;
    # 避免 pymysql %-格式化与 SQL 字面 %(LIKE '% %')冲突
    f = f"AND f.file_type IN {ftypes_sql}"
    join = ("FROM skp_file f LEFT JOIN skp_project p ON p.file_id = f.id "
            "LEFT JOIN skp_file_extra e ON e.project_id = p.id")
    return [
        Check('project_name 过短', '名称 <10 字(疑似 分类/备注/碎片 被当项目)',
              f"""SELECT f.file_name, f.file_path, p.project_name, p.category,
                         p.source_row, e.extra_info
                  {join} WHERE p.project_name IS NOT NULL AND LENGTH(p.project_name) < 10
                  AND LENGTH(TRIM(p.project_name)) > 0 {f} ORDER BY LENGTH(p.project_name)
                  LIMIT {limit}""",
              note='真项目名也可能 <10 字(如 "腾冲灌区")需结合上下文;重点看 备注/表头/碎片 类'),
        Check('名称残留 "(N个/项/件)" 统计后缀', '项目名以 "（N个）" 等收尾 = 分类行统计未剥离',
              f"""SELECT f.file_name, p.project_name, p.category, p.source_row
                  {join} WHERE p.project_name REGEXP '[（(][0-9]+(个|项|件)[)）]+$' {f}
                  ORDER BY f.file_name LIMIT {limit}"""),
        Check('category 过长(>30 字)', '疑似 拼接/未清洗 的分类名;按分类聚合条数',
              f"""SELECT p.category, COUNT(*) AS cnt, GROUP_CONCAT(DISTINCT f.file_type) AS types
                  {join} WHERE p.category <> '' AND LENGTH(p.category) > 30 {f}
                  GROUP BY p.category ORDER BY LENGTH(p.category) DESC, cnt DESC
                  LIMIT {limit}""", kind='agg',
              note='常见成因:合并单元格文本重复/多级分类整段拼接(见 3b)'),
        Check('category 疑似污染(空格拼接/序号残留)', '含内部空格拼接(如 "基础设施 一、基础设施")'
              '或序号前缀(一、/（一）)残留',
              f"""SELECT p.category, COUNT(*) AS cnt, GROUP_CONCAT(DISTINCT f.file_type) AS types
                  {join}
                  WHERE p.category <> '' AND (
                      p.category LIKE '% %'
                      OR p.category REGEXP '^(一|二|三|四|五|六|七|八|九|十|[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]|[0-9])+[、.]'
                      OR p.category REGEXP '[（(][一二三四五六七八九十]+[)）]')
                  {f} GROUP BY p.category ORDER BY cnt DESC LIMIT {limit}""", kind='agg',
              note='合并单元格跨列重复("一、基础设施 ×2")曾致 "基础设施 一、基础设施" 入库'),
        Check('单文件解析条数过少(疑似漏解析)', f'项目数 <= {min_count} 的文件',
              f"""SELECT f.file_name, f.file_type, COUNT(p.id) AS cnt
                  FROM skp_file f LEFT JOIN skp_project p ON p.file_id = f.id
                  WHERE f.file_type IN {ftypes_sql}
                  GROUP BY f.id, f.file_name, f.file_type
                  HAVING cnt <= {min_count}
                  ORDER BY cnt, f.file_name LIMIT {limit}""", kind='agg',
              note='可能:该文件本就无明细(新闻稿/仅通知/清单在附件)、结构未识别、或解析遗漏'),
        Check('同文件存在"无详情"项目', 'location/建设内容/起止年限 全空的项目(部分或全部无详情)',
              f"""SELECT f.file_name, f.file_type,
                         SUM(CASE WHEN p.location='' AND p.construction_content=''
                                       AND p.start_year=0 THEN 1 ELSE 0 END) AS no_detail,
                         COUNT(p.id) AS total
                  FROM skp_file f LEFT JOIN skp_project p ON p.file_id = f.id
                  WHERE f.file_type IN {ftypes_sql}
                  GROUP BY f.id, f.file_name, f.file_type
                  HAVING no_detail > 0
                  ORDER BY no_detail DESC LIMIT {limit}""", kind='agg',
              note='no_detail == total:整文件仅名称(目录/正文排版被当项目);no_detail < total:部分行缺字段'),
        Check('机构/地区名被识别为项目', '名称以 市/区/县/州/盟/省/政府/厅/局/委/办/管委会/集团/公司 结尾',
              f"""SELECT p.project_name, COUNT(*) AS cnt, GROUP_CONCAT(DISTINCT f.file_type) AS types
                  {join}
                  WHERE p.project_name REGEXP
                        '(市|区|县|州|盟|省|人民政府|政府|厅|局|委|办|管委会|集团|公司)$'
                  {f} GROUP BY p.project_name ORDER BY cnt DESC LIMIT {limit}""", kind='agg',
              note='"xx园区/小区/校区/灌区" 等"区"结尾多为真项目;短名(<=5 字)城市名/机构单行才是漏网分组行'),
    ]


def run_checks(conn, checks: List[Check]) -> List[Dict[str, Any]]:
    results = []
    with conn.cursor() as cur:
        for chk in checks:
            cur.execute(chk.sql)
            rows = cur.fetchall()
            results.append({'check': chk, 'rows': rows, 'count': len(rows)})
    return results


def render(results: List[Dict[str, Any]], out: Any) -> None:
    def say(s: str = '') -> None:
        print(s)
        out.write(s + '\n')

    total_hits = 0
    for r in results:
        chk = r['check']
        rows = r['rows']
        hit = len(rows) > 0
        total_hits += len(rows)
        say('=' * 78)
        say(f"[{'命中' if hit else '通过'}] {chk.title}")
        say(f"   {chk.desc}")
        if chk.note:
            say(f"   提示: {chk.note}")
        if not rows:
            say('   (无)')
            continue
        # 列头:取第一条 dict 的键
        cols = list(rows[0].keys())
        widths = [len(c) for c in cols]
        rendered = []
        for row in rows:
            line = []
            for i, c in enumerate(cols):
                v = '' if row[c] is None else str(row[c])
                if c in ('file_path', 'project_name', 'category') and len(v) > 44:
                    v = v[:44] + '…'
                line.append(v)
                widths[i] = max(widths[i], len(v))
            rendered.append(line)
        widths = [min(w, 60) for w in widths]
        head = ' | '.join(c.ljust(widths[i]) for i, c in enumerate(cols))
        say('  ' + head)
        say('  ' + '-' * min(len(head), 120))
        for line in rendered:
            say('  ' + ' | '.join(line[i].ljust(widths[i]) for i in range(len(cols))))
    say('=' * 78)
    say(f'完成:共 {len(results)} 项检查,命中 {total_hits} 行(明细行上限 {args.top} 条/项)。')
    say('命中项可作为解析优化依据:对照 analyzer 相关规则(text_clean/装饰行/分类词表/别名)定位来源文件后,'
        '补充规则并重跑对应文件(batch_test.py <type>)。')


def main() -> None:
    global args
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--type', dest='ftype', default='all',
                    help='仅检查该文件类型: ' + '/'.join(TYPE_CHOICES) + ' 或 all(默认)')
    ap.add_argument('--exclude', dest='exclude', default='',
                    help='排除的文件类型(与 --type 叠加,如 --type all --exclude xlsx '
                         '= 检查 docx/pdf/xls)')
    ap.add_argument('--top', type=int, default=10, help='每项输出明细行上限(默认 10)')
    ap.add_argument('--min', type=int, default=3, help='“条数过少”阈值(默认 3)')
    ap.add_argument('--db', default='local', help='数据库: local / db252(默认 local)')
    ap.add_argument('--out', default='', help='结果同时写入该 utf-8 文件')
    args = ap.parse_args()

    if args.ftype == 'all':
        ftypes = TYPE_CHOICES
    elif args.ftype in TYPE_CHOICES:
        ftypes = (args.ftype,)
    else:
        raise SystemExit(f"--type 仅支持 {'/'.join(TYPE_CHOICES)} 或 all")
    if args.exclude:
        if args.exclude not in TYPE_CHOICES:
            raise SystemExit(f"--exclude 仅支持 {'/'.join(TYPE_CHOICES)}")
        ftypes = tuple(t for t in ftypes if t != args.exclude)
        if not ftypes:
            raise SystemExit("--type 与 --exclude 叠加后为空,请调整参数")
    # 类型值来自白名单枚举,可直接拼 SQL IN 子句(避免 pymysql %-格式化)
    ftypes_sql = '(' + ','.join(f"'{t}'" for t in ftypes) + ')'

    sys.stdout.reconfigure(encoding='utf-8')
    out = open(args.out, 'w', encoding='utf-8') if args.out else open(os.devnull, 'w')
    try:
        print(f"数据库: {args.db} | 文件类型: {args.ftype} | 每项明细上限: {args.top}")
        conn = connect(args.db)
        try:
            results = run_checks(conn, build_checks(args.min, ftypes_sql, args.top))
            render(results, out)
        finally:
            conn.close()
    finally:
        out.close()


if __name__ == '__main__':
    main()
