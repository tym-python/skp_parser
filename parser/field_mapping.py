"""表头别名映射与数值清洗。

不同省份、不同年份的重点项目文件表头格式差异较大,所有"表头→标准字段"
的规则集中在此文件维护,方便按实际文件迭代调整。
"""

import re
from typing import Any, Dict, List, Optional, Tuple

# 表头别名 → 标准字段(注意:别名用完整词,避免短词误匹配,如用"项目名称"而非"项目")
#
# 单位类列名分组(语义相同者合并,无法区分者留 extra):
# - construction_unit(建设单位/项目法人):项目的建设实施方(含 项目实施主体)
# - project_owner(项目业主/业主单位):项目的业主/出资方,单独一组
# - responsible_unit(责任单位/牵头单位/项目主管单位):行政监管/责任/牵头方
# 三组入库时转入 skp_project_unit(单位表头 + 单位名称),字段见 UNIT_FIELDS
HEADER_ALIASES: Dict[str, Tuple[str, ...]] = {
    'project_name': ('项目名称', '项目名', '工程名称', '工程名', '名称', '项目单位及名称'),
    'construction_unit': ('建设单位', '实施单位', '项目单位', '项目法人', '建设主体', '法人单位','项目实施主体','项目（法人）单位'),
    'project_owner': ('项目业主', '业主单位', '业主'),
    'location': ('建设地点', '项目地点', '建设地址', '所在市县', '所在地', '所在盟市','项目位置','隶属区县','所在省辖市、县区'),
    'total_investment': ('总投资', '项目总投资', '总投资额', '投资额'),
    'annual_investment': ('年度计划投资', '年度投资', '本年度计划投资', '年计划投资', '计划投资', '预计投资', '投资计划', '计划完成投资'),
    'annual_goal': ('年度工作目标', '年度目标', '当年工作目标', '进度目标或新增效益','年度建设目标','年工作目标', '年主要建设任务', '年工作计划', '年目标任务','工程形象进度','计划形象进度'),
    'year_range': ('建设起止年限', '建设起止时间', '建设年限', '建设周期', '起止年限', '计划工期','计划建设期限'),
    'start_year': ('开工年份', '开工时间', '开工年度', '计划开工', '开工'),
    'end_year': ('竣工年份', '竣工时间', '完工年份', '计划竣工', '竣工'),
    'construction_content': ('建设内容', '主要建设内容', '建设规模', '建设规模和内容',
                             '建设规模及内容', '建设规模及主要内容', '拟建设规模', '项目内容', '项目简介'),
    'responsible_unit': ('责任单位', '牵头单位', '项目主管单位', '监管单位', '主管部门', '主管单位', '主责单位'),
    'category': ('项目类别', '产业类别', '项目分类', '项目大类', '行业分类', '项目类型', '项目领域', '领域分类', '所属行业', '行业类别', '九大领域','领域'),
    'project_type': ('建设性质', '建设阶段', '建设批次','项目性质'),
}

# 单位类字段:入库时转入 skp_project_unit(单位表头 + 单位名称),不再写入 skp_project
UNIT_FIELDS: Tuple[str, ...] = ('construction_unit', 'project_owner', 'responsible_unit')

# 金额文本:如 "120.5亿元"、"120000万元"、"120,000"、"总投资:250000万元"
INVESTMENT_RE = re.compile(r'([\d,，]+(?:\.\d+)?)\s*(亿元|万元|亿|万)?')
# 表头中的单位,如 "(亿元)"、"（万元）"
HEADER_UNIT_RE = re.compile(r'[（(]\s*(亿元|万元|亿|万)\s*[)）]')
# 常见非信息列(序号/编号等),不收入 extra_fields
SKIP_EXTRA_HEADERS = ('序号', '编号', '序次', 'no', 'seq')
# 数量词:"万"后跟这些字表示数量而非金额(如 2000万件、5万亩、10万千瓦、1000万立方米)
_AMOUNT_QUANTIFIERS = '件片吨亩米个台套户人支节栋座处头只辆艘架次平千瓦标立'
# 年份文本:如 "2023"、"2023-2025"、"2023年至2025年"
YEAR_RE = re.compile(r'(20\d{2})\s*[年\-/—至~～]{0,3}\s*(20\d{2})?')


# 短别名采用精确匹配,防止 "项目名单/进度目标责任表" 等复合词被误配为表头
_EXACT_ALIASES = frozenset({'名称', '项目名', '工程名', '进度目标'})


def match_field(header: Any) -> Optional[str]:
    """把表头文本映射到标准字段名,映射不到返回 None。

    短别名("名称/项目名/工程名")精确匹配——如 "项目名单" 含子串 "项目名",
    但它是标题而非表头;复合词表头(如 "单位名称")也不应误配。
    """
    matched = match_field_with_alias(header.replace(' ',''))
    return matched[0] if matched else None


def match_field_with_alias(header: Any) -> Optional[Tuple[str, str]]:
    """同 match_field,但连命中的别名原文一起返回(如 "项目法人"),映射不到返回 None。

    别名原文用于单位类列记录来源表头(skp_project_unit.unit_header);
    年投资计划组合表头无对应别名,原文为 ""。
    """
    # 去空格/换行/连字符(合并表头可能生成 "开工-时间"、"建设-地点")
    text = str(header or '').strip().lower().replace('\n', '').replace(' ', '').replace('-', '')
    if not text:
        return None
    # 年投资计划合并表头(父-子)组合判定:父标题含 投资计划/计划投资/年度投资/
    # 资金来源/推进计划,子表头为 主要建设内容/新增生产能力/小计/总投资/形象进度
    # (如 广东 "2021年投资计划-主要建设内容"、宿迁 "2024年计划投资-计划总投资"、
    # "项目资金来源-计划总投资"、"2024年推进计划-整体形象进度")。
    # 父-子拼接后连字符已去除,按词组合判定;须先于通用别名
    # (否则 "投资计划" 子串先命中 annual_investment)
    if re.search(r'(投资计划|计划投资|年度投资|资金来源|推进计划)', text):
        if '主要建设内容' in text or '建设内容' in text:
            return 'annual_goal', ''          # 子=主要建设内容 → 年度建设内容
        if '新增生产' in text or '生产能力' in text:
            return None                       # 子=新增生产能力 → 非金额,留 extra
        if '小计' in text or '合计' in text:
            return 'annual_investment', ''    # 子=小计 → 年度计划投资
        if '总投资' in text:
            # 父=资金来源 → 总投资;父=计划投资类 → 年投资(其"计划总投资"是年度口径)
            return ('total_investment', '') if '资金来源' in text \
                else ('annual_investment', '')
        if '形象' in text:
            return 'annual_goal', ''          # 子=整体形象进度/形象进度 → 年度工作目标
        # 父级模式命中但子表头非上述已知映射目标:去掉 父级词+数字年月 后仍有剩余
        # (即 "父-子" 组合的子表头,如 资金构成明细 省级以上补助/市财政/社会资本、
        # 季度 第一季度)→ 该列留 extra(return None),防止 fall through 通用别名把
        # "2024年计划投资市财政" 等误配 annual_investment(资金明细非年投资,仅
        # "计划总投资"小计列才是);单纯父级表头("2021年计划投资" 去父级词+数字后
        # 为空)residual 为空 → 仍 fall through 通用别名,广东 投资计划列不受影响
        residual = re.sub(r'(投资计划|计划投资|年度投资|资金来源|推进计划)', '', text)
        residual = re.sub(r'[0-9年月日.\-]', '', residual)
        if residual:
            return None
    for field, aliases in HEADER_ALIASES.items():
        for alias in aliases:
            if alias in _EXACT_ALIASES:
                if text == alias:
                    return field, alias
            elif alias in text:
                return field, alias
    return None


def build_header_map(headers: List[Any]) -> Dict[int, str]:
    """表头行 → {列索引: 标准字段名};识别不了的列跳过。"""
    header_map: Dict[int, str] = {}
    for idx, header in enumerate(headers):
        field = match_field(header)
        if field:
            header_map[idx] = field
    return header_map


def clean_amount(text: Any, require_unit: bool = False, unit_scale: str = '') -> float:
    """把金额文本清洗为万元数值;无法解析返回 0.0。

    Args:
        require_unit: True 时只接受带单位(亿/万)的数字,用于行级文本兜底解析,
            避免把行首序号(如 "1.某某项目")误当金额。
        unit_scale: 文本无单位时采用的表头单位(如 "亿元"/"亿"),如 "(亿元)" 列中的裸数字。
    """
    if text is None:
        return 0.0
    s = str(text).strip().replace(',', '').replace('，', '')
    if not s or s in {'-', '/', '—', '—', '--'}:
        return 0.0
    matches = list(INVESTMENT_RE.finditer(s))
    for m in matches:
        unit = m.group(2) or unit_scale
        if require_unit and not unit:
            continue
        # 排除数量词:如 "2000万件/5万亩/128万平方米" 的 "万" 不是金额单位
        after = s[m.end():m.end() + 1]
        if after and after in _AMOUNT_QUANTIFIERS:
            continue
        value = float(m.group(1))
        if unit.startswith('亿'):
            value = value * 10000
        # 规整到 2 位小数,避免浮点误差(如 0.69亿→6899.9999…)触发 MySQL 截断警告
        return round(value, 2)
    return 0.0


def header_unit(header: Any) -> str:
    """从表头文本提取金额单位(如 "(亿元)" → 亿),无则返回空串。"""
    if header is None:
        return ''
    m = HEADER_UNIT_RE.search(str(header).replace('\n', ''))
    return m.group(1) if m else ''


def extract_years(text: Any) -> Tuple[int, int]:
    """从文本/数值中提取起止年份,返回 (start_year, end_year),无则 0。

    支持:
    - 文本: "2023"、"2023-2025"、"2023年至2025年"、"2024年10月"
    - Excel 日期序列号: 45597 → 2024(openpyxl 对日期格式单元格返回数字)
    """
    if text is None:
        return 0, 0
    if isinstance(text, (int, float)) and not isinstance(text, bool):
        year = _excel_serial_to_year(text)
        return (year, 0) if year else (0, 0)
    m = YEAR_RE.search(str(text))
    if not m:
        return 0, 0
    start = int(m.group(1))
    end = int(m.group(2)) if m.group(2) else 0
    return start, end


def _excel_serial_to_year(value: float) -> int:
    """Excel 日期序列号 → 年份(1899-12-30 起的天数,如 45597 → 2024)。

    仅处理日期合理范围(1954-2064 年),避免投资额等普通数字误转。
    """
    if 20000 < value < 60000:
        try:
            from datetime import date, timedelta
            return (date(1899, 12, 30) + timedelta(days=int(value))).year
        except (OverflowError, ValueError):
            return 0
    return 0


def _matched_alias(idx: int, headers: Optional[List[Any]], field: str) -> str:
    """取表头列命中的别名原文(如 "项目法人"),无表头/未命中/与字段不符返回 ""。

    跨页续页复用上一页表头映射时 headers 可能是数据行
    (base_parser.extract_rows_from_table 的 prev_header_map 分支),
    故须校验命中字段与本列字段一致,防把数据文本里的其他单位别名当来源表头。
    """
    if not headers or idx >= len(headers):
        return ''
    matched = match_field_with_alias(headers[idx])
    return matched[1] if matched and matched[0] == field else ''


def map_row(header_map: Dict[int, str], row: List[Any],
            headers: Optional[List[Any]] = None, file_year: int = 0,
            pname_candidates: Optional[List[int]] = None) -> Dict[str, Any]:
    """按 表头列映射 把一行单元格转为项目 dict。

    - 金额列 → 万元数值(裸数字按表头单位换算);表头含显式年份且非文件年份的
      "年计划投资"类列 → 收入 extra(区分当年/往年投资)
    - 年份列(含 year_range) → start_year/end_year
    - 单位类列名并存时非空优先(如 建设单位 与 项目法人 同现),来源表头记入
      `unit_headers`(字段名 → 命中的别名原文,如 {"construction_unit": "项目法人"}),
      供入库转存 skp_project_unit;不改变字段取值
    - 未映射列(表头有文本)→ 收入 extra_fields(文件特有信息)
    - pname_candidates: project_name 候选列(表头修正前后),主列为空时
      (合并单元格只首格有值,如 芜湖/宁夏 名称在左格)回退取第一个合格值
    """
    project: Dict[str, Any] = {}
    for idx, cell in enumerate(row):
        field = header_map.get(idx)
        header_text = str(headers[idx] or '').replace('\n', '').strip() \
            if headers and idx < len(headers) else ''
        if field is None:
            # 未映射列:文件特有信息,如 内蒙古表的"合作方式"(序号列/空表头除外)
            if header_text and header_text.lower() not in SKIP_EXTRA_HEADERS:
                project.setdefault('extra_fields', {})[header_text] = str(cell or '').strip()
            continue
        if field in ('total_investment', 'annual_investment'):
            # 表头显式年份且不是文件年份 → 往年/其他年度投资,入 extra
            m_year = re.search(r'(20\d{2})', header_text)
            if field == 'annual_investment' and m_year and file_year \
                    and int(m_year.group(1)) != file_year:
                if header_text:
                    project.setdefault('extra_fields', {})[header_text] = str(cell or '').strip()
                continue
            unit_scale = header_unit(headers[idx]) if headers and idx < len(headers) else ''
            project[field] = clean_amount(cell, unit_scale=unit_scale)
        elif field == 'year_range':
            start, end = extract_years(cell)
            project['start_year'] = project.get('start_year') or start
            project['end_year'] = project.get('end_year') or end
        elif field == 'start_year':
            start, _ = extract_years(cell)
            if start:
                project['start_year'] = project.get('start_year') or start
        elif field == 'end_year':
            # 单值列(如 Excel 日期序列号 45839 → 2025),年份在 extract_years 第一位
            start, end = extract_years(cell)
            year = end or start
            if year:
                project['end_year'] = project.get('end_year') or year
        else:
            # PDF 表格单元格常含换行(中文跨行),直接去除避免产生间隙
            value = str(cell or '').replace('\n', '').strip()
            # 单位类列名并存(如 建设单位+项目法人)→ 非空优先
            if field not in project or not project[field]:
                project[field] = value
                # 单位类列:记录文件实际命中的别名原文,供入库转存 skp_project_unit
                if value and field in UNIT_FIELDS:
                    alias = _matched_alias(idx, headers, field)
                    if alias:
                        project.setdefault('unit_headers', {})[field] = alias

    # project_name 候选列回退:主列(表头修正/合并单元格)为空时,取候选列
    # (修正前后列)中第一个合格值——非空、非纯数字(序号/金额)、非占位符、含中文
    if not project.get('project_name') and pname_candidates:
        for cand in pname_candidates:
            if cand >= len(row):
                continue
            v = str(row[cand] or '').replace('\n', '').strip()
            if not v or re.fullmatch(r'[\d,，.．\s]+', v):
                continue  # 空或纯数字(序号/金额)
            if re.fullmatch(r'[—－\s-]+', v):
                continue  # 占位符("——")
            if not re.search(r'[一-鿿]', v):
                continue  # 无中文 → 非项目名
            project['project_name'] = v
            break
    return project


def extract_file_year(file_path: str) -> int:
    """从文件名/路径中提取文件年份(取最后一个年份,离文件最近),无则 0。"""
    years = re.findall(r'(20\d{2})', str(file_path).split('\\')[-1]) \
        or re.findall(r'(20\d{2})', str(file_path))
    return int(years[-1]) if years else 0
