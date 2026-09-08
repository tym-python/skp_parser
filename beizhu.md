## 检查记录
### 1. project_name过短；
    SELECT
    f.id AS fileId,
    f.file_path,
    p.*,
    e.extra_info
    FROM skp_file f
    LEFT JOIN skp_project p ON p.file_id = f.id
    LEFT JOIN skp_file_extra e ON e.project_id = p.id
		where length(project_name) <10;
### 2. project_name末尾包含 \d+个|项[)）]
    SELECT
    f.id AS fileId,
    f.file_path,
    p.*,
    e.extra_info
    FROM skp_file f
    LEFT JOIN skp_project p ON p.file_id = f.id
    LEFT JOIN skp_file_extra e ON e.project_id = p.id 
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
        LEFT JOIN skp_file_extra e ON e.project_id = p.id 
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
    p.*,
    e.extra_info
    FROM skp_file f
    LEFT JOIN skp_project p ON p.file_id = f.id
    LEFT JOIN skp_file_extra e ON e.project_id = p.id
		where project_name REGEXP '市$|区$|县$|州$|盟$|省$|人民政府$|政府$|厅$|局$|委$|办$|管委会$|集团$|公司$';



## 特殊文件格式xlsx
### 1. 2025年重点项目\04重庆市2025年重点项目清单\璧山区2025年\2025年璧山区重点项目清单.xlsx

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
        LEFT JOIN skp_file_extra e 
            ON e.project_id = p.id
            AND (e.extra_info = '' OR e.extra_info IS NULL)
        GROUP BY f.id, f.file_path
        ORDER BY file_num;
### 2. 