# 交接摘要 · skp_parser

## 1. 项目目标与技术栈

**目标**:解析指定目录(默认 `util/file_config.py: skpFilePath`)下所有 `pdf/docx/xlsx`,把「省重点项目」
明细入库(`skp_file` 文件表 → `skp_project` 项目表,`file_id` 关联),
明细提取出的单位列 → `skp_project_unit`(`skp_project` 文件表 → `skp_project_unit` 项目表,`project_id` 关联);
通知类文件(文件名含 通知/印发/下达)额外解析元信息入 `skp_notice`,
分类声明项数与实际解析数入 `skp_category_declared`;原文件同时上传
GoFast,库内留 URL(Win 不上传 / Linux 上传)。

**技术栈**:

| 项 | 说明 |
|---|---|
| 语言/运行时 | Python 3.12,asyncio |
| 数据库 | MySQL + aiomysql 连接池(DictCursor,autocommit=False,显式 commit) |
| 选库 | Windows → `local`(127.0.0.1);Linux → `db252`(192.168.1.252),见 `util/db_config.py` |
| 解析库 | openpyxl(xlsx)、xlrd(xls)、python-docx(docx)、pdfplumber(pdf) |
| 上传 | aiohttp(`util/go_fast.py`、`util/http/http_request_util.py`) |
| 日志 | `util/log_util.get_logger`,统一不用 print |
| 测试 | **无测试框架**;回归靠 `analy/`(`baseline_pre.jsonl`/`baseline_post.jsonl` + `regress_fast.py`),人工核查 SQL 见 `beizhu.md` |

## 2. 关键约束 / 不能动的部分

1. **解析逻辑是核心资产**:`parser/base_parser.py`(大文件,规则密集,含大量边界注释)与各
   `*_parser.py` 的业务判定不得随意改。本次唯一允许的解析层改动是在 `field_mapping.map_row`
   **透传**来源表头(`unit_headers`),映射结果必须逐字段不变;改任何映射规则前,先用同一批
   表头文本对拍 `match_field` 新旧行为(本次对拍 ~180 条,0 差异)。
2. **schema 三处必须齐平**:改表结构时 `CREATE TABLE` 常量(文件顶部)、`INSERT_*_SQL`、
   `_normalize_project/_normalize_file` 的键必须同步改,否则入库报参数缺失。已建库的演进
   只能走 `init_db()` 的 `_ensure_column` / `_drop_column_if_exists`(DDL 为代码内常量),
   不要手工改库、不要另写迁移脚本。
3. **SQL 全参数化**(`%s` / `%(name)s`),列名走白名单或代码常量,禁止拼接。
4. **稳健性契约**:单文件失败不中断整个目录;通知/分类统计/单位等附加入库失败不影响主流程;
   同目录重复执行幂等(SHA-256 去重)。
5. **不要碰**:`backups/`、`analy/` 下的基线产物(`baseline_*.jsonl`、`noise_sheets.json`)、
    / `extra_stats.py` / `batch_test.py` / `full_scan.py` 等分析脚本、
   `beizhu.md`(人工核查 SQL 清单)。
6. **别随手跑全流程**:`main.py` / `run_single.py` / `batch_test.py` 都会执行 `init_db()`
   (会 DROP 列/表)并上传文件+写库。抽查验证只用 `parser.parse_file(path)` 做纯解析;
   按用户要求**不做全量回归,少数文件测试即可**。
7. **遗留 TODO**:`AsyncDB.get_company_id(unit_name)`(`util/db_util.py:452`)只有声明
   (`raise NotImplementedError`),`unit_id` 类型为 `BIGINT UNSIGNED`(单位为数字 ID),
   当前固定写 0;实现后填入 `_build_project_unit_rows`。
8. **数据影响(已确认可接受)**:`init_db()` 会 DROP `skp_project` 的三个旧单位列与
   `full_field_status` 列、DROP `skp_file_extra` 表,**历史值不回填**,需要历史数据请重跑源文件。
9. **现有非项目行检测逻辑**:备注、概述、category、type、group的检测，优先调用现有方法，修改其他问题是不单独对此类方法修改，需确认。
  方法|逻辑列举：
  前置过滤：
  │ is_prose_row / is_decor_text │ 装饰行（备注行首 / 正文标签 / ≥150字 / 概况总结句）→ 跳过，不参与分类分组
  │ is_business_data_row         │ 业务列（排除项目名；建设内容>20字）含真实文本 → 真数据行，全行文本不喂分类判断
  category（行业分类）：
  │ update_category_context │ 主入口。先剔行内纯数字 token → 结构门控（须含 序号/括号项数/罗马/——/行尾N个 等暗示）→ 按序匹配：①性质+括号项数→type ②纯性质词→type ③一、X→一级替换 ④（一）X→二级追加/同级替换 ⑤(1)X/-1 X/Ⅰ    │
  │                         │ X/①X→三级挂 dash_base ⑥——X→三级子分类 ⑦行尾N个→分类或type ⑧行尾（N）→须命中分类词 ⑨兜底：去序号整段，护栏≤24字且无句读                                                                        │
  │ apply_category          │ 包装：调 update_category_context + 收集（共N项）声明数                                                                                                                                        │
  │ classify_single_row     │ 单格行版：同上模式（序号+分类/性质词/机构名/罗马/括号序号），外加 _relax ≤12字放宽                                                                                                            │
  │ _looks_like_category    │ 强词≤12字 / 弱词≤6字 / 补充词全等 / 括号项数                                                                                                                                                  │
  │ _clean_category_name    │ 清洗：去序号、括号统计、省略号、行尾金额、性质后缀                                                                                                                                            │
  │ _set_category           │ 写入 context；明细/合计/性质混合不设；重置 dash_base                                                                                                                                          │
  │ _record_declared        │ 抽（共N项）数字存 context 供校验                                                                                                                                                              │
  │ _is_section_head        │ bare 段落模式：序号前缀+分类词尾 → 分区启动信号                                                                                                                                               │
  project_type（建设性质）：
  │ group_type_title                                           │ 形态1：单格纯性质词行（续建）；形态2（需 header_map）：首列空+名称列全词性质词+项目（计划新开工项目→新开工） │
  │ _is_type_title                                             │ 子标题=性质词/性质词+项目 → 只设 type 不设 category                                                          │
  │ （内置于 update_category_context / map_row / parse_lines） │ 性质+括号项数、文本中部性质词、行尾N个性质开头、建设性质列、续建项目：组头行                                 │
  group（责任单位/地区分组 → 跳过）
  │ group_type_title                                           │ 形态1：单格纯性质词行（续建）；形态2（需 header_map）：首列空+名称列全词性质词+项目（计划新开工项目→新开工） │
  │ _is_type_title                                             │ 子标题=性质词/性质词+项目 → 只设 type 不设 category                                                          │
  │ （内置于 update_category_context / map_row / parse_lines） │ 性质+括号项数、文本中部性质词、行尾N个性质开头、建设性质列、续建项目：组头行                                 │
  group（责任单位/地区分组 → 跳过）
  │ is_group_header_row  │ 多列表：首列空 + 名称列机构后缀 + 非空列≤max(2, normal_cols−2) + 计数特征（N项或1–999整数）         │
  │ is_group_row         │ 单格行：区划尾 县/州/盟/省 任意长；市/区 ≤5字且行内无数字；机构名≤14字（场所尾"厅"如餐厅/展厅排除） │
  │ is_group_row_minimal │ 极简表（≤1列映射）窄化版：同上但机构不含 集团/公司/学院/研究院；allow_city=False 关闭市/区分支      │
  │ _is_count_value      │ 计数特征：N项 或整数 1–999（含 4.0）                                                                │

  判定顺序（xlsx 与 extract_rows_from_table 共用）：prose → 窄化分组(≤1列) → 多列分组 → 首列空跳过 → group_type_title → apply_category → classify_single_row(单格) → map_row。

## 3. 本次改动落点

**`parser/base_parser.py`,`parser/docx_parser.py`**

## 4. 示例文件
-  1. 2023年重点项目\03天津市2023年重点项目清单\2023年西青区\西青区2023年重点项目清单.docx
-  2. 2023年重点项目\20湖南省2023年重点项目清单\2023年湖南省重点建议项目.docx
-  3. 2025年重点项目\02上海市2025年重点项目清单\临港新片区2025年\2025年临港新片区重大项目清单.docx
-  4. 2025年重点项目\13广东省2025年重点项目清单\珠海市2025年\珠海市2025年重点建设项目计划清单.docx
-  5. 2026年重点项目\02上海市2026年重点项目清单\2026年临港新片区\2026年临港新片区重大项目清单.docx
-  6. 2025年重点项目\02上海市2025年重点项目清单\松江区2025年\2025年松江区重大建设项目清单.docx
-  7. 2023年重点项目\20湖南省2023年重点项目清单\湖南5.png

## 5. 存在情况
- 图片格式的项目清单。
- 存在于docx文件或以图片形式出现。

## 6. 需要解决
- 目前没有图片解析，补充图片解析，正确解析项目名单。
- 不干扰其他文件解析。
- 单独的图片解析、docx中的图片解析采用一套逻辑。
- 思路清晰，结构清晰。

## 7. 要求
- 在关键约束 / 不能动的部分 的要求下补充：
- 先定位根因，用 5 行内说明；不确定先问我，不要猜、不要编造文件或 API。
- 找原因，提方案，待确定方案，再修改代码。
- 最小改动。
- 遵循现有代码风格、命名、类型、错误处理、日志规范。
- 保证正确性：覆盖空值、异常、边界、并发；不破坏现有接口和功能。
- 兼顾效率：避免 N+1、重复计算、无意义拷贝；性能优化需说明依据。
- 如果上下文不足，先列出需要我提供的文件/片段，不要编造。
- 先正确，再高效；不为了性能牺牲可读性和正确性。
- 算法和数据结构合理，避免 O(n²)、N+1 查询、重复计算。
- 限制每次输出 token，低于5k，避免再次超上下文。
- 修改完成之后，梳理更新skilldraft.md。


## 6. 验证方式

- 修改之后少量文件测试，不全量。快速回归。

