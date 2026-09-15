## 检查记录
### 1. project_name过短；
    SELECT
    f.id AS fileId,
    f.file_path,
    p.project_name,source_row,project_type,category,construction_content,location,extra_info,total_investment,annual_investment,annual_goal,start_year,end_year,remark
    FROM skp_file f
    LEFT JOIN skp_project p ON p.file_id = f.id
		where length(project_name) <10;
### 2. project_name末尾包含 \d+个|项[)）]
    SELECT
    f.id AS fileId,
    f.file_path,
    p.project_name,source_row,project_type,category,construction_content,location,extra_info,total_investment,annual_investment,annual_goal,start_year,end_year,remark
    FROM skp_file f
    LEFT JOIN skp_project p ON p.file_id = f.id
	where p.project_name REGEXP '[(（][0-9]+个[)）]+$';
### 3. category过长
    		SELECT
    p.category,                -- 分类在项目表
    COUNT(*) AS count_num      -- 统计项目条数
    FROM skp_file f
    JOIN skp_project p ON p.file_id = f.id   -- 必须 JOIN，因为 category 在 p 表
    WHERE f.file_name REGEXP 'xlsx'
    GROUP BY p.category HAVING length(p.category)>30 ORDER BY length(p.category);            -- 按项目表的分类分组
### 4. 解析项目条数过少
    SELECT
    f.file_path,count(f.file_path) as file_path_num
        FROM skp_file f
        LEFT JOIN skp_project p ON p.file_id = f.id
             GROUP BY f.file_path ORDER BY file_path_num;
### 5. 同文件中，无详情项目数与项目总数不一致
    WITH file_stats AS (
    SELECT
        file_id,
        COUNT(*) AS total_count,
        SUM(
            CASE
                WHEN location = ''
                 AND construction_content = ''
                 AND start_year = ''
                THEN 1
                ELSE 0
            END
        ) AS qualified_count
    FROM skp_project
    GROUP BY file_id
    )
    SELECT
        f.id AS fileId,
        f.file_path,
        s.qualified_count AS 符合项目数,
        s.total_count AS 原始项目总数
    FROM skp_file f
    INNER JOIN file_stats s ON f.id = s.file_id
    WHERE s.qualified_count > 0
      AND s.qualified_count < s.total_count
    ORDER BY s.qualified_count;

### 6. 县区市省政府等机构名称被识别为项目：
    SELECT
    f.id AS fileId,
    f.file_path,
    p.project_name,source_row,project_type,category,construction_content,location,extra_info,total_investment,annual_investment,annual_goal,start_year,end_year,remark
    FROM skp_file f
    LEFT JOIN skp_project p ON p.file_id = f.id
		where project_name REGEXP '市$|区$|县$|州$|盟$|省$|人民政府$|政府$|厅$|局$|委$|办$|管委会$|集团$|公司$';

### 7. 每个文件展示5条
    WITH ranked AS (
    SELECT
        f.id AS file_id,
        f.file_path,
        p.project_name,source_row,project_type,category,construction_content,location,extra_info,total_investment,annual_investment,annual_goal,start_year,end_year,remark,
        ROW_NUMBER() OVER (PARTITION BY f.id ORDER BY p.id) AS rn   -- 按文件分组，按项目ID排序取前5
    FROM skp_file f
    LEFT JOIN skp_project p ON p.file_id = f.id 
		where f.file_name REGEXP 'docx'
    )
    SELECT file_id, file_path, project_name,source_row,project_type,category,construction_content,location,extra_info,total_investment,annual_investment,annual_goal,start_year,end_year,remark
    FROM ranked
    WHERE rn <= 5;

## 特殊文件格式xlsx
### 1. 2025年重点项目\04重庆市2025年重点项目清单\璧山区2025年\2025年璧山区重点项目清单.xlsx
## docx没表格：
    1. 2023年重点项目\26山东省2023年重点项目清单\附件：2023年山东省重点项目名单.docx
    2. 2025年重点项目\02上海市2025年重点项目清单\嘉定区2025年\2025年嘉定区重大工程项目.docx
    
## 前面干扰数据
    1. 2022年重点项目\08西藏自治区2022年重点项目清单\2021西藏自治区招商引资项目WORD.docx
## 清单截图
    1. 2023年重点项目\03天津市2023年重点项目清单\2023年西青区\西青区2023年重点项目清单.docx
    2. 2023年重点项目\20湖南省2023年重点项目清单\2023年湖南省重点建议项目.docx
    3. 2024年重点项目\19湖北省2024年重点项目清单\十堰市2024年\十堰市2024年省级重点项目清单.docx
    4. 2025年重点项目\02上海市2025年重点项目清单\临港新片区2025年\2025年临港新片区重大项目清单.docx
    5. 2025年重点项目\13广东省2025年重点项目清单\珠海市2025年\珠海市2025年重点建设项目计划清单.docx
    6. 2026年重点项目\02上海市2026年重点项目清单\2026年临港新片区\2026年临港新片区重大项目清单.docx
    7. 2025年重点项目\02上海市2025年重点项目清单\松江区2025年\2025年松江区重大建设项目清单.docx
## 图片(docx解析图片&图片文件解析)
    1. "E:\STangWork\STangFiles\各省重点项目：2020年起\2023年重点项目\20湖南省2023年重点项目清单\湖南5.png"

## 存在合并单元格作为分类的情况
    1. 2023年重点项目\22江苏省2023年重点项目清单\2023年宿迁市\迁市2023年中心城市建设重点工程计划.docx
    2. 2024年重点项目\22江苏省2024年重点项目清单\宿迁市2024年\宿迁市2024年中心城市建设重点工程计划.docx
    3. 2025年重点项目\22江苏省2025年重点项目清单\宿迁市2025年\宿迁市2025年中心城市建设重点工程计划.docx
    
## 解析失败: 不支持的扩展名: .doc,
    1. 2024年重点项目\11福建省2024年重点项目清单\泉州市2024年\2024年度泉州市重点项目名单.docx

![img_1.png](img_1.png)
    
    "综合体项目"单独为一行。现有逻辑会将其识别为分类。（没法处理了）

   其他示例：2025年重点项目\04重庆市2025年重点项目清单\重庆市2025年市级重点项目.xlsx。相关查询语句：
    
        sql :
        SELECT
            f.id AS fileId,
            f.file_path,
            COUNT(p.file_id) AS file_num
        FROM skp_file f
        LEFT JOIN skp_project p 
            ON p.file_id = f.id
            AND p.location = ''
            AND p.construction_content = ''
            AND p.start_year = ''
            AND (p.extra_info = '' OR p.extra_info IS NULL)
        GROUP BY f.id, f.file_path
        ORDER BY file_num;
### 2. 