import re

import pandas as pd
import pymysql
from pymysql.cursors import DictCursor
from sympy.sets import conditionset

from parser.field_mapping import clean_amount
from util.db_config import mysql

def get_conn(db_config):
    """
    建立数据库连接,参数可动态传入
    调用时:get_conn(host='x', user='y', password='z', database='d')
    """
    # 默认值,未传的用默认
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '123456',
        'database': 'suidaobig',
        'charset': 'utf8mb4',
        'cursorclass': DictCursor,
    }
    config.update(db_config)          # 传入的参数覆盖默认值
    return pymysql.connect(**config)

def query(sql, params=None, fetch='all',dbKey={}):
    """
    通用查询函数
    :param sql: SQL 语句
    :param params: 参数元组/字典
    :param fetch: 'all' / 'one' / 'count'
    """
    conn = get_conn(dbKey)
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            if fetch == 'one':
                return cursor.fetchone()
            elif fetch == 'count':
                return cursor.rowcount
            else:
                return cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"查询失败: {e}")
        raise
    finally:
        conn.close()

def execute(sql, params=None, many=False, return_id=False, dbKey={}):
    """
    通用执行函数(INSERT / UPDATE / DELETE)
    :param sql: SQL 语句
    :param params: 单条参数元组,或批量插入时的列表
    :param many: True 时使用 executemany 批量执行
    :param return_id: True 时返回自增 ID
    :return: 受影响行数 或 自增 ID
    """
    conn = get_conn(dbKey)
    try:
        with conn.cursor() as cursor:
            if many:
                affected = cursor.executemany(sql, params)  # 批量
            else:
                affected = cursor.execute(sql, params)      # 单条

            new_id = cursor.lastrowid
        conn.commit()
        return new_id if return_id else affected
    except pymysql.MySQLError as e:
        conn.rollback()
        print(f"执行失败: {e}")
        raise
    finally:
        conn.close()

def is_long_body(text: str, fileType:str = '') -> bool:
    s = text.strip()
    if len(s) < 50 and fileType not in ['jpg','png']:
        return False
    punctuation = s.count('，') + s.count('。') + s.count('；')
    density = punctuation / len(s)
    has_verb_phrase = any(k in s for k in ('审议', '认为', '通过', '表示', '指出', '涵盖', '同意', '政策性','领导干部'))
    return density > 0.03 or (len(s) > 80 and has_verb_phrase) or (punctuation and has_verb_phrase)

import re

_LEFT  = re.compile(r'[（(]')
_RIGHT = re.compile(r'[）)]')

def is_continuation(prev: str, cur: str) -> bool:
    """
    判断 cur 是否为 prev 的续行（同一行数据被换行截断）。

    规则：
      - prev：恰好 1 个左括号（（ 或 (），且 0 个右括号（） 或 )）
      - cur ：恰好 1 个右括号（） 或 )），且 0 个左括号（（ 或 (）

    >>> is_continuation('沁河带状公园（两', '河交汇口-陵西桥）绿化景观提升')
    True
    """
    if not isinstance(prev, str) or not isinstance(cur, str):
        return False

    p_left, p_right = len(_LEFT.findall(prev)), len(_RIGHT.findall(prev))
    c_left, c_right = len(_LEFT.findall(cur)),  len(_RIGHT.findall(cur))

    # return p_left == 1 and p_right == 0 and c_right == 1 and c_left == 0
    p_diff = p_left - p_right
    c_diff = c_right - c_left
    return p_diff==1 and c_diff==1

def check_continue(projectsInfo):
    df = pd.DataFrame(projectsInfo)
    isShow = False
    for file_path,data in df.groupby('file_path'):
        prev = data['project_name'].iloc[:-1].to_numpy()
        cur = data['project_name'].iloc[1:].to_numpy()

        for i, (p, c) in enumerate(zip(prev, cur), start=1):
            # print(f"第 {i - 1} 行 vs 第 {i} 行:", p, c)
            if re.search('^[(（][^()（）]*?[)）]$', c) or is_continuation(p, c):
                isShow = True
                print('换行',p,c)
        if isShow:
            print('===文件：', file_path)
        isShow = False


def show_long_body(projectsInfo):
    for data in projectsInfo:
        line = data['project_name']
        file_type = data['file_type']
        if is_long_body(line,file_type):
            print(file_type, line)

def show_col(showKey:str,conditions:str='',dbKey={}):
    _sql = f'''
           SELECT {showKey}
           FROM skp_file f
                    LEFT JOIN skp_project p ON p.file_id = f.id
           where file_type='xls' and p.id and f.file_name!='附件：2023年重点项目表.xls' {conditions}  group by {showKey} ;
           '''
    # '''and category regexp '谷''''
    # '''order by length(project_name)'''
    showList = []
    projectsInfo = query(_sql,dbKey=dbKey)
    for data in projectsInfo:
        showData = data[showKey]
        if showKey == 'category':
            showList = showList+str(showData).split('-')
        else:
            showList.append(showData)
    showList = list(set(showList))
    showList.sort()
    for c in showList:
        # if len(c)<5:
        # if '谷' in c :
            print(c)

def show_amount(projectsInfo,dbKey={}):
    '''
    处理 docx，parse_line导致的错误total_investment
    :param projectsInfo:
    :param dbKey:
    :return:
    '''
    df = pd.DataFrame(projectsInfo)
    for file_path,data in df.groupby('file_path'):
        # 两条特征：大部分没金额；金额在project_name中出现
        dataNum = len(data)
        # for investment in ['total_investment']:  # ,'annual_investment']:
        investment = 'total_investment'
        investment_mask = data[investment] != 0
        investment_no_zero_df = data.loc[investment_mask, ['pid','project_name', investment]]
        if len(investment_no_zero_df)==0:
            continue
        elif len(investment_no_zero_df) / dataNum > 0.2:
            continue
        print('===文件：',file_path)
        print(f'有金额占比：{len(investment_no_zero_df)/dataNum*100:.2f}%')
        if len(investment_no_zero_df) / dataNum > 0.03:
            print('=====占比较大，跳过=====')
            continue
        for d in investment_no_zero_df.itertuples():
            pid = d.pid
            project_name = d.project_name
            investment_amount = getattr(d, investment)
            amount = clean_amount(project_name, require_unit=True, textType='line')
            if investment_amount == amount:
                print(f'{pid}，{project_name}, {investment_amount}, 金额：{amount}，需修改')
                update_sql = f'''update skp_project set {investment}=0 where id={pid};'''
                affected = execute(update_sql,dbKey=dbKey)
                print(f"更新了 {affected} 行")


if __name__ == '__main__':
    # user = query("SELECT * FROM users WHERE id = %s", (1,), fetch='one')
    # users = query("SELECT * FROM users WHERE age > %s", (18,))
    # dbKey = {}
    dbKey = mysql['db220']
    _sql = '''	
	    SELECT
    f.id AS fileId,p.id,
    p.id AS pid,
    f.file_path,
    f.file_type,
    p.project_name,source_row,project_type,category,construction_content,location,extra_info,total_investment,annual_investment,annual_goal,start_year,end_year,remark
    FROM skp_file f
    LEFT JOIN skp_project p ON p.file_id = f.id

		where f.file_type = 'xls' and p.id
    '''
    # projectsInfo = query(_sql,dbKey=dbKey)
    # show_long_body(projectsInfo)
    show_col('category',conditions='',dbKey=dbKey)

    # show_amount(projectsInfo,dbKey=dbKey)
    # check_continue(projectsInfo)
