# filter_utils.py
"""文件过滤工具:按 filter_file.txt 规则跳过文件。

规则文件每行一条,支持:
  - 含通配符(* ? [):  按完整路径通配匹配(规则可用 \ 或 / 作分隔符,
                       且允许任意目录前缀,便于匹配绝对路径)
  - 不含通配符:        完整文件名精确相等,或完整路径包含该串
空行和以 # 开头的行忽略。
"""
from __future__ import annotations

import fnmatch
from pathlib import Path

DEFAULT_FILTER_FILE = Path("filter_file.txt")


def load_rules(filter_file: Path = DEFAULT_FILTER_FILE) -> list[str]:
    """读取规则文件,返回规范化后的规则列表。文件不存在返回 []。"""
    if not filter_file.exists():
        return []
    return [
        r.strip().replace("\\", "/")
        for r in filter_file.read_text(encoding="utf-8").split("\n")
        if r.strip() and not r.strip().startswith("#")
    ]


def match_rule(rule: str, norm_path: str, file_name: str) -> bool:
    """单条规则是否命中。norm_path 为 / 分隔的完整路径。"""
    if any(c in rule for c in "*?["):
        return fnmatch.fnmatch(norm_path, rule) or fnmatch.fnmatch(norm_path, f"*/{rule}")
    return rule == file_name or rule in norm_path


def match_any(file_path: str | Path,
              filter_file: Path = DEFAULT_FILTER_FILE) -> str | None:
    """命中返回命中的规则字符串,未命中返回 None。"""
    norm = str(file_path).replace("\\", "/")
    name = norm.rsplit("/", 1)[-1]
    for rule in load_rules(filter_file):
        if match_rule(rule, norm, name):
            return rule
    return None


def is_filtered(file_path: str | Path,
                filter_file: Path = DEFAULT_FILTER_FILE) -> bool:
    """便捷布尔接口。"""
    return match_any(file_path, filter_file) is not None