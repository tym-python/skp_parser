"""解析器抽象基类:统一各文件类型解析器的接口与公共逻辑。"""

import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from parser.field_mapping import build_header_map, clean_amount, extract_years, map_row
from util.log_util import get_logger

logger = get_logger(__file__)

# 分类标题名单词(行业/领域类):从历史解析数据的分类词频统计 + 常见分类命名整理。
# 强词:命中即判为分类(如 "高速公路项目"/"中型水利工程");
# 弱词:命中且文本较短才判为分类(如 "光伏发电项目"),避免 "光伏组件制造项目" 误判。
CATEGORY_STRONG_WORDS = (
    # 纯行业大类词:几乎不会出现在具体项目名中
    '基础设施', '基础产业', '重大产业', '产业发展', '产业工程', '产业转型',
    '制造业', '服务业', '现代服务', '交通', '民生', '社会事业', '社会民生',
    '市政', '城建', '战略性新兴', '传统产业',
)
CATEGORY_WEAK_WORDS = (
    # 弱词命中且文本 ≤6 字才判为分类。
    # 具体设施词(公路/铁路/高速/水利/光伏等)常出现在项目名中
    # (如 "G7611西昌至香格里拉高速公路 凉山州"),长文本不判分类
    '公路', '高速公路', '铁路', '轨道', '机场', '港口', '航运', '能源',
    '电力', '电网', '水利', '生态', '环保', '物流', '信息', '科技', '创新',
    '数字', '文化', '旅游', '医疗', '教育', '卫生', '体育', '电子', '汽车',
    '装备', '化工', '医药', '生物', '农业', '工业', '食品', '轻工', '大数据',
    '智能制造', '光伏', '风电', '水电', '火电', '核电', '新能源', '环境治理',
    '绿化', '城市更新', '保障房', '棚改', '老旧小区', '供水', '排水', '燃气',
    '供热', '休闲', '康养', '应急', '安全', '资源', '粮食', '冷链', '革命',
    '新材料', '房地产', '领域', '类','国铁干线', '航道整治','天然气发电',
    '城市建设','城市道路','国省','航空', '体系', '类','油气开发','风力发电',
)
CATEGORY_Supplement_WORDS = (
    # 部分被识别成项目的分类，全等
    '林业', '城市更新改造（棚户区改造）', '城市轨道交通（含地铁、轻轨、市郊铁路等）', '数字化（大数据、信息化建设等）', '城镇基础设施（含新型城镇化建设）',
    '新型基础设施（含信息、融合、创新基础设施等）', '教育、文化、体育及社会服务', '生态修复、环境整治（含流域治理）','种植业','草产业','城镇污水垃圾处理',
    '港口、码头、航运及航电枢纽','综合交通枢纽及一体化设施项目', '水资源保障建设项目', '高性能船舶与海洋工程装备项目','普及高水平公共教育建设项目',
    '一产项目','二产项目','三产项目',
)
PROJECT_TYPE_WORDS = (
    '竣工投产', '新开工', '新建', '续建', '在建', '投产', '预备', '储备', '前期', '收尾', '竣工', '计划开工'
)
PT = "|".join(map(re.escape, PROJECT_TYPE_WORDS))

# 兜底分支(序号+分类标题)护栏参数:update_category_context 的兜底把"去序号、
# 去括号统计后"的整段文本当分类名,但整段实为 项目名称+建设内容 拼接的业务数据行
# (如 温州 882 "878 科技创新强基领域 全省海上风电…（白马湖实验室） 项目拟选址…
# （5个桩基式…）…"——括号统计门控被建设内容里的 "（5个桩基式…" 放行)时,
# 会把 90 余字的名称+内容整体误设为分类,污染后续全部项目的 category。护栏:
# 长度上限(真实分类名极少超过该长度;项目名+内容拼接必超长)+ 句子标点限定
# (真实分类名无句读——顿号"、"是枚举、可出现在分类名中,不作限定;名称+内容
# 拼接必含 ，。； 等句读)。
FALLBACK_CATEGORY_MAX_LEN = 24
FALLBACK_CATEGORY_PUNCT_RE = re.compile(r'[，。；;:：,]')

# 城市/地区分组行的名称长度上限(去单元格内空格后统计,如 "南宁市"3、"防城港市"4、
# "乌鲁木齐市"5、正文对齐变体 "南 宁 市"→3):市/区 结尾须短名才认作分组行——
# "汉中综合保税区"、"…灌区/…新校区/…园区" 等真项目名以"市/区"结尾但更长,不误弃
GROUP_CITY_MAX_LEN = 5
# 单行表头(极简清单,header_map ≤1 列)分组行的机构/区划后缀:
# 不含 集团/公司/学院/研究院/中心 等真项目名单格常见结尾(如 "xx公司"/"xx研究中心")
GROUP_SINGLE_SUFFIX_RE = re.compile(
    r'(人民政府|政府|厅|局|委|办|管委会|县|州|盟|省|联合会|农业科学院|广播电视台)$')
GROUP_CITY_SUFFIX_RE = re.compile(r'[市区]$')
# 多列映射表分组的机构名单格后缀(≤14 字,防长文本误判;不含 学院/医院/学校/研究院,
# "xx商务中心" 等真项目名由业务字段判断识别)
GROUP_ORG_SUFFIX_RE = re.compile(
    r'(人民政府|政府|厅|局|委|办|管委会|集团|公司|联合会|农业科学院|广播电视台)$')
# 机构后缀中的 "厅" 与场所类项目名冲突:以 餐厅/展厅/音乐厅/办事大厅 等结尾的是
# 真项目(如 "骏升新能源汽车城市展厅"、"金拱门食品有限公司未来智慧餐厅"),
# 不按机构分组识别。机构名("自治区教育厅" 等)不命中该词表。
GROUP_VENUE_TAIL_RE = re.compile(
    r'(餐厅|展厅|音乐厅|宴会厅|舞厅|客厅|饭厅|茶厅|大厅|礼堂)$')
# 正文排版行识别(招商手册/项目简介正文,如 广西(第一批).xlsx 目录之后的正文区域):
# 正文为"单列多行"排版,每行/每段独立成行,无序号、无业务列结构——字段标签行
# (项目名称：/项目属地：/联 系 人： 等,项目名称列不会以这些标签开头)、
# 超长段落/续段行。真数据行(名称+建设内容等多文本格)不受影响。
PROSE_LABEL_RE = re.compile(
    r'^(项目名称|项目属地|项目建设地点|项目类别|项目概述|项目总投资|'
    r'项目经济效益|项目已具备|项目合作单位|产业概况|产业背景|产业政策|'
    r'投资要素|合作方式|联\s*系\s*人|联系电话|联系方式|电子邮箱|联系地址|'
    r'邮\s*编|项目有效期)\s*[:：]')
# 单文本格正文行的最小长度:超过即正文段落(项目名不会长到该长度)
PROSE_CELL_MAX_LEN = 150
# 备注/注记行(表尾/页眉说明文字,如 "备注：标"★"的为2025年重大项目。"、
# "注：预备项目是指…"):整行是说明,不产生项目、不参与分类。识别整行文本行首
# 的 备注/注/附注/注释/说明/特别说明/注记 + 冒号(容忍空格,如 "备 注:")
NOTE_LABEL_RE = re.compile(
    r'^(备\s*注|附\s*注|注释|特别说明|注记|说明|注)\s*[:：]')
# 清单概况/总结句特征(如 "重大前期项目92个,总投资494亿元。其中,政府投资项目
# 54个,总投资102.4亿元;社会投资项目38个,总投资391.6亿元。"、渝北 2025
# "项目总数246个（新开工73个、续建73个、完工62个、重大前期38个）。"):整行叙述性概述。
# 条件1 数量短语("N个/项/件")后跟 句子标点/顿号/右括号/其中/总投资/亿元 或行尾;
# 条件2 句子成分词(，。；; 其中/总投资/亿元/万元)——条件2 拦截纯列举的项目名
# ("…年产300万个轴承、500万个齿轮项目" 无句读/总额词,不误伤)
SUMMARY_QTY_RE = re.compile(
    r'\d+\s*(?:个|项|件)(?=[，。；;,，、)）]|其中|总投资|亿元|万元|$)')
SUMMARY_CLAUSE_RE = re.compile(r'[，。；;,，]|其中|总投资|亿元|万元')


class BaseParser(ABC):
    """各文件类型解析器必须实现 parse(file_path),返回项目 dict 列表。"""

    SUPPORTED_EXT: Tuple[str, ...] = ()

    def __init__(self) -> None:
        # 分类声明校验:分类标题声明 "（共N项）" 与实际解析条数的对比(解析检验手段)
        self.declared_categories: List[Tuple[str, int]] = []

    def apply_category(self, text: str, context: Dict[str, str], type:str=None) -> bool:
        """更新分类上下文并收集分类标题的声明项数("（共N项）")。

        同一 (分类, 声明数) 去重:PDF 每页顶部常重复打印分类标题。
        超长分类名(>50 字,如 省份汇总说明文本)不记录声明。

        补充type，不同情况下的apply_category，有不同情况
        joined_non_empty：不是业务数据，xlsx。_is_business_data_row，已清洗。
        """
        if not self.update_category_context(text, context,type):
            return False
        declared = context.get('declared_count')
        if declared:
            cat = context.get('category', '')
            if len(cat) > 50:
                return True  # 汇总说明文本(如 "第一批-.0 河北省 703个…"),不记录
            item = (cat, int(declared))
            if item not in self.declared_categories:
                self.declared_categories.append(item)
        return True

    @abstractmethod
    def parse(self, file_path: str) -> List[Dict[str, Any]]:
        """解析单个文件,返回项目记录列表(字段见 field_mapping.map_row)。"""

    # ---------- 公共逻辑 ----------

    @staticmethod
    def find_header(rows: List[List[Any]], max_scan: int = 6
                    ) -> Tuple[Optional[Dict[int, str]], int]:
        """在表格行中定位表头行,返回 (列映射, 表头行索引)。

        两遍扫描:
        1. 优先命中 ≥2 字段的行 = 完整表头(备注行如 "注:项目名称标注▲…"
           仅命中 project_name 不构成表头);
        2. 兜底:仅命中 project_name 且非"单格长文本"行(如 山东"序号|项目名称"
           两列表;单格 >30 字的备注行排除)。
        """
        for idx, row in enumerate(rows[:max_scan]):
            header_map = build_header_map(row)
            if len(header_map) >= 2:
                return header_map, idx
        for idx, row in enumerate(rows[:max_scan]):
            header_map = build_header_map(row)
            non_empty = [str(c).strip() for c in row if c is not None and str(c).strip()]
            if len(header_map) == 1 and 'project_name' in header_map.values() \
                    and not (len(non_empty) == 1 and len(non_empty[0]) > 30):
                return header_map, idx
        return None, -1

    # 无表头清单表:数据行首列序号形态(纯数字,容忍 "（1）"/"1、"/"1." 等包裹)
    POSITIONAL_SEQ_RE = re.compile(r'^[（(]?\s*\d+\s*[)）]?[、.．]?\s*$')
    # 无表头清单表:表名行特征(含 项目/工程 + 清单类词,如 "2022年市级重点项目名单（建设类）")
    POSITIONAL_TITLE_RE = re.compile(r'(?:项目|工程)[^（()）\n]{0,16}?(?:名单|清单|列表|目录|总表)')

    @staticmethod
    def _positional_header(rows: List[List[Any]]) -> Optional[Tuple[Dict[int, str], int]]:
        """无表头项目清单表的位置式兜底映射(find_header 未命中且无 prev_header_map 时调用)。

        场景:通知文件文末表格,首行为表名(如 "2022年市级重点项目名单（建设类）")
        或直接分组/分类行,无列头;数据行按非空列顺序 = 序号/项目名称/建设规模
        (烟台 2022、濮阳 2023 等)。列角色:
        - 首列序号(POSITIONAL_SEQ_RE)→ 不映射;
        - 第 2 个非空列 → project_name;第 3 个非空列 → construction_content(建设规模)。
        护栏:须有 ≥5 行 "数字首列 + 中文名称" 数据行,否则返回 None(保持整表跳过的
        原行为,抄送/空模板/统计表等自然排除)。
        返回 (header_map, 表名行索引;无表名行为 -1,此时数据从第 0 行起)。
        """
        title_idx = -1
        for idx in range(min(3, len(rows))):
            texts = [str(c).strip() for c in rows[idx]
                     if c is not None and str(c).strip() and not BaseParser._is_number(c)
                     and not BaseParser._is_placeholder(c)]
            if len(texts) == 1 and BaseParser.POSITIONAL_TITLE_RE.search(texts[0]):
                title_idx = idx
                break
        name_col = scale_col = None
        data_cnt = 0
        for row in rows[title_idx + 1:title_idx+21]:
            cells = [str(c or '').strip() for c in row]
            if not cells or not BaseParser.POSITIONAL_SEQ_RE.match(cells[0]):
                continue
            cols = [i for i in range(1, len(cells))
                    if cells[i] and not BaseParser._is_number(cells[i])
                    and not BaseParser._is_placeholder(cells[i])]
            if not cols:  # 非数字、占位符列下标
                continue
            if name_col is None:
                if not re.search(r'[一-鿿]', cells[cols[0]]):  # 汉字匹配
                    continue
                name_col = cols[0]
            elif scale_col is None and len(cols) >= 2:
                scale_col = cols[1]
            data_cnt += 1
        if data_cnt < 5 or name_col is None:
            return None
        header_map: Dict[int, str] = {name_col: 'project_name'}
        if scale_col is not None:
            header_map[scale_col] = 'construction_content'
        return header_map, title_idx

    @staticmethod
    def skip_summary_row(row: List[Any]) -> bool:
        """跳过合计/总计/小计/全区等汇总行。"""
        first = str(row[0] or '').strip() if row else ''
        return any(kw in first for kw in ('合计', '总计', '小计', '全区'))

    @staticmethod
    def _row_has_number(cells: List[Any]) -> bool:
        """行内是否存在纯数字单元格(序号/数量/金额,如 "206"、"1,584,946.56")。"""
        return any(c is not None and str(c).strip()
                   and BaseParser._is_number(str(c).strip()) for c in cells)

    @staticmethod
    def is_group_row(cells: List[Any]) -> bool:
        """判断是否为城市/地区/责任单位分组行:单格行(排数字/占位后唯一文本)且:

        - 以 县/州/盟/省 结尾(如 "东兴县""凉山州"),及 区域级词(市直/区直,
          如 贵港 "市直|97|金额")
        - 以 市/区 结尾且**短名称**(≤ GROUP_CITY_MAX_LEN 去空格)且**行内无任何
          数字单元格**:城市分组行(南宁市/南 宁 市)无序号无金额;编号清单中的
          短名行是真项目(如 福州 责任表 "963|君澜府小区"、"206|汉中综合保税区"、
          "…灌区" 等,名称外有 序号/金额 数字列)——只有长度限制会误弃 小区/园区/
          校区 等 4-5 字真项目名(用户库内审计已见大量此类)
        - 机构名结尾(如 广西责任表 "自治区教育厅|12|金额" 分组行,
          机构名在序号列且 ≤14 字——数据行项目名不单格带机构尾)
        """
        non_empty = [str(c).strip() for c in cells if c is not None and str(c).strip() and not BaseParser._is_number(c) and not BaseParser._is_placeholder(c)]
        if len(non_empty) != 1:
            return False
        v = non_empty[0]
        # 去单元格内对齐空格(如 广西正文 "南 宁 市"),再做后缀/长度判断
        v_c = re.sub(r'\s+', '', v)
        if re.match(r'^.+[县州盟省]$', v_c) or v_c in ('市直', '区直'):
            return True
        if (len(v_c) <= GROUP_CITY_MAX_LEN and GROUP_CITY_SUFFIX_RE.search(v_c)):
            return True
        # 机构名单格分组行(如 责任单位 "自治区教育厅");≤14 字防长文本误判。
        # 不含 中心/学院/医院/学校/研究院 结尾(项目名常见,如 "xx商务中心" 是
        # 真项目名,由业务字段判断识别);漏网行在入库时备注标记供人工核查
        # "…餐厅/展厅/办事大厅" 等场所名尾"厅"是真项目(GROUP_VENUE_TAIL_RE),不算机构
        if len(v) <= 14 and GROUP_ORG_SUFFIX_RE.search(v):
            return not bool(GROUP_VENUE_TAIL_RE.search(v_c))
        return False

    @staticmethod
    def is_group_row_minimal(cells: List[Any],
                             allow_city: bool = True) -> bool:
        """极简清单(单行表头,header_map ≤1 列 = 纯 序号+名称/目录,如 汉中/广西目录)
        的窄化分组行识别。

        这类表无 责任单位/计数 分组行形态,但城市/地区分组行仍会以单格行出现
        (如 广西目录 "南宁市"、正文对齐变体 "南 宁 市")——多列分组检测被跳过时
        它们会被当项目入库。此处仅对**短单格名**收窄识别(真项目名单格出现,
        如 汉中 "206|汉中综合保税区" 尾"区"):
        - 区划后缀 县/州/盟/省 与 区域级词(市直/区直):任意长度
        - 机构后缀 人民政府/政府/厅/局/委/办/管委会(不含 集团/公司/学院/研究院)
        - 市/区 后缀:仅短名称(≤ GROUP_CITY_MAX_LEN 去空格)且行内无数字单元格
          (编号清单中 "963|君澜府小区" 是真项目);allow_city=False(整个 sheet
          无任何编号行,纯名称单列清单)时该分支关闭——此类 sheet 不存在城市分组行,
          "xx小区/园区" 短名一律保留
        """
        non_empty = [str(c).strip() for c in cells if c is not None and str(c).strip() and not BaseParser._is_number(c) and not BaseParser._is_placeholder(c)]
        if len(non_empty) != 1:
            return False
        v_c = re.sub(r'\s+', '', non_empty[0])
        if re.match(r'^.+[县州盟省]$', v_c) or v_c in ('市直', '区直'):
            return True
        if (allow_city and len(v_c) <= GROUP_CITY_MAX_LEN
                and GROUP_CITY_SUFFIX_RE.search(v_c)):
            return True
        # 机构/区划后缀分组行;"…餐厅/展厅" 等场所名尾"厅"是真项目,不算机构
        if GROUP_SINGLE_SUFFIX_RE.search(v_c):
            return not bool(GROUP_VENUE_TAIL_RE.search(v_c))
        return False

    @staticmethod
    def _is_overview_sentence(text: str) -> bool:
        """清单概况/总结句判定(文本级):整行叙述性概述,如 "重大前期项目92个,
        总投资494亿元。其中,政府投资项目54个,总投资102.4亿元;社会投资项目38个,
        总投资391.6亿元。"(奉节 "2023年续建项目共85个,总投资338…" 同理)。

        特征:去空白后长度 >20 且同时满足
        1. 数量短语 "N个/项/件" 后跟 句子标点/其中/总投资/亿元/万元 或位于行尾
           (顿号不算——"…300万个、…" 是项目名常见列举,防误伤)
        2. 含句子成分词:，。；;、逗号 或 其中/总投资/亿元/万元
        """
        t = re.sub(r'\s+', '', str(text))
        if len(t) <= 20:
            return False
        if SUMMARY_QTY_RE.search(t) and SUMMARY_CLAUSE_RE.search(t):
            return True
        # 括号内数量枚举式总结(渝北 2025 "项目总数246个（新开工73个、续建73个、
        # 完工62个、重大前期38个）"):以 "N个（" 开头前缀、括号内 ≥2 个顿号分隔的
        # "N个/项" 段且以 右括号 收尾——无 句读/其中/总额词 也判概况句
        m_paren = re.match(r'^.{0,16}?\d+\s*(?:个|项|件)?\s*[（(].*[）)]$', t)
        if m_paren:
            inner = re.search(r'[（(]([^（()）]*)[）)]$', t).group(1)
            if len(re.findall(r'\d+\s*(?:个|项|件)', inner)) >= 2:
                return True
        return False

    @staticmethod
    def is_prose_row(cells: List[Any]) -> bool:
        """装饰行(非项目)统一判定,合并 正文排版行/备注说明行/清单概况总结句:
        - 正文排版行:招商手册/项目简介正文(如 广西(第一批) 目录后正文区域按单列
          多行排版,每行/每段独立成行):单文本格且 以正文标签开头(项目名称：/
          项目属地：/项目概述：/联 系 人： 等 PROSE_LABEL)或 ≥ PROSE_CELL_MAX_LEN
        - 备注说明行:整行文本行首 = 备注/注/附注/注释/说明 + 冒号(NOTE_LABEL_RE)
        - 清单概况/总结句:单文本格的整句概述(_is_overview_sentence,如 "重大前期
          项目92个,总投资494亿元。其中,政府投资项目54个…")
        约束:正文/概况仅对**单文本格**行判定(真数据行 = 名称+建设内容等多文本格,
        不受影响;备注行在多格时行首仍是标签则命中——数据行行首是项目名,不误伤)。
        命中 → 不产生项目、不参与分组/分类(xlsx/xls 循环与 pdf/docx 表格共用)。
        """
        texts = [str(c).strip() for c in cells if c is not None and str(c).strip()
                 and not BaseParser._is_number(c) and not BaseParser._is_placeholder(c)]
        if not texts:
            return False
        joined = " ".join(texts)
        if BaseParser.is_note_text(joined):
            return True
        if len(texts) != 1:
            return False
        v = re.sub(r'\s+', ' ', texts[0])  # 折叠连续空白(如 "联  系  人："),统一标签匹配
        if PROSE_LABEL_RE.match(v):
            return True
        if len(v) >= PROSE_CELL_MAX_LEN:
            return True
        return BaseParser._is_overview_sentence(v)

    @staticmethod
    def is_note_text(text: str) -> bool:
        """备注/注记说明行判定(整行文本行首 = 备注/注/附注/注释/说明 + 冒号,
        如 "备注：标"★"的为2025年重大项目。"、"注：预备项目是指…")。

        表尾/页眉说明文字整行被当项目入库(重庆/开州/甘孜/绵阳等 13 条):
        不产生项目、不参与分组/分类。仅认行首标签,数据行(名称+建设内容,
        建设内容列可能含 "备注：…" 文字)行首是项目名,不受影响。
        """
        return bool(NOTE_LABEL_RE.match(re.sub(r'\s+', ' ', str(text).strip())))

    @staticmethod
    def _unwrap_cat_bracket(text: str) -> str:
        """分类行前缀归一:去掉 【】 强调包装(与无括号等价)——贵阳 2026
        "【预备】(1个)" 等同 "预备(1个)";"【一、交通】" 等同 "一、交通"。
        """
        s = str(text)
        m = re.match(r'^【([^】]{1,24})】', s)
        if m:
            return m.group(1) + s[m.end():]
        return s

    @staticmethod
    def is_decor_text(text: str) -> bool:
        """文本级装饰行统一判定(无 cells 上下文场景,如 表头前说明行/文本行):
        备注/注记(NOTE_LABEL)、正文标签(PROSE_LABEL)、清单概况/总数总结句
        (_is_overview_sentence,如 "项目总数246个(新开工73个、续建73个…)"、
        奉节 "重大前期项目92个,总投资494亿元。其中…")→ 应跳过且不设任何 category。
        """
        collapsed = re.sub(r'\s+', ' ', str(text).strip())
        return bool(PROSE_LABEL_RE.match(collapsed)
                    or NOTE_LABEL_RE.match(collapsed)
                    or BaseParser._is_overview_sentence(collapsed))

    @staticmethod
    def is_group_header_row(cells: List[Any], header_map: Dict[int, str],
                            normal_cols: int = 0) -> str:
        """责任单位/地区分组行(如 "['','南宁市人民政府','16','',...,'1528601.56']")。

        特征(全满足):
        1. 首列(序号列)为空
        2. 名称列(项目名称列)非空且含中文(纯数字列不可能是分组名)
        3. 非空列数显著少于普遍数据行(≤ max(2, normal_cols-2))
        4. 计数特征:含 "N项" 或 纯小整数(1-999,无小数点,如 "16")
        返回分类词,非分组行返回空。
        """
        if not cells or str(cells[0] or '').strip():
            return ''
        non_empty = [str(c).strip() for c in cells if c is not None and str(c).strip() and not BaseParser._is_number(c) and not BaseParser._is_placeholder(c)]
        if len(non_empty) <= 1:
            return ''  # 单格行走 classify_single_row / is_group_row
        name_col = next((col for col, field in header_map.items() if field == 'project_name'), None)
        if name_col is None or name_col >= len(cells):
            return ''
        name = str(cells[name_col] or '').strip()
        if not name or not re.search(r'[一-鿿]', name):
            return ''  # 名称列为空或纯数字 → 非分组行
        # 名称列需以机构后缀结尾(责任单位分块行,如 "南宁市人民政府"/"区水利局";
        # "…快充站建设工程" 等数据行不误判)
        if not re.search(r'(人民政府|政府|市|区|县|厅|局|委|办|管委会|集团|公司|学院|研究院)$',
                         name):
            return ''
        if normal_cols > 0 and len(non_empty) > max(2, normal_cols - 2):
            return ''  # 非空列数不显著少于普遍数据行 → 数据行
        has_count = any(BaseParser._is_count_value(c) for c in non_empty)
        if not has_count:
            return ''
        return name[:128]

    @staticmethod
    def _is_count_value(c: str) -> bool:
        """计数特征:"N项" 或 纯小整数(1-999,含 float 形式如 "4.0"/"16.0")。"""
        if re.match(r'^\d+\s*[项|个]$', c):
            return True
        try:
            f = float(c)
            return f.is_integer() and 1 <= f <= 999
        except ValueError:
            return False

    @staticmethod
    def _fix_merged_header(header_map: Dict[int, str], merged_ranges: List[tuple],
                           header_idx: int) -> Dict[int, str]:
        """合并表头检查:表头行横向合并覆盖 project_name 列
        (如 "项目名称" 合并跨 序号+名称 两列)→ project_name 右移一列。

        merged_ranges: 0-based (rlo, rhi, clo, chi) 列表。
        """
        pname_col = next((c for c, f in header_map.items() if f == 'project_name'), None)
        if pname_col is None:
            return header_map
        for rlo, rhi, clo, chi in merged_ranges:
            if chi > clo and rlo <= header_idx <= rhi \
                    and clo <= pname_col <= chi and chi > pname_col:
                header_map.pop(pname_col)
                header_map[pname_col + 1] = 'project_name'
                logger.info(f"合并表头修正: project_name 列 {pname_col} → {pname_col + 1}")
                break
        return header_map

    @staticmethod
    def _fix_numeric_project_col(header_map: Dict[int, str], all_rows: List[List[Any]],
                                 header_idx: int) -> Dict[int, str]:
        """数字列检测兜底:project_name 列数据 ≥80% 为纯数字(表头与数据列错位)→ 右移一列。

        覆盖 云南"四个一百" 等无合并单元格的文件:表头"项目名称"在列0,
        但数据列0为序号("1.0"/"20.0")、真实项目名在列1(表头为空)。
        """
        pname_col = next((c for c, f in header_map.items() if f == 'project_name'), None)
        if pname_col is None:
            return header_map
        total = 0
        numeric = 0
        for cells in all_rows[header_idx + 1:]:
            if pname_col >= len(cells):
                continue
            v = str(cells[pname_col] or '').strip()
            if not v:
                continue
            total += 1
            if re.fullmatch(r'[\d.]+', v):
                numeric += 1
        if total < 3 or numeric / total < 0.8:
            return header_map
        next_col = pname_col + 1
        has_text = any(
            next_col < len(c) and str(c[next_col] or '').strip()
            and not re.fullmatch(r'[\d.]+', str(c[next_col]).strip())
            for c in all_rows[header_idx + 1:])
        if not has_text:
            return header_map
        header_map.pop(pname_col)
        header_map[next_col] = 'project_name'
        logger.info(f"数字列修正: project_name 列 {pname_col}(数据纯数字) → {next_col}")
        return header_map

    @staticmethod
    def _fix_special_project_col(header_map: Dict[int, str], all_rows: List[List[Any]],
                                 header_idx: int) -> Dict[int, str]:
        """部分文件，项目名称列占据两列。
        2025年重点项目\10安徽省2025年重点项目清单\芜湖市2025年\芜重建财〔2025〕24号附件—2025年市政府投资计划分解表.xlsx
        header中project左右两边的None，如果对于列内容是有效文字+None组合，两列取有效列为project。
        """

        return header_map

    @staticmethod
    def _normal_cols(rows: List[List[Any]], header_map:Dict[int, str]) -> int:
        """统计 sheet 普遍数据行的非空且非数字列数(众数),作为分组行判定的列数基准。"""
        from collections import Counter
        counts = Counter()
        for cells in rows:
            n = len([cells[i] for i in header_map
                     if cells[i] is not None
                     and str(cells[i]).strip()
                     and not BaseParser._is_number(cells[i])
                     and not BaseParser._is_placeholder(cells[i])])
            if n >= 2:
                counts[n] += 1
        if not counts:
            return 3
        return counts.most_common(1)[0][0]

    @staticmethod
    def group_type_title(cells: List[Any],
                         header_map: Optional[Dict[int, str]] = None) -> str:
        """建设性质标题行识别(合并原 is_build_type_row 与 xlsx_parser._group_type_title),
        返回规范化性质词,非标题行返回空串。

        两种形态:
        1. 单格纯词(任意表,如 安徽 "续建"/"计划开工" 单格标题行):
           整行排数字/占位后唯一文本,且 = 性质词(不含 "项目" 后缀)
        2. 性质分组行(仅多列映射表传 header_map 时,如 贵港 "计划新开工项目|19|金额",
           文件无建设性质列,性质由分组行提供):首列(序号列)空 + 项目名称列
           匹配 "性质词+项目"(全词匹配)——映射 计划新开工→新开工、
           竣工投产或部分竣工投产→竣工投产
        严格全词匹配 + 首列空(形态2),不误伤项目名(项目名不会恰好等于这些词)。
        """
        non_empty = [str(c).strip() for c in cells if c is not None and str(c).strip() and not BaseParser._is_number(c) and not BaseParser._is_placeholder(c)]
        # 形态1:单格性质词标题行
        if len(non_empty) == 1:
            value = non_empty[0]
            # 较完善的type匹配
            mt = re.match(rf'^[\d一二三四五六七八九十]*[、.．\s]*(?P<pt>{PT})(?:项目)?'
                                rf'(?:\s*[（(]\s*\d+\s*(?:个|项|件)?\s*[)）]|\s*\d+\s*(?:个|项|件)?)?'
                                rf'\s*$', value)
            if mt:
                return mt.group('pt')
        # 形态2:性质分组行(序号列空 + 名称列 "性质词+项目")
        if header_map is not None and cells and not str(cells[0] or '').strip():
            name_col = next((c for c, f in header_map.items() if f == 'project_name'), None)
            if name_col is None or name_col >= len(cells):
                return ''
            name = str(cells[name_col] or '').strip()
            m = re.match(
                rf'^({PT}|计划新开工|竣工投产或部分竣工投产)项目?$', name)
            if not m:
                return ''
            word = m.group(1)
            return {'计划新开工': '新开工',
                    '竣工投产或部分竣工投产': '竣工投产'}.get(word, word)
        return ''

    @staticmethod
    def classify_single_row(value: str, context: Dict[str, str]) -> bool:
        """单格分类行识别(安徽/广西等"分类独立一行"结构),更新上下文并返回是否分类行。

        支持:
        - 城市/序号标题: "1、合肥市(915个)" / "一、工业(321项)" → category
        - 建设性质: "续建项目(597个)" / "计划开工项目(318个)" → project_type
        - 其他短分类文本(≤12 字)→ category
        """
        value = value.strip()
        if not value:
            return False
        # 【】强调包装去壳(如 "【预备】(1个)" 等同 "预备(1个)",贵阳 2026)
        value = BaseParser._unwrap_cat_bracket(value)
        # 序号+分类: "1、合肥市(915个)" / "一、工业(321项)" / "一、创新能力提升项目26个"
        m = re.match(r'^[\d一二三四五六七八九十]+[、.．]\s*(.+)$', value)
        if m:
            cat = re.sub(r'[（(]\d+\s*(?:个|项)[)）].*$', '', m.group(1)).strip()
            cat = re.sub(r'\d+\s*(?:个|项|件)\s*$', '', cat).strip()  # 去行尾数字量词
            if cat and (len(cat) <= 12 or BaseParser._looks_like_category(cat)):
                BaseParser._set_category(context, cat)
                return True
            if cat:
                # 序号+长文本(如 "2.城区公交站台升级改造:拟对…" 项目内容续行)→ 跳过不产生项目
                return True
        # 建设性质: "续建项目(597个)" / "计划开工项目(318个)"
        m2 = re.match(rf'^[\d一二三四五六七八九十]*[、.．\s]*(?P<pt>{PT})(?:项目)?'
                                rf'(?:\s*[（(]\s*\d+\s*(?:个|项|件)?\s*[)）]|\s*\d+\s*(?:个|项|件)?)?'
                                rf'\s*$', value)
        if m2:
            context['project_type'] = m2.group('pt')
            return True
        # 机构名单格行(如 "区水利局"/"宏畅交通集团",责任单位分组)→ 跳过,不产生项目;
        # "…餐厅/展厅/办事大厅" 等场所名尾"厅"是真项目,不按机构处理
        if (re.search(r'(人民政府|政府|市|区|县|厅|局|委|办|管委会|集团|公司|学院|研究院)$',
                      value)
                and not GROUP_VENUE_TAIL_RE.search(re.sub(r'\s+', '', value))):
            return True
        # 罗马数字序号 = 三级分类(如 "Ⅰ、机场（9项）"):追加到当前二级分类下
        # 构成 "一级-二级-三级"(与 update_category_context 的罗马分支一致)
        m_roman = re.match(r'^[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+[、.．]\s*(.+)$', value)
        if m_roman:
            cat = re.sub(r'[（(]\d+\s*(?:个|项)[)）].*$', '', m_roman.group(1)).strip()
            cat = re.sub(r'\d+\s*(?:个|项|件)\s*$', '', cat).strip()
            if cat and len(cat) <= 16:
                base = context.get('dash_base') or context.get('category', '')
                context['category'] = f"{base}-{cat}"[:128] if base else cat[:128]
            return True  # 跳过不产生项目
        # "——" 子分类单格行(如 "——铁路")→ 三级分类,挂到当前分类下
        m_dash_cell = re.match(r'^[—－-]{2,}\s*(.+)$', value)
        if m_dash_cell:
            sub = BaseParser._clean_category_name(m_dash_cell.group(1))
            if sub and len(sub) <= 16:
                base = context.get('dash_base') or context.get('category', '')
                context['category'] = f"{base}-{sub}"[:128] if base else sub[:128]
            return True
        # 括号序号二级标题(如 "（一）交通（104项）" / "（一）交通"):追加到当前
        # 一级分类下("基础设施"+"交通" → "基础设施-交通"),同级 "（二）" 替换最后一段;
        # 与 update_category_context 的 m2 语义一致(替代 _set_category 替换,不丢一级)
        m_seq = re.match(r'^[（(][一二三四五六七八九十ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+[)）]\s*(.+)$', value)
        if m_seq:
            raw_sub = m_seq.group(1).strip()
            # 统计后缀(量词 "2个" 或 括号整数 "（10）")→ 直接认作分类标题;
            # 无统计后缀需命中分类名单词(防 "（三）李家岩水库" 数据行误判)
            has_stat = bool(re.search(r'\d+\s*(?:个|项|件)\s*$'
                                      r'|[（(]\s*共?\s*\d+\s*(?:项|个|件)?\s*[)）]\s*$',
                                      raw_sub))
            sub = re.sub(r'[（(]\d+\s*(?:个|项)[)）].*$', '', raw_sub).strip()
            sub = re.sub(r'\d+\s*(?:个|项|件)\s*$', '', sub).strip()
            if has_stat or (sub and BaseParser._looks_like_category(sub)):
                if sub:
                    base = context.get('dash_base') or context.get('category', '')
                    if '-' in base:
                        context['category'] = f"{base.rsplit('-', 1)[0]}-{sub}"[:128]
                    elif base:
                        context['category'] = f"{base}-{sub}"[:128]
                    else:
                        context['category'] = sub[:128]
                    context['dash_base'] = context['category']
                return True  # 跳过不产生项目(无分类名时仅跳过)
            return False  # 无统计且非分类词 → 数据行(如 "（三）李家岩水库")
        # 其他分类文本:命中分类名单词(如 "基础设施工程"/"中型水利工程")
        if BaseParser._looks_like_category(value):
            BaseParser._set_category(context, value)
            return True
        # 词表外单格分类行(如 "高新产业园"):文件级完整表 + 行级无业务文本
        # (context['_relax'])且 ≤16 字 → 放宽判为分类
        if context.get('_relax') and len(value) <= 12 and value:
            BaseParser._set_category(context, value)
            return True
        return False

    @staticmethod
    def merge_header_rows(header_rows: List[List[Any]], header_idx: int,
                          header_merged: bool = False,
                          merged_ranges: Optional[List[Tuple[int, int, int, int]]] = None
                          ) -> tuple[List[Any], int]:
        """构造表头行并定位数据起始行(两行表头场景)。

        1. 父标题在表头行上方(横向合并):仅认**横向合并单元格**为父标题
           (merged_ranges 提供时;如 "2020年计划" 合并跨列覆盖本列),
           上方非合并的短文本不再作父标题;
        2. 子表头行紧邻表头下方(如 "2020年计划"下 "计划投资/进度目标或新增效益"):
           合并方向:上一行(表头行)自身是横向合并的父标题(header_merged=True,
           如 "2020年计划" 合并跨列),下一行才是可合并的子表头——仅当满足此前提
           且下一行非空单元格均为短文本(≤30 字,概况文字行如 "2025年全市城建工程
           项目共376个…" 不满足)时才合并进表头,数据起始行后移一行。
        """
        raw_headers = list(header_rows[header_idx]) if header_idx >= 0 else []
        headers = list(raw_headers)
        for col in range(len(headers)):
            child = str(headers[col] or '').strip()
            if not child:
                continue
            for r in range(header_idx - 1, -1, -1):
                if col >= len(header_rows[r]):
                    continue
                parent = str(header_rows[r][col] or '').strip()
                # 父标题须为横向合并单元格(如 "2020年计划" 合并跨列覆盖本列);
                # merged_ranges 未提供(如 旧版 xls 路径)时保持旧逻辑(任意短文本)
                if merged_ranges is not None and not any(
                        rlo <= r <= rhi and clo <= col <= chi and chi > clo
                        for rlo, rhi, clo, chi in merged_ranges):
                    continue
                # 排除 附件编号("附件－1")、单位说明行("投资单位：万元")、纯数字
                # (列宽行,如 北京 row1 "5|25|20|20|50")等非父标题
                if parent and len(parent) <= 12 and parent not in child \
                        and not parent.startswith('附件') and '单位' not in parent \
                        and not re.fullmatch(r'[\d.，,]+', parent):
                    headers[col] = f"{parent}-{child}"
                    break

        sub_idx = header_idx + 1
        if sub_idx < len(header_rows) and header_merged:
            sub = header_rows[sub_idx]
            sub_texts = [str(c or '').strip() for c in sub if str(c or '').strip()]
            if sub_texts and all(len(t) <= 30 for t in sub_texts) \
                    and any(re.search(r'(计划投资|投资|目标|内容|进度|形象|时间|地点)', t)
                            for t in sub_texts):
                for col in range(len(sub)):
                    child = str(sub[col] or '').strip()
                    if not child:
                        continue
                    parent = str(headers[col] or '').strip()
                    if not parent:  # 父标题在左侧(横向合并,基于原始表头避免叠加)
                        for left in range(col - 1, -1, -1):
                            p = str(raw_headers[left] or '').strip()
                            if p and len(p) <= 12:
                                parent = p
                                break
                    if parent and parent not in child:
                        headers[col] = f"{parent}-{child}"
                header_idx = sub_idx

        # 垂直拆词表头行(主表头无横向合并时的两行表头,如 垫江前期
        # "建设起" + 下行"止年限" / "至2025年底已" + "完成的前期工作"):
        # 表头行下方行,其非空单元格对应主表头行同列也非空、每格为短文本
        # (≤8 字、非纯数字、非 合计/总计 开头)→ 表头词拆两行,直接拼接
        # ("建设起"+"止年限" → "建设起止年限")并下移数据起始行(拆词行非数据)
        if not header_merged:
            sub2 = header_rows[header_idx + 1] if header_idx + 1 < len(header_rows) else None
            if sub2:
                pieces: List[Tuple[int, str]] = []
                valid = True
                for col in range(len(sub2)):
                    s = str(sub2[col] or '').strip()
                    if not s:
                        continue
                    main = str(headers[col] or '').strip() if col < len(headers) else ''
                    if not main or len(s) > 8 or re.fullmatch(r'[\d.,，]+', s) \
                            or re.match(r'^(合计|总计|小计)', s):
                        valid = False
                        break
                    pieces.append((col, s))
                # 至少 2 列拆词才拼(真实拆词表头如 垫江前期 "建设起"/"止年限" 多列;
                # 单格行如 性质标题 "新建项目(1项)" 不触发,防止拼坏表头)
                if valid and len(pieces) >= 2:
                    for col, s in pieces:
                        headers[col] = f"{str(headers[col]).strip()}{s}"
                    header_idx += 1
        return headers, header_idx

    @staticmethod
    def _trim_org_fragment(name: str) -> str:
        """清洗项目名中的机构碎片(pdfplumber 表格垂直错位把相邻格并入名称列)。

        两段式:
        1. 机构词开头段:"…建设项目教育厅桂林理工大学教学" → "…建设项目"
        2. 机构词结尾段:"…物流园南宁市人民政府" → "…物流园"
        """
        # 段1:项目/工程后紧跟机构词("教育厅/人民政府/信息港…")的内容 → 截断
        # 前瞻排除仅针对连续"项目/工程"词,避免"理工大学"的"工"字误停
        name = re.sub(r'(项目|工程)(?:(?:教育厅|教育局|人民政府|信息港|农垦局|'
                      r'厅|局|委|办|部|院|校|府|司|团|社|所|站)(?:(?!项目|工程).){0,14})',
                      r'\1', name)
        # 段2:项目/工程/园/基地 后为机构段(如 "…物流园南宁市人民政府")→ 截断
        def _repl(m: re.Match) -> str:
            tail = m.group(2)
            # 尾部机构段(政府/厅/局/委/办/中心/管委会 类;"公司"不截防误伤数据行)
            trimmed = re.sub(r'[一-鿿]{1,4}?(?:市人民政府|人民政府|政府|厅|局|委|办|管委会)$',
                             '', tail)
            if trimmed != tail:
                return m.group(1) + trimmed.rstrip(' /')
            return m.group(0)
        return re.sub(r'(项目|工程|园|基地)([^项目工程园基地]{1,16})$', _repl, name)

    @staticmethod
    def _is_year_list_title(name: str) -> bool:
        """年份+清单类文档/章节标题行判定(整名):含 "20xx年/20xx年度" 且以
        清单/名单/目录/总表 收尾(允许括号类别后缀),如:
        - "2026年上海市重大工程项目清单（预备项目）"
        - "2026年市级重点储备项目清单"
        - "安徽省2026年重点项目清单（B类）"
        - "2026年省重点前期工作项目清单"
        - "云南省2026年度第一批“重中之重”项目清单"
        真项目名以 清单/名单/目录/总表 结尾几乎不存在,可安全整名匹配;
        名称**含**年份但不以清单类结尾的真项目不受影响(如 "渝北区2025年
        “四好农村路”建设(打捆项目)"、"2024年城镇老旧小区改造项目")。
        """
        n = str(name).replace(' ', '')
        if len(n) > 45:
            return False
        if not re.search(r'20\d{2}\s*(?:年|年度)', n):
            return False
        # 结尾:清单/名单/目录/总表 + 可选括号类别后缀("（预备项目）"/"（B类）")
        return bool(re.search(
            r'(?:清单|名单|目录|总表)\s*(?:[（(][^（()）]{0,14}[)）])?\s*$', n))

    @staticmethod
    def filter_blank_projects(projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """过滤无效项目:合计行;项目名少于 3 字且其他内容为空;清洗名称尾部机构碎片。
        过滤，_filter_seconde_name
        """
        def has_info(p: Dict[str, Any]) -> bool:
            return any(p.get(k) for k in ('construction_unit', 'location', 'total_investment',
                                          'construction_content', 'responsible_unit',
                                          'annual_goal', 'start_year'))
        result = []
        for p in projects:
            name = p.get('project_name', '')
            if name.endswith('中心'):
                pass
            if name.replace(' ', '').startswith(('合计', '总计', '小计')):
                continue
            # 单位说明行(如 "金额单位:万元" / "单位：万元")不作为项目
            if re.search(r'(?:金额)?单位\s*[:：]\s*[万|亿]元', name):
                continue
            if name in ('项目名称', '序号', '名称'):
                continue  # 跨页重复表头行
            if BaseParser._is_year_list_title(name):
                continue  # 年份+清单/名单类文档标题行(如 "2026年省重点前期工作项目清单")
            if BaseParser._filter_seconde_name(name):
                continue
            # 全数字/占位符清洗:项目名全数字或全破折号("——")→ 整条过滤;字段同型 → 置空
            if name and (re.fullmatch(r'[\d,，.．\s]+', name)
                         or re.fullmatch(r'[—－\s-]+', name)):
                continue
            for field in ('location', 'project_type', 'construction_unit',
                          'responsible_unit', 'project_owner'):
                v = p.get(field, '')
                if v and (re.fullmatch(r'[\d,，.．\s]+', str(v))
                          or re.fullmatch(r'[—－\s-]+', str(v))):
                    p[field] = ''
            # category 清洗:去行首序号/括号统计(如 "一、基础设施类（共32项）" → "基础设施类")
            if p.get('category'):
                p['category'] = BaseParser._clean_category_name(p['category'])
            if len(name) < 3 and not has_info(p):
                continue
            # 子序号前缀清理:"(3)银川市…光伏发电项目" → "银川市…光伏发电项目"
            name = re.sub(r'^[（(]\s*\d+\s*[)）]\s*', '', name).strip()
            p['project_name'] = BaseParser._trim_org_fragment(name)
            result.append(p)
        return result

    @staticmethod
    def is_category_name(name: str) -> bool:
        """判断文本是否为分类/汇总行(如 "一、工业(321项)"、"总计(803项)"、"（一）电子信息"、"(1)高速公路项目")。

        括号序号标题(如 "(1)高速公路项目"、"（一）电子信息")要求短标题(≤15 字)
        或含项数,避免 "(3)银川市…光伏发电项目" 这类子序号+完整项目名的数据行误判。
        """
        m = re.match(r'^[（(]\s*(?:[一二三四五六七八九十ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+|\d+)\s*[)）]\s*(.+)$', name)
        if m:
            # 分类名单词或数字量词结尾(如 "（一）实验室体系建设项目2个")
            return (BaseParser._looks_like_category(m.group(1))
                    or re.search(r'\d+\s*(?:个|项|件)\s*$', m.group(1)))
        return bool(
            re.match(r'^[一二三四五六七八九十ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+、', name)
            or re.search(r'[（(]\s*共?\s*\d+\s*(?:项|个)?[)）]', name)
            # "——" 子分类行(如 "——铁路"),路由到 update_category_context 处理
            or re.match(r'^[—－-]{2,}\s*\S', name)
        )

    @staticmethod
    def update_category_context(text: str, context: Dict[str, str], type:str=None) -> bool:
        """识别分类/分组行并更新上下文(category 行业分类 / project_type 建设性质)。

        返回 True 表示该行是分类行(不产生项目)。层级规则:
        - "一、工业(321项)" → category="工业"
        - "（一）电子信息" → 追加为 "工业-电子信息"
        - "（二）汽车" → 同级,替换最后一段 → "工业-汽车"
        - "新建项目(1项)" → project_type="新建"

        type,不同调用的补充措施
        """
        if not text:
            return False
        # 单元格内跨行文本(如 "港口、码头、航运\n（7项）")归一为空格,
        # 否则 ".+$" 无法跨换行匹配,分类行落入兜底分支保留序号前缀
        text = text.replace('\r', ' ').replace('\n', ' ')
        # 【】强调包装去壳(如 "【预备】(1个)" 等同 "预备(1个)",贵阳 2026)
        text = BaseParser._unwrap_cat_bracket(text)
        # 分类行多余信息多为数量/金额(如 "一、基础设施 64 8393887.27"、"——铁路 2 402600"):
        # 先剔除空格分隔的纯数字 token(序号/数量/金额),再匹配分类特征,
        # 避免金额数字干扰分类名判断;括号内数字("（16项）")、带单位数字("1.5万亿")、
        # 量词前导数字("项目数 426 个" 的 "426")保留
        raw = text
        text = re.sub(r'(^|\s)\d[\d,，.．]*(?!\s*(?:个|项|件)\b)(?=\s|$)', ' ', text).strip()
        # 括号统计支持括号内含金额(如 内蒙古板块 "（115个，1730.03亿元）")
        if not (re.search(r'[（(]\s*共?\s*\d+\s*(?:项|个)[^）)]*[)）]', text)
                # 无"项/个"的括号数字仅认行首(避免数据行内容如 "小（1）型水库" 误触发)
                or re.match(r'^[（(]\s*\d+\s*[)）]', text)
                or re.match(r'^[一二三四五六七八九十ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ①②③④⑤⑥⑦⑧⑨⑩]+[、.．\s]', text)
                or re.match(r'^[（(][一二三四五六七八九十ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+[)）]', text)
                # -1 分类
                or re.match(r'^-\d+\s+', text)
                or re.match(r'^[（(]\s*\d+\s*[)）]', text)
                or re.match(r'^[—－-]{2,}\s*', text)
                # 行尾括号整数统计: "合计(2617)" / "城镇（含园区）基础设施类（52）"
                or re.search(r'[（(]\s*共?\s*\d+\s*(?:项|个|件)?\s*[)）]\s*$', text)
                # 行尾数字量词(如 "前期准备项目135个")
                or re.search(r'\d+\s*(?:个|项|件)\s*$', text)
                or re.match(rf'^(?P<pt>{PT})项目?$', text)):
            # 补充词表全等分类行(人工维护的 CATEGORY_Supplement_WORDS,全等即分类):
            # 无 序号/括号/量词 等前缀也可放行——如 银川 "一产项目 4"(计数纯数字已
            # 随数字剔除 → "一产项目"),强/弱词仍需结构前缀防数据行误判(名称/建设内容
            # 可能包含 "交通/市政" 等词),补充词全等不存在该歧义
            if text in CATEGORY_Supplement_WORDS:
                BaseParser._set_category(context, text)
                return True
            return False

        # 性质分组头 + 括号项数(如 "预备(1个)"、"【预备】(4)"、"一、在建（257个）",
        # 贵阳 2026 docx):只设 project_type、不产生项目;性质纯词不入 category
        m_pt = re.match(rf'^[\d一二三四五六七八九十]*[、.．\s]*(?P<pt>{PT})(?:项目)?'
                                rf'(?:\s*[（(]\s*\d+\s*(?:个|项|件)?\s*[)）]|\s*\d+\s*(?:个|项|件)?)?'
                                rf'\s*$', text)
        if m_pt:
            context['project_type'] = m_pt.group('pt')
            return True

        # m = re.search(rf'(?P<pt>{PT})', text)
        # if m and len(text) <= 10:
        #     context['project_type'] = m.group('pt')

        # 纯建设性质标题(如 "投产项目")→ 更新 project_type
        m_type = re.match(rf'^(?P<pt>{PT})项目?$', text)
        if m_type:
            word = m_type.group('pt')
            context['project_type'] = '竣工投产' if word == '竣工投产' else word
            return True

        m1 = re.match(r'^[一二三四五六七八九十]+[、\s]\s*(.+)$', text)
        if m1:
            # 去掉 "（12项/172个，投资额xx亿元）" 等统计后缀及后续金额数字
            category = re.sub(r'[（(]\s*共?\s*\d+\s*(?:项|个)[^）)]*[)）].*$', '', m1.group(1)).strip()
            # 概况统计说明截断:分类行名称列可能带 "项目59个。其中,市住建委14个…" 说明文字
            category = re.split(r'[。；;]|其中', category, maxsplit=1)[0].strip()
            category = re.sub(r'\s+(?:项目|项)?\s*\d+\s*(?:个|项|件).*$', '', category).strip()
            BaseParser._set_category(context, category)
            BaseParser._record_declared(text, context)
            return True

        m2 = re.match(r'^[（(][一二三四五六七八九十ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+[)）]\s*(.+)$', text)
        if m2:
            sub_raw = m2.group(1)
            # 概况说明文字(如 "市住建委 项目14个，2025年计划完成4.36亿元")→ 跳过不设分类
            if re.search(r'[，。；;]', sub_raw) and len(sub_raw) > 12:
                return True
            # 分类名单判断:命中分类词、行尾括号整数统计(如 "实验室体系建设（10）")
            # 或数字量词结尾(如 "实验室体系建设项目2个")才视为分类标题,
            # 否则是数据行(如 "（三）李家岩水库")
            if not (BaseParser._looks_like_category(sub_raw)
                    or re.search(r'[（(]\s*共?\s*\d+\s*(?:项|个|件)?\s*[)）]\s*$', sub_raw)
                    or re.search(r'\d+\s*(?:个|项|件)\s*$', sub_raw)):
                # 词表外分类行(如 "（二） 国省道"):文件级完整表 + 行级无业务文本
                # (context['_relax'],由 xlsx 循环按文件统计设置)+ 子名 ≤12 字 → 放宽;
                # 无 _relax(数据行/少列文件)仍判数据行(如 "（三）李家岩水库")
                if not (context.get('_relax') and len(sub_raw) <= 12):
                    if type in ['valid_normal_ratio']:
                        # 有效项数最多两个。
                        pass
                    else:
                        return False

            BaseParser._record_declared(text, context)
            sub = BaseParser._clean_category_name(sub_raw)
            if sub:
                # 纯建设性质标题(如 "续建项目"/"新建")→ 只更新 project_type
                if BaseParser._is_type_title(sub, context):
                    return True
                # dash_base:最近一次非"——"分类行后的分类("——X" 子分类挂在其下);
                # （二）级标题回退时按 dash_base 替换,不把 "——" 子分类带进新分类
                base = context.get('dash_base') or context.get('category', '')
                if '-' in base:
                    # 同级子分类:(二)替换(一),保留大类
                    context['category'] = f"{base.rsplit('-', 1)[0]}-{sub}"[:128]
                elif base:
                    context['category'] = f"{base}-{sub}"[:128]
                else:
                    context['category'] = sub[:128]
                context['dash_base'] = context['category']
            return True

        # 三级标题:数字序号括号标题,如 "(1)高速公路项目"
        # 三级标题:-数字序号 ,如 "-1 信息基础设施项目"
        # 注意 "(3)银川市…光伏发电项目" 是子序号+项目名(数据行),非分类标题
        # ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ 优先三级标题
        m3 = re.match(r'^[（(]\s*\d+\s*[)）]\s*(.+)$', text)
        is_roman = False
        if not m3:
            # 负号序号(如 广东 "-1 信息基础设施项目")= 三级分类(与罗马同级挂载)
            m3 = re.match(r'^-\d+\s+(.+)$', text)
            is_roman = bool(m3)
        if not m3:
            # 罗马数字 / 带圈序号(如 "① 交通项目7个")= 三级分类
            m3 = re.match(r'^[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ①②③④⑤⑥⑦⑧⑨⑩]+[、.．\s]\s*(.+)$', text)
            is_roman = bool(m3)
        if m3:
            sub_raw = m3.group(1)
            # 概况说明文字(如 "（一）市住建委 项目14个，2025年计划完成4.36亿元")→ 跳过
            if re.search(r'[，。；;]', sub_raw) and len(sub_raw) > 12:
                return True
            # 分类名单判断:命中分类词、行尾括号整数统计(如 "(1)高速公路项目（8）")
            # 或数字量词结尾(如 "(1)续建项目2个")才视为分类标题,
            # 否则是数据行(如 "(1)李家岩水库")
            if not (BaseParser._looks_like_category(sub_raw)
                    or re.search(r'[（(]\s*共?\s*\d+\s*(?:项|个|件)?\s*[)）]\s*$', sub_raw)
                    or re.search(r'\d+\s*(?:个|项|件)\s*$', sub_raw)):
                # 词表外分类行(如 "（二） 国省道"):文件级完整表 + 行级无业务文本
                # (context['_relax'],由 xlsx 循环按文件统计设置)+ 子名 ≤12 字 → 放宽;
                # 无 _relax(数据行/少列文件)仍判数据行(如 "（三）李家岩水库")
                if not (context.get('_relax') and len(sub_raw) <= 12):
                    return False
            BaseParser._record_declared(text, context)
            sub = BaseParser._clean_category_name(sub_raw)
            if sub:
                # 纯建设性质标题(如 "(1)续建项目")→ 只更新 project_type
                if BaseParser._is_type_title(sub, context):
                    return True
                if is_roman:
                    # 罗马数字序号 = 三级分类(如 "Ⅰ 机场（9项）"):追加到当前
                    # 二级分类下构成 "一级-二级-三级"(如 "基础设施-交通"+"机场"
                    # → "基础设施-交通-机场");兄弟 "Ⅱ 铁路" 仍挂在 dash_base 下,
                    # 不更新 dash_base(三级不是新父级)
                    base = context.get('dash_base') or context.get('category', '')
                    context['category'] = f"{base}-{sub}"[:128] if base else sub[:128]
                else:
                    base = context.get('dash_base') or context.get('category', '')
                    if '-' in base:
                        context['category'] = f"{base.rsplit('-', 1)[0]}-{sub}"[:128]
                    elif base:
                        context['category'] = f"{base}-{sub}"[:128]
                    else:
                        context['category'] = sub[:128]
                    context['dash_base'] = context['category']
            return True

        # "——" 子分类行:如 桂林市 "——铁路 2 402600"(首列空,名称列 "——X" + 数量 + 金额)
        # → 子分类标题,不产生项目;挂在 dash_base 之下("基础设施-交通" + "铁路"
        # → "基础设施-交通-铁路")。兄弟 "——航空" 替换为 "基础设施-交通-航空"。
        # 分类特征二选一:名称后跟空格分隔的数量+金额(表格行,如 "——其他服务 21 6184874"),
        # 或名称命中分类名单词(文本行,如 "——铁路")。其余(如 PDF 内容续行 "——含5座桥涵")
        # 不认作分类,回退原逻辑
        m_dash = re.match(r'^[—－-]{2,}\s*(.+)$', text)
        if m_dash:
            sub = BaseParser._clean_category_name(m_dash.group(1))
            if not sub or len(sub) > 16:
                return False
            # 表格行特征:数量+金额在去数字前的原文里(如 "——其他服务 21 6184874")
            raw_tail = re.match(r'^[—－-]{2,}\s*(.+)$', raw)
            has_count = bool(
                raw_tail and re.search(r'\s[\d,，.]+(?:\s[\d,，.]+)*\s*$',
                                       raw_tail.group(1).strip()))
            if not has_count and not BaseParser._looks_like_category(sub):
                return False
            base = context.get('dash_base') or context.get('category', '')
            context['category'] = f"{base}-{sub}"[:128] if base else sub[:128]
            return True

        # 行尾数字量词(如 "前期准备项目135个"):性质词开头 → project_type;其他 → 分类
        if re.search(r'\d+\s*(?:个|项|件)\s*$', text):
            cleaned = re.sub(r'\d+\s*(?:个|项|件)\s*$', '', text).strip()
            m_typ = re.match(rf'^(?P<pt>{PT})\S*项目?$', cleaned)
            if m_typ:
                context['project_type'] = m_typ.group('pt')
            elif re.match(r'^.{0,3}项目(总\s*计|合\s*计|小\s*计)', cleaned):
                return True  # 汇总行,跳过不产生项目、不设分类
            elif cleaned and len(cleaned) <= 16 and BaseParser._looks_like_category(cleaned):
                BaseParser._set_category(context, cleaned)
                return True  # 跳过不产生项目
            return False

        # 行尾括号整数统计: "城镇（含园区）基础设施类（52）"、"合计(2617)"
        # → 去末尾 "（N）" 后为分类名;汇总词("合计/总计/小计")仅跳过不设分类;
        # 未命中分类名单词(如 "某项目（2）" 数据行)→ 非分类行
        m_paren = re.search(r'[（(]\s*共?\s*\d+\s*(?:项|个|件)?\s*[)）]\s*$', text)
        if m_paren:
            cat = text[:m_paren.start()].strip()
            if re.match(r'^(总\s*计|合\s*计|小\s*计)', cat):
                return True  # 汇总行,跳过不产生项目、不设分类
            if cat and len(cat) <= 16 and BaseParser._looks_like_category(cat):
                BaseParser._set_category(context, cat)
                return True
            return False

        # 兜底:序号+分类标题(如 "42 光伏发电项目（16项）",序号列有值)→ 去序号去项数
        cleaned = re.sub(r'^\s*\d+\s*', '', text)
        cleaned = re.sub(r'[（(]\s*共?\s*\d+\s*(?:项|个)[^）)]*[)）].*$', '', cleaned).strip()
        # 排除 汇总行("总计/合计/小计")
        # 护栏:长度上限 + 句子标点限定——兜底放行后 cleaned 实为 名称+建设内容
        # 拼接的业务数据行(温州 882 "878 科技创新强基领域 全省海上风电…（5个桩基
        # 式…）…" 括号统计门控被建设内容括号放行)时超长且含句读,不再误设分类;
        # 真实分类名(≤24 字、无句读)不受影响
        if cleaned and cleaned != text.strip() \
                and not re.match(r'^(总\s*计|合\s*计|小\s*计)', cleaned) \
                and len(cleaned) <= FALLBACK_CATEGORY_MAX_LEN \
                and not FALLBACK_CATEGORY_PUNCT_RE.search(cleaned):
            BaseParser._record_declared(text, context)
            BaseParser._set_category(context, cleaned)
            return True
        # 前置检查通过但未识别出分类特征(如 "(10)中车…\n、中宁县人民政府" 数据行)→ 非分类行
        return False

    @staticmethod
    def _clean_category_name(name: str) -> str:
        """统一清洗分类名:
        - 去前后空格
        - 去开头序号/顿号(如 "（一）房地产"、"1、工业"、"、续建项目")
        - 去括号统计("（16项）"/"（172个）")及后续
        - 去省略号及后续("基础设施…" → "基础设施")
        - 去同行金额数字("前期储备项目 2265.58 838742…" → "前期储备项目")
        """
        # 去引号(如 "'2+4'产业链项目" → "2+4产业链项目")
        name = name.replace("'", '').replace('"', '').replace('“', '').replace('”', '')
        name = name.strip()
        # 带圈序号/PUA 字符("③新材料" / "汽车" → "新材料/汽车")
        name = re.sub(r'^[①②③④⑤⑥⑦⑧⑨⑩]+\s*', '', name)
        name = re.sub(r'^[-]+\s*', '', name)
        # 括号序号("（一）房地产" → "房地产")
        name = re.sub(r'^[（(]\s*[一二三四五六七八九十ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ\d]+\s*[)）]\s*', '', name)
        # 合并序号范围/残留("428-442 4.房地产开发" → "4.房地产开发";"-442" → "";"2+4…" 无破折号不误去)
        name = re.sub(r'^[\d－-]*[－-][\d－-]*\s*', '', name)
        # 顿号/点号序号("1、工业" / "一、工业" / "4.房地产开发" → "工业/房地产开发";"2+4…" 的"+"非分隔,不误去)
        name = re.sub(r'^[一二三四五六七八九十ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ\d]+\s*[、.．]\s*', '', name)
        name = re.sub(r'^[、,，.\s]+', '', name)
        name = re.sub(r'[（(]\s*共?\s*\d+\s*(?:项|个|件)?[^）)]*[)）].*$', '', name)
        # 无括号项数("项目45个" 的 "45个"/"项目2件")→ 去
        name = re.sub(r'\d+\s*(?:项|个|件)(?=\s|$)', '', name)
        # "项目数 426 个"(浙江 千项万亿 分类行统计列)→ 剥离
        name = re.sub(r'项目数\s*[\d,，.．]*\s*(?:个|项|件)?', '', name)
        # "——" 占位归一为空格(后续金额截断可识别行尾数字)
        name = re.sub(r'[—－-]{2,}', ' ', name)
        name = re.sub(r'[…]{1,}.*$', '', name)
        # 性质词后截断("…抽水蓄能电站 新建 长阳县" → "…抽水蓄能电站")
        name = re.sub(rf'\s+(?:{PT})\b.*$', '', name)
        # 同行金额截断:空格分隔的行尾数字序列
        # ("前期储备项目 2265.58 838742…" → "前期储备项目";"'2+4'产业链项目" 不误截)
        name = re.sub(r'\s+[\d,，.]+(?:\s+[\d,，.]+)*\s*$', '', name)
        # 去尾部斜杠(如 "基础设施项目/（193项）" 跨行归一后 → "基础设施项目")
        name = name.rstrip('/')
        # 去尾部冒号(如 "市场主导类项目：162个" 去量词后残留 "市场主导类项目："
        # 的分类名+冒号;冒号分隔的项数说明不属于分类名)
        name = name.rstrip('：:').strip()
        return name.strip()[:128]

    @staticmethod
    def _set_category(context: Dict[str, str], raw: str) -> None:
        """清洗并设置分类上下文;无效分类("明细" 等)不设置。

        性质+内容混合标题(如 "、续建项目-湖北长阳清江抽水蓄能电站 新建 …")
        → 只设 project_type,不设 category。
        """
        cleaned = BaseParser._clean_category_name(raw)
        if BaseParser._filter_seconde_name(cleaned):
            return
        if not cleaned or '明细' in cleaned:
            return
        if re.match(r'^(总\s*计|合\s*计|小\s*计)', cleaned):
            return  # 汇总词("合计/总计/小计")不做分类上下文
        m_mix = re.match(rf'^(?P<pt>{PT})(?:项目)?\s*[-－\s]', cleaned)
        if m_mix:
            context['project_type'] = m_mix.group('pt')
            return
        context['category'] = cleaned[:128]
        # 一级分类重置 "——" 子分类的挂载点(新分类下 "——X" 从新分类开始挂)
        context['dash_base'] = cleaned[:128]

    @staticmethod
    def _looks_like_category(sub: str) -> bool:
        """判断 sub(括号序号标题后的文本)是否为分类标题。

        依据分类名单词:强词命中 → 分类(如 "高速公路项目"/"中型水利工程");
        弱词命中且文本较短(≤8 字)→ 分类(如 "光伏发电项目");
        否则视为项目名(如 "李家岩水库"/"光伏组件制造项目")。
        """
        # 先去除数字(分类标题可能同行带金额,如 "房地产 123 456")
        cleaned = re.sub(r'\s+\d+(?:[，,.]\d+)*', '', sub)
        # 项数特征:尾部括号数字("（16项）"/"（172个）"/"（10）" 纯数字,如 "实验室体系建设（10）")
        if re.search(r'[（(]\s*共?\s*\d+\s*(?:项|个|件)?\s*[)）]\s*$', sub):
            return True
        if BaseParser._is_type_title(cleaned, {}):
            return True
        # 强词/弱词命中均需文本较短(≤12/≤6 字),避免 "…快充站建设工程:在KZ-1-368…" 等长文本行误判
        if len(cleaned) <= 12 and any(kw in cleaned for kw in CATEGORY_STRONG_WORDS):
            return True
        if len(cleaned) <= 6 and any(kw in cleaned for kw in CATEGORY_WEAK_WORDS):
            return True
        if cleaned in CATEGORY_Supplement_WORDS:
            return True
        return False

    @staticmethod
    def _is_section_head(text: str) -> bool:
        """清单分区标题判定(bare 段落清单的启动信号):序号/括号序号 前缀 + 分类词尾
        的项目分区行,如 "（一）农业水利项目"、"一、交通项目(8项)"。

        公文正文小标题(如 "一、总体要求"、"（二）压实责任")不以 项目/工程/产业/
        设施/类/建设 收尾 → 不当作清单分区,避免纯通知文档正文被 bare 误收。
        """
        t = text.strip()
        if not re.match(
                r'^(?:[一二三四五六七八九十ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+[、.．\s]'
                r'|[（(][一二三四五六七八九十ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+[)）]'
                r'|[\d]+[、.．]|[—－-]{2,})', t):
            return False
        return bool(re.search(
            r'(?:项目|工程|产业|设施|类|建设)\s*(?:[（(][^（()）]*[)）])?\s*$', t))

    @staticmethod
    def _is_type_title(sub: str, context: Dict[str, str]) -> bool:
        """判断子标题是否为纯建设性质标题(如 "续建项目"/"新建"),是则更新 project_type。"""
        type_words = ('新建', '续建', '竣工投产', '投产', '预备', '储备', '新开工', '前期')
        for word in type_words:
            if sub == word or sub == word + '项目':
                context['project_type'] = word
                return True
        return False

    @staticmethod
    def _record_declared(text: str, context: Dict[str, str]) -> None:
        """记录分类标题声明的项数("（共N项）"/"（172个）"),仅限分类行内部调用。"""
        m_decl = re.search(r'[（(]\s*(?:共)?\s*(\d+)\s*(?:项|个)\b', text)
        if m_decl:
            context['declared_count'] = int(m_decl.group(1))

    @staticmethod
    def is_data_row(cells: List[Any]) -> bool:
        """是否为有内容的数据行(全空返回 False)。"""
        return any(c is not None and str(c).strip() for c in cells)

    def parse_lines(self, lines: List[str], context: Optional[Dict[str, str]] = None,
                    bare: bool = False) -> List[Dict[str, Any]]:
        """行级兜底解析:从纯文本行中抽取项目信息。

        规则:
        - 数字序号开头(序号后可为空格/顿号/点号) → 新项目
        - 序号独占一行 → 下一行作为项目名
        - 分类行("一、工业"、"（一）电子信息"、"总计(803项)") → 更新分类上下文
        - 性质分组头("续建项目：") → 更新 project_type 上下文
        - 其他行 → 拼接到当前项目名(跨行拆分),含投资/年份时抽取字段
        - bare=True(docx 无表格段落清单,如 甘肃 "续建项目：…（一）农业水利项目
          → 逐行项目名"):尚未产出项目时的无序号短文本行(2-60 字、无句读/逗号、
          非 名单/清单 类标题行)作为**独立项目条目**,不做续行拼接

        context: 跨段共享的分类上下文(如 PDF 跨页共享),None 则新建。
        """
        projects: List[Dict[str, Any]] = []
        context = context if context is not None else {}
        pending = False
        list_mode = False  # bare 模式:出现 分区标题/性质组头 后才把裸行当项目条目
        for line_idx, line in enumerate(lines, start=1):
            text = line.strip()
            if not text:
                continue
            # 页码信息清洗:"第 武汉市经济开发区1页,共 34 页 904400 50000" → 去页码片段
            text = re.sub(r'\s*\d+\s*页\s*,?\s*共\s*\d+\s*页\s*', ' ', text)
            text = re.sub(r'^\s*第\s*', '', text).strip()
            # 页眉/表头/页码/落款行 → 忽略:
            # 纯年份("2020")、表头("序号 项目名称 备注",容忍空格如"序 号")、页码("- 1 -")、
            # 年份开头行("2020 年第四批…")、附件/联系人/代章(通知落款区)
            compact = text.replace(' ', '')
            if (text.isdigit() and len(text) == 4
                    or ('序号' in compact and '项目名称' in compact)
                    or re.match(r'^-\s*\d+\s*-$', text)
                    or re.match(r'^\d{4}\s*年', text)
                    or '附件' in text or '联系人' in text or '代章' in text):
                pending = False
                continue
            # 装饰行(文本级统一判定):招商简介正文字段标签行(如 "项目名称：xxx…"、
            # "联 系 人：xxx")、备注/注记行(如 "备注：…"/"注：…")、清单概况/总数
            # 总结句(如 "项目总数246个(新开工73个…)"、"重大前期项目92个,总投资
            # 494亿元。其中…")→ 不产生项目、不拼入上一项目名;
            # 概况句不作用于数字序号开头的行(真实项目行可能含 "…个,总投资…"
            # 描述短语,如 "3.xxx项目,年产xx万个,总投资…")
            collapsed = re.sub(r'\s+', ' ', text)
            if (PROSE_LABEL_RE.match(collapsed)
                    or BaseParser.is_note_text(collapsed)
                    or (BaseParser._is_overview_sentence(collapsed)
                        and not re.match(r'^\s*\d+[、.．]', collapsed))):
                pending = False
                continue
            # 性质分组头独立行(如 "续建项目："/"预备项目:" 后接该类项目条目,
            # docx 段落式清单常见,如 甘肃 "续建项目：")→ 更新 project_type 上下文
            m_grp = re.match(
                rf'^(?P<pt>{PT})(?:项目|名单)?\s*[:：]\s*$',
                text)
            if m_grp:
                context['project_type'] = m_grp.group('pt')
                if bare:
                    list_mode = True  # 性质组头 = 段落式清单的启动信号
                pending = False
                continue
            if self.is_category_name(text) and self.apply_category(text, context):
                # bare 模式仅接受 分类词尾 的分区标题作为启动信号
                # (如 "（一）农业水利项目");"一、总体要求" 等公文正文小标题不算,
                # 否则纯通知文档的正文会被当清单
                if bare and BaseParser._is_section_head(text):
                    list_mode = True
                pending = False
                continue
            # 序号独占一行(如 "9"),下一行是项目名
            if re.match(r'^\d{1,3}$', text):
                pending = True
                continue
            m = re.match(r'^(\d+)\s*[、.．]?\s*(.*)$', text)
            if m:
                name = m.group(2).strip()
                if not name:
                    pending = True  # 序号独占一行,下一行是项目名
                elif re.match(r'^20\d{2}\s*年', name):
                    pending = False  # 序号+年份行(如 "2.2020 年第四批…"),忽略
                elif re.match(r'^(全长|其中|线路全长)', name):
                    pending = False  # 内容片段行(表格错乱文本流),忽略
                else:
                    # 多列合并整行("序号 项目名 单位 地点 内容")时,项目名取第一个空格前
                    if name.count(' ') >= 2:
                        name = name.split(' ', 1)[0]
                    project = self._new_project(name, text, context)
                    project['source_row'] = line_idx  # 文本行号(1-based)
                    projects.append(project)
                    pending = False
                continue
            if pending:
                project = self._new_project(text, text, context)
                project['source_row'] = line_idx  # 文本行号(1-based)
                projects.append(project)
                pending = False
                continue
            # bare 模式(docx 无表段落清单,如 甘肃 "续建项目：…（一）农业水利项目
            # → 逐行项目名"):无序号文本行 = 独立项目条目,不做续行拼接。
            # 门控:必须先出现 分区标题(分类行,已在 apply 命中时置 list_mode)或
            # 性质组头,之后的短文本行才视为项目;纯通知/新闻稿(docx 无清单表格、
            # 无分类信号)→ 标题/正文段落一律忽略,不产生项目
            if bare:
                entry = text
                if list_mode and not pending and 2 <= len(entry) <= 60 \
                        and not re.search(r'[。！？!?；;]$', entry) \
                        and not re.search(r'[,，。:：]', entry) \
                        and not entry.endswith(('名单', '清单', '汇总', '目录', '通知')) \
                        and not entry.isdigit():
                    project = self._new_project(entry, entry, context)
                    project['source_row'] = line_idx  # 文本行号(1-based)
                    projects.append(project)
                continue
            # 无序号行:抽取投资/年份补充到当前项目,或拼接项目名续行
            if projects:
                last = projects[-1]
                investment = clean_amount(text, require_unit=True)
                if investment:
                    last['total_investment'] = investment
                start, end = extract_years(text)
                if start and not last.get('start_year'):
                    last['start_year'] = start
                if end and not last.get('end_year'):
                    last['end_year'] = end
                # 续行拼接:仅无空格且 ≥2 字的行(避免碎片叠加)
                if not investment and ' ' not in text and len(text) >= 2:
                    last['project_name'] = f"{last['project_name']} {text}".strip()[:255]
        return projects

    @staticmethod
    def _new_project(name: str, full_line: str,
                     context: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """从行文本构造项目 dict(去标点、抽投资与年份,附带分类上下文)。"""
        project: Dict[str, Any] = {
            'project_name': name.rstrip('。，,、;；').strip()[:255],
        }
        if context:
            project['category'] = context.get('category', '')
            project['project_type'] = context.get('project_type', '')
        investment = clean_amount(full_line, require_unit=True)
        if investment:
            project['total_investment'] = investment
        start, end = extract_years(full_line)
        if start:
            project['start_year'] = start
        if end:
            project['end_year'] = end
        return project

    def extract_rows_from_table(self, rows: List[List[Any]],
                                context: Optional[Dict[str, str]] = None,
                                file_year: int = 0,
                                prev_header_map: Optional[Dict[int, str]] = None,
                                ) -> tuple[List[Dict[str, Any]], Optional[Dict[int, str]]]:
        """公共表格处理:定位表头 → 数据行 map_row → 过滤空项目名,维护分类上下文。

        - 跨页表格:首页有表头,后续页无(prev_header_map 复用上一页映射,如 湖北多页表)
        - 续行合并:首列(序号列)为空或首列为短分段名(如 广东"江门段")→ 拼接到上一行
        - 单格行(无序号)→ 分类标题行(如 广东表 "基础设施工程/高速公路项目")
        - 返回 (projects, header_map),header_map 供下一页复用
        """
        projects: List[Dict[str, Any]] = []
        context = context if context is not None else {}
        # 每表重新定位表头:同文件含多个独立表格且表头不一致时(如 永川 2022
        # 通知——附件一"政府主导"表[建设性质/起止年限/工作目标/责任部门] 与
        # 附件二"前期"表[建设内容/工作计划/牵头部门/配合部门] 列不同),各表表头
        # 行须按本表识别,否则后表会被前表映射错位(建设内容→project_type 等)。
        # 仅当本表无表头行(跨页表格续页,首页表头被拆成独立 table 且续页顶部无
        # 表头,如 湖北 多页表)才复用上一页映射 prev_header_map
        header_map, header_idx = BaseParser.find_header(rows)
        positional = False
        if header_map is not None:
            headers = rows[header_idx] if header_idx >= 0 else None
            start = header_idx + 1
        elif prev_header_map is not None:
            header_map = prev_header_map
            headers = rows[0] if rows else None
            start = 0
        else:
            # 无表头项目清单兜底:首行为表名(…项目名单/项目清单)的表格,按非空列
            # 顺序默认 序号/项目名称/建设规模(烟台 2022、濮阳 2023 等通知文末表)
            pos = BaseParser._positional_header(rows)
            if pos is None:
                return [], None
            header_map, header_idx = pos
            positional = True
            logger.warning(
                f"识别 headermap 失败但判定为项目清单,按列位置默认为项目"
                f"(序号/项目名称/建设规模;名称列={header_map},表名行={header_idx})")
            headers = rows[header_idx] if header_idx >= 0 else None
            start = header_idx + 1 if header_idx >= 0 else 0
        if 'project_name' not in header_map.values():
            logger.info('未匹配到有效header_map')
            return [], None
        for row_i, row in enumerate(rows[start:], start=1):
            cells = list(row)
            if row_i == 14-1:
                pass
            if BaseParser.skip_summary_row(cells) or not BaseParser.is_data_row(cells):
                continue
            # 页顶重复表头行(跨页表格):跳过,不参与续行/数据
            joined_all = " ".join(str(c).strip() for c in cells if c is not None and str(c).strip())
            if joined_all.startswith(('项目名称', '序号', '项目代码', '项目分类', '主要建设内容',
                                      '建设起止', '责任单位', '合计', '小计', '资金到位',
                                      '前期工作', '形象进度', '进展情况', '审批完成情况')):
                continue
            # 装饰行统一判定(同 xlsx,is_prose_row 内含 备注/正文/概况句)→ 不产生项目
            if BaseParser.is_prose_row(cells):
                continue
            # 单行表头(极简清单,header_map ≤1 列,如 汉中 "序号|项目名称")窄化分组识别
            # (同 xlsx):城市/机构分组短名行跳过,单格真项目名(如 "汉中综合保税区")不误弃
            if len(header_map) <= 1 and BaseParser.is_group_row_minimal(cells):
                continue
            # 责任单位/地区分组行(如 广西 "['','自治区农垦局','2 项',...]")→ 跳过
            # 不设 category(项目分类参考"项目类别/项目分类"列)
            if self.is_group_row(cells):
                continue
            if BaseParser.is_group_header_row(cells, header_map):
                continue
            # 跨行单元格续行 → 直接跳过,不再拼接(合并效果差,已取消):
            # - 首列(序号列)为空的行
            # - 首列为短分段名(≤6 字且以"段"结尾,如 广东"江门段",无序号列表格)
            first = str(cells[0] or '').strip() if cells else ''
            if not first or re.match(r'^.{1,6}段$', first):
                # 无表头清单表:首列空的分类/性质行(如 濮阳 "一、现代服务业项目3个")
                # 不走续行跳过,仍更新分类/建设性质上下文
                if positional:
                    joined = " ".join(str(c).strip() for c in cells if c is not None and str(c).strip())
                    if (BaseParser.group_type_title(cells, header_map)
                            or self.apply_category(joined, context)):
                        continue
                continue # TODO,为什么要有这一步
            # 建设性质标题行(单格纯词,如 安徽表 "续建"/"计划开工")→ project_type 上下文
            build_type = BaseParser.group_type_title(cells, header_map)
            if build_type:
                context['project_type'] = build_type
                continue
            # 全行文本做分类检测(分类行可能出现在项目名称列之外,如合并单元格)。
            # 参考 xlsx 补充业务行检测:业务数据行(序号列为纯数字 + 业务字段列含
            # 真文本,见 is_business_data_row)的全行文本不喂 apply_category——
            # 否则建设内容里的 "（5个桩基式…）" 等括号会被括号统计门控放行、落入
            # 兜底分支把 名称+内容 整体误设为分类,污染后续项目 category(温州 882)。
            # 护栏:仅当 序号列为纯数字 才短路——分类/分组行的序号列为 "一、续建类"
            # 等非数字文本,不受影响,照常走 apply_category 识别分类。
            joined = " ".join(str(c).strip() for c in cells if c is not None and str(c).strip())
            is_biz_row = bool(first) and BaseParser._is_number(first) \
                and BaseParser.is_business_data_row(cells, header_map)
            if not is_biz_row and self.apply_category(joined, context):
                continue
            group_pending = False
            # 单格行且无序号 → 分类标题行(如 广东表 "基础设施工程"、安徽表 "1、合肥市(915个)")
            non_empty = [str(c).strip() for c in cells if c is not None and str(c).strip() and not BaseParser._is_number(c) and not BaseParser._is_placeholder(c)]
            if len(non_empty) == 1 and len(header_map) > 1:
                if BaseParser.classify_single_row(non_empty[0], context):
                    continue
            project = map_row(header_map, cells, headers=headers, file_year=file_year)
            name = project.get('project_name')
            if not name:
                continue
            # 上下文分类仅补充,不覆盖 项目类别/产业类别 列的映射值
            if context.get('category') and not project.get('category'):
                project['category'] = context['category']
            if not project.get('project_type'):
                project['project_type'] = context.get('project_type', '')
            project['source_row'] = row_i  # 表格内行号(表头后第 1 行 = 1)
            projects.append(project)
        return projects, header_map

    @staticmethod
    def _is_number(s):
        '''统计行有效项数时，需要排除纯数字项(含千分位逗号,如 "1,584,946.56")'''
        try:
            num = float(str(s).replace(',', ''))
            if num < 0:
                return False
            return True
        except ValueError:
            return False

    @staticmethod
    def _is_placeholder(s):
        '''占位符单元格(如 "——" / "--"):无意义,视为空,不参与文本/分类判断'''
        return bool(re.fullmatch(r'[—－\s-]+', str(s or '').strip()))

    @staticmethod
    def is_business_data_row(cells: List[Any], header_map: Dict[int, str]) -> bool:
        """业务数据行检测(header_map 列语义):业务字段列含非纯数字文本 → 数据行。

        业务字段列 = header_map 映射字段中排除 项目名称 的列(责任单位/建设性质/
        建设年限/项目业主/总投资 等),含 建设内容(表头别名与项目名称互斥,内容列
        不会放项目名;长文本 >20 字必为真建设内容 → 业务数据)。
        分类行的"数量+金额"为纯数字单元格,不触发;
        数据行(如 渭南/开州 含 "（N个）" 的行)由责任单位/性质/年限等文本列识别,
        建设内容中的 "（N个）" 不参与判定。
        纯数字、占位符、numCell 不是有效业务数据。

        上提到 BaseParser 供 xlsx 循环与 docx/pdf 表格路径(extract_rows_from_table)
        共用:xlsx 用它短路"非业务行才做 分组/性质/分类 识别",docx/pdf 表格路径
        同样需要——否则业务行建设内容里的 "（5个桩基式…）" 等括号文本会被
        apply_category 的括号统计门控 + 兜底分支误吞为分类行(温州 882)。
        """
        for col, field in header_map.items():
            if field == 'project_name':
                continue
            if col >= len(cells):
                continue
            v = str(cells[col] or '').strip()
            if field == 'construction_content':
                # 建设内容:文本 >20 字 = 真建设内容 → 业务数据;
                # 短文本(≤20,分类行说明/数量/占位)不触发
                if v and not BaseParser._is_number(v) and not BaseParser._is_placeholder(v) \
                        and len(v) > 20:
                    return True
                continue
            # 纯数字、占位符、numCell(如 "（共33个）")不是有效业务数据
            numCell = re.fullmatch(r'[（(]?\s*共?\s*\d+\s*(?:项|个|件)?\s*[)）]?', v)
            if v and not BaseParser._is_number(v) and not BaseParser._is_placeholder(v) and not numCell:
                return True
        return False

    @staticmethod
    def _filter_seconde_name(s):
        ''' 2024年合川区重大建设项目名单.xlsx
        存在 未合并、但肉眼看上去合并的单元格 作为项目名称。
        第二行项目名如果：大道|项目|工程|生产|建设|设备|改造，不认为是有效project_name。
        :return 需要过滤 True
        '''
        return bool(re.fullmatch(r'大道|项目|工程|生产|建设|设备|改造|租赁|程|分序号|总序号|附件\d', s))