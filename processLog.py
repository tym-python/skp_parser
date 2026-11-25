import re
log = r'''(py312_stc) PS E:\STangWork\PythonProjects\skp_parser> python batch_test.py png
本次批量解析状态：文件类型：png，是否上传：False，数据库地址：local

2026-11-06 17:17:12 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 批量测试: E:\STangWork\STangFiles\各省重点项目：2020年起 下 png 文件 438 个(上传 GoFast: False)
2026-11-06 17:17:12 - E:\STangWork\PythonProjects\skp_parser\util\db_util.py - INFO - 数据库连接池已创建: 127.0.0.1:3306/suidaobig
E:\miniconda3\envs\py312_stc\Lib\site-packages\aiomysql\cursors.py:458: Warning: Table 'skp_file' already exists
  await self._do_get_result()
E:\miniconda3\envs\py312_stc\Lib\site-packages\aiomysql\cursors.py:458: Warning: Table 'skp_project' already exists
  await self._do_get_result()
E:\miniconda3\envs\py312_stc\Lib\site-packages\aiomysql\cursors.py:458: Warning: Table 'skp_project_unit' already exists
  await self._do_get_result()
E:\miniconda3\envs\py312_stc\Lib\site-packages\aiomysql\cursors.py:458: Warning: Table 'skp_notice' already exists
  await self._do_get_result()
E:\miniconda3\envs\py312_stc\Lib\site-packages\aiomysql\cursors.py:458: Warning: Table 'skp_category_declared' already exists
  await self._do_get_result()
2026-11-06 17:17:12 - E:\STangWork\PythonProjects\skp_parser\util\db_util.py - INFO - 数据库表初始化完成(skp_file/skp_project/skp_project_unit/skp_notice/skp_category_declared)
2026-11-06 17:17:12 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 陕西省2021年重点建设项目分布.png - 跳过该文件（filter_file.txt）
2026-11-06 17:17:12 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 0.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
[INFO] 2026-11-06 17:17:13,599 [RapidOCR] base.py:23: Using engine_name: onnxruntime
[INFO] 2026-11-06 17:17:13,704 [RapidOCR] download_file.py:60: File exists and is valid: E:\miniconda3\envs\py312_stc\Lib\site-packages\rapidocr\models\PP-OCRv6_det_small.onnx
[INFO] 2026-11-06 17:17:13,705 [RapidOCR] main.py:63: Using E:\miniconda3\envs\py312_stc\Lib\site-packages\rapidocr\models\PP-OCRv6_det_small.onnx
[INFO] 2026-11-06 17:17:13,783 [RapidOCR] base.py:23: Using engine_name: onnxruntime
[INFO] 2026-11-06 17:17:13,787 [RapidOCR] download_file.py:60: File exists and is valid: E:\miniconda3\envs\py312_stc\Lib\site-packages\rapidocr\models\ch_ppocr_mobile_v2.0_cls_mobile.onnx
[INFO] 2026-11-06 17:17:13,787 [RapidOCR] main.py:63: Using E:\miniconda3\envs\py312_stc\Lib\site-packages\rapidocr\models\ch_ppocr_mobile_v2.0_cls_mobile.onnx
[INFO] 2026-11-06 17:17:13,845 [RapidOCR] base.py:23: Using engine_name: onnxruntime
[INFO] 2026-11-06 17:17:13,894 [RapidOCR] download_file.py:60: File exists and is valid: E:\miniconda3\envs\py312_stc\Lib\site-packages\rapidocr\models\PP-OCRv6_rec_small.onnx
[INFO] 2026-11-06 17:17:13,894 [RapidOCR] main.py:63: Using E:\miniconda3\envs\py312_stc\Lib\site-packages\rapidocr\models\PP-OCRv6_rec_small.onnx
OCR 结果疑似乱码（items=2, 乱码分=15.00），跳过解析
2026-11-06 17:17:14 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2022年重点项目\0.png: 图片未识别到文本(疑似非清单图片)
2026-11-06 17:17:14 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 0.png (file_id=13072, 项目 0 条)
2026-11-06 17:17:14 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 171个地市级.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:17:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 171个地市级.png (file_id=13073, 项目 0 条)
2026-11-06 17:17:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_10.png(文件 1 条, 项目 18 条, 通知 0 条, 分类声明 2 条)
2026-11-06 17:17:21 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_10.png] 商贸产业: 标题声明 9 项,解析 1 项
2026-11-06 17:17:21 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_10.png: No /Root object! - Is this really a PDF?
E:\miniconda3\envs\py312_stc\Lib\site-packages\aiomysql\cursors.py:458: Warning: 'VALUES function' is deprecated and will be removed in a future release. Please use an alias (INSERT INTO ... VALUES (...) AS alias) and replace VALUES(col) in the ON DUPLICATE KEY UPDATE clause with alias.col instead
  await self._do_get_result()
2026-11-06 17:17:21 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_10.png (file_id=13074, 项目 19 条)
2026-11-06 17:17:22 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_11.png(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:17:24 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_11.png] 商务服务产业: 标题声明 22 项,解析 12 项
2026-11-06 17:17:24 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_11.png: No /Root object! - Is this really a PDF?
2026-11-06 17:17:24 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_11.png (file_id=13075, 项目 20 条)
2026-11-06 17:17:24 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_12.png(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:17:26 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_12.png] 文化创意产业: 标题声明 19 项,解析 10 项
2026-11-06 17:17:26 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_12.png: No /Root object! - Is this really a PDF?
2026-11-06 17:17:27 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_12.png (file_id=13076, 项目 20 条)
2026-11-06 17:17:27 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_13.png(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:17:29 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_13.png] 现代高效农业产业: 标题声明 14 项,解析 11 项
2026-11-06 17:17:29 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_13.png: No /Root object! - Is this really a PDF?
2026-11-06 17:17:29 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_13.png (file_id=13077, 项目 20 条)
2026-11-06 17:17:29 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_14.png(文件 1 条, 项目 18 条, 通知 0 条, 分类声明 3 条)
2026-11-06 17:17:31 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_14.png] 新能源新材料产业: 标题声明 32 项,解析 1 项
2026-11-06 17:17:31 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_14.png: No /Root object! - Is this really a PDF?
2026-11-06 17:17:31 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_14.png (file_id=13078, 项目 18 条)
2026-11-06 17:17:31 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_15.png(文件 1 条, 项目 21 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:17:33 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_15.png: No /Root object! - Is this really a PDF?
2026-11-06 17:17:34 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_15.png (file_id=13079, 项目 21 条)
2026-11-06 17:17:34 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_16.png(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:17:36 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_16.png] 新一代信息技术产业: 标题声明 34 项,解析 10 项
2026-11-06 17:17:36 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_16.png: No /Root object! - Is this really a PDF?
2026-11-06 17:17:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_16.png (file_id=13080, 项目 20 条)
2026-11-06 17:17:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_17.png(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:17:38 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_17.png: No /Root object! - Is this really a PDF?
2026-11-06 17:17:38 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_17.png (file_id=13081, 项目 19 条)
2026-11-06 17:17:38 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_18.png(文件 1 条, 项目 18 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:17:40 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_18.png] 医养健康产业: 标题声明 26 项,解析 13 项
2026-11-06 17:17:40 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_18.png: No /Root object! - Is this really a PDF?
2026-11-06 17:17:41 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_18.png (file_id=13082, 项目 18 条)
2026-11-06 17:17:47 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_19.png(文件 1 条, 项目 18 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:17:49 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_19.png] 基础设施: 标题声明 12 项,解析 5 项
2026-11-06 17:17:49 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_19.png: No /Root object! - Is this really a PDF?
2026-11-06 17:17:49 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_19.png (file_id=13083, 项目 18 条)
2026-11-06 17:17:49 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_20.png(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
横线分布不合理
2026-11-06 17:17:50 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_20.png: No /Root object! - Is this really a PDF?
2026-11-06 17:17:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_20.png (file_id=13084, 项目 4 条)
2026-11-06 17:17:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_21.png(文件 1 条, 项目 16 条, 通知 0 条, 分类声明 3 条)
2026-11-06 17:17:53 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_21.png] 高端装备产业: 标题声明 33 项,解析 4 项
2026-11-06 17:17:53 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_21.png: No /Root object! - Is this really a PDF?
2026-11-06 17:17:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_21.png (file_id=13085, 项目 16 条)
2026-11-06 17:17:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_22.png(文件 1 条, 项目 21 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:17:55 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_22.png: No /Root object! - Is this really a PDF?
2026-11-06 17:17:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_22.png (file_id=13086, 项目 21 条)
2026-11-06 17:17:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_23.png(文件 1 条, 项目 18 条, 通知 0 条, 分类声明 3 条)
2026-11-06 17:17:57 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_23.png] 商务服务产业: 标题声明 11 项,解析 6 项
2026-11-06 17:17:57 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_23.png: No /Root object! - Is this really a PDF?
2026-11-06 17:17:58 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_23.png (file_id=13087, 项目 18 条)
2026-11-06 17:17:58 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_24.png(文件 1 条, 项目 18 条, 通知 0 条, 分类声明 3 条)
2026-11-06 17:18:00 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_24.png] 现代金融服务产业: 标题声明 2 项,解析 1 项
2026-11-06 17:18:00 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_24.png: No /Root object! - Is this really a PDF?
2026-11-06 17:18:01 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_24.png (file_id=13088, 项目 18 条)
2026-11-06 17:18:01 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_25.png(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 2 条)
2026-11-06 17:18:03 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_25.png] 新一代信息技术产业: 标题声明 13 项,解析 4 项
2026-11-06 17:18:03 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_25.png: No /Root object! - Is this really a PDF?
2026-11-06 17:18:03 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_25.png (file_id=13089, 项目 19 条)
2026-11-06 17:18:03 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_26.png(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 2 条)
2026-11-06 17:18:05 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_26.png] 基础设施: 标题声明 7 项,解析 2 项
2026-11-06 17:18:05 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_26.png: No /Root object! - Is this really a PDF?
2026-11-06 17:18:05 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_26.png (file_id=13090, 项目 19 条)
2026-11-06 17:18:06 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_27.png(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
横线分布不合理
2026-11-06 17:18:07 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_27.png: No /Root object! - Is this really a PDF?
2026-11-06 17:18:07 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_27.png (file_id=13091, 项目 5 条)
2026-11-06 17:18:07 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_5.png(文件 1 条, 项目 18 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:18:09 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_5.png] 现代海洋产业: 标题声明 19 项,解析 18 项
2026-11-06 17:18:09 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_5.png: No /Root object! - Is this really a PDF?
2026-11-06 17:18:10 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_5.png (file_id=13092, 项目 18 条)
2026-11-06 17:18:10 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_6.png(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:18:18 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_6.png: No /Root object! - Is this really a PDF?
2026-11-06 17:18:18 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_6.png (file_id=13093, 项目 20 条)
2026-11-06 17:18:18 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_7.png(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:18:21 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_7.png] 高端装备产业: 标题声明 67 项,解析 20 项
2026-11-06 17:18:21 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_7.png: No /Root object! - Is this really a PDF?
2026-11-06 17:18:21 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_7.png (file_id=13094, 项目 20 条)
2026-11-06 17:18:21 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_8.png(文件 1 条, 项目 21 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:18:23 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_8.png: No /Root object! - Is this really a PDF?
2026-11-06 17:18:23 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_8.png (file_id=13095, 项目 21 条)
2026-11-06 17:18:24 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_9.png(文件 1 条, 项目 21 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:18:26 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 通知信息解析失败 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_9.png: No /Root object! - Is this really a PDF?
2026-11-06 17:18:27 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 青政字[2022]1号-关于公布青岛市2022年重点项目名单的通知_9.png (file_id=13096, 项目 21 条)
2026-11-06 17:18:27 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 清单列表.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
横线分布不合理
2026-11-06 17:18:29 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 清单列表.png (file_id=13097, 项目 0 条)
2026-11-06 17:18:29 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 订阅.png - 跳过该文件（filter_file.txt）
2026-11-06 17:18:29 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 北京市2023年重点工程计划_1.png(文件 1 条, 项目 18 条, 通知 0 条, 分类声明 2 条)
2026-11-06 17:18:33 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[北京市2023年重点工程计划_1.png] 重大科技设施平台集群: 标题声明 9 项,解析 18 项
2026-11-06 17:18:33 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[北京市2023年重点工程计划_1.png] 重大科技设施平台集群-先进制造业: 标题声明 35 项,解析 9 项
2026-11-06 17:18:33 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 北京市2023年重点工程计划_1.png (file_id=13098, 项目 18 条)
2026-11-06 17:18:33 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 北京市2023年重点工程计划_10.png(文件 1 条, 项目 10 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:18:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 北京市2023年重点工程计划_10.png (file_id=13099, 项目 10 条)
2026-11-06 17:18:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 北京市2023年重点工程计划_11.png(文件 1 条, 项目 21 条, 通知 0 条, 分类声明 2 条)
2026-11-06 17:18:40 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[北京市2023年重点工程计划_11.png] 民生改善项目: 标题声明 100 项,解析 21 项
2026-11-06 17:18:40 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[北京市2023年重点工程计划_11.png] 民生改善项目-城市更新: 标题声明 8 项,解析 15 项
2026-11-06 17:18:40 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 北京市2023年重点工程计划_11.png (file_id=13100, 项目 21 条)
2026-11-06 17:18:41 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 北京市2023年重点工程计划_12.png(文件 1 条, 项目 24 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:18:44 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[北京市2023年重点工程计划_12.png] 医疗养老: 标题声明 17 项,解析 11 项
2026-11-06 17:18:44 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 北京市2023年重点工程计划_12.png (file_id=13101, 项目 24 条)
2026-11-06 17:18:45 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 北京市2023年重点工程计划_13.png(文件 1 条, 项目 24 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:18:49 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 北京市2023年重点工程计划_13.png (file_id=13102, 项目 24 条)
2026-11-06 17:18:49 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 北京市2023年重点工程计划_14.png(文件 1 条, 项目 22 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:18:52 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[北京市2023年重点工程计划_14.png] 消费新地标: 标题声明 6 项,解析 2 项
2026-11-06 17:18:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 北京市2023年重点工程计划_14.png (file_id=13103, 项目 22 条)
2026-11-06 17:18:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 北京市2023年重点工程计划_15.png(文件 1 条, 项目 9 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:18:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 北京市2023年重点工程计划_15.png (file_id=13104, 项目 9 条)
2026-11-06 17:18:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 北京市2023年重点工程计划_2.png(文件 1 条, 项目 24 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:19:00 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 北京市2023年重点工程计划_2.png (file_id=13105, 项目 24 条)
2026-11-06 17:19:00 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 北京市2023年重点工程计划_3.png(文件 1 条, 项目 22 条, 通知 0 条, 分类声明 3 条)
2026-11-06 17:19:03 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[北京市2023年重点工程计划_3.png] 服务业扩大开放: 标题声明 10 项,解析 21 项
2026-11-06 17:19:03 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[北京市2023年重点工程计划_3.png] 服务业扩大开放-金融业: 标题声明 7 项,解析 0 项
2026-11-06 17:19:03 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 北京市2023年重点工程计划_3.png (file_id=13106, 项目 22 条)
2026-11-06 17:19:04 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 北京市2023年重点工程计划_4.png(文件 1 条, 项目 24 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:19:07 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[北京市2023年重点工程计划_4.png] 科技创新空间资源: 标题声明 21 项,解析 17 项
2026-11-06 17:19:07 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 北京市2023年重点工程计划_4.png (file_id=13107, 项目 24 条)
2026-11-06 17:19:07 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 北京市2023年重点工程计划_5.png(文件 1 条, 项目 11 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:19:11 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 北京市2023年重点工程计划_5.png (file_id=13108, 项目 11 条)
2026-11-06 17:19:11 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 北京市2023年重点工程计划_6.png(文件 1 条, 项目 21 条, 通知 0 条, 分类声明 3 条)
2026-11-06 17:19:14 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[北京市2023年重点工程计划_6.png] 基础设施项目: 标题声明 100 项,解析 21 项
2026-11-06 17:19:14 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[北京市2023年重点工程计划_6.png] 基础设施项目-站城一体化交通枢纽: 标题声明 10 项,解析 3 项
2026-11-06 17:19:14 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 北京市2023年重点工程计划_6.png (file_id=13109, 项目 21 条)
2026-11-06 17:19:14 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 北京市2023年重点工程计划_7.png(文件 1 条, 项目 23 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:19:18 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[北京市2023年重点工程计划_7.png] 城市道路: 标题声明 20 项,解析 2 项
2026-11-06 17:19:18 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 北京市2023年重点工程计划_7.png (file_id=13110, 项目 23 条)
2026-11-06 17:19:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 北京市2023年重点工程计划_8.png(文件 1 条, 项目 24 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:19:22 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 北京市2023年重点工程计划_8.png (file_id=13111, 项目 24 条)
2026-11-06 17:19:22 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 北京市2023年重点工程计划_9.png(文件 1 条, 项目 22 条, 通知 0 条, 分类声明 2 条)
2026-11-06 17:19:26 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[北京市2023年重点工程计划_9.png] 固废处理: 标题声明 5 项,解析 6 项
2026-11-06 17:19:26 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[北京市2023年重点工程计划_9.png] 固废处理-新基建: 标题声明 11 项,解析 1 项
2026-11-06 17:19:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 北京市2023年重点工程计划_9.png (file_id=13112, 项目 22 条)
2026-11-06 17:19:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 重点.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=505, 乱码分=45.00），跳过解析
2026-11-06 17:19:42 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2023年重点项目\15海南省2023年重点项目清单\重点.png: 图片未识别到文本(疑似非清单图 片)                                                                                                                                                                                                                            
2026-11-06 17:19:42 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 重点.png (file_id=13113, 项目 0 条)
2026-11-06 17:19:43 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 预备.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:19:51 - E:\STangWork\PythonProjects\skp_parser\parser\base_parser.py - INFO - 未匹配到有效header_map
2026-11-06 17:19:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 预备.png (file_id=13114, 项目 0 条)
2026-11-06 17:19:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_1.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_10.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_11.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_12.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_13.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_14.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_15.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_16.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_17.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_18.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_19.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_2.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_20.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_21.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_22.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_23.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_24.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_25.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_26.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_27.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_28.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_29.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_3.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_30.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_31.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_32.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_33.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_34.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_35.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_36.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_37.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_38.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_39.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_4.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_40.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_41.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_42.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_43.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_44.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_45.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_46.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_47.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_48.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_49.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_5.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_50.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_51.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_52.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_53.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_54.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_6.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_7.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_8.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_9.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_1.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_10.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_11.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_12.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_13.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_14.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_15.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_16.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_17.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_18.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_19.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_2.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_20.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_21.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_22.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_23.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_24.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_25.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_26.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_27.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_28.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_29.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_3.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_30.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_31.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_32.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_33.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_34.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_35.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_36.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_37.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_38.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_39.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_4.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_40.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_41.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_42.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_43.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_44.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_45.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_46.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_47.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_48.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_49.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_5.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_50.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_51.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_52.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_53.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_54.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_6.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_7.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_8.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 河北省2023年省重点建设项目名单_9.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 1.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
横线分布不合理
2026-11-06 17:19:57 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 1.png (file_id=13115, 项目 0 条)
2026-11-06 17:19:57 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2.png - 跳过该文件（filter_file.txt）
2026-11-06 17:19:57 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 十堰市2023年省级重点项目清单1.png(文件 1 条, 项目 23 条, 通知 0 条, 分类声明 4 条)
2026-11-06 17:20:07 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[十堰市2023年省级重点项目清单1.png] 重大产业发展类: 标题声明 6 项,解析 24 项
2026-11-06 17:20:07 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[十堰市2023年省级重点项目清单1.png] 重大产业发展类-重大基础设施类: 标题声明 10 项,解析 9 项
2026-11-06 17:20:07 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[十堰市2023年省级重点项目清单1.png] 重大产业发展类-社会民生保障类: 标题声明 5 项,解析 7 项
2026-11-06 17:20:07 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 十堰市2023年省级重点项目清单1.png (file_id=13116, 项目 24 条)
2026-11-06 17:20:08 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 十堰市2023年省级重点项目清单2.png(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:20:10 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 十堰市2023年省级重点项目清单2.png (file_id=13117, 项目 5 条)
2026-11-06 17:20:11 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 潜江市2023年省级重点项目建设清单.png(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:20:13 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 潜江市2023年省级重点项目建设清单.png (file_id=13118, 项目 3 条)
2026-11-06 17:20:14 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荆州市2023年省级重点项目清单.png(文件 1 条, 项目 50 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:20:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荆州市2023年省级重点项目清单.png (file_id=13119, 项目 50 条)
2026-11-06 17:20:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 湖南1.png(文件 1 条, 项目 39 条, 通知 0 条, 分类声明 5 条)
2026-11-06 17:20:23 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[湖南1.png] 铁路: 标题声明 6 项,解析 4 项
2026-11-06 17:20:23 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[湖南1.png] 高速公路: 标题声明 26 项,解析 25 项
2026-11-06 17:20:23 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[湖南1.png] 水运: 标题声明 8 项,解析 6 项
2026-11-06 17:20:23 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 湖南1.png (file_id=13120, 项目 39 条)
2026-11-06 17:20:23 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 湖南2.png(文件 1 条, 项目 54 条, 通知 0 条, 分类声明 3 条)
2026-11-06 17:20:27 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[湖南2.png] 城市建设-水利网: 标题声明 7 项,解析 0 项
2026-11-06 17:20:27 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[湖南2.png] 城市建设-能源网: 标题声明 26 项,解析 0 项
2026-11-06 17:20:27 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[湖南2.png] 城市建设-信息网: 标题声明 10 项,解析 0 项
2026-11-06 17:20:27 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 湖南2.png (file_id=13121, 项目 54 条)
2026-11-06 17:20:27 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 湖南3.png(文件 1 条, 项目 46 条, 通知 0 条, 分类声明 4 条)
2026-11-06 17:20:31 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[湖南3.png] 物流网-其他: 标题声明 1 项,解析 0 项
2026-11-06 17:20:31 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[湖南3.png] 生态环保: 标题声明 10 项,解析 9 项
2026-11-06 17:20:31 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[湖南3.png] 社会民生: 标题声明 15 项,解析 14 项
2026-11-06 17:20:31 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 湖南3.png (file_id=13122, 项目 46 条)
2026-11-06 17:20:31 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 湖南4.png(文件 1 条, 项目 54 条, 通知 0 条, 分类声明 3 条)
2026-11-06 17:20:35 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[湖南4.png] 产业发展: 标题声明 178 项,解析 26 项
2026-11-06 17:20:35 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[湖南4.png] 产业发展-汽车: 标题声明 5 项,解析 0 项
2026-11-06 17:20:35 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[湖南4.png] 产业发展-先进材料: 标题声明 23 项,解析 0 项
2026-11-06 17:20:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 湖南4.png (file_id=13123, 项目 54 条)
2026-11-06 17:20:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 湖南5.png(文件 1 条, 项目 52 条, 通知 0 条, 分类声明 4 条)
2026-11-06 17:20:39 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[湖南5.png] 电子信息-钢铁有色石化: 标题声明 18 项,解析 0 项
2026-11-06 17:20:39 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[湖南5.png] 电子信息-生物医药: 标题声明 9 项,解析 0 项
2026-11-06 17:20:39 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[湖南5.png] 电子信息-消费品产业: 标题声明 13 项,解析 0 项
2026-11-06 17:20:39 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 湖南5.png (file_id=13124, 项目 52 条)
2026-11-06 17:20:39 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 湖南6.png(文件 1 条, 项目 70 条, 通知 0 条, 分类声明 5 条)
2026-11-06 17:20:44 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[湖南6.png] 旅游康养-文化创意: 标题声明 5 项,解析 0 项
2026-11-06 17:20:44 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[湖南6.png] 旅游康养-科技创新: 标题声明 15 项,解析 0 项
2026-11-06 17:20:44 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[湖南6.png] 旅游康养-现代农业: 标题声明 11 项,解析 0 项
2026-11-06 17:20:44 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[湖南6.png] 旅游康养-园区基础设施: 标题声明 27 项,解析 0 项
2026-11-06 17:20:44 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 湖南6.png (file_id=13125, 项目 70 条)
2026-11-06 17:20:45 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2023年省重大项目清单（泰州）.png(文件 1 条, 项目 16 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:20:46 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2023年省重大项目清单（泰州）.png (file_id=13126, 项目 16 条)
2026-11-06 17:20:46 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2023绵阳1.png(文件 1 条, 项目 45 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:20:50 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2023绵阳1.png (file_id=13127, 项目 45 条)
2026-11-06 17:20:50 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2023绵阳2.png(文件 1 条, 项目 50 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:20:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2023绵阳2.png (file_id=13128, 项目 50 条)
2026-11-06 17:20:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2023绵阳3.png(文件 1 条, 项目 51 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:20:57 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2023绵阳3.png (file_id=13129, 项目 51 条)
2026-11-06 17:20:57 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2023绵阳4.png(文件 1 条, 项目 49 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:21:01 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2023绵阳4.png (file_id=13130, 项目 49 条)
2026-11-06 17:21:01 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2023绵阳5.png(文件 1 条, 项目 50 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:21:05 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2023绵阳5.png (file_id=13131, 项目 50 条)
2026-11-06 17:21:05 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2023绵阳6.png(文件 1 条, 项目 51 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:21:10 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2023绵阳6.png (file_id=13132, 项目 51 条)
2026-11-06 17:21:10 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2023绵阳7.png(文件 1 条, 项目 50 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:21:14 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2023绵阳7.png (file_id=13133, 项目 50 条)
2026-11-06 17:21:14 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2023绵阳8.png(文件 1 条, 项目 50 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:21:18 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2023绵阳8.png (file_id=13134, 项目 50 条)
2026-11-06 17:21:18 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2023绵阳9.png(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:21:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2023绵阳9.png (file_id=13135, 项目 3 条)
2026-11-06 17:21:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地市级102个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地市级121个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地市级136个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地市级146个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地市级158个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地市级189个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地市级25个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地市级33个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地市级43个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地市级59个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地市级61个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地市级65个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地市级80个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地市级97个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地市级清单.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地级市32个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地级市69个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 更新（10.23）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 更新（5.10）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 更新（5.23）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 更新（7.10）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 更新（7.25）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 更新（8.18）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 更新（9.20）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级清单.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级（2.16）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级（2.20）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级（3.14）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级（3.1）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级（3.20）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级（3.28）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级（3.3）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级（3.4）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级（4.18）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级（4.27）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级（7.10）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:21:21 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 轮播图_1.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=5, 乱码分=55.00），跳过解析
2026-11-06 17:21:22 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2023年重点项目\轮播图\轮播图_1.png: 图片未识别到文本(疑似非清单图片)
2026-11-06 17:21:22 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 轮播图_1.png (file_id=13136, 项目 0 条)
2026-11-06 17:21:22 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 重大项目.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=2, 乱码分=15.00），跳过解析
2026-11-06 17:21:23 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2023年重点项目\重大项目.png: 图片未识别到文本(疑似非清单图片)
2026-11-06 17:21:23 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 重大项目.png (file_id=13137, 项目 0 条)
2026-11-06 17:21:23 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 重点项目清单.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=116, 乱码分=70.00），跳过解析
2026-11-06 17:21:32 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2024年重点项目\02上海市2024年重点项目清单\徐汇区2024年\重点项目清单.png: 图片未识 别到文本(疑似非清单图片)                                                                                                                                                                                                       
2026-11-06 17:21:33 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 重点项目清单.png (file_id=13138, 项目 0 条)
2026-11-06 17:21:33 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 金山2024年重大工程（新开）一览表.png(文件 1 条, 项目 27 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:21:42 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 金山2024年重大工程（新开）一览表.png (file_id=13139, 项目 27 条)
2026-11-06 17:21:42 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 金山2024年重大工程（结转）一览表.png(文件 1 条, 项目 52 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:21:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 金山2024年重大工程（结转）一览表.png (file_id=13140, 项目 52 条)
2026-11-06 17:21:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年仙桃市省级重点项目清单1.png.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:21:56 - E:\STangWork\PythonProjects\skp_parser\parser\base_parser.py - INFO - 未匹配到有效header_map
2026-11-06 17:21:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年仙桃市省级重点项目清单1.png.png (file_id=13141, 项目 0 条)
2026-11-06 17:21:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年仙桃市省级重点项目清单2.png.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:21:59 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年仙桃市省级重点项目清单2.png.png (file_id=13142, 项目 0 条)
2026-11-06 17:21:59 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年仙桃市省级重点项目清单3.png.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:22:01 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年仙桃市省级重点项目清单3.png.png (file_id=13143, 项目 0 条)
2026-11-06 17:22:01 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荆州市2024年省级重点项目清单.png(文件 1 条, 项目 51 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:22:06 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荆州市2024年省级重点项目清单.png (file_id=13144, 项目 51 条)
2026-11-06 17:22:07 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024重大项目.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=2, 乱码分=0.00），跳过解析
2026-11-06 17:22:07 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2024年重点项目\2024重大项目.png: 图片未识别到文本(疑似非清单图片)
2026-11-06 17:22:08 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024重大项目.png (file_id=13145, 项目 0 条)
2026-11-06 17:22:08 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.1.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:22:12 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.1.png (file_id=13146, 项目 0 条)
2026-11-06 17:22:13 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.10.png(文件 1 条, 项目 2 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:22:17 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.10.png (file_id=13147, 项目 2 条)
2026-11-06 17:22:17 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.11.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:22:22 - E:\STangWork\PythonProjects\skp_parser\parser\base_parser.py - INFO - 未匹配到有效header_map
2026-11-06 17:22:22 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.11.png (file_id=13148, 项目 0 条)
2026-11-06 17:22:22 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.12.png(文件 1 条, 项目 8 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:22:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.12.png (file_id=13149, 项目 10 条)
2026-11-06 17:22:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.13.png(文件 1 条, 项目 6 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:22:31 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.13.png (file_id=13150, 项目 6 条)
2026-11-06 17:22:31 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.14.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:22:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.14.png (file_id=13151, 项目 0 条)
2026-11-06 17:22:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.15.png(文件 1 条, 项目 8 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:22:40 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.15.png (file_id=13152, 项目 8 条)
2026-11-06 17:22:40 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.16.png(文件 1 条, 项目 8 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:22:45 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.16.png (file_id=13153, 项目 11 条)
2026-11-06 17:22:45 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.17.png(文件 1 条, 项目 8 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:22:49 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.17.png (file_id=13154, 项目 8 条)
2026-11-06 17:22:49 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.18.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:22:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.18.png (file_id=13155, 项目 0 条)
2026-11-06 17:22:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.19.png(文件 1 条, 项目 11 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:22:59 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.19.png (file_id=13156, 项目 11 条)
2026-11-06 17:23:00 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.2.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:23:04 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.2.png (file_id=13157, 项目 0 条)
2026-11-06 17:23:04 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.20.png(文件 1 条, 项目 8 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:23:09 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.20.png (file_id=13158, 项目 8 条)
2026-11-06 17:23:10 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.21.png(文件 1 条, 项目 6 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:23:14 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.21.png (file_id=13159, 项目 9 条)
2026-11-06 17:23:14 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.22.png(文件 1 条, 项目 9 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:23:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.22.png (file_id=13160, 项目 12 条)
2026-11-06 17:23:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.23.png(文件 1 条, 项目 9 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:23:24 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.23.png (file_id=13161, 项目 9 条)
2026-11-06 17:23:24 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.24.png(文件 1 条, 项目 7 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:23:29 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.24.png (file_id=13162, 项目 7 条)
2026-11-06 17:23:29 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.25.png(文件 1 条, 项目 8 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:23:33 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[徐州市2024年.25.png] 其他项目: 标题声明 1 项,解析 9 项
2026-11-06 17:23:33 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.25.png (file_id=13163, 项目 9 条)
2026-11-06 17:23:33 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.26.png(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:23:37 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.26.png (file_id=13164, 项目 7 条)
2026-11-06 17:23:37 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.3.png(文件 1 条, 项目 9 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:23:42 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.3.png (file_id=13165, 项目 9 条)
2026-11-06 17:23:42 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.4.png(文件 1 条, 项目 6 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:23:46 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.4.png (file_id=13166, 项目 6 条)
2026-11-06 17:23:46 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.5.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:23:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.5.png (file_id=13167, 项目 0 条)
2026-11-06 17:23:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.6.png(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:23:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.6.png (file_id=13168, 项目 3 条)
2026-11-06 17:23:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.7.png(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:23:59 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.7.png (file_id=13169, 项目 4 条)
2026-11-06 17:23:59 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.8.png(文件 1 条, 项目 10 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:24:03 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.8.png (file_id=13170, 项目 12 条)
2026-11-06 17:24:03 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 徐州市2024年.9.png(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:24:08 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 徐州市2024年.9.png (file_id=13171, 项目 9 条)
2026-11-06 17:24:09 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年广元市重点项目名单.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
[WARNING] 2026-11-06 17:24:16,686 [RapidOCR] main.py:132: The text detection result is empty
2026-11-06 17:24:16 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2024年重点项目\29四川省2024年重点项目清单\广元市2024年\2024年广元市重点项目名单.png: 图片未识别到文本(疑似非清单图片)                                                                                                                                                                                            
2026-11-06 17:24:16 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年广元市重点项目名单.png (file_id=13172, 项目 0 条)
2026-11-06 17:24:16 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024绵阳1.png(文件 1 条, 项目 14 条, 通知 0 条, 分类声明 4 条)
2026-11-06 17:24:19 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2024绵阳1.png] 基础设施: 标题声明 87 项,解析 15 项
2026-11-06 17:24:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024绵阳1.png (file_id=13173, 项目 15 条)
2026-11-06 17:24:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024绵阳10.png(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:24:22 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2024绵阳10.png] 教育、文化、体育及社会服务: 标题声明 34 项,解析 21 项
2026-11-06 17:24:22 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024绵阳10.png (file_id=13174, 项目 21 条)
2026-11-06 17:24:23 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024绵阳11.png(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:24:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024绵阳11.png (file_id=13175, 项目 20 条)
2026-11-06 17:24:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024绵阳12.png(文件 1 条, 项目 14 条, 通知 0 条, 分类声明 3 条)
2026-11-06 17:24:28 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2024绵阳12.png] 基础设施: 标题声明 48 项,解析 15 项
2026-11-06 17:24:28 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2024绵阳12.png] 基础设施-能源基础设施: 标题声明 6 项,解析 2 项
2026-11-06 17:24:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024绵阳12.png (file_id=13176, 项目 15 条)
2026-11-06 17:24:29 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024绵阳13.png(文件 1 条, 项目 17 条, 通知 0 条, 分类声明 2 条)
2026-11-06 17:24:31 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2024绵阳13.png] 水利基础设施: 标题声明 4 项,解析 13 项
2026-11-06 17:24:31 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2024绵阳13.png] 水利基础设施-城镇基础设施: 标题声明 17 项,解析 9 项
2026-11-06 17:24:32 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024绵阳13.png (file_id=13177, 项目 17 条)
2026-11-06 17:24:32 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024绵阳14.png(文件 1 条, 项目 16 条, 通知 0 条, 分类声明 2 条)
2026-11-06 17:24:35 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2024绵阳14.png] 产业项目: 标题声明 57 项,解析 0 项
2026-11-06 17:24:35 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2024绵阳14.png] 产业项目-制造业: 标题声明 29 项,解析 0 项
2026-11-06 17:24:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024绵阳14.png (file_id=13178, 项目 16 条)
2026-11-06 17:24:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024绵阳15.png(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:24:38 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024绵阳15.png (file_id=13179, 项目 19 条)
2026-11-06 17:24:38 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024绵阳16.png(文件 1 条, 项目 16 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:24:41 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2024绵阳16.png] 现代服务: 标题声明 16 项,解析 8 项
2026-11-06 17:24:42 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024绵阳16.png (file_id=13180, 项目 18 条)
2026-11-06 17:24:42 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024绵阳17.png(文件 1 条, 项目 18 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:24:45 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2024绵阳17.png] 现代农业: 标题声明 12 项,解析 10 项
2026-11-06 17:24:45 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024绵阳17.png (file_id=13181, 项目 18 条)
2026-11-06 17:24:45 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024绵阳18.png(文件 1 条, 项目 16 条, 通知 0 条, 分类声明 3 条)
2026-11-06 17:24:48 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2024绵阳18.png] 民生工程及社会事业项目: 标题声明 15 项,解析 14 项
2026-11-06 17:24:48 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024绵阳18.png (file_id=13182, 项目 16 条)
2026-11-06 17:24:48 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024绵阳19.png(文件 1 条, 项目 7 条, 通知 0 条, 分类声明 3 条)
2026-11-06 17:24:50 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024绵阳19.png (file_id=13183, 项目 7 条)
2026-11-06 17:24:50 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024绵阳2.png(文件 1 条, 项目 17 条, 通知 0 条, 分类声明 2 条)
2026-11-06 17:24:53 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2024绵阳2.png] 水利基础设施: 标题声明 14 项,解析 18 项
2026-11-06 17:24:53 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2024绵阳2.png] 水利基础设施-城镇基础设施: 标题声明 34 项,解析 4 项
2026-11-06 17:24:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024绵阳2.png (file_id=13184, 项目 18 条)
2026-11-06 17:24:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024绵阳3.png(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:24:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024绵阳3.png (file_id=13185, 项目 20 条)
2026-11-06 17:24:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024绵阳4.png(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:25:00 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024绵阳4.png (file_id=13186, 项目 19 条)
2026-11-06 17:25:01 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024绵阳5.png(文件 1 条, 项目 15 条, 通知 0 条, 分类声明 2 条)
2026-11-06 17:25:03 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2024绵阳5.png] 产业项目: 标题声明 68 项,解析 3 项
2026-11-06 17:25:03 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2024绵阳5.png] 产业项目-制造业: 标题声明 41 项,解析 3 项
2026-11-06 17:25:03 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024绵阳5.png (file_id=13187, 项目 18 条)
2026-11-06 17:25:04 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024绵阳6.png(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:25:07 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024绵阳6.png (file_id=13188, 项目 20 条)
2026-11-06 17:25:07 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024绵阳7.png(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:25:10 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2024绵阳7.png] 现代服务: 标题声明 17 项,解析 1 项
2026-11-06 17:25:10 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024绵阳7.png (file_id=13189, 项目 19 条)
2026-11-06 17:25:11 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024绵阳8.png(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:25:13 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2024绵阳8.png] 现代农业: 标题声明 10 项,解析 4 项
2026-11-06 17:25:14 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024绵阳8.png (file_id=13190, 项目 20 条)
2026-11-06 17:25:14 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024绵阳9.png(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 2 条)
2026-11-06 17:25:16 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2024绵阳9.png] 民生工程及社会事业项目: 标题声明 47 项,解析 13 项
2026-11-06 17:25:17 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024绵阳9.png (file_id=13191, 项目 19 条)
2026-11-06 17:25:17 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 禄丰市2024年重点建设项目清单（前期项目）1.png(文件 1 条, 项目 7 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:25:22 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 禄丰市2024年重点建设项目清单（前期项目）1.png (file_id=13192, 项目 7 条)
2026-11-06 17:25:22 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 禄丰市2024年重点建设项目清单（前期项目）2.png(文件 1 条, 项目 9 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:25:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 禄丰市2024年重点建设项目清单（前期项目）2.png (file_id=13193, 项目 9 条)
2026-11-06 17:25:27 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 禄丰市2024年重点建设项目清单（前期项目）3.png(文件 1 条, 项目 8 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:25:31 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 禄丰市2024年重点建设项目清单（前期项目）3.png (file_id=13194, 项目 8 条)
2026-11-06 17:25:31 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 禄丰市2024年重点建设项目清单（前期项目）4.png(文件 1 条, 项目 6 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:25:34 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 禄丰市2024年重点建设项目清单（前期项目）4.png (file_id=13195, 项目 6 条)
2026-11-06 17:25:34 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2024.11.28新增40家.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2024.3.26新增10家.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2024.4.22新增8家.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2024.4.5新增20家.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2024.6.25新增28家.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2024.7.23新增4家.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地级市项目清单（截止2024.3.12）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 更新项目清单（截止2024.11.28）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 更新项目清单（截止2024.3.22）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 更新项目清单（截止2024.3.26）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 更新项目清单（截止2024.4.22）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 更新项目清单（截止2024.4.5）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 更新项目清单（截止2024.6.26）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级清单（16个）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 轮播图.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 项目清单（118个地级市）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 项目清单（138个地级市）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 项目清单（146个地级市）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 项目清单（174个地级市）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 项目清单（2.15）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 项目清单（2.4）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 项目清单（27个地级市）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 项目清单（29个地级市）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 项目清单（3.1）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 项目清单（3.26）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 项目清单（35个地级市）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 项目清单（4.22）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 项目清单（4.5）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 项目清单（40个地级市）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 项目清单（6.25）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 项目清单（6.26）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 项目清单（60个地级市）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 项目清单（63个地级市）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 项目清单（78个地级市） .png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 项目清单（78个地级市）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:25:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 金山区2025年重大工程（新开）一览表.png(文件 1 条, 项目 25 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:25:41 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 金山区2025年重大工程（新开）一览表.png (file_id=13196, 项目 25 条)
2026-11-06 17:25:42 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 金山区2025年重大工程（结转）一览表.png(文件 1 条, 项目 41 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:25:50 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 金山区2025年重大工程（结转）一览表.png (file_id=13197, 项目 41 条)
2026-11-06 17:25:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 十堰市2025年省级重点项目清单.png(文件 1 条, 项目 78 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:25:57 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 十堰市2025年省级重点项目清单.png (file_id=13198, 项目 82 条)
2026-11-06 17:25:57 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荆州市2025年省级重点项目清单.png(文件 1 条, 项目 51 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:26:02 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荆州市2025年省级重点项目清单.png (file_id=13199, 项目 51 条)
2026-11-06 17:26:02 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 1.png(文件 1 条, 项目 16 条, 通知 0 条, 分类声明 3 条)
2026-11-06 17:26:04 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[1.png] 产业转型类: 标题声明 277 项,解析 16 项
2026-11-06 17:26:05 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 1.png (file_id=13200, 项目 16 条)
2026-11-06 17:26:05 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 10.png(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:26:07 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[10.png] 文化旅游: 标题声明 20 项,解析 16 项
2026-11-06 17:26:07 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 10.png (file_id=13201, 项目 20 条)
2026-11-06 17:26:07 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 11.png(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:26:09 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[11.png] 商贸物流: 标题声明 24 项,解析 16 项
2026-11-06 17:26:09 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 11.png (file_id=13202, 项目 20 条)
2026-11-06 17:26:10 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 12.png(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 2 条)
2026-11-06 17:26:12 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[12.png] 战略腹地和物资储备: 标题声明 8 项,解析 11 项
2026-11-06 17:26:12 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[12.png] 战略腹地和物资储备-其他产业: 标题声明 55 项,解析 3 项
2026-11-06 17:26:12 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 12.png (file_id=13203, 项目 19 条)
2026-11-06 17:26:13 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 13.png(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:26:16 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 13.png (file_id=13204, 项目 21 条)
2026-11-06 17:26:16 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 14.png(文件 1 条, 项目 21 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:26:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 14.png (file_id=13205, 项目 21 条)
2026-11-06 17:26:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 15.png(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 2 条)
2026-11-06 17:26:21 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[15.png] 能源革命类: 标题声明 65 项,解析 9 项
2026-11-06 17:26:21 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[15.png] 能源革命类-煤炭先进产能: 标题声明 15 项,解析 9 项
2026-11-06 17:26:21 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 15.png (file_id=13206, 项目 19 条)
2026-11-06 17:26:21 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 16.png(文件 1 条, 项目 16 条, 通知 0 条, 分类声明 5 条)
2026-11-06 17:26:23 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[16.png] 煤矿智能化改造: 标题声明 1 项,解析 10 项
2026-11-06 17:26:23 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[16.png] 煤矿智能化改造-保障性并网新能源发电: 标题声明 11 项,解析 1 项
2026-11-06 17:26:23 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 16.png (file_id=13207, 项目 16 条)
2026-11-06 17:26:24 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 17.png(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 2 条)
2026-11-06 17:26:26 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[17.png] 抽水蓄能: 标题声明 7 项,解析 9 项
2026-11-06 17:26:26 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[17.png] 抽水蓄能-新型储能: 标题声明 7 项,解析 2 项
2026-11-06 17:26:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 17.png (file_id=13208, 项目 19 条)
2026-11-06 17:26:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 18.png(文件 1 条, 项目 15 条, 通知 0 条, 分类声明 4 条)
2026-11-06 17:26:28 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[18.png] 晋电外送通道: 标题声明 2 项,解析 10 项
2026-11-06 17:26:28 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[18.png] 晋电外送通道-非常规天然气增储上产: 标题声明 12 项,解析 6 项
2026-11-06 17:26:29 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 18.png (file_id=13209, 项目 15 条)
2026-11-06 17:26:29 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 19.png(文件 1 条, 项目 18 条, 通知 0 条, 分类声明 2 条)
2026-11-06 17:26:31 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[19.png] 科教人才类: 标题声明 57 项,解析 12 项
2026-11-06 17:26:31 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[19.png] 科教人才类-晋创谷: 标题声明 16 项,解析 12 项
2026-11-06 17:26:31 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 19.png (file_id=13210, 项目 18 条)
2026-11-06 17:26:31 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2.png(文件 1 条, 项目 17 条, 通知 0 条, 分类声明 3 条)
2026-11-06 17:26:34 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2.png] 高端装备制造产业链: 标题声明 9 项,解析 18 项
2026-11-06 17:26:34 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2.png (file_id=13211, 项目 18 条)
2026-11-06 17:26:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 20.png(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:26:37 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[20.png] 科技攻关: 标题声明 16 项,解析 15 项
2026-11-06 17:26:38 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 20.png (file_id=13212, 项目 19 条)
2026-11-06 17:26:38 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 21.png(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:26:40 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[21.png] 教育: 标题声明 25 项,解析 18 项
2026-11-06 17:26:40 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 21.png (file_id=13213, 项目 19 条)
2026-11-06 17:26:40 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 22.png(文件 1 条, 项目 17 条, 通知 0 条, 分类声明 3 条)
2026-11-06 17:26:43 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[22.png] 基础设施类: 标题声明 121 项,解析 10 项
2026-11-06 17:26:43 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[22.png] 基础设施类-铁路: 标题声明 19 项,解析 7 项
2026-11-06 17:26:43 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 22.png (file_id=13214, 项目 17 条)
2026-11-06 17:26:43 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 23.png(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:26:45 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[23.png] 公路: 标题声明 34 项,解析 7 项
2026-11-06 17:26:45 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 23.png (file_id=13215, 项目 19 条)
2026-11-06 17:26:46 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 24.png(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:26:48 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 24.png (file_id=13216, 项目 19 条)
2026-11-06 17:26:48 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 25.png(文件 1 条, 项目 17 条, 通知 0 条, 分类声明 3 条)
2026-11-06 17:26:57 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[25.png] 机场: 标题声明 4 项,解析 9 项
2026-11-06 17:26:57 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[25.png] 机场-水利: 标题声明 32 项,解析 2 项
2026-11-06 17:26:57 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 25.png (file_id=13217, 项目 17 条)
2026-11-06 17:26:57 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 26.png(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:27:00 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 26.png (file_id=13218, 项目 20 条)
2026-11-06 17:27:01 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 27.png(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:27:05 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[27.png] 开发区（园区）基础设施: 标题声明 26 项,解析 9 项
2026-11-06 17:27:05 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 27.png (file_id=13219, 项目 19 条)
2026-11-06 17:27:05 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 28.png(文件 1 条, 项目 17 条, 通知 0 条, 分类声明 2 条)
2026-11-06 17:27:10 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[28.png] 社会民生类: 标题声明 91 项,解析 1 项
2026-11-06 17:27:10 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[28.png] 社会民生类-新型城镇化: 标题声明 18 项,解析 1 项
2026-11-06 17:27:10 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 28.png (file_id=13220, 项目 18 条)
2026-11-06 17:27:10 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 29.png(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:27:13 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[29.png] 乡村振兴千万工程: 标题声明 22 项,解析 2 项
2026-11-06 17:27:13 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 29.png (file_id=13221, 项目 19 条)
2026-11-06 17:27:14 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 3.png(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 2 条)
2026-11-06 17:27:17 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[3.png] 光伏产业链: 标题声明 13 项,解析 19 项
2026-11-06 17:27:17 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[3.png] 光伏产业链-现代医药产业链: 标题声明 11 项,解析 6 项
2026-11-06 17:27:17 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 3.png (file_id=13222, 项目 19 条)
2026-11-06 17:27:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 31.png(文件 1 条, 项目 18 条, 通知 0 条, 分类声明 2 条)
2026-11-06 17:27:22 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[31.png] 一泓清水入黄河工程: 标题声明 15 项,解析 18 项
2026-11-06 17:27:22 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[31.png] 一泓清水入黄河工程-生态修复治理等社会民生: 标题声明 12 项,解析 3 项
2026-11-06 17:27:22 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 31.png (file_id=13224, 项目 18 条)
2026-11-06 17:27:23 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 32.png(文件 1 条, 项目 18 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:27:25 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[32.png] 省市重点医院建设: 标题声明 24 项,解析 10 项
2026-11-06 17:27:25 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 32.png (file_id=13225, 项目 19 条)
2026-11-06 17:27:25 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 33.png(文件 1 条, 项目 14 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:27:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 33.png (file_id=13226, 项目 14 条)
2026-11-06 17:27:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 34.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:27:29 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 34.png (file_id=13227, 项目 0 条)
2026-11-06 17:27:29 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 4.png(文件 1 条, 项目 18 条, 通知 0 条, 分类声明 3 条)
2026-11-06 17:27:31 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[4.png] 第三代半导体产业链: 标题声明 8 项,解析 13 项
2026-11-06 17:27:31 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[4.png] 第三代半导体产业链-新型储能产业链: 标题声明 11 项,解析 1 项
2026-11-06 17:27:31 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 4.png (file_id=13228, 项目 18 条)
2026-11-06 17:27:32 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 5.png(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 2 条)
2026-11-06 17:27:34 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[5.png] 废弃资源综合利用产业链: 标题声明 7 项,解析 9 项
2026-11-06 17:27:34 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[5.png] 废弃资源综合利用产业链-碳基新材料产业链: 标题声明 14 项,解析 2 项
2026-11-06 17:27:34 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 5.png (file_id=13229, 项目 19 条)
2026-11-06 17:27:34 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 6.png(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:27:37 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[6.png] 信息技术融合应用产业链: 标题声明 12 项,解析 8 项
2026-11-06 17:27:37 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 6.png (file_id=13230, 项目 20 条)
2026-11-06 17:27:37 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 7.png(文件 1 条, 项目 18 条, 通知 0 条, 分类声明 3 条)
2026-11-06 17:27:40 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[7.png] 铜基新材料产业链: 标题声明 3 项,解析 14 项
2026-11-06 17:27:40 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[7.png] 铜基新材料产业链-专业镇: 标题声明 8 项,解析 7 项
2026-11-06 17:27:40 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 7.png (file_id=13231, 项目 18 条)
2026-11-06 17:27:40 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 8.png(文件 1 条, 项目 18 条, 通知 0 条, 分类声明 3 条)
2026-11-06 17:27:42 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[8.png] 低空经济: 标题声明 9 项,解析 17 项
2026-11-06 17:27:42 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[8.png] 低空经济-消费品工业: 标题声明 11 项,解析 3 项
2026-11-06 17:27:42 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 8.png (file_id=13232, 项目 18 条)
2026-11-06 17:27:43 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 9.png(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 1 条)
2026-11-06 17:27:45 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[9.png] 现代农业: 标题声明 16 项,解析 12 项
2026-11-06 17:27:45 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 9.png (file_id=13233, 项目 20 条)
2026-11-06 17:27:45 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2025年广元市重点项目名单.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=36, 乱码分=70.00），跳过解析
2026-11-06 17:27:55 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2025年重点项目\29四川省2025年重点项目清单\广元市2025年\2025年广元市重点项目名单.png: 图片未识别到文本(疑似非清单图片)                                                                                                                                                                                            
2026-11-06 17:27:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2025年广元市重点项目名单.png (file_id=13234, 项目 0 条)
2026-11-06 17:27:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 一图概览.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2025.10.31新增地级清单（14家）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2025.12.31新增地级清单（9家）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2025.2.27新增地级清单（9家）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2025.3.11新增地级清单（28家）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2025.3.26新增地级清单（12家）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2025.4.16新增地级清单（24家）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2025.5.15新增地级清单（41家）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2025.6.23新增地级清单（16家）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2025.7.23新增地级清单（4家）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2025年省级重点项目清单-地级市（47个）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2025年省级重点项目清单-省级（12个）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2025年重点项目清单（截止2025.10.31）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2025年重点项目清单（截止2025.12.31）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2025年重点项目清单（截止2025.2.27）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2025年重点项目清单（截止2025.3.11）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2025年重点项目清单（截止2025.3.26）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2025年重点项目清单（截止2025.4.16）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2025年重点项目清单（截止2025.5.15）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2025年重点项目清单（截止2025.6.23）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2025年重点项目清单（截止2025.7.23）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地级市120家（截止2025.4.16）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地级市161家（截止2025.5.15）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地级市177家（截止2025.6.23）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地级市181家（截止2025.7.23）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地级市195家（截止2025.10.29）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地级市47家（截止2025.2.18）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地级市56家（截止2025.2.27）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地级市84家（截止2025.3.11）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地级市96家（截止2025.3.26）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级清单（2025.10.31）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级清单（2025.12.31） -.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级清单（2025.2.18）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级清单（2025.2.27）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:57 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级清单（2025.3.11）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:57 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级清单（2025.4.16）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:57 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级清单（2025.5.15）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:27:57 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 轮播图.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=5, 乱码分=55.00），跳过解析
2026-11-06 17:27:58 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2025年重点项目\轮播图.png: 图片未识别到文本(疑似非清单图片)
2026-11-06 17:27:58 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 轮播图.png (file_id=13235, 项目 0 条)
2026-11-06 17:27:58 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2026年区重大工程项目清单.png(文件 1 条, 项目 110 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:28:08 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2026年区重大工程项目清单.png (file_id=13236, 项目 110 条)
2026-11-06 17:28:08 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2026年宁夏自治区重点建设项目清单_1.png(文件 1 条, 项目 13 条, 通知 0 条, 分类声明 2 条)
2026-11-06 17:28:13 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2026年宁夏自治区重点建设项目清单_1.png] 产业项目: 标题声明 67 项,解析 13 项
2026-11-06 17:28:13 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2026年宁夏自治区重点建设项目清单_1.png] 产业项目-工业项目: 标题声明 61 项,解析 13 项
2026-11-06 17:28:13 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2026年宁夏自治区重点建设项目清单_1.png (file_id=13237, 项目 13 条)
2026-11-06 17:28:13 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2026年宁夏自治区重点建设项目清单_2.png(文件 1 条, 项目 17 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:28:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2026年宁夏自治区重点建设项目清单_2.png (file_id=13238, 项目 17 条)
2026-11-06 17:28:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2026年宁夏自治区重点建设项目清单_3.png(文件 1 条, 项目 16 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:28:25 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2026年宁夏自治区重点建设项目清单_3.png (file_id=13239, 项目 16 条)
2026-11-06 17:28:25 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2026年宁夏自治区重点建设项目清单_4.png(文件 1 条, 项目 16 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:28:31 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2026年宁夏自治区重点建设项目清单_4.png (file_id=13240, 项目 16 条)
2026-11-06 17:28:31 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2026年宁夏自治区重点建设项目清单_5.png(文件 1 条, 项目 14 条, 通知 0 条, 分类声明 5 条)
2026-11-06 17:28:35 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2026年宁夏自治区重点建设项目清单_5.png] 服务业项目: 标题声明 2 项,解析 6 项
2026-11-06 17:28:35 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2026年宁夏自治区重点建设项目清单_5.png] 基础设施项目: 标题声明 17 项,解析 8 项
2026-11-06 17:28:35 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2026年宁夏自治区重点建设项目清单_5.png] 基础设施项目-铁路工程: 标题声明 6 项,解析 4 项
2026-11-06 17:28:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2026年宁夏自治区重点建设项目清单_5.png (file_id=13241, 项目 14 条)
2026-11-06 17:28:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2026年宁夏自治区重点建设项目清单_6.png(文件 1 条, 项目 15 条, 通知 0 条, 分类声明 4 条)
2026-11-06 17:28:40 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2026年宁夏自治区重点建设项目清单_6.png] 公路工程: 标题声明 3 项,解析 4 项
2026-11-06 17:28:40 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2026年宁夏自治区重点建设项目清单_6.png] 公路工程-新基建项目: 标题声明 1 项,解析 0 项
2026-11-06 17:28:40 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2026年宁夏自治区重点建设项目清单_6.png (file_id=13242, 项目 15 条)
2026-11-06 17:28:41 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2026年宁夏自治区重点建设项目清单_7.png(文件 1 条, 项目 16 条, 通知 0 条, 分类声明 4 条)
2026-11-06 17:28:46 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2026年宁夏自治区重点建设项目清单_7.png (file_id=13243, 项目 16 条)
2026-11-06 17:28:46 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荆州市2026年省级重点项目清单.png(文件 1 条, 项目 49 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:28:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荆州市2026年省级重点项目清单.png (file_id=13244, 项目 49 条)
2026-11-06 17:28:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2026重大项目.png(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=2, 乱码分=0.00），跳过解析
2026-11-06 17:28:52 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2026年重点项目\2026重大项目.png: 图片未识别到文本(疑似非清单图片)
2026-11-06 17:28:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2026重大项目.png (file_id=13245, 项目 0 条)
2026-11-06 17:28:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026.2.10新增地级市8个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026.2.17新增地级市10个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026.3.13新增地级市24个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026.3.19新增地级市4个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026.3.25新增地级市14个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026.3.3新增地级市9个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026.4.30新增地级市22个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026.4.7新增地级市8个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026.6.7新增地级市34个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026.8.19新增地级市4个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026.8.5新增地级市7个.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026年省级重点项目清单-地级市（22个）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026年省级重点项目清单-省级（9个）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026年省级重点项目清单（截止2026.2.10）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026年省级重点项目清单（截止2026.2.17）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026年省级重点项目清单（截止2026.3.13）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026年省级重点项目清单（截止2026.3.19）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026年省级重点项目清单（截止2026.3.25）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026年省级重点项目清单（截止2026.3.3）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026年省级重点项目清单（截止2026.4.30）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026年省级重点项目清单（截止2026.4.7）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026年省级重点项目清单（截止2026.6.7）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026年省级重点项目清单（截止2026.8.19）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2026年省级重点项目清单（截止2026.8.5）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地级市121家（截止2026.4.30）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地级市155家（截止2026.6.7）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地级市22家（截止2026.2.4）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地级市30家（截止2026.2.10）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地级市40家（截止2026.2.17）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地级市49家（截止2026.3.3）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地级市73家（截止2026.3.13）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地级市77家（截止2026.3.19）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地级市91家（截止2026.3.25）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 地级市99家（截止2026.4.7）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级清单（2026.02.04）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级清单（2026.02.10）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级清单（2026.02.17）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级清单（2026.03.03）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级清单（2026.03.13）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级清单（2026.03.19）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级清单（2026.03.25）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级清单（2026.04.07）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级清单（2026.04.30）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 省级清单（2026.06.07）.png - 跳过该文件（filter_file.txt）
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\util\db_util.py - INFO - 数据库连接池已关闭
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - ========================================
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 批量测试完成: png 共 438 个
2026-11-06 17:28:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 成功: 174 个, 入库项目 3255 条 | 失败: 264 个 | 跳过: 0 个
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 陕西省2021年重点建设项目分布.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 订阅.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_1.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_10.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_11.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_12.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_13.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_14.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_15.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_16.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_17.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_18.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_19.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_2.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_20.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_21.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_22.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_23.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_24.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_25.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_26.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_27.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_28.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_29.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_3.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_30.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_31.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_32.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_33.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_34.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_35.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_36.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_37.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_38.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_39.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_4.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_40.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_41.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_42.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_43.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_44.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_45.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_46.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_47.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_48.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_49.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_5.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_50.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_51.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_52.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_53.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_54.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_6.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_7.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_8.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_9.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_1.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_10.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_11.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_12.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_13.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_14.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_15.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_16.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_17.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_18.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_19.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_2.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_20.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_21.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_22.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_23.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_24.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_25.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_26.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_27.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_28.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_29.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_3.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_30.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_31.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_32.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_33.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_34.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_35.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_36.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_37.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_38.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_39.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_4.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_40.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_41.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_42.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_43.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_44.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_45.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_46.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_47.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_48.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_49.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_5.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_50.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_51.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_52.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_53.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_54.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_6.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_7.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_8.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 河北省2023年省重点建设项目名单_9.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地市级102个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地市级121个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地市级136个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地市级146个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地市级158个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地市级189个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地市级25个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地市级33个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地市级43个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地市级59个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地市级61个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地市级65个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地市级80个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地市级97个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地市级清单.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地级市32个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地级市69个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 更新（10.23）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 更新（5.10）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 更新（5.23）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 更新（7.10）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 更新（7.25）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 更新（8.18）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 更新（9.20）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级清单.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级（2.16）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级（2.20）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级（3.14）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级（3.1）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级（3.20）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级（3.28）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级（3.3）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级（3.4）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级（4.18）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级（4.27）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级（7.10）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2024.11.28新增40家.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2024.3.26新增10家.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2024.4.22新增8家.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2024.4.5新增20家.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2024.6.25新增28家.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2024.7.23新增4家.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地级市项目清单（截止2024.3.12）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 更新项目清单（截止2024.11.28）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 更新项目清单（截止2024.3.22）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 更新项目清单（截止2024.3.26）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 更新项目清单（截止2024.4.22）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 更新项目清单（截止2024.4.5）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 更新项目清单（截止2024.6.26）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级清单（16个）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 轮播图.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 项目清单（118个地级市）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 项目清单（138个地级市）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 项目清单（146个地级市）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 项目清单（174个地级市）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 项目清单（2.15）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 项目清单（2.4）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 项目清单（27个地级市）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 项目清单（29个地级市）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 项目清单（3.1）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 项目清单（3.26）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 项目清单（35个地级市）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 项目清单（4.22）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 项目清单（4.5）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 项目清单（40个地级市）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 项目清单（6.25）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 项目清单（6.26）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 项目清单（60个地级市）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 项目清单（63个地级市）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 项目清单（78个地级市） .png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 项目清单（78个地级市）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 一图概览.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2025.10.31新增地级清单（14家）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2025.12.31新增地级清单（9家）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2025.2.27新增地级清单（9家）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2025.3.11新增地级清单（28家）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2025.3.26新增地级清单（12家）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2025.4.16新增地级清单（24家）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2025.5.15新增地级清单（41家）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2025.6.23新增地级清单（16家）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2025.7.23新增地级清单（4家）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2025年省级重点项目清单-地级市（47个）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2025年省级重点项目清单-省级（12个）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2025年重点项目清单（截止2025.10.31）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2025年重点项目清单（截止2025.12.31）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2025年重点项目清单（截止2025.2.27）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2025年重点项目清单（截止2025.3.11）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2025年重点项目清单（截止2025.3.26）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2025年重点项目清单（截止2025.4.16）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2025年重点项目清单（截止2025.5.15）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2025年重点项目清单（截止2025.6.23）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2025年重点项目清单（截止2025.7.23）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地级市120家（截止2025.4.16）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地级市161家（截止2025.5.15）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地级市177家（截止2025.6.23）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地级市181家（截止2025.7.23）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地级市195家（截止2025.10.29）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地级市47家（截止2025.2.18）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地级市56家（截止2025.2.27）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地级市84家（截止2025.3.11）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地级市96家（截止2025.3.26）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级清单（2025.10.31）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级清单（2025.12.31） -.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级清单（2025.2.18）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级清单（2025.2.27）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级清单（2025.3.11）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级清单（2025.4.16）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级清单（2025.5.15）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026.2.10新增地级市8个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026.2.17新增地级市10个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026.3.13新增地级市24个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026.3.19新增地级市4个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026.3.25新增地级市14个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026.3.3新增地级市9个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026.4.30新增地级市22个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026.4.7新增地级市8个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026.6.7新增地级市34个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026.8.19新增地级市4个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026.8.5新增地级市7个.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026年省级重点项目清单-地级市（22个）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026年省级重点项目清单-省级（9个）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026年省级重点项目清单（截止2026.2.10）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026年省级重点项目清单（截止2026.2.17）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026年省级重点项目清单（截止2026.3.13）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026年省级重点项目清单（截止2026.3.19）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026年省级重点项目清单（截止2026.3.25）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026年省级重点项目清单（截止2026.3.3）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026年省级重点项目清单（截止2026.4.30）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026年省级重点项目清单（截止2026.4.7）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026年省级重点项目清单（截止2026.6.7）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026年省级重点项目清单（截止2026.8.19）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2026年省级重点项目清单（截止2026.8.5）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地级市121家（截止2026.4.30）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地级市155家（截止2026.6.7）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地级市22家（截止2026.2.4）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地级市30家（截止2026.2.10）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地级市40家（截止2026.2.17）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地级市49家（截止2026.3.3）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地级市73家（截止2026.3.13）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地级市77家（截止2026.3.19）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地级市91家（截止2026.3.25）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 地级市99家（截止2026.4.7）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级清单（2026.02.04）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级清单（2026.02.10）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级清单（2026.02.17）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级清单（2026.03.03）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级清单（2026.03.13）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级清单（2026.03.19）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级清单（2026.03.25）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级清单（2026.04.07）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级清单（2026.04.30）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 省级清单（2026.06.07）.png: 跳过该文件（filter_file.txt）
2026-11-06 17:28:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - ========================================
(py312_stc) PS E:\STangWork\PythonProjects\skp_parser> python batch_test.py jpg
本次批量解析状态：文件类型：jpg，是否上传：False，数据库地址：local

2026-11-06 17:41:23 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 批量测试: E:\STangWork\STangFiles\各省重点项目：2020年起 下 jpg 文件 270 个(上传 GoFast: False)
2026-11-06 17:41:23 - E:\STangWork\PythonProjects\skp_parser\util\db_util.py - INFO - 数据库连接池已创建: 127.0.0.1:3306/suidaobig
E:\miniconda3\envs\py312_stc\Lib\site-packages\aiomysql\cursors.py:458: Warning: Table 'skp_file' already exists
  await self._do_get_result()
E:\miniconda3\envs\py312_stc\Lib\site-packages\aiomysql\cursors.py:458: Warning: Table 'skp_project' already exists
  await self._do_get_result()
E:\miniconda3\envs\py312_stc\Lib\site-packages\aiomysql\cursors.py:458: Warning: Table 'skp_project_unit' already exists
  await self._do_get_result()
E:\miniconda3\envs\py312_stc\Lib\site-packages\aiomysql\cursors.py:458: Warning: Table 'skp_notice' already exists
  await self._do_get_result()
E:\miniconda3\envs\py312_stc\Lib\site-packages\aiomysql\cursors.py:458: Warning: Table 'skp_category_declared' already exists
  await self._do_get_result()
2026-11-06 17:41:24 - E:\STangWork\PythonProjects\skp_parser\util\db_util.py - INFO - 数据库表初始化完成(skp_file/skp_project/skp_project_unit/skp_notice/skp_category_declared)
2026-11-06 17:41:24 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2020.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
[INFO] 2026-11-06 17:41:24,903 [RapidOCR] base.py:23: Using engine_name: onnxruntime
[INFO] 2026-11-06 17:41:25,011 [RapidOCR] download_file.py:60: File exists and is valid: E:\miniconda3\envs\py312_stc\Lib\site-packages\rapidocr\models\PP-OCRv6_det_small.onnx
[INFO] 2026-11-06 17:41:25,011 [RapidOCR] main.py:63: Using E:\miniconda3\envs\py312_stc\Lib\site-packages\rapidocr\models\PP-OCRv6_det_small.onnx
[INFO] 2026-11-06 17:41:25,108 [RapidOCR] base.py:23: Using engine_name: onnxruntime
[INFO] 2026-11-06 17:41:25,112 [RapidOCR] download_file.py:60: File exists and is valid: E:\miniconda3\envs\py312_stc\Lib\site-packages\rapidocr\models\ch_ppocr_mobile_v2.0_cls_mobile.onnx
[INFO] 2026-11-06 17:41:25,112 [RapidOCR] main.py:63: Using E:\miniconda3\envs\py312_stc\Lib\site-packages\rapidocr\models\ch_ppocr_mobile_v2.0_cls_mobile.onnx
[INFO] 2026-11-06 17:41:25,170 [RapidOCR] base.py:23: Using engine_name: onnxruntime
[INFO] 2026-11-06 17:41:25,219 [RapidOCR] download_file.py:60: File exists and is valid: E:\miniconda3\envs\py312_stc\Lib\site-packages\rapidocr\models\PP-OCRv6_rec_small.onnx
[INFO] 2026-11-06 17:41:25,219 [RapidOCR] main.py:63: Using E:\miniconda3\envs\py312_stc\Lib\site-packages\rapidocr\models\PP-OCRv6_rec_small.onnx
OCR 结果疑似乱码（items=2, 乱码分=15.00），跳过解析
2026-11-06 17:41:26 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2021年重点项目\2020.jpg: 图片未识别到文本(疑似非清单图片)
2026-11-06 17:41:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2020.jpg (file_id=13246, 项目 0 条)
2026-11-06 17:41:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2021.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=4, 乱码分=30.00），跳过解析
2026-11-06 17:41:27 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2021年重点项目\2021.jpg: 图片未识别到文本(疑似非清单图片)
2026-11-06 17:41:27 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2021.jpg (file_id=13247, 项目 0 条)
2026-11-06 17:41:27 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 54万亿.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=3, 乱码分=30.00），跳过解析
2026-11-06 17:41:27 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2021年重点项目\54万亿.jpg: 图片未识别到文本(疑似非清单图片)
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 54万亿.jpg (file_id=13248, 项目 0 条)
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 1.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 1_副本.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 1_副本1.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 1_副本2.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 1_副本3.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 1_副本4.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2_副本.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2_副本1.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2_副本2.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2_副本3.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2_副本4.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 3.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 3_副本.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 3_副本1.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 3_副本2.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 3_副本3.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 4.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 4_副本.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 4_副本1.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 4_副本2.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 4_副本3.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 4_副本4.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:29 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2022年重大项目封面.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=2, 乱码分=15.00），跳过解析
2026-11-06 17:41:30 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2022年重点项目\2022年重大项目封面.jpg: 图片未识别到文本(疑似非清单图片)
2026-11-06 17:41:30 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2022年重大项目封面.jpg (file_id=13249, 项目 0 条)
2026-11-06 17:41:30 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2022年重点项目清单.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=2, 乱码分=15.00），跳过解析
2026-11-06 17:41:30 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2022年重点项目\2022年重点项目清单.jpg: 图片未识别到文本(疑似非清单图片)
2026-11-06 17:41:30 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2022年重点项目清单.jpg (file_id=13250, 项目 0 条)
2026-11-06 17:41:31 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 重大项目清单.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=2, 乱码分=0.00），跳过解析
2026-11-06 17:41:31 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2022年重点项目\重大项目清单.jpg: 图片未识别到文本(疑似非清单图片)
2026-11-06 17:41:32 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 重大项目清单.jpg (file_id=13251, 项目 0 条)
2026-11-06 17:41:32 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 1.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:41:32 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 10.jpg(文件 1 条, 项目 2 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:41:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 10.jpg (file_id=13252, 项目 2 条)
2026-11-06 17:41:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 11.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:41:39 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 11.jpg (file_id=13253, 项目 3 条)
2026-11-06 17:41:40 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 12.jpg(文件 1 条, 项目 2 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:41:43 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 12.jpg (file_id=13254, 项目 2 条)
2026-11-06 17:41:43 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 13.jpg(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:41:46 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 13.jpg (file_id=13255, 项目 5 条)
2026-11-06 17:41:46 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 14.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:41:50 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 14.jpg (file_id=13256, 项目 4 条)
2026-11-06 17:41:50 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 15.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:41:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 15.jpg (file_id=13257, 项目 4 条)
2026-11-06 17:41:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 16.jpg(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:42:00 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 16.jpg (file_id=13258, 项目 5 条)
2026-11-06 17:42:00 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 17.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:42:07 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 17.jpg (file_id=13259, 项目 4 条)
2026-11-06 17:42:07 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 18.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:42:12 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 18.jpg (file_id=13260, 项目 3 条)
2026-11-06 17:42:12 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 19.jpg(文件 1 条, 项目 2 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:42:16 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 19.jpg (file_id=13261, 项目 2 条)
2026-11-06 17:42:16 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:42:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2.jpg (file_id=13262, 项目 4 条)
2026-11-06 17:42:29 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 20.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:42:39 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 20.jpg (file_id=13263, 项目 3 条)
2026-11-06 17:42:39 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 21.jpg(文件 1 条, 项目 7 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:42:45 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 21.jpg (file_id=13264, 项目 7 条)
2026-11-06 17:42:45 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 22.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:42:49 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 22.jpg (file_id=13265, 项目 4 条)
2026-11-06 17:42:49 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 23.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:42:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 23.jpg (file_id=13266, 项目 3 条)
2026-11-06 17:42:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 24.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:42:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 24.jpg (file_id=13267, 项目 3 条)
2026-11-06 17:42:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 25.jpg(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:42:59 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 25.jpg (file_id=13268, 项目 5 条)
2026-11-06 17:42:59 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 26.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:43:03 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 26.jpg (file_id=13269, 项目 3 条)
2026-11-06 17:43:03 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 27.jpg(文件 1 条, 项目 2 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:43:06 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 27.jpg (file_id=13270, 项目 2 条)
2026-11-06 17:43:06 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 28.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:43:10 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 28.jpg (file_id=13271, 项目 3 条)
2026-11-06 17:43:10 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 29.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:43:13 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 29.jpg (file_id=13272, 项目 3 条)
2026-11-06 17:43:13 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 3.jpg(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:43:16 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 3.jpg (file_id=13273, 项目 5 条)
2026-11-06 17:43:17 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 30.jpg(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:43:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 30.jpg (file_id=13274, 项目 5 条)
2026-11-06 17:43:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 31.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:43:24 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 31.jpg (file_id=13275, 项目 4 条)
2026-11-06 17:43:24 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 32.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:43:27 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 32.jpg (file_id=13276, 项目 3 条)
2026-11-06 17:43:27 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 33.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:43:31 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 33.jpg (file_id=13277, 项目 4 条)
2026-11-06 17:43:31 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 34.jpg(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:43:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 34.jpg (file_id=13278, 项目 5 条)
2026-11-06 17:43:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 35.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:43:38 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 35.jpg (file_id=13279, 项目 4 条)
2026-11-06 17:43:38 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 36.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:43:44 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 36.jpg (file_id=13280, 项目 3 条)
2026-11-06 17:43:44 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 37.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:43:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 37.jpg (file_id=13281, 项目 4 条)
2026-11-06 17:43:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 38.jpg(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:43:58 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 38.jpg (file_id=13282, 项目 5 条)
2026-11-06 17:43:58 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 39.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:44:01 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 39.jpg (file_id=13283, 项目 4 条)
2026-11-06 17:44:01 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 4.jpg(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:44:04 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 4.jpg (file_id=13284, 项目 5 条)
2026-11-06 17:44:05 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 40.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:44:07 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 40.jpg (file_id=13285, 项目 3 条)
2026-11-06 17:44:07 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 41.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:44:10 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 41.jpg (file_id=13286, 项目 3 条)
2026-11-06 17:44:11 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 42.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:44:14 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 42.jpg (file_id=13287, 项目 3 条)
2026-11-06 17:44:14 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 43.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:44:17 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 43.jpg (file_id=13288, 项目 4 条)
2026-11-06 17:44:17 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 44.jpg(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:44:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 44.jpg (file_id=13289, 项目 5 条)
2026-11-06 17:44:21 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 45.jpg(文件 1 条, 项目 7 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:44:25 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 45.jpg (file_id=13290, 项目 7 条)
2026-11-06 17:44:25 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 46.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:44:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 46.jpg (file_id=13291, 项目 3 条)
2026-11-06 17:44:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 47.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:44:31 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 47.jpg (file_id=13292, 项目 4 条)
2026-11-06 17:44:31 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 5.jpg(文件 1 条, 项目 6 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:44:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 5.jpg (file_id=13293, 项目 6 条)
2026-11-06 17:44:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 6.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:44:38 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 6.jpg (file_id=13294, 项目 4 条)
2026-11-06 17:44:38 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 7.jpg(文件 1 条, 项目 2 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:44:40 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 7.jpg (file_id=13295, 项目 2 条)
2026-11-06 17:44:41 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 8.jpg(文件 1 条, 项目 6 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:44:44 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 8.jpg (file_id=13296, 项目 6 条)
2026-11-06 17:44:44 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 9.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:44:47 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 9.jpg (file_id=13297, 项目 3 条)
2026-11-06 17:44:47 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 1.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:44:47 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 10.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:44:47 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:44:47 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 3.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:44:47 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 4.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:44:48 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 5.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:44:48 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 6.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:44:48 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 7.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:44:48 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 8.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:44:48 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 9.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:44:48 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 1.jpg(文件 1 条, 项目 13 条, 通知 0 条, 分类声明 5 条)
横线分布不合理
2026-11-06 17:44:51 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[1.jpg] 四化项目: 标题声明 377 项,解析 0 项
2026-11-06 17:44:51 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[1.jpg] 四化项目-新型工业化项目: 标题声明 73 项,解析 0 项
2026-11-06 17:44:51 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[1.jpg] 四化项目-新型工业化项目-新能源电池及材料产业: 标题声明 6 项,解析 0 项
2026-11-06 17:44:51 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[1.jpg] 四化项目-新型工业化项目-酱香白酒产业: 标题声明 6 项,解析 0 项
2026-11-06 17:44:51 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[1.jpg] 四化项目-新型工业化项目-现代能源产业: 标题声明 12 项,解析 0 项
E:\miniconda3\envs\py312_stc\Lib\site-packages\aiomysql\cursors.py:458: Warning: 'VALUES function' is deprecated and will be removed in a future release. Please use an alias (INSERT INTO ... VALUES (...) AS alias) and replace VALUES(col) in the ON DUPLICATE KEY UPDATE clause with alias.col instead
  await self._do_get_result()
2026-11-06 17:44:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 1.jpg (file_id=13298, 项目 13 条)
2026-11-06 17:44:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 10.jpg(文件 1 条, 项目 27 条, 通知 0 条, 分类声明 1 条)
横线分布不合理
2026-11-06 17:44:54 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[10.jpg] 房地产健康发展工程: 标题声明 71 项,解析 21 项
2026-11-06 17:44:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 10.jpg (file_id=13299, 项目 27 条)
2026-11-06 17:44:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 11.jpg(文件 1 条, 项目 31 条, 通知 0 条, 分类声明 0 条)
横线分布不合理
2026-11-06 17:44:57 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 11.jpg (file_id=13300, 项目 31 条)
2026-11-06 17:44:57 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 12.jpg(文件 1 条, 项目 22 条, 通知 0 条, 分类声明 4 条)
横线分布不合理
2026-11-06 17:45:00 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[12.jpg] 农业现代化: 标题声明 67 项,解析 0 项
2026-11-06 17:45:00 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[12.jpg] 农业现代化-茶产业: 标题声明 2 项,解析 0 项
2026-11-06 17:45:00 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[12.jpg] 农业现代化-食用菌产业: 标题声明 1 项,解析 0 项
2026-11-06 17:45:00 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[12.jpg] 农业现代化-牛羊产业: 标题声明 3 项,解析 0 项
2026-11-06 17:45:00 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 12.jpg (file_id=13301, 项目 22 条)
2026-11-06 17:45:00 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 13.jpg(文件 1 条, 项目 26 条, 通知 0 条, 分类声明 1 条)
横线分布不合理
2026-11-06 17:45:03 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[13.jpg] 特色林（竹、油茶、花椒、皂角等）产业: 标题声明 28 项,解析 23 项
2026-11-06 17:45:03 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 13.jpg (file_id=13302, 项目 26 条)
2026-11-06 17:45:03 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 14.jpg(文件 1 条, 项目 17 条, 通知 0 条, 分类声明 4 条)
横线分布不合理
2026-11-06 17:45:05 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[14.jpg] 水果产业-生猪产业: 标题声明 1 项,解析 0 项
2026-11-06 17:45:05 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[14.jpg] 水果产业-生猪产业-中药（石斛）产业: 标题声明 4 项,解析 0 项
2026-11-06 17:45:05 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[14.jpg] 水果产业-生猪产业-中药（石斛）产业-生态渔业产业: 标题声明 4 项,解析 0 项
2026-11-06 17:45:06 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 14.jpg (file_id=13303, 项目 17 条)
2026-11-06 17:45:06 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 15.jpg(文件 1 条, 项目 21 条, 通知 0 条, 分类声明 4 条)
横线分布不合理
2026-11-06 17:45:09 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[15.jpg] 生态家禽产业-其他农业产业: 标题声明 16 项,解析 0 项
2026-11-06 17:45:09 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[15.jpg] 生态家禽产业-旅游产业化: 标题声明 51 项,解析 0 项
2026-11-06 17:45:09 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[15.jpg] 生态家禽产业-旅游产业化-旅游景区建设: 标题声明 9 项,解析 0 项
2026-11-06 17:45:09 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 15.jpg (file_id=13304, 项目 21 条)
2026-11-06 17:45:09 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 16.jpg(文件 1 条, 项目 25 条, 通知 0 条, 分类声明 1 条)
横线分布不合理
2026-11-06 17:45:12 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[16.jpg] 旅游服务设施: 标题声明 24 项,解析 16 项
2026-11-06 17:45:12 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 16.jpg (file_id=13305, 项目 25 条)
2026-11-06 17:45:12 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 17.jpg(文件 1 条, 项目 21 条, 通知 0 条, 分类声明 2 条)
横线分布不合理
2026-11-06 17:45:15 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[17.jpg] 乡村旅游-红色旅游: 标题声明 1 项,解析 0 项
2026-11-06 17:45:15 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 17.jpg (file_id=13306, 项目 21 条)
2026-11-06 17:45:15 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 18.jpg(文件 1 条, 项目 25 条, 通知 0 条, 分类声明 1 条)
横线分布不合理
2026-11-06 17:45:18 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[18.jpg] 基础设施117个（不含四化基础设施项目）-产业基础设施项目: 标题声明 37 项,解析 0 项
2026-11-06 17:45:18 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 18.jpg (file_id=13307, 项目 25 条)
2026-11-06 17:45:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 19.jpg(文件 1 条, 项目 26 条, 通知 0 条, 分类声明 1 条)
横线分布不合理
2026-11-06 17:45:21 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[19.jpg] 交通基础设施: 标题声明 33 项,解析 9 项
2026-11-06 17:45:22 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 19.jpg (file_id=13308, 项目 26 条)
2026-11-06 17:45:22 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2.jpg(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 2 条)
横线分布不合理
2026-11-06 17:45:24 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[2.jpg] 大数据电子信息产业-基础材料产业: 标题声明 7 项,解析 0 项
2026-11-06 17:45:25 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2.jpg (file_id=13309, 项目 20 条)
2026-11-06 17:45:25 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 20.jpg(文件 1 条, 项目 28 条, 通知 0 条, 分类声明 1 条)
横线分布不合理
2026-11-06 17:45:27 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[20.jpg] 水利基础设施: 标题声明 41 项,解析 4 项
2026-11-06 17:45:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 20.jpg (file_id=13310, 项目 28 条)
2026-11-06 17:45:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 21.jpg(文件 1 条, 项目 28 条, 通知 0 条, 分类声明 0 条)
横线分布不合理
2026-11-06 17:45:30 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 21.jpg (file_id=13311, 项目 28 条)
2026-11-06 17:45:30 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 22.jpg(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 5 条)
横线分布不合理
2026-11-06 17:45:33 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[22.jpg] 能源基础设施-新型基础设施: 标题声明 2 项,解析 0 项
2026-11-06 17:45:33 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[22.jpg] 能源基础设施-其他基础设施: 标题声明 2 项,解析 0 项
2026-11-06 17:45:33 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[22.jpg] 民生工程65个（不含四化民生工程项目）: 标题声明 2 项,解析 0 项
2026-11-06 17:45:33 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[22.jpg] 民生工程65个（不含四化民生工程项目）-教育: 标题声明 24 项,解析 0 项
2026-11-06 17:45:33 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 22.jpg (file_id=13312, 项目 19 条)
2026-11-06 17:45:33 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 23.jpg(文件 1 条, 项目 26 条, 通知 0 条, 分类声明 1 条)
横线分布不合理
2026-11-06 17:45:35 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[23.jpg] 医疗卫生: 标题声明 26 项,解析 6 项
2026-11-06 17:45:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 23.jpg (file_id=13313, 项目 26 条)
2026-11-06 17:45:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 24.jpg(文件 1 条, 项目 25 条, 通知 0 条, 分类声明 1 条)
横线分布不合理
2026-11-06 17:45:38 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[24.jpg] 其他公共服务: 标题声明 15 项,解析 5 项
2026-11-06 17:45:38 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 24.jpg (file_id=13314, 项目 25 条)
2026-11-06 17:45:39 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 25.jpg(文件 1 条, 项目 10 条, 通知 0 条, 分类声明 0 条)
横线分布不合理
2026-11-06 17:45:40 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 25.jpg (file_id=13315, 项目 10 条)
2026-11-06 17:45:40 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 3.jpg(文件 1 条, 项目 23 条, 通知 0 条, 分类声明 2 条)
横线分布不合理
2026-11-06 17:45:44 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[3.jpg] 新型建材产业: 标题声明 20 项,解析 21 项
2026-11-06 17:45:44 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[3.jpg] 新型建材产业-现代化工产业: 标题声明 3 项,解析 0 项
2026-11-06 17:45:44 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 3.jpg (file_id=13316, 项目 23 条)
2026-11-06 17:45:44 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 4.jpg(文件 1 条, 项目 18 条, 通知 0 条, 分类声明 4 条)
横线分布不合理
2026-11-06 17:45:47 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[4.jpg] 生态食品产业-健康医药产业: 标题声明 2 项,解析 0 项
2026-11-06 17:45:47 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[4.jpg] 生态食品产业-健康医药产业-其他工业产业: 标题声明 12 项,解析 0 项
2026-11-06 17:45:47 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[4.jpg] 生态食品产业-健康医药产业-新型城镇化: 标题声明 186 项,解析 0 项
2026-11-06 17:45:47 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 4.jpg (file_id=13317, 项目 18 条)
2026-11-06 17:45:47 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 5.jpg(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 3 条)
横线分布不合理
2026-11-06 17:45:50 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[5.jpg] 路网优化提升工程-供水安全保障工程: 标题声明 11 项,解析 0 项
2026-11-06 17:45:50 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[5.jpg] 路网优化提升工程-供水安全保障工程-供电供气供热工程: 标题声明 5 项,解析 0 项
2026-11-06 17:45:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 5.jpg (file_id=13318, 项目 19 条)
2026-11-06 17:45:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 6.jpg(文件 1 条, 项目 27 条, 通知 0 条, 分类声明 1 条)
横线分布不合理
2026-11-06 17:45:54 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[6.jpg] 住房保障工程: 标题声明 33 项,解析 25 项
2026-11-06 17:45:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 6.jpg (file_id=13319, 项目 27 条)
2026-11-06 17:45:54 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 7.jpg(文件 1 条, 项目 22 条, 通知 0 条, 分类声明 2 条)
横线分布不合理
2026-11-06 17:45:57 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[7.jpg] 智慧黔城工程-服务保障工程: 标题声明 13 项,解析 0 项
2026-11-06 17:45:57 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 7.jpg (file_id=13320, 项目 22 条)
2026-11-06 17:45:58 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 8.jpg(文件 1 条, 项目 24 条, 通知 0 条, 分类声明 2 条)
横线分布不合理
2026-11-06 17:46:01 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[8.jpg] 污水垃圾处理工程-生态环境提升工程: 标题声明 5 项,解析 0 项
2026-11-06 17:46:01 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 8.jpg (file_id=13321, 项目 24 条)
2026-11-06 17:46:01 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 9.jpg(文件 1 条, 项目 17 条, 通知 0 条, 分类声明 3 条)
横线分布不合理
2026-11-06 17:46:03 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[9.jpg] 地下空间开发利用工程-安全保障工程: 标题声明 3 项,解析 0 项
2026-11-06 17:46:03 - E:\STangWork\PythonProjects\skp_parser\main.py - WARNING - 分类校验[9.jpg] 地下空间开发利用工程-安全保障工程-城镇产业融合发展工程: 标题声明 10 项,解析 0 项
2026-11-06 17:46:04 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 9.jpg (file_id=13322, 项目 17 条)
2026-11-06 17:46:04 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 1.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:46:05 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 1.jpg (file_id=13323, 项目 0 条)
2026-11-06 17:46:05 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2.jpg(文件 1 条, 项目 64 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:46:11 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2.jpg (file_id=13324, 项目 64 条)
2026-11-06 17:46:11 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 3.jpg(文件 1 条, 项目 77 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:46:17 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 3.jpg (file_id=13325, 项目 77 条)
2026-11-06 17:46:18 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 4.jpg(文件 1 条, 项目 67 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:46:23 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 4.jpg (file_id=13326, 项目 67 条)
2026-11-06 17:46:23 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 5.jpg(文件 1 条, 项目 77 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:46:29 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 5.jpg (file_id=13327, 项目 77 条)
2026-11-06 17:46:29 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 6.jpg(文件 1 条, 项目 63 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:46:33 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 6.jpg (file_id=13328, 项目 63 条)
2026-11-06 17:46:33 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 7.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=179, 乱码分=70.00），跳过解析
2026-11-06 17:46:44 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2023年重点项目\31浙江省2023年重点项目清单\2023年杨州市\7.jpg: 图片未识别到文本(疑 似非清单图片)                                                                                                                                                                                                                  
2026-11-06 17:46:44 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 7.jpg (file_id=13329, 项目 0 条)
2026-11-06 17:46:44 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州1.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=3, 乱码分=0.00），跳过解析
2026-11-06 17:46:45 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2023年重点项目\31浙江省2023年重点项目清单\2023年杨州市\扬州1.jpg: 图片未识别到文本(疑似非清单图片)                                                                                                                                                                                                               
2026-11-06 17:46:45 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州1.jpg (file_id=13330, 项目 0 条)
2026-11-06 17:46:45 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州10.jpg(文件 1 条, 项目 35 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:46:49 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州10.jpg (file_id=13331, 项目 35 条)
2026-11-06 17:46:49 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州11.jpg(文件 1 条, 项目 18 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:46:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州11.jpg (file_id=13332, 项目 18 条)
2026-11-06 17:46:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州12.jpg(文件 1 条, 项目 16 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:46:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州12.jpg (file_id=13333, 项目 16 条)
2026-11-06 17:46:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州13.jpg(文件 1 条, 项目 34 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:46:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州13.jpg (file_id=13334, 项目 34 条)
2026-11-06 17:46:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州14.jpg(文件 1 条, 项目 25 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:46:59 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州14.jpg (file_id=13335, 项目 25 条)
2026-11-06 17:46:59 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州15.jpg(文件 1 条, 项目 9 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:47:01 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州15.jpg (file_id=13336, 项目 9 条)
2026-11-06 17:47:01 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州16.jpg(文件 1 条, 项目 34 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:47:04 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州16.jpg (file_id=13337, 项目 34 条)
2026-11-06 17:47:04 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州17.jpg(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:47:06 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州17.jpg (file_id=13338, 项目 20 条)
2026-11-06 17:47:07 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州18.jpg(文件 1 条, 项目 16 条, 通知 0 条, 分类声明 0 条)
横线分布不合理
2026-11-06 17:47:09 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州18.jpg (file_id=13339, 项目 16 条)
2026-11-06 17:47:09 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州19.jpg(文件 1 条, 项目 15 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:47:12 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州19.jpg (file_id=13340, 项目 15 条)
2026-11-06 17:47:12 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州2.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:47:13 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州2.jpg (file_id=13341, 项目 0 条)
2026-11-06 17:47:13 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州20.jpg(文件 1 条, 项目 35 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:47:17 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州20.jpg (file_id=13342, 项目 35 条)
2026-11-06 17:47:17 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州21.jpg(文件 1 条, 项目 6 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:47:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州21.jpg (file_id=13343, 项目 6 条)
2026-11-06 17:47:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州22.jpg(文件 1 条, 项目 13 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:47:21 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州22.jpg (file_id=13344, 项目 13 条)
2026-11-06 17:47:21 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州23.jpg(文件 1 条, 项目 22 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:47:25 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州23.jpg (file_id=13345, 项目 22 条)
2026-11-06 17:47:25 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州24.jpg(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:47:27 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州24.jpg (file_id=13346, 项目 20 条)
2026-11-06 17:47:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州3.jpg(文件 1 条, 项目 16 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:47:30 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州3.jpg (file_id=13347, 项目 16 条)
2026-11-06 17:47:30 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州4.jpg(文件 1 条, 项目 35 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:47:34 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州4.jpg (file_id=13348, 项目 35 条)
2026-11-06 17:47:34 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州5.jpg(文件 1 条, 项目 13 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:47:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州5.jpg (file_id=13349, 项目 13 条)
2026-11-06 17:47:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州6.jpg(文件 1 条, 项目 21 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:47:38 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州6.jpg (file_id=13350, 项目 21 条)
2026-11-06 17:47:39 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州7.jpg(文件 1 条, 项目 36 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:47:42 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州7.jpg (file_id=13351, 项目 36 条)
2026-11-06 17:47:42 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州8.jpg(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:47:44 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州8.jpg (file_id=13352, 项目 20 条)
2026-11-06 17:47:45 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 扬州9.jpg(文件 1 条, 项目 14 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:47:46 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 扬州9.jpg (file_id=13353, 项目 14 条)
2026-11-06 17:47:46 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0001.jpg(文件 1 条, 项目 15 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:47:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0001.jpg (file_id=13354, 项目 15 条)
2026-11-06 17:47:51 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0002.jpg(文件 1 条, 项目 21 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:47:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0002.jpg (file_id=13355, 项目 21 条)
2026-11-06 17:47:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0003.jpg(文件 1 条, 项目 18 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:47:59 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0003.jpg (file_id=13356, 项目 22 条)
2026-11-06 17:48:00 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0004.jpg(文件 1 条, 项目 18 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:48:04 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0004.jpg (file_id=13357, 项目 20 条)
2026-11-06 17:48:05 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0005.jpg(文件 1 条, 项目 18 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:48:09 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0005.jpg (file_id=13358, 项目 22 条)
2026-11-06 17:48:09 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0006.jpg(文件 1 条, 项目 21 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:48:13 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0006.jpg (file_id=13359, 项目 21 条)
2026-11-06 17:48:13 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0007.jpg(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:48:17 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0007.jpg (file_id=13360, 项目 20 条)
2026-11-06 17:48:17 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0008.jpg(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:48:21 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0008.jpg (file_id=13361, 项目 20 条)
2026-11-06 17:48:21 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0009.jpg(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:48:25 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0009.jpg (file_id=13362, 项目 21 条)
2026-11-06 17:48:25 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0010.jpg(文件 1 条, 项目 21 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:48:29 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0010.jpg (file_id=13363, 项目 21 条)
2026-11-06 17:48:29 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0011.jpg(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:48:33 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0011.jpg (file_id=13364, 项目 20 条)
2026-11-06 17:48:33 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0012.jpg(文件 1 条, 项目 21 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:48:37 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0012.jpg (file_id=13365, 项目 21 条)
2026-11-06 17:48:37 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0013.jpg(文件 1 条, 项目 22 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:48:42 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0013.jpg (file_id=13366, 项目 22 条)
2026-11-06 17:48:42 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0014.jpg(文件 1 条, 项目 18 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:48:46 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0014.jpg (file_id=13367, 项目 21 条)
2026-11-06 17:48:46 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0015.jpg(文件 1 条, 项目 19 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:48:50 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0015.jpg (file_id=13368, 项目 20 条)
2026-11-06 17:48:50 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0016.jpg(文件 1 条, 项目 22 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:48:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0016.jpg (file_id=13369, 项目 22 条)
2026-11-06 17:48:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0017.jpg(文件 1 条, 项目 21 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:48:59 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0017.jpg (file_id=13370, 项目 21 条)
2026-11-06 17:48:59 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0018.jpg(文件 1 条, 项目 21 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:49:03 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0018.jpg (file_id=13371, 项目 21 条)
2026-11-06 17:49:03 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0019.jpg(文件 1 条, 项目 22 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:49:08 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0019.jpg (file_id=13372, 项目 22 条)
2026-11-06 17:49:08 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0020.jpg(文件 1 条, 项目 22 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:49:12 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0020.jpg (file_id=13373, 项目 22 条)
2026-11-06 17:49:13 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0021.jpg(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:49:17 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0021.jpg (file_id=13374, 项目 20 条)
2026-11-06 17:49:17 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0022.jpg(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:49:22 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0022.jpg (file_id=13375, 项目 20 条)
2026-11-06 17:49:22 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0023.jpg(文件 1 条, 项目 21 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:49:27 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0023.jpg (file_id=13376, 项目 21 条)
2026-11-06 17:49:27 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0024.jpg(文件 1 条, 项目 21 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:49:31 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0024.jpg (file_id=13377, 项目 21 条)
2026-11-06 17:49:32 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2024年厦门市重点项目名单（简版）_page-0025.jpg(文件 1 条, 项目 20 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:49:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2024年厦门市重点项目名单（简版）_page-0025.jpg (file_id=13378, 项目 21 条)
2026-11-06 17:49:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 1.jpg(文件 1 条, 项目 32 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:49:42 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 1.jpg (file_id=13379, 项目 32 条)
2026-11-06 17:49:42 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2.jpg(文件 1 条, 项目 81 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:49:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2.jpg (file_id=13380, 项目 81 条)
2026-11-06 17:49:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 3.jpg(文件 1 条, 项目 111 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:50:07 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 3.jpg (file_id=13381, 项目 111 条)
2026-11-06 17:50:07 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0001.jpg(文件 1 条, 项目 61 条, 通知 0 条, 分类声明 0 条)                                                                                                                                                                                                                         
2026-11-06 17:50:18 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0001.jpg (file_id=13382, 项目 61 条)
2026-11-06 17:50:18 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0002.jpg(文件 1 条, 项目 64 条, 通知 0 条, 分类声明 0 条)                                                                                                                                                                                                                         
2026-11-06 17:50:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0002.jpg (file_id=13383, 项目 64 条)
2026-11-06 17:50:29 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0003.jpg(文件 1 条, 项目 69 条, 通知 0 条, 分类声明 0 条)                                                                                                                                                                                                                         
2026-11-06 17:50:37 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0003.jpg (file_id=13384, 项目 69 条)
2026-11-06 17:50:38 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0004.jpg(文件 1 条, 项目 60 条, 通知 0 条, 分类声明 0 条)                                                                                                                                                                                                                         
2026-11-06 17:50:46 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0004.jpg (file_id=13385, 项目 60 条)
2026-11-06 17:50:47 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0005.jpg(文件 1 条, 项目 65 条, 通知 0 条, 分类声明 0 条)                                                                                                                                                                                                                         
2026-11-06 17:50:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0005.jpg (file_id=13386, 项目 65 条)
2026-11-06 17:50:55 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0006.jpg(文件 1 条, 项目 62 条, 通知 0 条, 分类声明 0 条)                                                                                                                                                                                                                         
2026-11-06 17:51:01 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0006.jpg (file_id=13387, 项目 62 条)
2026-11-06 17:51:01 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0007.jpg(文件 1 条, 项目 71 条, 通知 0 条, 分类声明 0 条)                                                                                                                                                                                                                         
2026-11-06 17:51:08 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0007.jpg (file_id=13388, 项目 71 条)
2026-11-06 17:51:08 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0008.jpg(文件 1 条, 项目 56 条, 通知 0 条, 分类声明 0 条)                                                                                                                                                                                                                         
2026-11-06 17:51:14 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0008.jpg (file_id=13389, 项目 56 条)
2026-11-06 17:51:14 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0009.jpg(文件 1 条, 项目 64 条, 通知 0 条, 分类声明 0 条)                                                                                                                                                                                                                         
2026-11-06 17:51:22 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0009.jpg (file_id=13390, 项目 64 条)
2026-11-06 17:51:22 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0010.jpg(文件 1 条, 项目 57 条, 通知 0 条, 分类声明 0 条)                                                                                                                                                                                                                         
2026-11-06 17:51:30 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0010.jpg (file_id=13391, 项目 57 条)
2026-11-06 17:51:30 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0011.jpg(文件 1 条, 项目 61 条, 通知 0 条, 分类声明 0 条)                                                                                                                                                                                                                         
2026-11-06 17:51:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0011.jpg (file_id=13392, 项目 61 条)
2026-11-06 17:51:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0012.jpg(文件 1 条, 项目 66 条, 通知 0 条, 分类声明 0 条)                                                                                                                                                                                                                         
2026-11-06 17:51:43 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0012.jpg (file_id=13393, 项目 66 条)
2026-11-06 17:51:43 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0013.jpg(文件 1 条, 项目 66 条, 通知 0 条, 分类声明 0 条)                                                                                                                                                                                                                         
2026-11-06 17:51:50 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0013.jpg (file_id=13394, 项目 66 条)
2026-11-06 17:51:50 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0014.jpg(文件 1 条, 项目 55 条, 通知 0 条, 分类声明 0 条)                                                                                                                                                                                                                         
2026-11-06 17:51:57 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0014.jpg (file_id=13395, 项目 55 条)
2026-11-06 17:51:57 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0015.jpg(文件 1 条, 项目 61 条, 通知 0 条, 分类声明 0 条)                                                                                                                                                                                                                         
2026-11-06 17:52:03 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0015.jpg (file_id=13396, 项目 61 条)
2026-11-06 17:52:04 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0016.jpg(文件 1 条, 项目 59 条, 通知 0 条, 分类声明 0 条)                                                                                                                                                                                                                         
2026-11-06 17:52:09 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0016.jpg (file_id=13397, 项目 59 条)
2026-11-06 17:52:09 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0017.jpg(文件 1 条, 项目 52 条, 通知 0 条, 分类声明 0 条)                                                                                                                                                                                                                         
2026-11-06 17:52:16 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 附件：浙江省扩大有效投资“千项万亿”工程2024年重大建设项目实施计划项目表_page-0017.jpg (file_id=13398, 项目 52 条)
2026-11-06 17:52:16 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 8.更新项目清单（截止2024.7.23）.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:52:18 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 8.更新项目清单（截止2024.7.23）.jpg (file_id=13399, 项目 0 条)
2026-11-06 17:52:18 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 更新项目清单（截止2024.7.23）.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:52:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 更新项目清单（截止2024.7.23）.jpg (file_id=13400, 项目 0 条)
2026-11-06 17:52:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 封面.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=2, 乱码分=15.00），跳过解析
2026-11-06 17:52:21 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2024年重点项目\封面.jpg: 图片未识别到文本(疑似非清单图片)
2026-11-06 17:52:21 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 封面.jpg (file_id=13401, 项目 0 条)
2026-11-06 17:52:21 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 1.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
横线分布不合理
2026-11-06 17:52:23 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 1.jpg (file_id=13402, 项目 0 条)
2026-11-06 17:52:24 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 10.jpg(文件 1 条, 项目 7 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:52:30 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 10.jpg (file_id=13403, 项目 7 条)
2026-11-06 17:52:30 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 11.jpg(文件 1 条, 项目 9 条, 通知 0 条, 分类声明 0 条)
横线分布不合理
2026-11-06 17:52:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 11.jpg (file_id=13404, 项目 9 条)
2026-11-06 17:52:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 12.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:52:41 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 12.jpg (file_id=13405, 项目 4 条)
2026-11-06 17:52:41 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 13.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
横线分布不合理
2026-11-06 17:52:46 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 13.jpg (file_id=13406, 项目 0 条)
2026-11-06 17:52:46 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 14.jpg(文件 1 条, 项目 10 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:52:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 14.jpg (file_id=13407, 项目 10 条)
2026-11-06 17:52:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 15.jpg(文件 1 条, 项目 7 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:52:57 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 15.jpg (file_id=13408, 项目 10 条)
2026-11-06 17:52:57 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 16.jpg(文件 1 条, 项目 8 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:53:03 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 16.jpg (file_id=13409, 项目 8 条)
2026-11-06 17:53:03 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 17.jpg(文件 1 条, 项目 7 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:53:08 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 17.jpg (file_id=13410, 项目 7 条)
2026-11-06 17:53:08 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 18.jpg(文件 1 条, 项目 7 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:53:13 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 18.jpg (file_id=13411, 项目 7 条)
2026-11-06 17:53:13 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 19.jpg(文件 1 条, 项目 7 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:53:18 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 19.jpg (file_id=13412, 项目 7 条)
2026-11-06 17:53:18 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
横线分布不合理
2026-11-06 17:53:22 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2.jpg (file_id=13413, 项目 0 条)
2026-11-06 17:53:22 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 20.jpg(文件 1 条, 项目 7 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:53:27 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 20.jpg (file_id=13414, 项目 7 条)
2026-11-06 17:53:27 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 21.jpg(文件 1 条, 项目 7 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:53:32 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 21.jpg (file_id=13415, 项目 7 条)
2026-11-06 17:53:32 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 22.jpg(文件 1 条, 项目 7 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:53:37 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 22.jpg (file_id=13416, 项目 7 条)
2026-11-06 17:53:37 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 23.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:53:43 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 23.jpg (file_id=13417, 项目 0 条)
2026-11-06 17:53:43 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 24.jpg(文件 1 条, 项目 7 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:53:48 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 24.jpg (file_id=13418, 项目 7 条)
2026-11-06 17:53:48 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 25.jpg(文件 1 条, 项目 7 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:53:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 25.jpg (file_id=13419, 项目 7 条)
2026-11-06 17:53:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 26.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:53:57 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 26.jpg (file_id=13420, 项目 4 条)
2026-11-06 17:53:57 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 3.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
横线分布不合理
2026-11-06 17:54:01 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 3.jpg (file_id=13421, 项目 0 条)
2026-11-06 17:54:01 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 4.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
横线分布不合理
2026-11-06 17:54:03 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 4.jpg (file_id=13422, 项目 0 条)
2026-11-06 17:54:03 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 5.jpg(文件 1 条, 项目 8 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:54:08 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 5.jpg (file_id=13423, 项目 8 条)
2026-11-06 17:54:08 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 6.jpg(文件 1 条, 项目 10 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:54:14 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 6.jpg (file_id=13424, 项目 10 条)
2026-11-06 17:54:14 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 7.jpg(文件 1 条, 项目 6 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:54:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 7.jpg (file_id=13425, 项目 6 条)
2026-11-06 17:54:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 8.jpg(文件 1 条, 项目 6 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:54:23 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 8.jpg (file_id=13426, 项目 6 条)
2026-11-06 17:54:24 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 9.jpg(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:54:29 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 9.jpg (file_id=13427, 项目 6 条)
2026-11-06 17:54:29 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点储备项目计划表1.jpg(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:54:32 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点储备项目计划表1.jpg (file_id=13428, 项目 5 条)
2026-11-06 17:54:32 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点储备项目计划表10.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:54:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点储备项目计划表10.jpg (file_id=13429, 项目 4 条)
2026-11-06 17:54:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点储备项目计划表11.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:54:38 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点储备项目计划表11.jpg (file_id=13430, 项目 3 条)
2026-11-06 17:54:39 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点储备项目计划表2.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:54:42 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点储备项目计划表2.jpg (file_id=13431, 项目 3 条)
2026-11-06 17:54:42 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点储备项目计划表3.jpg(文件 1 条, 项目 2 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:54:46 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点储备项目计划表3.jpg (file_id=13432, 项目 2 条)
2026-11-06 17:54:46 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点储备项目计划表4.jpg(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:54:49 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点储备项目计划表4.jpg (file_id=13433, 项目 5 条)
2026-11-06 17:54:49 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点储备项目计划表5.jpg(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:54:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点储备项目计划表5.jpg (file_id=13434, 项目 5 条)
2026-11-06 17:54:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点储备项目计划表6.jpg(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:54:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点储备项目计划表6.jpg (file_id=13435, 项目 5 条)
2026-11-06 17:54:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点储备项目计划表7.jpg(文件 1 条, 项目 2 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:54:59 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点储备项目计划表7.jpg (file_id=13436, 项目 2 条)
2026-11-06 17:54:59 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点储备项目计划表8.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:55:02 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点储备项目计划表8.jpg (file_id=13437, 项目 4 条)
2026-11-06 17:55:02 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点储备项目计划表9.jpg(文件 1 条, 项目 2 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:55:06 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点储备项目计划表9.jpg (file_id=13438, 项目 2 条)
2026-11-06 17:55:06 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表1.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:55:09 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表1.jpg (file_id=13439, 项目 4 条)
2026-11-06 17:55:09 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表10.jpg(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:55:13 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表10.jpg (file_id=13440, 项目 5 条)
2026-11-06 17:55:13 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表11.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:55:16 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表11.jpg (file_id=13441, 项目 3 条)
2026-11-06 17:55:16 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表12.jpg(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:55:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表12.jpg (file_id=13442, 项目 5 条)
2026-11-06 17:55:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表13.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:55:23 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表13.jpg (file_id=13443, 项目 3 条)
2026-11-06 17:55:23 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表14.jpg(文件 1 条, 项目 2 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:55:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表14.jpg (file_id=13444, 项目 2 条)
2026-11-06 17:55:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表15.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:55:30 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表15.jpg (file_id=13445, 项目 4 条)
2026-11-06 17:55:30 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表16.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:55:33 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表16.jpg (file_id=13446, 项目 4 条)
2026-11-06 17:55:33 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表17.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:55:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表17.jpg (file_id=13447, 项目 3 条)
2026-11-06 17:55:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表18.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:55:39 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表18.jpg (file_id=13448, 项目 4 条)
2026-11-06 17:55:39 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表19.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:55:42 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表19.jpg (file_id=13449, 项目 3 条)
2026-11-06 17:55:42 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表2.jpg(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:55:46 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表2.jpg (file_id=13450, 项目 5 条)
2026-11-06 17:55:46 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表20.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:55:49 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表20.jpg (file_id=13451, 项目 3 条)
2026-11-06 17:55:49 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表21.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:55:52 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表21.jpg (file_id=13452, 项目 4 条)
2026-11-06 17:55:53 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表22.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:55:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表22.jpg (file_id=13453, 项目 4 条)
2026-11-06 17:55:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表23.jpg(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:55:59 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表23.jpg (file_id=13454, 项目 5 条)
2026-11-06 17:56:00 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表24.jpg(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:56:03 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表24.jpg (file_id=13455, 项目 5 条)
2026-11-06 17:56:03 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表25.jpg(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:56:07 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表25.jpg (file_id=13456, 项目 5 条)
2026-11-06 17:56:07 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表26.jpg(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:56:11 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表26.jpg (file_id=13457, 项目 5 条)
2026-11-06 17:56:11 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表27.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:56:14 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表27.jpg (file_id=13458, 项目 4 条)
2026-11-06 17:56:14 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表28.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=85, 乱码分=45.00），跳过解析
2026-11-06 17:56:16 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2025年重点项目\04重庆市2025年重点项目清单\荣昌区2025年\荣昌区2025年重点建设项目计 划表28.jpg: 图片未识别到文本(疑似非清单图片)                                                                                                                                                                                   
2026-11-06 17:56:17 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表28.jpg (file_id=13459, 项目 0 条)
2026-11-06 17:56:17 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表29.jpg(文件 1 条, 项目 2 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:56:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表29.jpg (file_id=13460, 项目 2 条)
2026-11-06 17:56:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表3.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:56:23 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表3.jpg (file_id=13461, 项目 3 条)
2026-11-06 17:56:23 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表30.jpg(文件 1 条, 项目 4 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:56:31 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表30.jpg (file_id=13462, 项目 4 条)
2026-11-06 17:56:31 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表31.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:56:35 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表31.jpg (file_id=13463, 项目 3 条)
2026-11-06 17:56:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表4.jpg(文件 1 条, 项目 2 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:56:39 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表4.jpg (file_id=13464, 项目 2 条)
2026-11-06 17:56:39 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表5.jpg(文件 1 条, 项目 5 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:56:45 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表5.jpg (file_id=13465, 项目 5 条)
2026-11-06 17:56:45 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表6.jpg(文件 1 条, 项目 1 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:56:50 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表6.jpg (file_id=13466, 项目 1 条)
2026-11-06 17:56:50 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表7.jpg(文件 1 条, 项目 2 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:56:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表7.jpg (file_id=13467, 项目 2 条)
2026-11-06 17:56:56 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表8.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:57:01 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表8.jpg (file_id=13468, 项目 3 条)
2026-11-06 17:57:02 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 荣昌区2025年重点建设项目计划表9.jpg(文件 1 条, 项目 3 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:57:06 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 荣昌区2025年重点建设项目计划表9.jpg (file_id=13469, 项目 3 条)
2026-11-06 17:57:06 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2025年巴彦淖尔市重大项目清单.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
[WARNING] 2026-11-06 17:57:12,954 [RapidOCR] main.py:132: The text detection result is empty
2026-11-06 17:57:12 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2025年重点项目\06内蒙古自治区2025年重点项目清单\巴彦淖尔市2025年\2025年巴彦淖尔市 重大项目清单.jpg: 图片未识别到文本(疑似非清单图片)                                                                                                                                                                             
2026-11-06 17:57:13 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2025年巴彦淖尔市重大项目清单.jpg (file_id=13470, 项目 0 条)
2026-11-06 17:57:13 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2025年仙桃市省级重点项目清单1.jpg(文件 1 条, 项目 8 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:57:17 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2025年仙桃市省级重点项目清单1.jpg (file_id=13471, 项目 8 条)
2026-11-06 17:57:17 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2025年仙桃市省级重点项目清单2.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:57:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2025年仙桃市省级重点项目清单2.jpg (file_id=13472, 项目 0 条)
2026-11-06 17:57:19 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2025重点项目封面.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=2, 乱码分=0.00），跳过解析
2026-11-06 17:57:20 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2025年重点项目\2025重点项目封面.jpg: 图片未识别到文本(疑似非清单图片)
2026-11-06 17:57:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2025重点项目封面.jpg (file_id=13473, 项目 0 条)
2026-11-06 17:57:20 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2025年广元市加快前期工作重大项日名单1.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
2026-11-06 17:57:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2025年广元市加快前期工作重大项日名单1.jpg (file_id=13474, 项目 0 条)
2026-11-06 17:57:28 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2025年广元市加快前期工作重大项日名单2.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=111, 乱码分=70.00），跳过解析
2026-11-06 17:57:36 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2025年重点项目\29四川省2025年重点项目清单\广元市2025年\2025年广元市加快前期工作重 大项日名单2.jpg: 图片未识别到文本(疑似非清单图片)                                                                                                                                                                              
2026-11-06 17:57:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2025年广元市加快前期工作重大项日名单2.jpg (file_id=13475, 项目 0 条)
2026-11-06 17:57:36 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2025年广元市加快前期工作重大项日名单3.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=174, 乱码分=55.00），跳过解析
2026-11-06 17:57:44 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2025年重点项目\29四川省2025年重点项目清单\广元市2025年\2025年广元市加快前期工作重 大项日名单3.jpg: 图片未识别到文本(疑似非清单图片)                                                                                                                                                                              
2026-11-06 17:57:44 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2025年广元市加快前期工作重大项日名单3.jpg (file_id=13476, 项目 0 条)
2026-11-06 17:57:44 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR - FAIL: 2025年广元市加快前期工作重大项日名单4.jpg - 跳过该文件（filter_file.txt）
2026-11-06 17:57:44 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 封面.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=2, 乱码分=15.00），跳过解析
2026-11-06 17:57:45 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2025年重点项目\封面.jpg: 图片未识别到文本(疑似非清单图片)
2026-11-06 17:57:45 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 封面.jpg (file_id=13477, 项目 0 条)
2026-11-06 17:57:45 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2026年广元市加快前期点项目清单.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=211, 乱码分=70.00），跳过解析
2026-11-06 17:58:08 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2026年重点项目\29四川省2026年重点项目清单\2026年广元市\2026年广元市加快前期点项目 清单.jpg: 图片未识别到文本(疑似非清单图片)                                                                                                                                                                                     
2026-11-06 17:58:09 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2026年广元市加快前期点项目清单.jpg (file_id=13478, 项目 0 条)
2026-11-06 17:58:09 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 2026年广元市重点项目清单.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=136, 乱码分=55.00），跳过解析
2026-11-06 17:58:25 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2026年重点项目\29四川省2026年重点项目清单\2026年广元市\2026年广元市重点项目清单.jpg: 图片未识别到文本(疑似非清单图片)                                                                                                                                                                                            
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 2026年广元市重点项目清单.jpg (file_id=13479, 项目 0 条)
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 清除旧数据: 封面.jpg(文件 1 条, 项目 0 条, 通知 0 条, 分类声明 0 条)
OCR 结果疑似乱码（items=2, 乱码分=15.00），跳过解析
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\parser\ocr_parser.py - WARNING - E:\STangWork\STangFiles\各省重点项目：2020年起\2026年重点项目\封面.jpg: 图片未识别到文本(疑似非清单图片)
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - OK: 封面.jpg (file_id=13480, 项目 0 条)
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\util\db_util.py - INFO - 数据库连接池已关闭
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - ========================================
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 批量测试完成: jpg 共 270 个
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - INFO - 成功: 235 个, 入库项目 3650 条 | 失败: 35 个 | 跳过: 0 个
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 1.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 1_副本.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 1_副本1.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 1_副本2.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 1_副本3.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 1_副本4.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2_副本.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2_副本1.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2_副本2.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2_副本3.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2_副本4.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 3.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 3_副本.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 3_副本1.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 3_副本2.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 3_副本3.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 4.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 4_副本.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 4_副本1.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 4_副本2.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 4_副本3.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 4_副本4.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 1.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 1.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 10.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 3.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 4.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 5.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 6.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 7.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 8.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 9.jpg: 跳过该文件（filter_file.txt）
2026-11-06 17:58:26 - E:\STangWork\PythonProjects\skp_parser\batch_test.py - ERROR -   - 2025年广元市加快前期工作重大项日名单4.jpg: 跳过该文件（filter_file.txt）'''
logs = log.replace('已保存到 output_lines.jpg','').split('\n')

logs = [l for l in logs if not l.startswith('[跳过]')]

fileName = ''
showLog = False
pronum_re = re.compile(r"项目 (\d+) 条")
fileId_re = re.compile(r"file_id=(\d+)")
pronum = 0
now_pronum = 0
epc = ''
file_ids = []
for i, l in enumerate(logs):
    if '清除旧数据' in l:
        fileName = logs[i + 1]
        if not fileName.startswith('E:'):
            fileName = ''.join(re.findall(r'清除旧数据: (.*?)\(文',l,re.DOTALL))
            epc = logs[i + 1] if not re.search('STangWork', logs[i + 1]) else ''
        else:
            epc = logs[i + 2] if not re.search('STangWork', logs[i + 2]) else ''
        tempnum = pronum_re.findall(l)
        pronum = tempnum[0] if tempnum else 0
        if not re.findall('OCR 结果|Using engine_name: onnxr',epc,re.DOTALL):
            showLog = True
    if f'OK: {fileName}' in l:
        tempnum = pronum_re.findall(l)
        fileId = fileId_re.findall(l)
        now_pronum = tempnum[0] if tempnum else 0
        file_Id = fileId[0] if fileId else 0
        # if showLog and (epc or pronum!=now_pronum):
        #     print(f'======【{fileName}】{file_Id}======')
        #     # print(f'======【{file_Id}】======')
        #     file_ids.append(file_Id)
        #     # print(rf'{fileName}')
        #     print(f"特殊：{epc}")
        #     print(f'原：项目条数，旧{pronum}，新{now_pronum}，{"不一致" if pronum!=now_pronum else "一致"}')
        if pronum!=now_pronum:
            print(f'======【{file_Id}】======')
            file_ids.append(file_Id)
            print(rf'文件名：{fileName}')
            print(f"特殊：{epc}")
            print(f'原：项目条数，旧{pronum}，新{now_pronum}，{"不一致" if pronum!=now_pronum else "一致"}')
        showLog = False
print(','.join(file_ids))

