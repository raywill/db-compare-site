#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
db-compare-site 构建脚本
把 profiles/*.md（中/英双语档案）预渲染成纯静态 HTML 站点。
只用 Python 3 标准库。幂等：重复运行结果一致。
输出: site/index.html, site/profile-<slug>.html, site/compare.html,
      site/methodology.html, site/advisor.html, site/assets/*
用法: python3 build.py   (在 site/ 目录下运行)
"""
import re
import os
import html
import json
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent
SRC = SITE.parent / "profiles"

SLUGS = [
    "mysql", "postgresql", "oracle", "sqlserver", "mariadb",
    "oceanbase", "tidb", "edb", "cockroachdb", "yugabytedb",
    "aurora", "alloydb", "polardb", "tdsql", "spanner",
    "redis-valkey", "etcd", "dynamodb", "cassandra-scylladb", "mongodb",
    "clickhouse", "doris", "starrocks", "duckdb", "databricks", "snowflake",
    "redshift", "bigquery",
    "milvus", "weaviate", "qdrant",
]
# 领域体系：加新领域（如时序、图）只需在这里加一行 + DOMAIN_OF 映射
DOMAINS = [
    ("oltp", "关系型 OLTP", "Relational OLTP"),
    ("kvdoc", "KV · 宽列 · 文档", "KV · Wide-column · Document"),
    ("olap", "OLAP", "OLAP"),
    ("aidb", "AI 数据库", "AI databases"),
]
DOMAIN_NAMES = {d: (zh, en) for d, zh, en in DOMAINS}
# 产品英文显示名（英文模式零中文要求：不从中文档案标题派生）
NAME_EN = {
    "mysql": "MySQL", "postgresql": "PostgreSQL", "oracle": "Oracle Database",
    "sqlserver": "Microsoft SQL Server", "mariadb": "MariaDB",
    "oceanbase": "OceanBase", "tidb": "TiDB", "edb": "EDB Postgres",
    "cockroachdb": "CockroachDB", "yugabytedb": "YugabyteDB",
    "aurora": "Amazon Aurora", "alloydb": "Google AlloyDB",
    "polardb": "PolarDB", "tdsql": "Tencent Cloud TDSQL",
    "spanner": "Google Spanner",
    "redis-valkey": "Redis / Valkey", "etcd": "etcd",
    "dynamodb": "Amazon DynamoDB",
    "cassandra-scylladb": "Apache Cassandra / ScyllaDB", "mongodb": "MongoDB",
    "clickhouse": "ClickHouse", "doris": "Apache Doris",
    "starrocks": "StarRocks", "duckdb": "DuckDB",
    "databricks": "Databricks", "snowflake": "Snowflake",
    "redshift": "Amazon Redshift", "bigquery": "Google BigQuery",
    "milvus": "Milvus", "weaviate": "Weaviate", "qdrant": "Qdrant",
}
# 领域体系：一个产品可属多个领域（列表，第一项为主领域；展示/筛选时按所属领域出现）
DOMAIN_OF = {
    "mysql": ["oltp"], "postgresql": ["oltp"], "oracle": ["oltp"], "sqlserver": ["oltp"],
    "mariadb": ["oltp"], "oceanbase": ["oltp", "olap", "aidb"], "tidb": ["oltp"], "edb": ["oltp"],
    "cockroachdb": ["oltp"], "yugabytedb": ["oltp"], "aurora": ["oltp"], "alloydb": ["oltp"],
    "polardb": ["oltp"], "tdsql": ["oltp"], "spanner": ["oltp"],
    "redis-valkey": ["kvdoc"], "etcd": ["kvdoc"], "dynamodb": ["kvdoc"],
    "cassandra-scylladb": ["kvdoc"], "mongodb": ["kvdoc"],
    "clickhouse": ["olap"], "doris": ["olap"], "starrocks": ["olap"], "duckdb": ["olap"],
    "databricks": ["olap"], "snowflake": ["olap"], "redshift": ["olap"], "bigquery": ["olap"],
    "milvus": ["aidb"], "weaviate": ["aidb"], "qdrant": ["aidb"],
}

# 19 固定硬维度：中英名称 + 名称匹配关键词（只匹配维度名，不匹配正文）
DIMS = [
    {"zh": "静态加密 / TDE", "en": "Data-at-rest encryption / TDE",
     "keys": ["静态加密", "TDE", "tde", "数据加密", "Data-at-rest", "data-at-rest", "at rest"]},
    {"zh": "TLS / 传输加密", "en": "TLS / transport encryption",
     "keys": ["传输加密", "TLS", "SSL", "Transport encryption", "transport encryption", "in transit"]},
    {"zh": "审计", "en": "Auditing",
     "keys": ["审计", "Audit", "audit"]},
    {"zh": "认证与权限", "en": "Authentication & authorization",
     "keys": ["认证", "权限", "Authentication", "authorization"]},
    {"zh": "备份恢复", "en": "Backup & recovery",
     "keys": ["备份", "恢复", "Backup", "recovery"]},
    {"zh": "可观测性", "en": "Observability",
     "keys": ["可观测", "Observability", "observability"]},
    {"zh": "连接模型", "en": "Connection model",
     "keys": ["连接", "Connection", "connection"]},
    {"zh": "事务与隔离级别", "en": "Transactions & isolation levels",
     "keys": ["事务", "Transaction", "transaction"]},
    {"zh": "复制与一致性", "en": "Replication & consistency",
     "keys": ["复制", "Replication", "replication"]},
    {"zh": "扩展方式", "en": "Scaling",
     "keys": ["扩展", "分片", "Scal", "scal"]},
    {"zh": "兼容性", "en": "Compatibility",
     "keys": ["兼容", "Compatib", "compatib"]},
    {"zh": "许可证与商业模式", "en": "License & business model",
     "keys": ["许可", "商业模式", "Licens", "licens"]},
    {"zh": "中文资料丰富度", "en": "Chinese-language resources",
     "keys": ["中文资料", "中文", "Chinese", "chinese"]},
    {"zh": "性能与延迟特征", "en": "Performance & latency",
     "keys": ["性能", "延迟", "Performance", "performance", "Latency", "latency"]},
    {"zh": "合规与认证", "en": "Compliance & certifications",
     "keys": ["合规", "信创", "国测", "等保", "资质", "Compliance", "compliance",
              "Certification", "certification"]},
    {"zh": "成熟度与社区生态", "en": "Maturity & community",
     "keys": ["成熟度", "社区生态", "Maturity", "maturity"]},
    {"zh": "标杆用户", "en": "Notable adopters",
     "keys": ["标杆", "Notable adopters", "notable adopters"]},
    {"zh": "生态工具链", "en": "Ecosystem tooling",
     "keys": ["工具链", "Tooling", "tooling"]},
    {"zh": "云托管与 Serverless", "en": "Managed & serverless",
     "keys": ["云托管", "Serverless", "serverless", "Managed", "managed"]},
    {"zh": "数据接入与摄入", "en": "Data ingestion",
     "keys": ["数据接入", "数据摄入", "Ingestion", "ingestion", "接入"]},
    {"zh": "外部数据访问", "en": "External data access",
     "keys": ["外部数据", "External data", "联邦查询", "外部表"]},
    {"zh": "CDC 与下游同步", "en": "CDC & downstream",
     "keys": ["CDC", "cdc", "下游同步", "Downstream", "downstream"]},
    {"zh": "TTL 与数据生命周期管理", "en": "TTL & data lifecycle",
     "keys": ["TTL", "ttl", "生命周期", "Lifecycle", "数据过期"]},
    {"zh": "在线 DDL 与 Schema 演进", "en": "Online DDL & schema evolution",
     "keys": ["在线 DDL", "Online DDL", "Schema 演进", "schema evolution"]},
    {"zh": "多租户与资源隔离", "en": "Multi-tenancy & resource isolation",
     "keys": ["多租户", "资源隔离", "Multi-tenancy", "multi-tenancy", "资源组"]},
    {"zh": "跨地域多活", "en": "Cross-region active-active",
     "keys": ["多活", "跨地域", "active-active", "Active-active", "multi-region"]},
    {"zh": "高可用架构与 RTO/RPO", "en": "HA & RTO/RPO",
     "keys": ["高可用", "RTO", "RPO", "故障切换", "failover", "High availability"]},
    {"zh": "行级安全与数据脱敏", "en": "Row-level security & masking",
     "keys": ["行级安全", "数据脱敏", "脱敏", "RLS", "masking"]},
    {"zh": "JSON 与半结构化能力", "en": "JSON & semi-structured",
     "keys": ["半结构化", "semi-structured", "JSONB", "jsonb"]},
    {"zh": "全文检索能力", "en": "Full-text search",
     "keys": ["全文检索", "全文索引", "Full-text", "full-text", "全文搜索"]},
    {"zh": "存储效率与压缩", "en": "Storage efficiency & compression",
     "keys": ["存储效率", "存储放大", "Compression", "数据压缩"]},
    {"zh": "开源协议与厂商锁定风险", "en": "OSS license & lock-in risk",
     "keys": ["厂商锁定", "lock-in", "Lock-in", "SSPL", "开源协议"]},
    {"zh": "查询优化器与计划稳定性", "en": "Optimizer & plan stability",
     "keys": ["查询优化器", "计划稳定性", "执行计划", "plan stability"]},
    {"zh": "参数调优与自治能力", "en": "Tuning & autonomy",
     "keys": ["参数调优", "自治", "autonomous", "Autonomous", "autonomy", "Autonomy", "调优复杂度", "Tuning &"]},
    {"zh": "静默数据损坏防护", "en": "Silent corruption protection",
     "keys": ["静默损坏", "corruption", "Corruption", "checksum", "页校验"]},
    {"zh": "存储过程/触发器/过程语言", "en": "Stored procedures & triggers",
     "keys": ["存储过程", "触发器", "过程语言", "Stored procedure"]},
    {"zh": "约束与数据完整性", "en": "Constraints & integrity",
     "keys": ["数据完整性", "完整性约束", "外键约束", "integrity"]},
    {"zh": "分析 SQL 完备性", "en": "Analytical SQL",
     "keys": ["分析 SQL", "窗口函数", "window function", "分析函数"]},
    {"zh": "被遗忘权与数据擦除", "en": "Right to erasure",
     "keys": ["被遗忘", "数据擦除", "erasure", "Erasure", "删除权"]},
    {"zh": "数据血缘与目录集成", "en": "Data lineage & catalog",
     "keys": ["数据血缘", "血缘", "lineage", "Lineage", "数据目录"]},
    {"zh": "存算分离 vs 存算一体", "en": "Storage-compute architecture",
     "keys": ["存算分离", "存算一体", "存算", "disaggregated", "Storage-compute", "storage-compute"]},
    {"zh": "多模能力", "en": "Multi-model",
     "keys": ["多模", "Multi-model", "multi-model", "多模型"]},
    {"zh": "FinOps 成本可观测性", "en": "FinOps & cost observability",
     "keys": ["FinOps", "finops", "成本可观测", "成本归因"]},
    {"zh": "驱动与多语言生态", "en": "Drivers & clients",
     "keys": ["驱动", "Driver", "JDBC", "ODBC", "客户端生态"]},
    {"zh": "物化视图", "en": "Materialized views",
     "keys": ["物化视图", "Materialized view", "materialized view", "预聚合"]},
    {"zh": "支持跨云", "en": "Multi-cloud support",
     "keys": ["跨云", "多云", "Multi-cloud", "multi-cloud"]},
    {"zh": "热点数据更新能力", "en": "Hotspot update handling",
     "keys": ["热点数据更新", "热点更新", "Hotspot update", "hotspot"]},
]


def match_dim(name):
    """只用维度名称匹配，返回索引或 None。长 key 优先，避免“合规与认证”误匹配到“认证与权限”。"""
    best = None
    best_len = -1
    for idx, dim in enumerate(DIMS):
        # 全名精确匹配优先级最高
        if name == dim["zh"] or name == dim["en"]:
            return idx
        for k in dim["keys"]:
            if k in name and len(k) > best_len:
                best = idx
                best_len = len(k)
    return best


# ---------------------------------------------------------------------------
# 轻量 Markdown -> HTML（处理：标题/分隔线/引用/代码围栏/表格/列表/段落；
# 行内：代码/加粗/斜体/链接/图片）
# ---------------------------------------------------------------------------

def md_inline(s):
    s = html.escape(s)
    codes = []

    def save_code(m):
        codes.append(m.group(1))
        return "\x00CODE%d\x00" % (len(codes) - 1)

    s = re.sub(r"`([^`]+?)`", save_code, s)
    s = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)",
               r'<img alt="\1" src="\2" loading="lazy"/>', s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)",
               r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", s)
    for i, c in enumerate(codes):
        s = s.replace("\x00CODE%d\x00" % i, "<code>%s</code>" % c)
    return s


def _split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def _is_table(lines, i):
    if i + 1 >= len(lines):
        return False
    if "|" not in lines[i]:
        return False
    sep = lines[i + 1].strip()
    if "-" not in sep:
        return False
    if not re.match(r"^\|?[\s:|\-]+\|?$", sep):
        return False
    return True


def _render_table(lines, i):
    headers = _split_row(lines[i])
    j = i + 2
    rows = []
    while j < len(lines) and lines[j].strip() and "|" in lines[j]:
        rows.append(_split_row(lines[j]))
        j += 1
    out = ["<div class=\"table-wrap\"><table>"]
    out.append("<thead><tr>" + "".join("<th>%s</th>" % md_inline(h) for h in headers) + "</tr></thead>")
    if rows:
        out.append("<tbody>")
        for r in rows:
            cells = r + [""] * (len(headers) - len(r))
            out.append("<tr>" + "".join("<td>%s</td>" % md_inline(c) for c in cells[:len(headers)]) + "</tr>")
        out.append("</tbody>")
    out.append("</table></div>")
    return "\n".join(out), j


def _indent_of(line):
    n = 0
    for ch in line:
        if ch == " ":
            n += 1
        elif ch == "\t":
            n += 4
        else:
            break
    return n


_LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")


def _render_list(lines, i):
    items = []  # (indent, ordered, text_lines[])
    base = _indent_of(lines[i])
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                m = _LIST_RE.match(lines[j])
                if m and _indent_of(lines[j]) >= base:
                    i = j
                    continue
            break
        m = _LIST_RE.match(ln)
        if m:
            ind = _indent_of(ln)
            if ind < base:
                break
            ordered = bool(re.match(r"\d+[.)]", m.group(2)))
            items.append([ind, ordered, [m.group(3)]])
            i += 1
            continue
        if items and _indent_of(ln) > items[-1][0]:
            items[-1][2].append(ln.strip())
            i += 1
            continue
        break
    html_out, _ = _build_list(items, 0, base - 1)
    return html_out, i


def _build_list(items, pos, parent_indent):
    if pos >= len(items):
        return "", pos
    level_indent = items[pos][0]
    tag = "ol" if items[pos][1] else "ul"
    out = ["<%s>" % tag]
    while pos < len(items) and items[pos][0] == level_indent:
        _, _, text_lines = items[pos]
        pos += 1
        sub = ""
        if pos < len(items) and items[pos][0] > level_indent:
            sub, pos = _build_list(items, pos, level_indent)
        text = md_inline(" ".join(t for t in text_lines if t).strip())
        out.append("<li>%s%s</li>" % (text, sub))
    out.append("</%s>" % tag)
    return "\n".join(out), pos


def _is_block_start(line):
    s = line.strip()
    if not s:
        return True
    if re.match(r"^#{1,6}\s", line):
        return True
    if re.match(r"^\s*([-*_]\s*){3,}\s*$", line):
        return True
    if line.startswith("```") or line.startswith(">"):
        return True
    if _LIST_RE.match(line):
        return True
    return False


def render_md(text):
    lines = text.split("\n")
    out = []
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m:
            level = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (level, md_inline(m.group(2).strip()), level))
            i += 1
            continue
        if re.match(r"^\s*([-*_]\s*){3,}\s*$", ln):
            out.append("<hr/>")
            i += 1
            continue
        if ln.startswith("```"):
            buf = []
            i += 1
            while i < n and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(buf)))
            continue
        if ln.startswith(">"):
            buf = []
            while i < n and lines[i].startswith(">"):
                buf.append(lines[i][1:].lstrip())
                i += 1
            out.append("<blockquote>\n%s\n</blockquote>" % render_md("\n".join(buf)))
            continue
        if _is_table(lines, i):
            tbl, i = _render_table(lines, i)
            out.append(tbl)
            continue
        if _LIST_RE.match(ln):
            lst, i = _render_list(lines, i)
            out.append(lst)
            continue
        buf = [ln.strip()]
        i += 1
        while i < n and lines[i].strip() and not _is_block_start(lines[i]) and not _is_table(lines, i):
            buf.append(lines[i].strip())
            i += 1
        out.append("<p>%s</p>" % md_inline(" ".join(buf)))
    return "\n".join(out)

# ---------------------------------------------------------------------------
# 档案解析（容错：任何解析失败都回退为整节原文，不丢内容）
# ---------------------------------------------------------------------------

def split_sections(lines):
    """按 ## 切分，返回 [(title, body_lines)]（不含标题行本身）。"""
    secs = []
    cur_title, cur = None, None
    for ln in lines:
        m = re.match(r"^##\s+(.*)$", ln)
        if m:
            if cur_title is not None:
                secs.append((cur_title, cur))
            cur_title = m.group(1).strip()
            cur = []
        elif cur is not None:
            cur.append(ln)
    if cur_title is not None:
        secs.append((cur_title, cur))
    return secs


def classify_section(title):
    t = title
    tl = title.lower()
    if "硬维度" in t or "hard dimension" in tl or "固定题库" in t or "fixed question" in tl:
        return "dims"
    if "杀手特性" in t or "killer" in tl:
        return "killer"
    if "深水区" in t or ("deep" in tl and "dive" in tl) or ("deep" in tl and "water" in tl):
        return "deep"
    if "产品特色深挖" in t:
        return "killer_extra"
    if "最买账" in t or re.search(r"users?\s+(love|praise)|top 5|buy into|buy most|value most|praised", tl):
        return "loved"
    if "吐槽" in t or "complaint" in tl or "gripe" in tl or "grumble" in tl:
        return "complaints"
    if "判决" in t or "verdict" in tl:
        return "verdict"
    if "待验证" in t or "to-be-verified" in tl:
        return "tbd"
    if "来源" in t or "source" in tl or "更新记录" in t or "changelog" in tl:
        return "sources"
    if "基本信息" in t or "basic" in tl:
        return "basics"
    if "一句话定位" in t or re.search(r"one-?line|positioning", tl):
        return "oneliner"
    if "分类标签" in t or "tag" in tl:
        return "tags"
    return "extra"


def clean_name(title_line):
    t = re.sub(r"^#\s*", "", title_line).strip()
    t = re.sub(r"^(数据库档案|示例档案|研究档案|档案|Sample Profile|Database Profile|Profile)\s*[:：]?\s*", "", t)
    t = re.sub(r"\s*[（(]\s*(中文|英文|English)\s*[)）]\s*$", "", t)
    t = re.sub(r"\s*(数据库档案|研究档案|Database Profile|Research Profile|档案|Profile)\s*$", "", t)
    return t.strip()


def first_paragraph(body_lines):
    buf = []
    for ln in body_lines:
        s = ln.strip()
        if not s:
            if buf:
                break
            continue
        if s.startswith(">"):
            s = s[1:].strip()
        if s.startswith(("#", "|", "-", "*", "1.", "2.", "3.")):
            if buf:
                break
            continue
        buf.append(s)
    return " ".join(buf).strip()


def extract_tags(body_lines):
    text = "\n".join(body_lines)
    tags = re.findall(r"#([\w\u4e00-\u9fff][\w\u4e00-\u9fff\-]*)", text)
    seen, out = set(), []
    for tg in tags:
        if tg not in seen:
            seen.add(tg)
            out.append(tg)
    return out


def fullname_from_basics(body_lines):
    for ln in body_lines:
        m = re.match(r"^\|\s*(全称|Full name)\s*\|\s*(.+?)\s*\|?\s*$", ln)
        if m:
            return m.group(2).strip()
    return ""


# ---- 硬维度切分 ----

def _dim_name_and_rest_h3(header):
    h = re.sub(r"^#{3}\s*", "", header).strip()
    h = re.sub(r"^\d{1,2}[.)、]\s*", "", h)
    for sep in ("——", "——", "：", ":", "—", "–"):
        if sep in h:
            name, rest = h.split(sep, 1)
            return name.strip(), rest.strip()
    return h.strip(), ""


def _dim_name_and_rest_list(line):
    m = re.match(r"^(?:\d{1,2}[.)]|[-*+])\s+\*\*(.+?)\*\*\s*(.*)$", line.strip())
    if not m:
        return None, None
    name = m.group(1).strip()
    rest = m.group(2).strip()
    rest = re.sub(r"^[：:———–\-]+\s*", "", rest)
    # 名称里可能自带结论（如 **备份恢复——有**），拆出来并入 rest
    for sep in ("——", "——", "：", ":", "—", "–"):
        if sep in name:
            n, v = name.split(sep, 1)
            name, rest = n.strip(), (v.strip() + " " + rest).strip()
            break
    return name, rest


def split_dim_items(body_lines):
    """返回 (items, extras, style, intro_lines)。
    items: [{'name','rest','body':[...]}]; extras: 补充维度条目。"""
    has_h3 = any(re.match(r"^###\s+", ln) for ln in body_lines)
    has_numbered = any(re.match(r"^\d{1,2}[.)]\s+\*\*", ln) for ln in body_lines)
    has_bullet = any(re.match(r"^[-*+]\s+\*\*", ln) for ln in body_lines)
    style = "h3" if has_h3 else ("numbered" if has_numbered else ("bullet" if has_bullet else "none"))

    items, extras = [], []
    cur, in_extras = None, False
    intro = []

    def push():
        nonlocal cur
        if cur:
            (extras if in_extras else items).append(cur)
            cur = None

    for ln in body_lines:
        s = ln.strip()
        if re.match(r"^\*\*.+(补充维度|supplementary dimensions).+\*\*", s, re.IGNORECASE):
            push()
            in_extras = True
            extras.append({"name": "补充维度", "rest": "", "body": [], "_note": True})
            continue
        new_item = None
        if style == "h3" and re.match(r"^###\s+", ln):
            name, rest = _dim_name_and_rest_h3(ln)
            new_item = {"name": name, "rest": rest, "body": []}
        elif style == "numbered" and re.match(r"^\d{1,2}[.)]\s+\*\*", ln):
            name, rest = _dim_name_and_rest_list(ln)
            new_item = {"name": name, "rest": rest, "body": []}
        elif style == "bullet" and re.match(r"^[-*+]\s+\*\*", ln):
            name, rest = _dim_name_and_rest_list(ln)
            new_item = {"name": name, "rest": rest, "body": []}
        if new_item:
            push()
            cur = new_item
        elif cur is not None:
            cur["body"].append(ln)
        elif not items and not extras:
            intro.append(ln)
        else:
            # 游离行：并入上一条，避免丢内容
            (extras if in_extras else items)[-1]["body"].append(ln)
    push()
    return items, extras, style, intro


VERDICT_ZH_BOLD = re.compile(r"\*\*((?:部分支持|未找到证据|查证为无|不支持|不适用|无|有))[^*]{0,20}\*\*")
VERDICT_ZH_EARLY = re.compile(r"(部分支持|未找到证据|查证为无|不支持|不适用|无|有)")
VERDICT_EN_BOLD = re.compile(r"\*\*((?:Partially supported|Not supported|Supported|No\b[^*]{0,28}))\*\*", re.IGNORECASE)
VERDICT_EN_EARLY = re.compile(
    r"(Partially supported|Not supported|Supported|"
    r"No (?:native|built-in|official|public|engine|user-side|multi-row|more than)\b[^.。；]{0,24})",
    re.IGNORECASE)


def _zh_class(kw):
    if kw == "部分支持":
        return "partial"
    if kw == "未找到证据":
        return "tbd"
    if kw in ("查证为无", "不支持", "无"):
        return "no"
    if kw == "不适用":
        return "neutral"
    return "yes"


def extract_verdict(name, rest, body_lines, lang):
    # 策略：加粗结论优先；否则只看行首（前 15 字）避免正文串扰；最后看正文加粗
    body_txt = "\n".join(body_lines[:4])
    if lang == "zh":
        m = VERDICT_ZH_BOLD.search(rest)
        if m:
            inner = m.group(0)[len(m.group(1)) + 2:-2]
            return (m.group(1) + inner).strip(), _zh_class(m.group(1))
        head = re.sub(r"[*`]+", "", rest)[:15]
        m = VERDICT_ZH_EARLY.search(head)
        if m:
            kw = m.group(1)
            return (kw + _clean_after(re.sub(r"[*`]+", "", rest)[m.end():])).strip(), _zh_class(kw)
        m = VERDICT_ZH_BOLD.search(body_txt)
        if m:
            inner = m.group(0)[len(m.group(1)) + 2:-2]
            return (m.group(1) + inner).strip(), _zh_class(m.group(1))
        src_txt = re.sub(r"[*`]+", "", rest).strip() or re.sub(r"[*`]+", "", body_txt).strip()
        phrase = _clean_after(src_txt)[:16].strip()
        return (phrase or "—"), "neutral"
    else:
        m = VERDICT_EN_BOLD.search(rest)
        if m:
            kw = m.group(1).strip()
            kl = kw.lower()
            if kl.startswith("partially"):
                return kw, "partial"
            if kl.startswith("not supported") or kl == "no" or kl.startswith("no "):
                after = _clean_after(re.sub(r"[*`]+", "", rest)[m.end():])
                return ("No " + after).strip() if kl in ("no",) or kl.startswith("no ") and len(kw) <= 3 else kw, "no"
            return kw, "yes"
        head = re.sub(r"[*`]+", "", rest)[:18]
        m = VERDICT_EN_EARLY.search(head)
        if m:
            kw = m.group(1).strip()
            kl = kw.lower()
            if kl.startswith("partially"):
                return kw, "partial"
            if kl.startswith("not supported") or kl.startswith("no"):
                return re.sub(r"[.。；;()（）]$", "", kw), "no"
            return kw, "yes"
        m = VERDICT_EN_BOLD.search(body_txt)
        if m:
            kw = m.group(1).strip()
            kl = kw.lower()
            if kl.startswith("partially"):
                return kw, "partial"
            if kl.startswith("not supported") or kl.startswith("no"):
                return kw, "no"
            return kw, "yes"
        src_txt = re.sub(r"[*`]+", "", rest).strip() or re.sub(r"[*`]+", "", body_txt).strip()
        phrase = _clean_after(src_txt.split(".")[0])[:28].strip()
        return (phrase or "—"), "neutral"


def _clean_after(after):
    after = after.split("。")[0].split("；")[0][:18]
    after = re.sub(r"\s+", " ", after).strip()
    after = re.sub(r"^[-–—•\s]+", "", after)
    after = re.sub(r"[（(][^）)]*$", "", after)
    return after.strip()


def parse_profile(path):
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    title_line = next((l for l in lines if l.startswith("# ")), path.stem)
    lang = "en" if path.stem.endswith(".en") else "zh"
    prof = {
        "slug": re.sub(r"\.en$", "", path.stem),
        "lang": lang,
        "name": clean_name(title_line),
        "sections": {},   # kind -> list of (title, body_lines)
        "fallbacks": [],
    }
    for title, body in split_sections(lines):
        kind = classify_section(title)
        prof["sections"].setdefault(kind, []).append((title, body))
    return prof


# ---------------------------------------------------------------------------
# 证据等级徽章
# ---------------------------------------------------------------------------

EV_LEVELS = {
    "官方文档": ("ev-official", "官方文档", "official docs"),
    "厂商口径": ("ev-vendor", "厂商口径", "vendor claim"),
    "社区实测": ("ev-tested", "社区实测", "community-tested"),
    "社区共识": ("ev-consensus", "社区共识", "community consensus"),
    "待验证": ("ev-tbd", "待验证", "to-be-verified"),
    "official docs": ("ev-official", "官方文档", "official docs"),
    "vendor claim": ("ev-vendor", "厂商口径", "vendor claim"),
    "community-tested": ("ev-tested", "社区实测", "community-tested"),
    "community consensus": ("ev-consensus", "社区共识", "community consensus"),
    "to-be-verified": ("ev-tbd", "待验证", "to-be-verified"),
}

EV_NAMES = "(?:官方文档|厂商口径|社区实测|社区共识|待验证|official docs|vendor claim|community-tested|community consensus|to-be-verified)"


def _badge(cls, zh, en):
    return '<span class="ev %s" data-zh="%s" data-en="%s">%s</span>' % (cls, zh, en, zh)


def _combo_to_badges(inner):
    parts = re.split(r"\s*/\s*", inner.strip().strip("()（）").strip())
    out, hit = [], False
    for p in parts:
        p = p.strip()
        if p in EV_LEVELS:
            cls, zh, en = EV_LEVELS[p]
            out.append(_badge(cls, zh, en))
            hit = True
        elif p:
            out.append(html.escape(p))
    if not hit:
        return None
    return " ".join(out)


def _repl_code_strong(m):
    tag = m.group(1)
    inner = m.group(2)
    badges = _combo_to_badges(inner)
    if badges is None:
        return m.group(0)
    return badges


def apply_badges(page_html):
    h = page_html
    h = re.sub(r"<(code|strong)>(.*?)</\1>", _repl_code_strong, h)

    def repl_paren_en(m):
        cls, zh, en = EV_LEVELS[m.group(1)]
        return _badge(cls, zh, en)

    h = re.sub(r"\((official docs|vendor claim|community-tested|community consensus|to-be-verified)\)", repl_paren_en, h)
    h = re.sub("（(%s(?:/%s)*)）" % (EV_NAMES, EV_NAMES),
               lambda m: _combo_to_badges(m.group(1)) or m.group(0), h)

    def repl_evidence(m):
        prefix = m.group(1)
        badges = _combo_to_badges(m.group(2))
        if badges is None:
            return m.group(0)
        return prefix + badges

    h = re.sub(
        r"(证据[：:]\s*|｜)((?:官方文档|厂商口径|社区实测|社区共识|待验证)"
        r"(?:\s*[/+、]\s*(?:官方文档|厂商口径|社区实测|社区共识|待验证))*)",
        repl_evidence, h)
    return h

# ---------------------------------------------------------------------------
# 页面模板
# ---------------------------------------------------------------------------

# main() 在生成页面前写入：window.DB_CATALOG / window.DB_DOMAINS，供 app.js 的全局对比托盘使用
_CATALOG_SCRIPT = "window.DB_CATALOG=[];window.DB_DOMAINS={};"


def page_shell(title_zh, title_en, body_html, active="index", tail_scripts=""):
    nav = [
        ("index.html", "首页", "Home"),
        ("compare.html", "维度对比", "Compare"),
        ("advisor.html", "AI选型", "AI Selection"),
        ("cases.html", "场景案例", "Case Library"),
        ("methodology.html", "方法论", "Methodology"),
    ]
    nav_html = "\n".join(
        '<a href="%s" class="%s" data-zh="%s" data-en="%s">%s</a>'
        % (href, "active" if href.startswith(active) else "", zh, en, zh)
        for href, zh, en in nav
    )
    # 移动端下拉导航（对比托盘按钮除外，保持原样）
    nav_options = "\n".join(
        '<option value="%s"%s data-zh="%s" data-en="%s">%s</option>'
        % (href, " selected" if href.startswith(active) else "", zh, en, zh)
        for href, zh, en in nav
    )
    nav_select_html = (
        '<select class="nav-select" id="nav-select" aria-label="导航">\n%s\n</select>'
        % nav_options)
    # 全局对比托盘：跨页持久（localStorage），最多选 4 款；未选时各页保持通用显示
    tray_html = """<div class="cmp-tray">
      <button id="cmp-tray-btn" type="button" class="tray-btn" aria-expanded="false" aria-haspopup="true"><span data-zh="对比" data-en="Compare">对比</span> <b class="tray-count"><i id="cmp-count">0</i>/4</b></button>
      <div id="cmp-panel" class="tray-panel" hidden>
        <div class="tray-sec"><span data-zh="已选" data-en="Selected">已选</span></div>
        <div id="cmp-selected" class="tray-selected"></div>
        <div id="cmp-sel-actions" class="tray-sel-actions" hidden><span class="tray-sel-left"><button id="cmp-clear" type="button" class="tray-clear"><span data-zh="清空选择" data-en="Clear selection">清空选择</span></button></span><a id="cmp-checkout" class="tray-checkout" href="compare.html"><span id="cmp-checkout-label">去对比 →</span></a></div>
        <div class="tray-sec"><span data-zh="全部产品（最多选 4 款）" data-en="All products (up to 4)">全部产品（最多选 4 款）</span></div>
        <div id="cmp-list" class="tray-list"></div>
      </div>
    </div>"""
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title data-title-zh="%s" data-title-en="%s">%s</title>
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg"/>
<link rel="stylesheet" href="assets/style.css"/>
</head>
<body>
<header class="topbar">
  <div class="topbar-inner">
    <a class="brand" href="index.html"><span class="brand-mark">&#9672;</span> DB <span data-zh="选型参考" data-en="Compare">选型参考</span></a>
    <nav class="mainnav">
%s
    </nav>
    %s
    %s
    <button id="lang-toggle" class="lang-btn" type="button" aria-label="switch language">EN</button>
  </div>
</header>
<main class="page">
%s
</main>
<footer class="footer">
  <p><span data-zh="信息截至 2026-09-29。本站为纯静态页面，仅供数据库选型参考，不构成采购建议；不做综合评分、不做排名。" data-en="Information current as of 2026-09-29. This is a fully static site for database evaluation reference only, not procurement advice. No aggregate scores, no rankings.">信息截至 2026-09-29。本站为纯静态页面，仅供数据库选型参考，不构成采购建议；不做综合评分、不做排名。</span> <a href="https://github.com/raywill/db-compare-site/issues/new" target="_blank" rel="noopener"><span data-zh="报告错误" data-en="Report an issue">报告错误</span></a></p>
</footer>
<script>%s</script>
%s
<script src="assets/app.js"></script>
</body>
</html>
""" % (html.escape(title_zh), html.escape(title_en), html.escape(title_zh), nav_html, nav_select_html, tray_html, body_html, _CATALOG_SCRIPT, tail_scripts)


def lang_block(zh_html, en_html):
    return '<div class="lang-block lang-zh">\n%s\n</div>\n<div class="lang-block lang-en" hidden>\n%s\n</div>' % (
        zh_html, en_html)


def section_html(title_zh, title_en, zh_body, en_body):
    return """<section class="doc-section">
<h2><span data-zh="%s" data-en="%s">%s</span></h2>
%s
</section>""" % (title_zh, title_en, title_zh, lang_block(zh_body, en_body))


def ev_legend_html():
    items = [
        ("ev-official", "官方文档", "official docs"),
        ("ev-vendor", "厂商口径", "vendor claim"),
        ("ev-tested", "社区实测", "community-tested"),
        ("ev-consensus", "社区共识", "community consensus"),
        ("ev-tbd", "待验证", "to-be-verified"),
    ]
    chips = " ".join(
        '<span class="ev %s" data-zh="%s" data-en="%s">%s</span>' % (c, z, e, z)
        for c, z, e in items)
    return ('<div class="legend"><span class="legend-label" data-zh="证据等级：" '
            'data-en="Evidence levels: ">证据等级：</span>%s</div>') % chips


# ---------------------------------------------------------------------------
# 客户经验（招牌能力研究 site-copy 解析）
# ---------------------------------------------------------------------------

SITECOPY = SITE.parent.parent.parent / "research_notes" / "signature-capabilities-20261001" / "site-copy"

FAV_TAGS = {"内核": "Kernel", "生态": "Ecosystem", "政策": "Policy", "避坑": "Pitfall"}
FAV_TAG_CLASS = {"内核": "kernel", "生态": "eco", "政策": "policy", "避坑": "pitfall"}
FAV_FIELDS_ZH = ["一句话", "窄场景", "机制", "生产验证", "竞品差距", "证据等级", "最后核验"]
FAV_FIELDS_EN = ["In one line", "Narrow scenario", "Mechanism", "Production evidence",
                 "Gap vs rivals", "Evidence grade", "Last verified"]

# 证据薄弱、需挂诚实声明条的产品
WEAK_EVIDENCE_SLUGS = {"tdsql", "oracle", "dynamodb", "doris", "starrocks", "weaviate",
                       "sqlserver", "polardb"}

_URL_RE = re.compile(r"(https?://[^\s()）\"<>；，。（【】「」『』,;！]+)")


def linkify_html(text):
    parts = _URL_RE.split(html.escape(text))
    out = []
    for i, p in enumerate(parts):
        if i % 2 == 1:
            out.append('<a href="%s" target="_blank" rel="noopener">%s</a>' % (p, p))
        else:
            out.append(p)
    return "".join(out)


def parse_fav_file(path):
    """解析客户经验卡片文件，返回 [{"tag","name","fields"}]；文件缺失返回 []。"""
    cards = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return cards
    cur = None
    for ln in lines:
        s = ln.strip()
        m = re.match(r"^###\s*\[([^\]]+)\]\s*(.+)$", s)
        if m:
            if cur:
                cards.append(cur)
            cur = {"tag": m.group(1).strip(), "name": m.group(2).strip(), "fields": {}}
            continue
        m2 = re.match(r"^-\s*\*\*(.+?)\*\*\s*[:：]\s*(.*)$", s)
        if m2 and cur is not None:
            cur["fields"][m2.group(1).strip()] = m2.group(2).strip()
    if cur:
        cards.append(cur)
    return cards


def get_fav_cards(slug):
    return (parse_fav_file(SITECOPY / (slug + ".md")),
            parse_fav_file(SITECOPY / (slug + ".en.md")))


def fav_card_html(slug, idx, zc, ec):
    base = zc or ec
    tag_zh = base["tag"]
    tag_en = FAV_TAGS.get(tag_zh, tag_zh)
    tag_cls = FAV_TAG_CLASS.get(tag_zh, "kernel")
    name_zh = zc["name"] if zc else ""
    name_en = ec["name"] if ec else name_zh
    zf = zc["fields"] if zc else {}
    ef = ec["fields"] if ec else {}
    rows = []
    for fzh, fen in zip(FAV_FIELDS_ZH, FAV_FIELDS_EN):
        zv = linkify_html(zf.get(fzh, "")) or "—"
        ev = linkify_html(ef.get(fen, "")) or "—"
        rows.append(
            '<div class="fav-field"><dt><span data-zh="%s" data-en="%s">%s</span></dt>'
            '<dd><div class="lang-block lang-zh">%s</div>'
            '<div class="lang-block lang-en" hidden>%s</div></dd></div>'
            % (fzh, fen, fzh, zv, ev))
    return (
        '<article class="fav-card fav-tag-%s" id="fav-%s-%d">\n'
        '<h3><span class="fav-tag"><span data-zh="%s" data-en="%s">%s</span></span> '
        '<span data-zh="%s" data-en="%s">%s</span></h3>\n'
        '<dl class="fav-fields">\n%s\n</dl>\n</article>'
        % (tag_cls, slug, idx, tag_zh, tag_en, tag_zh,
           html.escape(name_zh, quote=True), html.escape(name_en, quote=True),
           html.escape(name_zh), "\n".join(rows)))


def fav_section_html(prod):
    slug = prod["slug"]
    zh_cards, en_cards = get_fav_cards(slug)
    if not zh_cards and not en_cards:
        return ""
    n = max(len(zh_cards), len(en_cards))
    cards = []
    for i in range(n):
        zc = zh_cards[i] if i < len(zh_cards) else None
        ec = en_cards[i] if i < len(en_cards) else None
        cards.append(fav_card_html(slug, i + 1, zc, ec))
    t_zh, t_en = SECTION_TITLES["fav"]
    inner = "\n".join(cards)
    if slug in WEAK_EVIDENCE_SLUGS:
        inner = ('<div class="disclaimer-bar"><span data-zh="本区内容主要基于厂商口径与媒体转述，'
                 '独立社区验证不足，引用时请打折。" data-en="This section relies mainly on vendor '
                 'claims and media coverage; independent community validation is limited. '
                 'Discount accordingly.">本区内容主要基于厂商口径与媒体转述，'
                 '独立社区验证不足，引用时请打折。</span></div>\n') + inner
    return ('<section class="doc-section"><h2><span data-zh="%s" data-en="%s">%s</span></h2>\n'
            '<div class="fav-list">\n%s\n</div>\n</section>' % (t_zh, t_en, t_zh, inner))


def _fav_norm(s):
    s = s.lower()
    return re.sub(r'[：:———\-–""\'\'「」『』（）()、，,。！？!?.·\s"“”‘’/]', '', s)


def _fav_tokens(s):
    """中英混合分词: 标点转空格后, 连续字母数字为一词, 每个 CJK 字符为一词。"""
    s = s.lower()
    s = re.sub(r'[：:———\-–""\'\'「」『』（）()、，,。！？!?.·"“”‘’/]', ' ', s)
    toks = set()
    for m in re.finditer(r'[a-z0-9]+|[\u4e00-\u9fff]', s):
        toks.add(m.group(0))
    return toks


def fav_lookup(fav_index, slug, name):
    """查能力卡片序号: 精确 -> 归一化精确 -> 子串 -> token 交叠(>=0.45)。"""
    if (slug, name) in fav_index:
        return fav_index[(slug, name)]
    nq = _fav_norm(name)
    # 归一化精确 + 子串
    cands = []
    for (s, nm), num in fav_index.items():
        if s != slug:
            continue
        nn = _fav_norm(nm)
        if nq == nn:
            return num
        if nq and (nq in nn or nn in nq):
            cands.append((1.0, num))
        # 前缀匹配: 查询前 8 个字符是卡片标题的子串
        if len(nq) >= 8 and nq[:8] in nn:
            cands.append((0.95, num))
    if cands:
        return cands[0][1]
    # token 交叠
    qt = _fav_tokens(name)
    best, best_score = None, 0.0
    for (s, nm), num in fav_index.items():
        if s != slug:
            continue
        ct = _fav_tokens(nm)
        if not qt or not ct:
            continue
        inter = len(qt & ct)
        score = inter / max(len(qt), len(ct))
        # 短查询放宽: 交叠覆盖查询 token 的 70% 也算
        recall = inter / len(qt)
        score = max(score, recall * 0.9 if recall >= 0.7 else 0)
        if score > best_score:
            best, best_score = num, score
    if best_score >= 0.45:
        return best
    return None


def build_fav_index(slugs):
    """(slug, 能力名) -> 卡片序号，供案例页交叉链接用；中英名都建索引。
    同时返回 (slug, 序号) -> (中文名, 英文名)，供链接文字双语渲染。"""
    idx = {}
    titles = {}
    for slug in slugs:
        zh_cards, en_cards = get_fav_cards(slug)
        for i, c in enumerate(zh_cards, 1):
            idx[(slug, c["name"].strip())] = i
        for i, c in enumerate(en_cards, 1):
            idx[(slug, c["name"].strip())] = i
        n = max(len(zh_cards), len(en_cards))
        for i in range(1, n + 1):
            zname = zh_cards[i - 1]["name"].strip() if i - 1 < len(zh_cards) else ""
            ename = en_cards[i - 1]["name"].strip() if i - 1 < len(en_cards) else zname
            titles[(slug, i)] = (zname or ename, ename or zname)
    return idx, titles


# ---------------------------------------------------------------------------
# 场景案例库（cases 解析 + 页面）
# ---------------------------------------------------------------------------

CASE_BODY_FIELDS_ZH = ["场景", "决策", "结果", "机制根因", "教训"]
CASE_BODY_FIELDS_EN = ["Scenario", "Decision", "Outcome", "Root cause", "Lesson"]
CASE_TYPE_CLASS = {"反例": "anti", "正例": "pro"}

# 场景家族：7 个一级筛选维度。每个家族一组关键词，按子串匹配案例的中文标签
# （去空格小写后匹配）。一个案例可归属多个家族。
SCENARIO_FAMILIES = [
    ("migrate", "迁移上云", "Migration",
     ["去o", "迁移", "上云", "商业数据库", "分库分表替代", "平滑迁移",
      "替代", "替换", "去ioe", "国产化", "本地迁云"]),
    ("scale", "扩展分片", "Scaling & Sharding",
     ["分片", "扩展", "热点", "id设计", "分片键", "分区", "分库分表",
      "超大规模", "多集群", "pb级", "数据倾斜", "全球部署", "全球复制"]),
    ("cost", "成本优化", "Cost Optimization",
     ["成本", "降本", "压缩", "整合", "布隆", "账单", "收敛"]),
    ("ha", "高可用容灾", "HA & Disaster Recovery",
     ["高可用", "多地域", "全球化", "零停机", "容灾", "故障隔离", "在线扩容",
      "两地三中心", "跨云", "生产事故", "凭证"]),
    ("perf", "性能调优", "Performance Tuning",
     ["延迟", "p99", "吞吐", "写入放大", "内存墙", "gc", "查询", "缓存",
      "并发", "摄入", "长尾", "连接", "物化", "写密集", "实时", "加速",
      "性能天花板"]),
    ("ops", "运维工程", "Operations",
     ["运维", "工具链", "生态", "变更", "模式", "索引", "自研存储",
      "开源许可", "sspl", "bsl", "许可证", "社区分叉", "供应商锁定",
      "选型", "故障注入", "零代码", "厂商"]),
    ("arch", "架构选型", "Architecture Choice",
     ["自研", "构建", "模型", "htap", "一致", "事务", "审计", "租户",
      "云原生", "存算", "olap", "实时分析", "时序", "cdc", "去中心化",
      "检索", "rag", "向量", "多模态", "湖仓", "微服务", "知识库",
      "遥测", "数据栈", "共享"]),
]


def case_families(case):
    """按 SCENARIO_FAMILIES 关键词把案例归入场景家族，返回 [fid, ...]。"""
    tags = _split_list(case["zh"]["fields"].get("标签", ""))
    fams = []
    for fid, _zh, _en, kws in SCENARIO_FAMILIES:
        for t in tags:
            tn = t.replace(" ", "").lower()
            if any(kw in tn for kw in kws):
                fams.append(fid)
                break
    return fams


def _case_slug_of(path):
    name = path.name
    if name.endswith(".en.md"):
        return name[:-6]
    if name.endswith(".md"):
        return name[:-3]
    return path.stem


def parse_case_file(path):
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    title, fields = "", {}
    for ln in lines:
        s = ln.strip()
        if s.startswith("# ") and not title:
            title = s[2:].strip()
            continue
        m = re.match(r"^-\s*\*\*(.+?)\*\*\s*[:：]\s*(.*)$", s)
        if m:
            fields[m.group(1).strip()] = m.group(2).strip()
    if not title:
        return None
    return {"title": title, "fields": fields}


def load_cases():
    cases = []
    cdir = SITECOPY / "cases"
    if not cdir.is_dir():
        return cases
    for zhp in sorted(cdir.glob("*.md")):
        if zhp.name.endswith(".en.md"):
            continue
        slug = _case_slug_of(zhp)
        zc = parse_case_file(zhp)
        if not zc:
            continue
        enp = cdir / (slug + ".en.md")
        ec = parse_case_file(enp) if enp.exists() else None
        cases.append({"slug": slug, "zh": zc, "en": ec})
    return cases


def _split_list(s):
    return [x.strip() for x in re.split(r"[,，]", s or "") if x.strip()]


def _split_caps(s):
    """切分"相关能力"：条目形如 slug:卡片标题，标题内可能含逗号；
    只在逗号/分号后紧跟 slug+冒号时才切分。"""
    parts = re.split(r"[,，;；]\s*(?=[a-z][a-z0-9\-]*\s*[:：])", s or "")
    return [x.strip() for x in parts if x.strip()]


def case_card_html(case, prod_by_slug, fav_index, fav_titles):
    slug = case["slug"]
    zh, en = case["zh"], case["en"]
    zf, ef = zh["fields"], (en["fields"] if en else {})
    ctype_zh = zf.get("类型", "反例")
    ctype_cls = CASE_TYPE_CLASS.get(ctype_zh, "anti")
    ctype_zh = "失败教训" if ctype_cls == "anti" else "成功经验"
    ctype_en = "Failure lesson" if ctype_cls == "anti" else "Success story"
    tags_zh = _split_list(zf.get("标签", ""))
    tags_en = _split_list(ef.get("Tags", ""))
    ntags = max(len(tags_zh), len(tags_en))
    tag_chips = []
    for i in range(ntags):
        tz = tags_zh[i] if i < len(tags_zh) else ""
        te = tags_en[i] if i < len(tags_en) else tz
        tag_chips.append('<span class="case-tag" data-zh="%s" data-en="%s">%s</span>'
                         % (html.escape(tz, quote=True), html.escape(te, quote=True),
                            html.escape(tz)))
    rows = []
    for fzh, fen in zip(CASE_BODY_FIELDS_ZH, CASE_BODY_FIELDS_EN):
        zv = linkify_html(zf.get(fzh, "")) or "—"
        ev = linkify_html(ef.get(fen, "")) or "—"
        rows.append(
            '<div class="case-field"><dt><span data-zh="%s" data-en="%s">%s</span></dt>'
            '<dd><div class="lang-block lang-zh">%s</div>'
            '<div class="lang-block lang-en" hidden>%s</div></dd></div>'
            % (fzh, fen, fzh, zv, ev))
    # 相关产品 / 相关能力链接
    rel_ps = _split_list(zf.get("相关产品", ""))
    p_links = []
    for ps in rel_ps:
        if ps == "无":
            p_links.append('<span data-zh="无" data-en="None">无</span>')
            continue
        p = prod_by_slug.get(ps)
        nm_zh = p["name"] if p else ps
        nm_en = p["name_en"] if p else ps
        p_links.append('<a href="profile-%s.html"><span data-zh="%s" data-en="%s">%s</span></a>'
                       % (ps, html.escape(nm_zh, quote=True), html.escape(nm_en, quote=True),
                          html.escape(nm_zh)))
    rel_cs = _split_caps(zf.get("相关能力", ""))
    c_links = []
    for rc in rel_cs:
        if rc == "无":
            continue
        if ":" in rc or "：" in rc:
            ps, nm = re.split(r"[:：]", rc, maxsplit=1)
            ps, nm = ps.strip(), nm.strip()
        else:
            ps, nm = "", rc.strip()
        num = fav_lookup(fav_index, ps, nm)
        if not ps or ps not in prod_by_slug:
            # 引用无法解析：降级为纯文本，不渲染死链
            c_links.append(html.escape(nm))
            continue
        href = "profile-%s.html#fav-%s-%d" % (ps, ps, num) if num else \
            "profile-%s.html" % ps
        if ps and num and (ps, num) in fav_titles:
            tzh, ten = fav_titles[(ps, num)]
            c_links.append('<a href="%s"><span data-zh="%s" data-en="%s">%s</span></a>'
                           % (href, html.escape(tzh, quote=True),
                              html.escape(ten, quote=True), html.escape(tzh)))
        else:
            c_links.append('<a href="%s">%s</a>' % (href, html.escape(nm)))
    title_en = en["title"] if en else zh["title"]
    # 来源：编号引用列表（每条依据列清楚）
    refs_zh = [x.strip() for x in (zf.get("来源", "") or "").split("；") if x.strip()]
    refs_en = [x.strip() for x in (ef.get("Sources", "") or "").split(";") if x.strip()]
    nrefs = max(len(refs_zh), len(refs_en))
    refs_html = ""
    if nrefs:
        items = []
        for i in range(nrefs):
            rz = linkify_html(refs_zh[i]) if i < len(refs_zh) else "—"
            re_ = linkify_html(refs_en[i]) if i < len(refs_en) else rz
            items.append('<li><div class="lang-block lang-zh">%s</div>'
                         '<div class="lang-block lang-en" hidden>%s</div></li>' % (rz, re_))
        refs_html = (
            '<div class="case-refs"><div class="case-refs-title">'
            '<span data-zh="来源" data-en="Sources">来源</span></div>'
            '<ol>\n%s\n</ol></div>' % "\n".join(items))
    # 多维筛选数据属性：相关产品 slug、搜索文本
    data_dbs = [ps for ps in rel_ps if ps != "无" and ps in prod_by_slug]
    data_fams = case_families(case)
    verify_zh = zf.get("最后核验", "")
    verify_en = ef.get("Last verified", verify_zh)
    return (
        '<article class="case-card" id="case-%s" data-ctype="%s" data-fam="%s" data-dbs="%s">\n'
        '<h3><span data-zh="%s" data-en="%s">%s</span> '
        '<span class="case-type case-%s"><span data-zh="%s" data-en="%s">%s</span></span></h3>\n'
        '<div class="case-tags">%s</div>\n'
        '<dl class="case-fields">\n%s\n</dl>\n'
        '%s\n'
        '<p class="case-meta"><span data-zh="相关产品：" data-en="Related products: ">相关产品：</span>%s'
        ' <span data-zh="相关能力：" data-en="Related capabilities: ">相关能力：</span>%s'
        ' <span class="case-verify" data-zh="最后核验：%s" data-en="Last verified: %s">最后核验：%s</span></p>\n'
        '</article>'
        % (slug, ctype_cls, html.escape(" ".join(data_fams), quote=True),
           html.escape(" ".join(data_dbs), quote=True),
           html.escape(zh["title"], quote=True), html.escape(title_en, quote=True),
           html.escape(zh["title"]), ctype_cls, ctype_zh, ctype_en, ctype_zh,
           "\n".join(tag_chips), "\n".join(rows),
           refs_html, "、".join(p_links) or "—", "、".join(c_links) or "—",
           html.escape(verify_zh, quote=True), html.escape(verify_en, quote=True),
           html.escape(verify_zh)))


CASE_FILTER_JS = """
function caseFilterInit(){
  var fType='',fDb='',fFam='';
  function $(s){return document.querySelector(s);}
  function $all(s){return Array.prototype.slice.call(document.querySelectorAll(s));}
  function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
  function chipLabel(btn){
    if(!btn){return '';}
    var sp=btn.querySelector('span[data-zh]');
    return sp?sp.textContent:btn.textContent.trim();
  }
  function isEn(){return document.documentElement.getAttribute('lang')==='en';}
  function apply(){
    var n=0;
    $all('.case-card').forEach(function(card){
      var okT=(!fType)||(card.getAttribute('data-ctype')===fType);
      var dbs=(card.getAttribute('data-dbs')||'').split(' ').filter(Boolean);
      var okD=(!fDb)||(dbs.indexOf(fDb)>=0);
      var fams=(card.getAttribute('data-fam')||'').split(' ').filter(Boolean);
      var okF=(!fFam)||(fams.indexOf(fFam)>=0);
      var show=okT&&okD&&okF;
      card.hidden=!show; if(show){n++;}
    });
    var cc=$('#case-count'); if(cc){cc.textContent=n;}
    var empty=$('#case-empty'); if(empty){empty.hidden=(n!==0);}
    renderActive();
  }
  function renderActive(){
    var box=$('#case-active'); if(!box){return;}
    var pills=[];
    if(fType){pills.push({k:'type',label:chipLabel(document.querySelector('[data-ctype-btn="'+fType+'"]'))});}
    if(fDb){pills.push({k:'db',label:chipLabel(document.querySelector('[data-cdb-btn="'+fDb+'"]'))});}
    if(fFam){pills.push({k:'fam',label:chipLabel(document.querySelector('[data-cfam-btn="'+fFam+'"]'))});}
    if(!pills.length){box.hidden=true;box.innerHTML='';return;}
    box.hidden=false;
    var t=isEn()?'Selected: ':'\\u5df2\\u9009\\uff1a';
    box.innerHTML='<span class="cf-active-label">'+t+'</span>'+pills.map(function(p){
      return '<button type="button" class="cf-pill" data-cpill="'+p.k+'">'+esc(p.label)+'<b>\\u00d7</b></button>';
    }).join('')+'<button type="button" class="cf-clear" data-cclear>'+(isEn()?'Clear all':'\\u6e05\\u9664\\u5168\\u90e8')+'</button>';
    $all('[data-cpill]',box).forEach(function(b){
      b.addEventListener('click',function(){clearOne(b.getAttribute('data-cpill'));});
    });
    var cb=box.querySelector('[data-cclear]');
    if(cb){cb.addEventListener('click',clearAll);}
  }
  function clearOne(k){
    if(k==='type'){fType='';syncChips('[data-ctype-btn]','');}
    if(k==='db'){fDb='';syncChips('[data-cdb-btn]','');}
    if(k==='fam'){fFam='';syncChips('[data-cfam-btn]','');}
    apply();
  }
  function clearAll(){
    fType='';fDb='';fFam='';
    syncChips('[data-ctype-btn]','');syncChips('[data-cdb-btn]','');syncChips('[data-cfam-btn]','');
    apply();
  }
  function syncChips(sel,val){
    $all(sel).forEach(function(x){
      var on=(x.getAttribute(sel.slice(1,-1))===val&&val!=='');
      x.classList.toggle('on',on);
    });
  }
  function bindDim(attrSel,get,set){
    $all(attrSel).forEach(function(b){
      b.addEventListener('click',function(){
        var v=b.getAttribute(attrSel.slice(1,-1));
        if(get()===v){set('');}
        else{set(v);}
        syncChips(attrSel,get());
        apply();
      });
    });
  }
  bindDim('[data-ctype-btn]',function(){return fType;},function(v){fType=v;});
  bindDim('[data-cdb-btn]',function(){return fDb;},function(v){fDb=v;});
  bindDim('[data-cfam-btn]',function(){return fFam;},function(v){fFam=v;});
  apply();
}
document.addEventListener('DOMContentLoaded',caseFilterInit);
"""

def cases_page_html(cases, prod_by_slug, fav_index, fav_titles):
    # 场景家族计数（一个案例可归属多个家族）
    fam_counts = {fid: 0 for fid, _, _, _ in SCENARIO_FAMILIES}
    case_fams = {}
    for c in cases:
        fams = case_families(c)
        case_fams[c["slug"]] = fams
        for fid in fams:
            fam_counts[fid] += 1
    orphans = [c["slug"] for c in cases if not case_fams[c["slug"]]]
    if orphans:
        print("  [案例库] 未归入任何家族: %s" % ", ".join(orphans))
    # DB 维度：统计各产品案例数，按领域分组（案例库的 DB 索引）
    db_counts = {}
    for c in cases:
        for ps in _split_list(c["zh"]["fields"].get("相关产品", "")):
            if ps == "无" or ps not in prod_by_slug:
                continue
            db_counts[ps] = db_counts.get(ps, 0) + 1
    db_groups = []
    for d, d_zh, d_en in DOMAINS:
        slugs = [s for s, p in prod_by_slug.items()
                 if s in db_counts and p["domains"][0] == d]
        slugs.sort(key=lambda s: (-db_counts[s], s))
        if slugs:
            db_groups.append((d_zh, d_en, slugs))
    type_btns = (
        '<button type="button" class="chip" data-ctype-btn="pro">'
        '<span data-zh="成功经验" data-en="Success stories">成功经验</span></button>'
        '<button type="button" class="chip" data-ctype-btn="anti">'
        '<span data-zh="失败教训" data-en="Failure lessons">失败教训</span></button>')
    db_groups_html = "".join(
        '<div class="cf-dbgroup"><span class="cf-dbgroup-label">'
        '<span data-zh="%s" data-en="%s">%s</span></span>'
        '<div class="cf-chips">%s</div></div>'
        % (html.escape(d_zh, quote=True), html.escape(d_en, quote=True),
           html.escape(d_zh), "".join(
               '<button type="button" class="chip" data-cdb-btn="%s">'
               '<span data-zh="%s" data-en="%s">%s</span><i class="cf-n">%d</i></button>'
               % (s,
                  html.escape(prod_by_slug[s]["name"], quote=True),
                  html.escape(prod_by_slug[s]["name_en"], quote=True),
                  html.escape(prod_by_slug[s]["name"]),
                  db_counts[s])
               for s in slugs))
        for d_zh, d_en, slugs in db_groups)
    fam_btns = "".join(
        '<button type="button" class="chip" data-cfam-btn="%s">'
        '<span data-zh="%s" data-en="%s">%s</span><i class="cf-n">%d</i></button>'
        % (fid, html.escape(fzh, quote=True), html.escape(fen, quote=True),
           html.escape(fzh), fam_counts[fid])
        for fid, fzh, fen, _kws in SCENARIO_FAMILIES)
    cards = "\n".join(case_card_html(c, prod_by_slug, fav_index, fav_titles) for c in cases)
    body = (
        '<div class="hero hero-slim"><h1><span data-zh="场景案例库" data-en="Case Library">场景案例库</span></h1>'
        '<p class="hero-sub"><span data-zh="真实世界的选型故事：选了什么、结果如何、机制层面的根因是什么。我们从错误里学习。"\n'
        ' data-en="Real-world selection stories: what was chosen, how it turned out, and the mechanism-level root cause. We learn from mistakes.">'
        '真实世界的选型故事：选了什么、结果如何、机制层面的根因是什么。我们从错误里学习。</span></p></div>'
        '<p class="case-intro"><span data-zh="提醒：高频最优解是“不换库”——很多案例的教训不是换一款数据库，而是把当前架构用对。先看案例，再看产品档案里的“客户经验”。"\n'
        ' data-en="Reminder: the most frequent optimal answer is “do not migrate” — many cases teach using your current stack correctly, not switching databases. Read the cases first, then the “Customer experiences” section in each profile.">'
        '提醒：高频最优解是“不换库”——很多案例的教训不是换一款数据库，而是把当前架构用对。先看案例，再看产品档案里的“客户经验”。</span></p>'
        '<div class="case-filters">'
        '<div class="cf-row"><span class="cf-label"><span data-zh="类型" data-en="Type">类型</span></span>'
        '<div class="cf-chips">%s</div></div>'
        '<div class="cf-row"><span class="cf-label"><span data-zh="数据库" data-en="Database">数据库</span></span>'
        '<div class="cf-chips-col"><div class="cf-chips">%s</div></div></div>'
        '<div class="cf-row"><span class="cf-label"><span data-zh="场景" data-en="Scenario">场景</span></span>'
        '<div class="cf-chips">%s</div></div>'
        '<div class="cf-active" id="case-active" hidden></div>'
        '<p class="case-count"><span data-zh="找到 " data-en="">找到 </span>'
        '<b id="case-count">%d</b><span data-zh=" 个案例" data-en=" cases"> 个案例</span></p></div>'
        '<div class="case-empty" id="case-empty" hidden><span data-zh="没有匹配的案例，换个条件试试。"\n'
        ' data-en="No matching cases — try different filters.">没有匹配的案例，换个条件试试。</span></div>'
        '<div class="case-list">\n%s\n</div>' % (type_btns, db_groups_html, fam_btns, len(cases), cards))
    return page_shell("DB 选型参考 - 场景案例库", "DB Compare - Case Library", body,
                      active="cases", tail_scripts="<script>%s</script>" % CASE_FILTER_JS)


# ---------------------------------------------------------------------------
# 数据组装
# ---------------------------------------------------------------------------

def get_section(prof, kind):
    secs = prof["sections"].get(kind, [])
    return secs[0] if secs else (None, [])


def render_section_body(body_lines):
    return render_md("\n".join(body_lines).strip())


def build_product(slug):
    """组装单个产品的双语数据。返回 dict。"""
    zh = parse_profile(SRC / (slug + ".md"))
    en = parse_profile(SRC / (slug + ".en.md"))
    prod = {"slug": slug, "zh": zh, "en": en, "fallbacks": []}
    prod["name"] = zh["name"] or en["name"] or slug
    prod["name_en"] = NAME_EN.get(slug) or en["name"] or zh["name"] or slug
    prod["domains"] = DOMAIN_OF[slug]
    prod["domain"] = DOMAIN_OF[slug][0]

    for lang_key, prof in (("zh", zh), ("en", en)):
        # 一句话定位
        _, olines = get_section(prof, "oneliner")
        oneliner = first_paragraph(olines)
        if not oneliner:
            _, blines = get_section(prof, "basics")
            oneliner = fullname_from_basics(blines)
        if not oneliner:
            oneliner = prof["name"]
        prod["oneliner_" + lang_key] = oneliner
        # 分类标签
        _, tlines = get_section(prof, "tags")
        prod["tags_" + lang_key] = extract_tags(tlines)

        # 硬维度
        dtitle, dlines = get_section(prof, "dims")
        dims = [None] * len(DIMS)
        extras = []
        intro_html = ""
        fallback = False
        if dtitle is None:
            fallback = True
            prod["fallbacks"].append("%s:missing-dims-section" % lang_key)
        else:
            items, extras_raw, style, intro = split_dim_items(dlines)
            intro_html = render_md("\n".join(intro).strip()) if any(s.strip() for s in intro) else ""
            matched = 0
            for it in items:
                if it.get("_note"):
                    continue
                d = match_dim(it["name"])
                if d is None:
                    prod["fallbacks"].append("%s:dim-unmatched:%s" % (lang_key, it["name"][:30]))
                    continue
                rest = it["rest"]
                body_md = (rest + "\n\n" if (style != "h3" and rest) else "") + "\n".join(it["body"]).strip()
                phrase, vclass = extract_verdict(it["name"], rest, it["body"], lang_key)
                dims[d] = {
                    "name": it["name"],
                    "phrase": phrase,
                    "vclass": vclass,
                    "body_md": body_md,
                    "body_html": render_md(body_md),
                    "snippet": plain_snippet(body_md, 170),
                }
                matched += 1
            extras = []
            for it in extras_raw:
                if it.get("_note"):
                    continue
                extras.append({"name": it["name"],
                               "html": render_md((it["rest"] + "\n\n" if it["rest"] else "") + "\n".join(it["body"]).strip())})
            if matched < len(DIMS):
                fallback = True
                prod["fallbacks"].append("%s:dims-matched-%d" % (lang_key, matched))
        prod["dims_" + lang_key] = None if fallback else dims
        prod["dims_extras_" + lang_key] = extras
        prod["dims_intro_" + lang_key] = intro_html
        prod["dims_section_html_" + lang_key] = render_section_body(dlines) if dtitle else ""
        prod["dims_fallback_" + lang_key] = fallback
    return prod


def plain_snippet(md_text, n=150):
    t = md_text
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"`([^`]+)`", r"\1", t)
    t = re.sub(r"^#{1,6}\s*", "", t, flags=re.M)
    t = re.sub(r"^>\s*", "", t, flags=re.M)
    t = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", t, flags=re.M)
    t = t.replace("|", " ")
    t = re.sub(r"\s+", " ", t).strip()
    return (t[:n] + "…") if len(t) > n else t


# ---------------------------------------------------------------------------
# 产品页
# ---------------------------------------------------------------------------

SECTION_TITLES = {
    "basics": ("基本信息", "Basics"),
    "dims": ("硬维度（47 项）", "Hard dimensions (47)"),
    "killer": ("招牌能力", "Signature strengths"),
    "fav": ("客户经验", "Customer experiences"),
    "deep": ("深水区", "Deep dives"),
    "loved": ("用户最买账的 5 点", "What users love most"),
    "complaints": ("吐槽清单", "Complaints"),
    "verdict": ("判决", "Verdict"),
    "sources": ("来源与待验证清单", "Sources & to-be-verified"),
}


def dims_block_html(prod):
    parts_zh, parts_en = [], []
    for lang_key, parts in (("zh", parts_zh), ("en", parts_en)):
        if prod["dims_fallback_" + lang_key]:
            parts.append('<div class="fallback-note"><p>%s</p>%s</div>' % (
                "本档案维度格式特殊，以下为整节原文（未做逐项拆分）：" if lang_key == "zh"
                else "This profile uses a non-standard dimension format; showing the full section as-is:",
                prod["dims_section_html_" + lang_key]))
            continue
        if prod["dims_intro_" + lang_key]:
            parts.append('<div class="dims-intro">%s</div>' % prod["dims_intro_" + lang_key])
        dims = prod["dims_" + lang_key]
        for idx in range(len(DIMS)):
            dim = DIMS[idx]
            d = dims[idx]
            if d is None:
                body = '<p class="dim-missing">%s</p>' % (
                    "本档案未单独列出此维度。" if lang_key == "zh"
                    else "This dimension is not separately covered in this profile.")
                chip = ""
            else:
                chip = ('<span class="verdict v-%s">%s</span>' % (d["vclass"], html.escape(d["phrase"]))
                        if d["phrase"] else "")
                body = d["body_html"]
            parts.append(
                '<div class="dim-item"><h3><span class="dim-num">%d</span> %s %s</h3>'
                '<div class="dim-body">%s</div></div>'
                % (idx + 1, html.escape(dim[lang_key]), chip, body))
        for ex in prod["dims_extras_" + lang_key]:
            parts.append('<div class="dim-item dim-extra"><h3>%s</h3><div class="dim-body">%s</div></div>'
                         % (html.escape(ex["name"]), ex["html"]))
    return lang_block("\n".join(parts_zh), "\n".join(parts_en))


def profile_page_html(prod):
    slug = prod["slug"]
    zh, en = prod["zh"], prod["en"]
    cats_html = " ".join(
        '<span class="cat cat-%s" data-zh="%s" data-en="%s">%s</span>'
        % (d, DOMAIN_NAMES[d][0], DOMAIN_NAMES[d][1], DOMAIN_NAMES[d][0])
        for d in prod["domains"])
    tags_zh = prod["tags_zh"] or []
    tags_en = prod["tags_en"] or []
    ntags = max(len(tags_zh), len(tags_en))
    tags_html = " ".join(
        '<span class="tag"><span data-zh="#%s" data-en="#%s">#%s</span></span>'
        % (html.escape(tags_zh[i] if i < len(tags_zh) else tags_en[i], quote=True),
           html.escape(tags_en[i] if i < len(tags_en) else tags_zh[i], quote=True),
           html.escape(tags_zh[i] if i < len(tags_zh) else tags_en[i]))
        for i in range(ntags))

    hero = """<div class="profile-hero">
  <a class="back" href="index.html"><span data-zh="← 返回首页" data-en="← Back to home">← 返回首页</span></a>
  <h1>%s</h1>
  <div class="meta-row">%s %s</div>
  <p class="oneliner">%s</p>
  <div class="ai-dive-row" data-product="%s">
    <span class="ai-dive-label" data-zh="用 AI 深挖这款：" data-en="Deep-dive with AI:">用 AI 深挖这款：</span>
    <button type="button" class="ai-btn" onclick="aiDeepDive('chatgpt', this)">ChatGPT <span aria-hidden="true">↗</span></button>
    <button type="button" class="ai-btn" onclick="aiDeepDive('grok', this)">Grok <span aria-hidden="true">↗</span></button>
    <button type="button" class="ai-btn" onclick="aiDeepDive('claude', this)">Claude <span aria-hidden="true">↗</span></button>
    <button type="button" class="ai-btn addcmp-btn" data-addcmp="%s"><span class="addcmp-label">＋ 对比</span></button>
  </div>
  %s
</div>""" % (
        html.escape(prod["name"]), cats_html, tags_html,
        lang_block("<p>%s</p>" % html.escape(prod["oneliner_zh"]),
                   "<p>%s</p>" % html.escape(prod["oneliner_en"])),
        html.escape(prod["name"], quote=True),
        slug, ev_legend_html())

    def sec(kind):
        if kind == "fav":
            return fav_section_html(prod)
        t_zh, t_en = SECTION_TITLES[kind]
        _, zlines = get_section(zh, kind)
        _, elines = get_section(en, kind)
        z_extra, e_extra = "", ""
        if kind == "killer":
            _, z2 = get_section(zh, "killer_extra")
            _, e2 = get_section(en, "killer_extra")
            if z2:
                z_extra = render_section_body(z2)
            if e2:
                e_extra = render_section_body(e2)
        if kind == "sources":
            zt, et = [], []
            for kk in ("tbd", "sources"):
                _, zl = get_section(zh, kk)
                _, el = get_section(en, kk)
                if zl:
                    zt.append(render_section_body(zl))
                if el:
                    et.append(render_section_body(el))
            if not zt and not et:
                return ""
            return section_html(t_zh, t_en, "\n".join(zt), "\n".join(et))
        if not zlines and not elines and not z_extra and not e_extra:
            return ""
        zb = render_section_body(zlines) + z_extra
        eb = render_section_body(elines) + e_extra
        return section_html(t_zh, t_en, zb, eb)

    body = [hero]
    # 基本信息
    _, zlines = get_section(zh, "basics")
    _, elines = get_section(en, "basics")
    if zlines or elines:
        body.append(section_html("基本信息", "Basics",
                                 render_section_body(zlines), render_section_body(elines)))
    # 硬维度
    t_zh, t_en = SECTION_TITLES["dims"]
    body.append('<section class="doc-section"><h2><span data-zh="%s" data-en="%s">%s</span></h2>\n%s\n</section>'
                % (t_zh, t_en, t_zh, dims_block_html(prod)))
    for kind in ("killer", "deep", "fav", "loved", "complaints", "verdict"):
        s = sec(kind)
        if s:
            body.append(s)
    # 档案自带的额外章节（产品矩阵 / 附录等），不丢内容
    for kind in ("extra",):
        zl = zh["sections"].get(kind, [])
        el = en["sections"].get(kind, [])
        blocks_z = [render_section_body(b) for _, b in zl]
        blocks_e = [render_section_body(b) for _, b in el]
        if blocks_z or blocks_e:
            body.append(section_html("附录", "Appendix", "\n".join(blocks_z), "\n".join(blocks_e)))
    s = sec("sources")
    if s:
        body.append(s)
    return page_shell("%s - DB 选型参考" % prod["name"], "DB Compare - %s" % prod["name_en"], "\n".join(body), active="index")

def cases_cta_html(n_cases):
    if not n_cases:
        return ""
    return ('<div class="cases-cta"><a href="cases.html">'
            '<span data-zh="场景案例库：%d 个真实选型故事——从别人的错误里学习" '
            'data-en="Case library: %d real-world selection stories — learn from others\' mistakes">'
            '场景案例库：%d 个真实选型故事——从别人的错误里学习</span>'
            ' <span aria-hidden="true">→</span></a></div>' % (n_cases, n_cases, n_cases))


# ---------------------------------------------------------------------------
# 首页
# ---------------------------------------------------------------------------

def index_page_html(products, n_cases=0):
    n = len(products)
    cards_by_domain = {}
    for p in products:
        for d in p["domains"]:
            cat_zh, cat_en = DOMAIN_NAMES[d]
            cards_by_domain.setdefault(d, []).append(
                """<article class="card" data-domain="%s">
  <div class="card-top"><span class="cat cat-%s" data-zh="%s" data-en="%s">%s</span><button type="button" class="addcmp-btn" data-addcmp="%s"><span class="addcmp-label">＋ 对比</span></button></div>
  <h3><a href="profile-%s.html"><span data-zh="%s" data-en="%s">%s</span></a></h3>
  <div class="lang-block lang-zh"><p class="card-one">%s</p></div>
  <div class="lang-block lang-en" hidden><p class="card-one">%s</p></div>
  <a class="card-link" href="profile-%s.html"><span data-zh="查看档案 →" data-en="View profile →">查看档案 →</span></a>
</article>""" % (d, d, cat_zh, cat_en, cat_zh, p["slug"],
                     p["slug"], html.escape(p["name"]), html.escape(p["name_en"]), html.escape(p["name"]),
                     html.escape(p["oneliner_zh"]), html.escape(p["oneliner_en"]),
                     p["slug"]))
    fbtns = ['<button type="button" class="filter-btn active" data-filter="all">'
             '<span data-zh="全部" data-en="All">全部</span> <b>%d</b></button>' % n]
    for d, zh, en in DOMAINS:
        c = len(cards_by_domain.get(d, []))
        fbtns.append('<button type="button" class="filter-btn" data-filter="%s">'
                     '<span data-zh="%s" data-en="%s">%s</span> <b>%d</b></button>' % (d, zh, en, zh, c))
    filter_html = ('<div class="filter-bar" role="group" aria-label="filter">\n  %s\n</div>'
                   % "\n  ".join(fbtns))
    secs = []
    for d, zh, en in DOMAINS:
        cards = cards_by_domain.get(d, [])
        if not cards:
            continue
        secs.append('<section class="domain-sec" data-domain="%s">\n'
                    '<h2 class="domain-h"><span data-zh="%s" data-en="%s">%s</span>'
                    ' <b class="domain-n">%d</b></h2>\n'
                    '<div class="card-grid">\n%s\n</div>\n</section>'
                    % (d, zh, en, zh, len(cards), "\n".join(cards)))
    body = """
<div class="hero">
  <h1><span data-zh="数据库选型参考" data-en="Database Selection Reference">数据库选型参考</span></h1>
  <p class="hero-sub"><span data-zh="%d 款数据库 · 47 个硬维度 · 证据分级 · 不做综合评分、不做排名" data-en="%d databases · 47 hard dimensions · evidence-graded · no aggregate scores, no rankings">%d 款数据库 · 47 个硬维度 · 证据分级 · 不做综合评分、不做排名</span></p>
  <p class="hero-note"><span data-zh="信息截至 2026-09-29。每个档案包含招牌能力、深水区、客户经验、用户买账点、吐槽清单与判决，并标注每条结论的证据等级。" data-en="Information current as of 2026-09-29. Each profile covers signature strengths, deep dives, customer experiences, praised points, complaints and a verdict, with evidence levels on every claim.">信息截至 2026-09-29。每个档案包含招牌能力、深水区、客户经验、用户买账点、吐槽清单与判决，并标注每条结论的证据等级。</span></p>
</div>
%s
%s
%s
""" % (n, n, n, cases_cta_html(n_cases), filter_html, "\n".join(secs))
    return page_shell("DB 选型参考 - 首页", "DB Compare - Home", body, active="index")


# ---------------------------------------------------------------------------
# 维度对比页：22 维度 × N 产品
# ---------------------------------------------------------------------------

def compare_cell_html(prod, idx, lang_key):
    dims = prod["dims_" + lang_key]
    if prod["dims_fallback_" + lang_key] or dims is None:
        inner = ('<span class="verdict v-neutral">%s</span>'
                 '<p class="snippet">%s</p>'
                 '<div class="full" hidden>%s</div>'
                 % ("整节原文" if lang_key == "zh" else "full section",
                    "该档案维度格式特殊，点击展开查看整节原文。" if lang_key == "zh"
                    else "Non-standard dimension format in this profile; expand to see the full section.",
                    prod["dims_section_html_" + lang_key]))
    else:
        d = dims[idx]
        if d is None:
            inner = ('<p class="snippet">%s</p>'
                     % ("本档案未单独列出此维度。" if lang_key == "zh"
                        else "Not separately covered in this profile."))
        else:
            chip = ('<span class="verdict v-%s">%s</span>' % (d["vclass"], html.escape(d["phrase"]))
                    if d["phrase"] else "")
            inner = ('%s<p class="snippet">%s</p>'
                     '<div class="full" hidden>%s</div>'
                     % (chip, html.escape(d["snippet"]), d["body_html"]))
    toggle_zh = "展开" if lang_key == "zh" else "Expand"
    return ('<div class="lang-block lang-%s"%s><div class="cell-main">%s</div>'
            '<button type="button" class="cell-toggle" data-zh="展开" data-en="Expand">%s</button></div>'
            % (lang_key, " hidden" if lang_key == "en" else "", inner, toggle_zh))


def compare_page_html(products):
    thead_cells = []
    for idx, dim in enumerate(DIMS):
        thead_cells.append("<th><span class=\"dim-h-zh\">%s</span><span class=\"dim-h-en\">%s</span></th>"
                           % (html.escape(dim["zh"]), html.escape(dim["en"])))
    rows = []
    # 单元格正文移入外部 JS 分片（单文件推送有大小上限）；apply_badges 对片段单独做一次，
    # 与整页处理等价（徽标输出不再命中任何徽标正则，保证幂等）。
    cell_data = {}
    for p in products:
        cat_zh, cat_en = DOMAIN_NAMES[p["domain"]]
        tds = []
        for idx in range(len(DIMS)):
            key = "%s__%d" % (p["slug"], idx)
            tds.append('<td class="cmp-cell" data-cell="%s"></td>' % key)
            cell_data[key] = apply_badges(
                compare_cell_html(p, idx, "zh") + compare_cell_html(p, idx, "en"))
        rows.append(
            '<tr data-domains="%s" data-slug="%s"><th class="row-head"><a href="profile-%s.html"><span data-zh="%s" data-en="%s">%s</span></a>'
            '<span class="cat cat-%s" data-zh="%s" data-en="%s">%s</span></th>%s</tr>'
            % (" ".join(p["domains"]), p["slug"], p["slug"], html.escape(p["name"]), html.escape(p["name_en"]), html.escape(p["name"]), p["domain"], cat_zh, cat_en, cat_zh, "".join(tds)))
    cfbtns = ['<button type="button" class="cmp-filter-btn active" data-filter="all">'
                '<span data-zh="全部产品" data-en="All products">全部产品</span></button>']
    for d, zh, en in DOMAINS:
        cfbtns.append('<button type="button" class="cmp-filter-btn" data-filter="%s">'
                      '<span data-zh="%s" data-en="%s">%s</span></button>' % (d, zh, en, zh))
    cmp_filter_html = ('<div class="cmp-toolbar">\n<div class="cmp-filter-bar" role="group" aria-label="domain filter">\n  %s\n</div>\n</div>'
                       % "\n  ".join(cfbtns))
    body = """
<div class="hero hero-slim">
  <h1><span data-zh="47 维度 × %d 产品 对比矩阵" data-en="47 Dimensions × %d Products Matrix">47 维度 × %d 产品 对比矩阵</span></h1>
  <div class="disclaimer">
    <strong><span data-zh="声明：本对比不做综合总分、不做排名。" data-en="Disclaimer: no aggregate scores, no rankings in this comparison.">声明：本对比不做综合总分、不做排名。</span></strong>
    <span data-zh="各维度独立并列，选型权重由你自己定（见方法论）。点击单元格可展开查看该维度的完整段落原文。" data-en="Dimensions are shown side by side independently; you set your own weights (see Methodology). Click a cell to expand the full original paragraph.">各维度独立并列，选型权重由你自己定（见方法论）。点击单元格可展开查看该维度的完整段落原文。</span>
  </div>
  %s
  %s
  <div id="cmp-sel-notice" class="sel-notice" hidden>
    <span data-zh="当前仅显示已选产品：" data-en="Showing selected products only: ">当前仅显示已选产品：</span><b id="cmp-sel-names"></b>
    <button id="cmp-sel-clear" type="button"><span data-zh="清除选择" data-en="Clear selection">清除选择</span></button>
  </div>
  <div class="legend"><span class="legend-label" data-zh="结论色标：" data-en="Verdict colors: ">结论色标：</span>
    <span class="verdict v-yes" data-zh="有 / 支持" data-en="Supported">有 / 支持</span>
    <span class="verdict v-partial" data-zh="部分支持" data-en="Partial">部分支持</span>
    <span class="verdict v-no" data-zh="无 / 不支持" data-en="Not supported">无 / 不支持</span>
    <span class="verdict v-neutral" data-zh="视情况" data-en="Depends">视情况</span>
    <span class="verdict v-tbd" data-zh="待验证" data-en="To verify">待验证</span>
  </div>
</div>
<div class="cmp-result-bar">
  <span id="cmp-visible-count" class="cmp-visible-count"></span>
  <span class="cmp-result-actions">
  <button id="cmp-share" type="button" class="copy-btn"><span data-zh="🔗 复制分享链接" data-en="🔗 Copy share link">🔗 复制分享链接</span></button>
  <button id="cmp-copy" type="button" class="copy-btn"><span data-zh="⧉ 复制对比结果" data-en="⧉ Copy comparison">⧉ 复制对比结果</span></button>
  </span>
</div>
<div class="table-wrap cmp-wrap">
<table class="cmp-table">
<thead><tr><th class="row-head"><span data-zh="产品" data-en="Product">产品</span></th>%s</tr></thead>
<tbody>
%s
</tbody>
</table>
</div>
""" % (len(products), len(products), len(products),
           ev_legend_html(), cmp_filter_html, "".join(thead_cells), "\n".join(rows))
    return body, cell_data


def _write_cmp_shards(outputs, cmp_cells):
    """对比矩阵单元格数据分片：单文件推送有大小上限，拆成多个 ~100KB 的 JS 文件。

    页面渲染出的 DOM 与原来内联时完全一致（注入发生在 app.js 的
    DOMContentLoaded 初始化之前），筛选 / 展开 / 中英文切换行为不变。
    """
    shards, cur, cur_size = [], {}, 0
    for key in sorted(cmp_cells):
        val = cmp_cells[key]
        size = len(json.dumps({key: val}, ensure_ascii=False).encode("utf-8"))
        if cur and cur_size + size > 100000:
            shards.append(cur)
            cur, cur_size = {}, 0
        cur[key] = val
        cur_size += size
    if cur:
        shards.append(cur)
    tags = []
    for i, sh in enumerate(shards, 1):
        name = "assets/cmp-%02d.js" % i
        js = ("Object.assign(window.__CMPDATA__=window.__CMPDATA__||{},%s);"
              % json.dumps(sh, ensure_ascii=False)).replace("</script", "<\\/script")
        outputs[name] = js
        tags.append('<script src="%s"></script>' % name)
    tags.append(
        "<script>(function(){var D=window.__CMPDATA__||{},"
        "t=document.querySelectorAll('td.cmp-cell[data-cell]');"
        "for(var i=0;i<t.length;i++){var k=t[i].getAttribute('data-cell');"
        "if(D[k])t[i].innerHTML=D[k];}})();</script>")
    return "\n".join(tags)

# ---------------------------------------------------------------------------
# 方法论页
# ---------------------------------------------------------------------------

METHODOLOGY = [
    ("覆盖粒度一致（中立性护栏）",
     "Coverage parity (neutrality guardrail)",
     """<p>每个档案都必须逐项回答固定的 47 个硬维度，给出"有 / 无 / 部分支持 / 未找到证据 / 查证为无"的结论并标注证据等级，<strong>不允许"因为不是特色就不写"</strong>。这条规则的存在理由：特性天然会被相对各自基线放大（"对社区 PG 而言 TDE 是加分项"），但同一能力在不同档案里覆盖粒度不同，就是偏颇。护栏保证的是<strong>覆盖一致</strong>，权重可以不同。</p>""",
     """<p>Every profile must answer the same fixed 47 hard dimensions, each with a verdict (<em>supported / not supported / partially supported / no evidence found / verified absent</em>) and an evidence level. <strong>Skipping a dimension "because it is not a highlight" is not allowed.</strong> The rationale: a feature always looks bigger against its own baseline, but inconsistent coverage of the same capability across profiles is bias. The guardrail guarantees <strong>consistent coverage</strong>; weights may differ.</p>"""),
    ("选型权重自定：不做综合总分、不做排名",
     "You set the weights: no aggregate scores, no rankings",
     """<p>本站<strong>不做综合总分、不做排名</strong>。对比页只做维度级并排，不做跨库加权。原因是：权重取决于你的场景——金融核心系统里"复制与一致性"的权重可能是初创 MVP 的十倍；任何替你定权重的做法都是在替你做决定。正确用法：先列出你自己的必备维度与否决项，再到对比矩阵里按行（产品）逐项核对。</p>""",
     """<p>This site produces <strong>no aggregate scores and no rankings</strong>. The comparison page only places dimensions side by side; it never computes a cross-database weighted total. The reason: weights depend on your scenario — "replication & consistency" may weigh ten times more for a financial core system than for a startup MVP. Anyone who sets the weights for you is making your decision for you. The right way to use this site: list your own must-have dimensions and deal-breakers first, then check them row by row (per product) in the matrix.</p>"""),
    ("证据分级",
     "Evidence levels",
     """<p>档案中每条关键结论都标注证据等级（彩色徽章）：</p><ul><li><strong>官方文档</strong>：来自厂商官方文档、论文或 release notes，可信度最高，但注意"官方口径"可能只讲上限；</li><li><strong>厂商口径</strong>：厂商发布、新闻稿、定价页中的说法，未经独立验证，引用时请打折；</li><li><strong>社区实测</strong>：来自生产事故报告、benchmark、故障复盘等一手实践，有具体版本与场景才可信；</li><li><strong>社区共识</strong>：多份独立社区资料一致指向的结论，单篇博客不算共识；</li><li><strong>待验证</strong>：信息不全或存在冲突，明确标出，不写进判决依据。</li></ul><p>AI 顾问（待接入）在引用档案回答时，必须原样携带证据等级徽章。</p>""",
     """<p>Key claims in every profile carry an evidence level (colored badge):</p><ul><li><strong>official docs</strong>: from vendor documentation, papers or release notes — the most trustworthy, but note that official statements may only describe the ceiling;</li><li><strong>vendor claim</strong>: from vendor announcements, press releases or pricing pages — not independently verified, discount accordingly;</li><li><strong>community-tested</strong>: from production incident reports, benchmarks or postmortems — only credible with a concrete version and scenario;</li><li><strong>community consensus</strong>: pointed to by multiple independent community sources — a single blog post is not consensus;</li><li><strong>to-be-verified</strong>: incomplete or conflicting information, explicitly marked, never used as a basis for verdicts.</li></ul><p>The AI advisor (pending integration) must carry these badges unchanged whenever it cites profile evidence.</p>"""),
    ("“未找到证据”不等于“不支持”",
     "“No evidence found” ≠ “not supported”",
     """<p>档案中"未找到证据"只表示：在本次信息采集范围内没有找到可靠出处，<strong>不能反推出"该产品不支持"</strong>。同样，"查证为无"是经过核实确认缺失的结论，证据效力完全不同。做选型否决项判断时，请区分这两者；拿不准的，请以官方文档最新版本为准，或在 POC 中实测验证。</p>""",
     """<p>"No evidence found" in a profile only means no reliable source was found within this research pass — it <strong>must not be read as "not supported"</strong>. "Verified absent", by contrast, is a confirmed gap. These two carry completely different evidential weight when you are judging deal-breakers. When in doubt, check the latest official documentation or verify with a POC.</p>"""),
    ("信息时效",
     "Freshness",
     """<p>全部档案信息截至 <strong>2026-09-29</strong>，各档案头部标注了评审版本。数据库迭代快，结论会过期：看到"深水区"里的版本号与调优参数时，请先对一下你手上的版本再照抄。</p>""",
     """<p>All profiles are current as of <strong>2026-09-29</strong>, and each profile header notes the reviewed version. Databases iterate fast and conclusions expire: before copying tuning parameters or workarounds from the "deep dives", check them against the version you actually run.</p>"""),
    ("招牌能力 vs 客户经验：两种视角",
     "Signature strengths vs customer experiences: two lenses",
     """<p>每个档案有两个并列大区，回答的是两个不同的问题：</p><ul><li><strong>招牌能力</strong>：厂商挂在门口的招牌——架构级、官方主打的硬核能力；</li><li><strong>客户经验</strong>：用户用生产实践投票选出来的、真正离不开的能力，含 <strong>[避坑]</strong> 标签的反向招牌（杀手级代价）。</li></ul><p>研究方法：来源优先级为<strong>社区实践 &gt; 迁移总结 &gt; 故障复盘 &gt; 独立基准 &gt; 官方实践指南 &gt; 官网营销</strong>。官网首页营销几乎不产生有效发现，但可作为"厂商吹 vs 用户用"的错位检测器。每个能力标注窄场景、机制解释、生产验证（含来源链接）、竞品差距与证据等级；<strong>证据不足就降级或不收录，绝不硬凑</strong>。两区重叠是最强共识，分歧处（只有招牌没有经验，或反之）往往是最有价值的信息。</p>""",
     """<p>Each profile carries two parallel sections answering two different questions:</p><ul><li><strong>Signature strengths</strong>: what the vendor puts on the signboard — architecture-level, officially marketed capabilities;</li><li><strong>Customer experiences</strong>: what users actually cannot live without, validated by production practice — including reverse signatures tagged <strong>[Pitfall]</strong> (killer costs).</li></ul><p>Research method: source priority is <strong>community practice &gt; migration write-ups &gt; postmortems &gt; independent benchmarks &gt; official guides &gt; homepage marketing</strong>. Homepage marketing yields almost no valid findings, but works as a mismatch detector between vendor claims and user reality. Each capability notes its narrow scenario, mechanism, production evidence (with source links), gap vs rivals, and evidence grade; <strong>weak evidence is downgraded or dropped, never padded</strong>. Overlap between the two sections is the strongest consensus; divergence (signboard-only or experience-only) is often the most valuable signal.</p>"""),
]


def methodology_page_html():
    secs = []
    for zh_t, en_t, zh_b, en_b in METHODOLOGY:
        secs.append('<section class="doc-section"><h2><span data-zh="%s" data-en="%s">%s</span></h2>%s</section>'
                    % (zh_t, en_t, zh_t, lang_block(zh_b, en_b)))
    body = ('<div class="hero hero-slim"><h1><span data-zh="方法论" data-en="Methodology">方法论</span></h1>'
            '<p class="hero-sub"><span data-zh="我们如何保证对比的中立与可用" data-en="How we keep this comparison neutral and useful">我们如何保证对比的中立与可用</span></p></div>'
            + "\n".join(secs))
    return page_shell("DB 选型参考 - 方法论", "DB Compare - Methodology", body, active="methodology")


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# AI 选型页：提示词模板 + 一键跳转外部 AI（ChatGPT / Grok / Claude）
# 本站不做假的"AI 顾问"：推理发生在用户自己的 AI 账号里，本站只给提示词。
# ---------------------------------------------------------------------------

AI_TEMPLATES = [
    {
        "title_zh": '通用选型对比',
        "title_en": 'General comparison',
        "use_zh": '适用：第一次选型，或在 2-4 个候选库之间做一次全面对比。',
        "use_en": 'Use when: selecting for the first time, or comparing 2-4 candidates head to head.',
        "cand_mode": 'multi',
        "candidates_hint_zh": '（填 2-4 个，如 PostgreSQL、TiDB、PolarDB）',
        "candidates_hint_en": '(2-4, e.g. PostgreSQL, TiDB, PolarDB)',
        "prompt_zh": """你是一名中立的数据库架构顾问，不代表任何厂商。请基于公开资料，帮我做一次数据库选型对比。

【我的业务场景】（以下已按通用推荐场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- 业务类型与读写特征：电商下单，读写比约 7:3，写操作以事务型订单创建为主
- 数据规模与增速：当前 2TB，年增约 50%
- 峰值负载：写 2 万 TPS，读 20 万 QPS
- 团队规模与运维能力：3 名 DBA，可接受自建
- 部署环境：公有云（华东地域为主），满足国内合规要求
- 预算约束：license 成本敏感，人力成本同样敏感
- 否决项：必须支持同城多可用区高可用；等保三级为加分项而非硬性要求
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【候选数据库】{{CANDIDATES}}

【输出要求】
1. 按这 47 个维度逐项对比：静态加密 / TDE、TLS / 传输加密、审计、认证与权限、备份恢复、可观测性、连接模型、事务与隔离级别、复制与一致性、扩展方式、兼容性、许可证与商业模式、中文资料丰富度、性能与延迟特征、合规与认证、成熟度与社区生态、标杆用户、生态工具链、云托管与 Serverless、数据接入与摄入、外部数据访问、CDC 与下游同步、TTL 与数据生命周期管理、在线 DDL 与 Schema 演进、多租户与资源隔离、跨地域多活、高可用架构与 RTO/RPO、行级安全与数据脱敏、JSON 与半结构化能力、全文检索能力、存储效率与压缩、开源协议与厂商锁定风险、查询优化器与计划稳定性、参数调优与自治能力、静默数据损坏防护、存储过程/触发器/过程语言、约束与数据完整性、分析 SQL 完备性、被遗忘权与数据擦除、数据血缘与目录集成、存算分离 vs 存算一体、多模能力、FinOps 成本可观测性、驱动与多语言生态、物化视图、支持跨云、热点数据更新能力。
2. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证。严格区分"查证为无"和"未找到证据"，不要把没查到的写成不支持。
3. 每款候选库给出：最适合的场景、最可能踩的三个坑（从机制层面解释，并说明在什么负载或故障下会触发）。
4. 不做综合总分、不排名，只给带条件的判断，格式为"如果……那么……"。
5. 仅在用户删掉场景中的某一行或标注"未知"导致信息不足以下结论时，才主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。
6. 用中文回答。""",
        "prompt_en": """You are a neutral database architecture advisor, not affiliated with any vendor. Help me compare candidate databases based on public information.

【My scenario】(Pre-filled with generic recommended defaults: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Workload and read/write pattern: e-commerce ordering, roughly 7:3 read/write, writes dominated by transactional order creation
- Data size and growth: 2TB today, ~50% yearly growth
- Peak load: 20k write TPS, 200k read QPS
- Team size and ops capacity: 3 DBAs, self-hosting acceptable
- Deployment: public cloud (primary region in East China), meeting local compliance requirements
- Budget constraints: sensitive to license costs; headcount costs matter too
- Deal-breakers: must support multi-AZ high availability in the same metro; compliance certification is a plus, not a hard requirement
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Candidate databases】{{CANDIDATES}}

【Output requirements】
1. Compare dimension by dimension across these 47 dimensions: data-at-rest encryption / TDE, TLS / transport encryption, auditing, authentication & authorization, backup & recovery, observability, connection model, transactions & isolation levels, replication & consistency, scaling, compatibility, license & business model, Chinese-language resources, performance & latency, compliance & certifications, maturity & community, notable adopters, ecosystem tooling, managed & serverless, data ingestion, external data access, CDC & downstream, TTL & data lifecycle, online DDL & schema evolution, multi-tenancy & resource isolation, cross-region active-active, HA & RTO/RPO, row-level security & masking, JSON & semi-structured, full-text search, storage efficiency & compression, OSS license & lock-in risk, optimizer & plan stability, tuning & autonomy, silent corruption protection, stored procedures & triggers, constraints & integrity, analytical SQL, right to erasure, data lineage & catalog, storage-compute architecture, multi-model, FinOps & cost observability, drivers & clients, materialized views, multi-cloud support, hotspot update handling.
2. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Strictly distinguish "verified absent" from "no evidence found"; never present something you could not find as unsupported.
3. For each candidate: the scenarios it fits best, and the three most likely production pitfalls, explained at the mechanism level, including the load or failure conditions that trigger them.
4. No aggregate total score and no ranking. Give only conditional verdicts in "if ..., then ..." form.
5. Only when a scenario line was deleted or marked "unknown" and information is missing, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts.
6. Answer in English.""",
    },
    {
        "title_zh": '去 O 迁移评估',
        "title_en": 'Migrating off Oracle',
        "use_zh": '适用：从 Oracle 迁出，评估目标库的真实兼容代价与迁移风险。',
        "use_en": 'Use when: migrating off Oracle and assessing the true compatibility cost and risk of a target database.',
        "cand_mode": 'multi',
        "candidates_hint_zh": '（填 1-2 个，如 PolarDB-O、EDB Postgres、OceanBase Oracle 模式）',
        "candidates_hint_en": '(1-2, e.g. PolarDB-O, EDB Postgres, OceanBase Oracle mode)',
        "prompt_zh": """你是一名中立的数据库架构顾问。请帮我评估"去 O"迁移（从 Oracle 迁出）的可行性与真实成本。

【现状】（以下已按典型去 O 场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- Oracle 版本与部署：19c，两节点 RAC
- 强依赖特性：PL/SQL 存储过程包、分区表、DBLINK（计划逐步下线）
- 数据量与停机窗口：5TB，要求停机小于 4 小时
- 性能基线：核心交易峰值 8000 TPS，慢查询主要集中在报表类 SQL
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【候选目标库】{{CANDIDATES}}

【输出要求】
1. 兼容性逐项核对：区分"语法能跑"和"语义等价"，这是两回事，必须分开写。每项标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证。
2. 迁移风险清单，按三档输出：一定会改的代码、可能要改的代码、必须做 POC 才能确认的项。
3. 给出数据校验策略（全量加增量对账思路）与回滚方案要点。
4. 不做综合评分。仅在用户删掉【现状】中的某一行或标注"未知"导致信息不足以下结论时，才主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。用中文回答。""",
        "prompt_en": """You are a neutral database architecture advisor. Help me assess the feasibility and true cost of migrating off Oracle.

【Current state】(Pre-filled with a typical Oracle-migration scenario: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Oracle version and topology: 19c, two-node RAC
- Hard dependencies: PL/SQL packages, partitioned tables, DBLINKs (planned for gradual decommission)
- Data size and downtime budget: 5TB, less than 4 hours of downtime
- Performance baseline: 8k peak TPS on core transactions; slow queries concentrated in reporting SQL
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Candidate target databases】{{CANDIDATES}}

【Output requirements】
1. Check compatibility item by item, separating "syntax runs" from "semantically equivalent" — these are different things and must be written separately. Tag each item with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified.
2. A migration risk list in three tiers: code that will definitely change, code that may need changes, items that can only be confirmed with a POC.
3. A data-validation strategy (full plus incremental reconciliation approach) and the key points of a rollback plan.
4. No aggregate score. Only when a 【Current state】 line was deleted or marked "unknown" and information is missing, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts. Answer in English.""",
    },
    {
        "title_zh": '读扩展架构选型',
        "title_en": 'Read-scaling architecture',
        "use_zh": '适用：一写多读架构，读压力大，需要搞清复制延迟与代理行为的真实边界。',
        "use_en": 'Use when: single-writer, multiple-reader architectures where read pressure is high and you need the real boundaries of replication lag and proxy behavior.',
        "cand_mode": 'multi',
        "candidates_hint_zh": '（如 MySQL 一主多从加代理、PolarDB 读写分离、TiDB、Aurora 读副本）',
        "candidates_hint_en": '(e.g. MySQL primary with replicas plus proxy, PolarDB read-write splitting, TiDB, Aurora read replicas)',
        "prompt_zh": """你是一名中立的数据库架构顾问。请帮我设计"一写多读"的读扩展架构，并对比候选方案。

【我的场景】（以下已按通用推荐场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- 写负载：主库峰值写 1 万 TPS，写放大不明显
- 读负载：读 30 万 QPS，读写比约 30:1
- 一致性要求：核心读可接受 1 秒内旧数据；分布式事务非刚需
- 可用性要求：主库故障时 RTO 小于 5 分钟，RPO 接近 0
- 候选方案：{{CANDIDATES}}
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【输出要求】
1. 对比各方案的：复制延迟的真实量级与放大的条件、代理或中间件在故障与事务中的行为（连接闪断、事务粘性）、只读节点的成本构成、写天花板在哪里。
2. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；严格区分"查证为无"与"未找到证据"。
3. 给出 2-3 种架构组合建议，说明各自的取舍与翻车点，不做综合评分和排名。
4. 仅在用户删掉场景中的某一行或标注"未知"导致信息不足以下结论时，才主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。用中文回答。""",
        "prompt_en": """You are a neutral database architecture advisor. Help me design a single-writer, multiple-reader architecture and compare candidate approaches.

【My scenario】(Pre-filled with generic recommended defaults: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Write load: 10k write TPS on the primary, no significant write amplification
- Read load: 300k read QPS, read/write ratio about 30:1
- Consistency requirements: core reads tolerate up to 1 second of staleness; distributed transactions not a hard requirement
- Availability targets: RTO under 5 minutes, RPO near zero on primary failure
- Candidate approaches: {{CANDIDATES}}
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Output requirements】
1. Compare: realistic replication-lag magnitude and the conditions that amplify it, proxy/middleware behavior during failures and inside transactions (connection blips, transaction stickiness), cost structure of read nodes, and where the write ceiling is.
2. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Strictly distinguish "verified absent" from "no evidence found".
3. Give 2-3 architecture combinations with their trade-offs and failure modes. No aggregate score, no ranking.
4. Only when a scenario line was deleted or marked "unknown" and information is missing, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts. Answer in English.""",
    },
    {
        "title_zh": 'KV / 文档库选型',
        "title_en": 'KV and document store selection',
        "use_zh": '适用：在 Redis、MongoDB、DynamoDB、Cassandra 等之间按访问模式选型。',
        "use_en": 'Use when: choosing between Redis, MongoDB, DynamoDB, Cassandra and similar, driven by access patterns.',
        "cand_mode": 'multi',
        "candidates_hint_zh": '（填 2-3 个，如 Redis、Valkey、MongoDB、DynamoDB、Cassandra）',
        "candidates_hint_en": '(2-3, e.g. Redis, Valkey, MongoDB, DynamoDB, Cassandra)',
        "prompt_zh": """你是一名中立的数据库架构顾问。请帮我做 KV / 文档数据库选型。

【我的场景】（以下已按通用推荐场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- 访问模式：高频点查为主，辅以计数器和会话存储
- 数据结构：以简单 KV 和哈希为主，少量 JSON 文档
- 规模与性能：key 量级 10 亿，峰值 50 万 QPS，P99 延迟要求 5ms
- 一致性与持久化：宕机可接受秒级数据丢失；不需要多副本强一致
- 运维方式：倾向云托管，Serverless 可接受
- 候选库：{{CANDIDATES}}
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【输出要求】
1. 按访问模式逐项对比候选库的匹配度，指出"能用但别扭"的地方。
2. 重点对比：持久化与故障恢复的真实行为、大 key 与热 key 下的表现、集群扩缩容时的数据搬迁代价、托管服务的计费边界。
3. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证。
4. 只给带条件的判断，不做综合评分与排名；仅在用户删掉场景中的某一行或标注"未知"导致信息不足以下结论时，才主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析。用中文回答。""",
        "prompt_en": """You are a neutral database architecture advisor. Help me select a KV or document database.

【My scenario】(Pre-filled with generic recommended defaults: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Access patterns: mostly high-frequency point lookups, plus counters and session storage
- Data structures: mostly plain KV and hashes, some JSON documents
- Scale and performance: ~1B keys, 500k peak QPS, P99 latency target 5ms
- Consistency and durability: seconds of data loss tolerable on crash; strongly-consistent multi-replica not required
- Operations: lean toward managed cloud, serverless acceptable
- Candidates: {{CANDIDATES}}
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Output requirements】
1. Compare each candidate against the access patterns item by item, and call out where something "works but feels wrong".
2. Focus on: real persistence and crash-recovery behavior, behavior under big keys and hot keys, data-movement cost during cluster scale-out/in, and billing boundaries of managed services.
3. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified.
4. Conditional verdicts only, no aggregate score and no ranking. Only when a scenario line was deleted or marked "unknown" and information is missing, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered. Answer in English.""",
    },
    {
        "title_zh": '单库深挖',
        "title_en": 'Single-database deep dive',
        "use_zh": '适用：锁定一款数据库后，把它推到极限，提前知道会在哪里翻车。',
        "use_en": 'Use when: you have shortlisted one database and want to push it to its limits before it pushes you.',
        "cand_mode": 'single',
        "candidates_hint_zh": '【候选库名称】',
        "candidates_hint_en": '【candidate database name】',
        "prompt_zh": """你是一名中立的数据库架构顾问，专长是把系统推到极限。请深入分析{{CANDIDATES}}：

1. 它的核心机制是什么？在什么负载、异常或故障下，这个机制会最先崩？
2. 列出 3 个最可能在生产环境踩到的坑，从机制层面解释，并说明触发条件。
3. 哪些场景是它的"甜蜜点"，哪些场景是"禁区"？为什么？
4. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；不确定的请明确说不知道，不要编造。
5. 开始前先用一道交互式选择题问我最关心的 3-5 个维度：从 47 维中给出 3-4 组带字母编号的典型组合（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可勾选；等我回答后，再针对性深挖。不要一次抛出大段文字，也不要面面俱到地平铺。
6. 不做综合评分。用中文回答。
（建议：把本站该产品的档案页内容贴在下面，作为分析的起点）""",
        "prompt_en": """You are a neutral database architecture advisor who specializes in pushing systems to their limits. Analyze {{CANDIDATES}} in depth:

1. What is its core mechanism? Under what load, anomaly, or failure does this mechanism break first?
2. List the 3 most likely production pitfalls, explain them at the mechanism level, and state their trigger conditions.
3. Which scenarios are its sweet spot, and which are no-go zones? Why?
4. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Say "I don't know" explicitly where uncertain instead of inventing facts.
5. Before starting, ask me which 3-5 dimensions I care about most with one interactive multiple-choice question: offer 3-4 lettered bundles of typical dimension combinations (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; go deep on those only after I answer. Do not dump a wall of text, and do not go a mile wide and an inch deep.
6. No aggregate score. Answer in English.
(Tip: paste this site's profile page for the product below as a starting point for the analysis.)""",
    },
]


NEW_TEMPLATES = [
    {
        "group": 'olap',
        "title_zh": '离线数据仓库',
        "title_en": 'Batch data warehouse',
        "use_zh": '适用：T+1 或小时级批量 ETL，大扫描聚合为主的离线分析。',
        "use_en": 'Use when: T+1 or hourly batch ETL, offline analytics dominated by large scans and aggregations.',
        "cand_mode": 'multi',
        "candidates_hint_zh": '（如 Hive/Spark、ClickHouse、Apache Doris、StarRocks、Snowflake，填 2-3 个）',
        "candidates_hint_en": '(2-3, e.g. Hive/Spark, ClickHouse, Apache Doris, StarRocks, Snowflake)',
        "prompt_zh": """你是一名中立的数据架构顾问。请帮我做离线数据仓库（OLAP 批处理）选型。

【我的场景】（以下已按通用推荐场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- 数据规模与增量：总量 200TB，日增 2TB
- ETL 窗口：每天凌晨 4 小时内必须跑完
- 查询特征：大表扫描聚合为主，偶发多表 JOIN；并发查询数约 20
- 数据更新需求：需要按天 UPDATE/DELETE 修正数据，每日一次
- 团队与运维：数据团队 8 人，可接受自建与调优
- 部署与成本：公有云；计算成本比存储更敏感
- 候选：{{CANDIDATES}}
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【输出要求】
1. 按这些维度逐项对比：写入吞吐与 ETL 友好度、列存压缩与向量化扫描性能、大 JOIN 与复杂 SQL 能力、并发查询能力、数据更新与删除机制、运维复杂度（扩缩容、版本升级）、弹性扩展与存算分离、成本模型（存储与计算的计费边界）。
2. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；严格区分"查证为无"与"未找到证据"。
3. 每款候选给出：甜蜜点、最可能踩的三个坑（从机制层面解释，如后台合并的写入放大、物化视图的刷新代价，并说明触发条件）。
4. 不做综合总分、不排名，只给"如果……那么……"的条件判断。
5. 仅在用户删掉场景中的某一行或标注"未知"导致信息不足以下结论时，才主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。用中文回答。""",
        "prompt_en": """You are a neutral data architecture advisor. Help me select an offline data warehouse (batch OLAP).

【My scenario】(Pre-filled with generic recommended defaults: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Data size and daily increment: 200TB total, 2TB per day
- ETL window: must finish within 4 hours every night
- Query pattern: mostly large-scan aggregations, occasional multi-table JOINs; ~20 concurrent queries
- Data updates: daily UPDATE/DELETE corrections, once per day
- Team and operations: 8-person data team, self-hosting and tuning acceptable
- Deployment and cost: public cloud; compute costs more sensitive than storage
- Candidates: {{CANDIDATES}}
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Output requirements】
1. Compare dimension by dimension: write throughput and ETL friendliness, columnar compression and vectorized scan performance, large-JOIN and complex-SQL capability, concurrent query capacity, data update/delete mechanics, operational complexity (scaling, upgrades), elastic scaling and storage-compute separation, cost model (billing boundaries of storage vs compute).
2. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Strictly distinguish "verified absent" from "no evidence found".
3. For each candidate: its sweet spot and the three most likely pitfalls, explained at the mechanism level (e.g. write amplification from background merges, materialized-view refresh cost), with trigger conditions.
4. No aggregate total score and no ranking. Conditional verdicts only, in "if ..., then ..." form.
5. Only when a scenario line was deleted or marked "unknown" and information is missing, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts. Answer in English.""",
    },
    {
        "group": 'olap',
        "title_zh": '实时数仓',
        "title_en": 'Real-time warehouse',
        "use_zh": '适用：秒级~分钟级延迟，流式写入、实时大屏、高并发查询。',
        "use_en": 'Use when: seconds-to-minutes latency, streaming ingestion, real-time dashboards, high-concurrency queries.',
        "cand_mode": 'multi',
        "candidates_hint_zh": '（如 ClickHouse、Apache Doris、StarRocks、Apache Pinot、Druid，填 2-3 个）',
        "candidates_hint_en": '(2-3, e.g. ClickHouse, Apache Doris, StarRocks, Apache Pinot, Druid)',
        "prompt_zh": """你是一名中立的数据架构顾问。请帮我做实时数仓选型（秒级~分钟级延迟）。

【我的场景】（以下已按通用推荐场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- 数据源与写入：Kafka，峰值每秒写入 50 万条
- 端到端延迟 SLA：95% 的数据 1 分钟内可查
- 查询模式：实时大屏聚合为主，辅以高并发点查和明细下钻
- 语义要求：需要精确去重，exactly-once 非强需求
- 运维与成本约束：运维人力 2-3 人，倾向云托管，成本敏感
- 候选：{{CANDIDATES}}
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【输出要求】
1. 按这些维度逐项对比：流式写入吞吐与延迟、去重与 exactly-once 语义的实现代价、实时 JOIN 能力、高并发查询下的稳定性、预聚合与物化视图、扩缩容与版本升级的运维成本、故障恢复（副本重建速度）。
2. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；严格区分"查证为无"与"未找到证据"。
3. 每款候选给出：甜蜜点、最可能踩的三个坑（从机制层面解释，如写入放大的触发条件、副本同步延迟的放大路径）。
4. 不做综合总分、不排名，只给"如果……那么……"的条件判断。
5. 仅在用户删掉场景中的某一行或标注"未知"导致信息不足以下结论时，才主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。用中文回答。""",
        "prompt_en": """You are a neutral data architecture advisor. Help me select a real-time data warehouse (seconds-to-minutes latency).

【My scenario】(Pre-filled with generic recommended defaults: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Sources and ingestion: Kafka, peak 500k rows/sec
- End-to-end latency SLA: 95% of data queryable within 1 minute
- Query pattern: real-time dashboard aggregations, plus high-concurrency point lookups and drill-downs
- Semantics: exact deduplication required; exactly-once not a hard requirement
- Operations and cost constraints: 2-3 ops staff, lean toward managed services, cost-sensitive
- Candidates: {{CANDIDATES}}
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Output requirements】
1. Compare dimension by dimension: streaming write throughput and latency, cost of implementing deduplication and exactly-once semantics, real-time JOIN capability, stability under high-concurrency queries, pre-aggregation and materialized views, operational cost of scaling and upgrades, failure recovery (replica rebuild speed).
2. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Strictly distinguish "verified absent" from "no evidence found".
3. For each candidate: its sweet spot and the three most likely pitfalls, explained at the mechanism level (e.g. trigger conditions of write amplification, amplification paths of replica-sync lag).
4. No aggregate total score and no ranking. Conditional verdicts only, in "if ..., then ..." form.
5. Only when a scenario line was deleted or marked "unknown" and information is missing, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts. Answer in English.""",
    },
    {
        "group": 'olap',
        "title_zh": '交互式 BI 与即席查询',
        "title_en": 'Interactive BI and ad-hoc queries',
        "use_zh": '适用：分析师即席查询、BI 报表，要求亚秒响应、高并发。',
        "use_en": 'Use when: analyst ad-hoc queries and BI dashboards needing sub-second response and high concurrency.',
        "cand_mode": 'multi',
        "candidates_hint_zh": '（如 ClickHouse、Apache Doris、StarRocks、Trino/Presto、DuckDB，填 2-3 个）',
        "candidates_hint_en": '(2-3, e.g. ClickHouse, Apache Doris, StarRocks, Trino/Presto, DuckDB)',
        "prompt_zh": """你是一名中立的数据架构顾问。请帮我做交互式 BI 与即席查询引擎选型。

【我的场景】（以下已按通用推荐场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- 用户规模与并发：200 名分析师，峰值并发查询 100
- 延迟要求：P95 在 2 秒内返回
- 数据量级与查询复杂度：多维下钻为主，每日约 30% 的查询会钻取明细
- BI 工具：Superset 为主，少量 Tableau
- 权限需求：需要行级权限，列级权限暂不需要
- 候选：{{CANDIDATES}}
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【输出要求】
1. 按这些维度逐项对比：亚秒查询能力、高并发下的排队与资源隔离、BI 工具兼容性（SQL 方言、连接协议）、语义层与行列级权限、查询加速手段（缓存、预聚合）、运维复杂度与成本模型。
2. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；严格区分"查证为无"与"未找到证据"。
3. 每款候选给出：甜蜜点、最可能踩的三个坑（从机制层面解释，如高并发下查询排队的触发条件、BI 生成 SQL 的方言坑）。
4. 不做综合总分、不排名，只给"如果……那么……"的条件判断。
5. 仅在用户删掉场景中的某一行或标注"未知"导致信息不足以下结论时，才主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。用中文回答。""",
        "prompt_en": """You are a neutral data architecture advisor. Help me select an engine for interactive BI and ad-hoc queries.

【My scenario】(Pre-filled with generic recommended defaults: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Users and concurrency: 200 analysts, 100 peak concurrent queries
- Latency target: P95 under 2 seconds
- Data size and query complexity: mostly multi-dimensional drill-downs; ~30% of daily queries drill through to detail rows
- BI tools: mainly Superset, some Tableau
- Authorization needs: row-level permissions required; column-level not needed yet
- Candidates: {{CANDIDATES}}
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Output requirements】
1. Compare dimension by dimension: sub-second query capability, queuing and resource isolation under high concurrency, BI tool compatibility (SQL dialect, wire protocol), semantic layer and row/column-level permissions, acceleration techniques (caching, pre-aggregation), operational complexity and cost model.
2. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Strictly distinguish "verified absent" from "no evidence found".
3. For each candidate: its sweet spot and the three most likely pitfalls, explained at the mechanism level (e.g. trigger conditions of query queuing under high concurrency, SQL-dialect pitfalls from BI-generated queries).
4. No aggregate total score and no ranking. Conditional verdicts only, in "if ..., then ..." form.
5. Only when a scenario line was deleted or marked "unknown" and information is missing, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts. Answer in English.""",
    },
    {
        "group": 'olap',
        "title_zh": '湖仓一体',
        "title_en": 'Lakehouse',
        "use_zh": '适用：已有数据湖，想统一批流、开放表格式、存算分离。',
        "use_en": 'Use when: you have a data lake and want unified batch/streaming, open table formats, and storage-compute separation.',
        "cand_mode": 'multi',
        "candidates_hint_zh": '（如 Iceberg 加 Trino、Hudi 加 Flink 等，填 1-2 组）',
        "candidates_hint_en": '(1-2, e.g. Iceberg plus Trino, Hudi plus Flink)',
        "prompt_zh": """你是一名中立的数据架构顾问。请帮我做湖仓一体架构选型。

【我的场景】（以下已按通用推荐场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- 数据湖现状：对象存储，总量约 300TB
- 表格式倾向：尚未确定，倾向 Iceberg
- 计算引擎：Spark 跑批处理，Trino 跑即席查询
- 事务需求：需要 ACID 与 schema evolution，time travel 为加分项
- 流批一体需求：希望同一份数据同时服务离线与实时，但可分阶段落地
- 候选组合：{{CANDIDATES}}
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【输出要求】
1. 按这些维度逐项对比：表格式能力（ACID、schema evolution、分区演进、time travel）、引擎生态与兼容性、元数据服务（catalog）选型、小文件问题与 compaction 代价、存算分离下的真实成本、流批一体的成熟度（区分"能跑"和"生产可用"）。
2. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；严格区分"查证为无"与"未找到证据"。
3. 每组候选给出：甜蜜点、最可能踩的三个坑（从机制层面解释，如小文件放大的触发条件、compaction 的资源争抢）。
4. 不做综合总分、不排名，只给"如果……那么……"的条件判断。
5. 仅在用户删掉场景中的某一行或标注"未知"导致信息不足以下结论时，才主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。用中文回答。""",
        "prompt_en": """You are a neutral data architecture advisor. Help me select a lakehouse architecture.

【My scenario】(Pre-filled with generic recommended defaults: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Data lake status: object storage, ~300TB total
- Table format leaning: undecided, leaning toward Iceberg
- Compute engines: Spark for batch, Trino for ad-hoc queries
- Transactional needs: ACID and schema evolution required; time travel a plus
- Streaming-batch unification: want one dataset serving offline and real-time, phased rollout acceptable
- Candidate combinations: {{CANDIDATES}}
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Output requirements】
1. Compare dimension by dimension: table-format capabilities (ACID, schema evolution, partition evolution, time travel), engine ecosystem and compatibility, metadata service (catalog) choice, small-files problem and compaction cost, real cost under storage-compute separation, maturity of streaming-batch unification (separate "it runs" from "production-ready").
2. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Strictly distinguish "verified absent" from "no evidence found".
3. For each candidate combination: its sweet spot and the three most likely pitfalls, explained at the mechanism level (e.g. trigger conditions of small-file amplification, resource contention from compaction).
4. No aggregate total score and no ranking. Conditional verdicts only, in "if ..., then ..." form.
5. Only when a scenario line was deleted or marked "unknown" and information is missing, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts. Answer in English.""",
    },
    {
        "group": 'olap',
        "title_zh": '嵌入式与单机分析',
        "title_en": 'Embedded and single-node analytics',
        "use_zh": '适用：笔记本/单机/边缘的零运维分析，数据量 GB 到数 TB。',
        "use_en": 'Use when: zero-ops analytics on a laptop, single server, or edge, with GBs to a few TBs of data.',
        "cand_mode": 'multi',
        "candidates_hint_zh": '（如 DuckDB、ClickHouse 单机版、SQLite 相关方案，填 2-3 个）',
        "candidates_hint_en": '(2-3, e.g. DuckDB, single-node ClickHouse, SQLite-based options)',
        "prompt_zh": """你是一名中立的数据架构顾问。请帮我做嵌入式与单机 OLAP 选型。

【我的场景】（以下已按通用推荐场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- 运行环境：单机服务器（64 核 / 256GB 内存）
- 数据量级：几百 GB，未来 2 年可能到 2TB
- 语言生态：Python/Arrow 为刚需
- 写入特征：单并发批量写入，每日一次
- 运维要求：要求零运维，嵌入应用分发
- 候选：{{CANDIDATES}}
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【输出要求】
1. 按这些维度逐项对比：单机扫描性能天花板、内存管理与溢出行为、Python/Arrow 生态集成度、并发写入限制、文件格式与外部数据互操作、从单机扩展到集群的迁移路径。
2. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；严格区分"查证为无"与"未找到证据"。
3. 每款候选给出：甜蜜点、最可能踩的三个坑（从机制层面解释），以及"出现什么信号就必须换成集群架构"的判断线。
4. 不做综合总分、不排名，只给"如果……那么……"的条件判断。
5. 仅在用户删掉场景中的某一行或标注"未知"导致信息不足以下结论时，才主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。用中文回答。""",
        "prompt_en": """You are a neutral data architecture advisor. Help me select an embedded or single-node OLAP engine.

【My scenario】(Pre-filled with generic recommended defaults: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Environment: single server (64 cores / 256GB RAM)
- Data size: hundreds of GB, possibly 2TB within 2 years
- Language ecosystem: Python/Arrow integration is a hard requirement
- Write pattern: single-writer batch loads, once daily
- Operations: zero-ops required, embedded distribution with the app
- Candidates: {{CANDIDATES}}
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Output requirements】
1. Compare dimension by dimension: single-node scan performance ceiling, memory management and spilling behavior, Python/Arrow ecosystem integration, concurrent-write limits, file-format and external-data interoperability, migration path from single node to a cluster.
2. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Strictly distinguish "verified absent" from "no evidence found".
3. For each candidate: its sweet spot, the three most likely pitfalls explained at the mechanism level, and the tripwire — what signals mean you must move to a cluster architecture.
4. No aggregate total score and no ranking. Conditional verdicts only, in "if ..., then ..." form.
5. Only when a scenario line was deleted or marked "unknown" and information is missing, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts. Answer in English.""",
    },
    {
        "group": 'aidb',
        "title_zh": 'RAG 向量库选型',
        "title_en": 'Vector DB for RAG',
        "use_zh": '适用：RAG 知识库，在专用向量库与通用库 AI 扩展之间做选择。',
        "use_en": 'Use when: building a RAG knowledge base and choosing between dedicated vector databases and AI extensions of general databases.',
        "cand_mode": 'multi',
        "candidates_hint_zh": '（如 Milvus、Weaviate、Qdrant、Pinecone、pgvector、OceanBase 向量、Elasticsearch，填 2-3 个）',
        "candidates_hint_en": '(2-3, e.g. Milvus, Weaviate, Qdrant, Pinecone, pgvector, OceanBase vector, Elasticsearch)',
        "prompt_zh": """你是一名中立的 AI 基础设施顾问。请帮我做 RAG 场景的向量数据库选型。

【我的场景】（以下已按通用推荐场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- 向量规模：5000 万条，维度 1024
- embedding 模型：bge-m3，已固定
- 查询负载：峰值 2000 QPS，P99 延迟要求 100ms
- 过滤需求：需要标量过滤（按租户、时间、标签过滤后再做向量检索）
- 数据更新：每日新增约 1%，删除量小
- 部署方式：倾向云托管
- 候选：{{CANDIDATES}}
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【输出要求】
1. 按 AI 数据库自己的维度对比（不要套用 OLTP 的维度）：向量索引算法（HNSW/IVF/DiskANN）与召回率-延迟权衡、标量过滤加向量混合检索（注意 pre-filtering 与 post-filtering 的正确性陷阱）、十亿级扩展（分片与分布式）、实时写入与删除的代价、embedding 流水线（切分与向量化谁来做、模型集成方式）、与现有技术栈的协同、成本模型。
2. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；严格区分"查证为无"与"未找到证据"。
3. 每款候选给出：甜蜜点、最可能踩的三个坑（从机制层面解释，如 HNSW 参数调优空间、过滤导致召回率塌陷的条件）。
4. 不做综合总分、不排名，只给"如果……那么……"的条件判断。
5. 仅在用户删掉场景中的某一行或标注"未知"导致信息不足以下结论时，才主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。用中文回答。""",
        "prompt_en": """You are a neutral AI infrastructure advisor. Help me select a vector database for a RAG workload.

【My scenario】(Pre-filled with generic recommended defaults: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Vector scale: 50M vectors, 1024 dimensions
- Embedding model: bge-m3, fixed
- Query load: 2k peak QPS, P99 latency target 100ms
- Filtering needs: scalar filtering required (by tenant, time, tags before vector search)
- Data churn: ~1% daily inserts, few deletes
- Deployment: lean toward managed cloud
- Candidates: {{CANDIDATES}}
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Output requirements】
1. Compare along dimensions native to AI databases (do not reuse OLTP dimensions): vector index algorithms (HNSW/IVF/DiskANN) and the recall-latency trade-off, scalar-filter plus vector hybrid search (watch the correctness trap of pre-filtering vs post-filtering), billion-scale-out (sharding and distribution), cost of real-time writes and deletes, the embedding pipeline (who does chunking and vectorization, model integration), fit with the existing stack, cost model.
2. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Strictly distinguish "verified absent" from "no evidence found".
3. For each candidate: its sweet spot and the three most likely pitfalls, explained at the mechanism level (e.g. HNSW parameter tuning headroom, conditions under which filtering collapses recall).
4. No aggregate total score and no ranking. Conditional verdicts only, in "if ..., then ..." form.
5. Only when a scenario line was deleted or marked "unknown" and information is missing, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts. Answer in English.""",
    },
    {
        "group": 'aidb',
        "title_zh": '专用向量库 vs 通用库 AI 扩展',
        "title_en": 'Dedicated vector DB vs AI extensions',
        "use_zh": '适用：已有 PG/OceanBase/ES，想判断要不要引入专用向量库。',
        "use_en": 'Use when: you already run PG/OceanBase/ES and need to decide whether a dedicated vector database is warranted.',
        "cand_mode": 'first',
        "candidates_hint_zh": '（如 PostgreSQL 加 pgvector / OceanBase 向量 / Elasticsearch dense_vector / MongoDB Atlas Vector Search）',
        "candidates_hint_en": '(e.g. PostgreSQL with pgvector / OceanBase vector / Elasticsearch dense_vector / MongoDB Atlas Vector Search)',
        "prompt_zh": """你是一名中立的 AI 基础设施顾问。请帮我判断：RAG 场景下，继续用现有通用数据库的 AI 扩展，还是引入专用向量数据库？

【我的现状】（以下已按通用推荐场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- 现有数据库：{{CANDIDATES}}
- 向量规模与增长预期：当前 2000 万条，维度 1024，未来一年预计增长到 1 亿
- 当前痛点：召回率不达标（Top10 召回率约 85%），过滤查询写起来别扭
- 团队对引入新组件的接受度：可以接受，但希望运维负担可控
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【输出要求】
1. 对比通用库 AI 扩展与专用向量库（Milvus、Qdrant、Weaviate）在五个方面的差异：索引算法丰富度、规模天花板、混合检索能力、运维负担、生态集成。
2. 给出明确的取舍线：什么规模与什么信号出现之前，通用库的 AI 扩展够用；出现哪些信号，就必须迁到专用向量库。
3. 如果建议迁移，给出迁移代价评估（数据迁移、双写、回滚方案）。
4. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；严格区分"查证为无"与"未找到证据"。
5. 不做综合总分、不排名；仅在用户删掉【我的现状】中的某一行或标注"未知"导致信息不足以下结论时，才主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。用中文回答。""",
        "prompt_en": """You are a neutral AI infrastructure advisor. Help me decide: for a RAG workload, should I stay on my general-purpose database's AI extension or adopt a dedicated vector database?

【Current state】(Pre-filled with generic recommended defaults: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Existing database: {{CANDIDATES}}
- Vector scale and growth outlook: 20M vectors at 1024 dims today, expected to reach 100M within a year
- Current pain points: recall below bar (~85% Top-10 recall), filtered queries awkward to write
- Team appetite for adding a new component: acceptable if operational burden stays manageable
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Output requirements】
1. Contrast general-purpose AI extensions against dedicated vector databases (Milvus, Qdrant, Weaviate) on five axes: index-algorithm richness, scale ceiling, hybrid-search capability, operational burden, ecosystem integration.
2. Draw an explicit line: below what scale and signals the general-purpose extension is enough; which signals mean you must move to a dedicated vector database.
3. If migration is advised, assess the migration cost (data migration, dual writes, rollback plan).
4. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Strictly distinguish "verified absent" from "no evidence found".
5. No aggregate total score and no ranking. Only when a 【Current state】 line was deleted or marked "unknown" and information is missing, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts. Answer in English.""",
    },
    {
        "group": 'aidb',
        "title_zh": '混合检索与召回质量',
        "title_en": 'Hybrid search and recall quality',
        "use_zh": '适用：RAG 检索质量不达标，需要深水区诊断与调优。',
        "use_en": 'Use when: RAG retrieval quality is below bar and you need deep diagnosis and tuning.',
        "prompt_zh": """你是一名中立的 AI 基础设施顾问，专长检索质量调优。我的 RAG 检索质量不达标，请帮我做混合检索与召回质量的深水区诊断。

【我的现状】（以下已按通用推荐场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- 当前方案：单一向量检索
- 症状：召回率低（Top10 召回率约 80%），相关文档排不上
- 数据特征：中英文混合，长文档，结构化字段多（租户、时间、标签）
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【输出要求】
1. 给出诊断框架：先判断是 embedding 模型问题、索引参数问题、切分策略问题，还是过滤写法问题，并说明每种的判别方法。
2. 对比混合检索策略：多路召回（向量加全文加稀疏）与结果融合（RRF 这类方法）、重排（rerank）模型的取舍与代价。
3. 给出离线评测方法：如何构建评测集、用什么指标（召回率、MRR、nDCG）验证优化真的有效。
4. 说明 GraphRAG 这类方案在什么条件下值得上、什么条件下是过度设计。
5. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；不确定的明确说不知道，不要编造。
6. 若用户删掉【我的现状】中的行或标注"未知"，像医生问诊一样先向我提问：交互式逐题进行，一次只问一个关键症状，每个症状给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一个，所有关键症状问完后，再开始诊断。不要一次把所有问题都列出来，也不要编造。问诊时优先覆盖：召回不达标的具体症状（查全/查准/排序哪个环节）、向量规模与索引类型、标量过滤复杂度、查询模式（TopK 取值）、已尝试过的优化手段。用中文回答。""",
        "prompt_en": """You are a neutral AI infrastructure advisor specializing in retrieval-quality tuning. My RAG retrieval quality is below bar — help me with a deep diagnosis of hybrid search and recall quality.

【Current state】(Pre-filled with generic recommended defaults: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Current approach: pure vector search
- Symptoms: low recall (~80% Top-10 recall), relevant documents not ranking
- Data characteristics: mixed Chinese-English, long documents, many structured fields (tenant, time, tags)
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Output requirements】
1. A diagnostic framework: determine first whether it is an embedding-model problem, an index-parameter problem, a chunking-strategy problem, or a filter-writing problem — with a discrimination method for each.
2. Compare hybrid strategies: multi-path retrieval (vector plus full-text plus sparse) with result fusion (methods like RRF), and the trade-offs and costs of rerank models.
3. An offline evaluation method: how to build an eval set and which metrics (recall, MRR, nDCG) prove an optimization actually worked.
4. When GraphRAG-style approaches are worth it and when they are over-engineering.
5. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Say explicitly where uncertain instead of inventing facts.
6. If the user deleted 【Current state】 lines or marked them "unknown", take a doctor-like history first, interactively one symptom at a time: each step ask one key symptom with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next one, and start the diagnosis only after the history is complete. Do not list all questions at once, and do not invent facts. Prioritize asking about: which stage underperforms (recall/precision/ranking), vector scale and index type, scalar-filter complexity, query pattern (TopK value), optimizations already tried. Answer in English.""",
    },
]

AI_TEMPLATES.extend(NEW_TEMPLATES)

# 主动问询的领域聚焦点：场景留空时，AI 出选择题应优先覆盖这些维度
# （键为 title_zh；单库深挖、混合检索诊断两个模板单独处理）
Q_FOCUS = {
    "通用选型对比": (
        "业务类型与读写特征、数据规模与年增速、峰值负载形态（QPS/并发/热点）、团队运维能力与值班体系、部署环境与合规要求、预算范围与一票否决项",
        "workload type and read/write profile, data size and annual growth, peak load shape (QPS/concurrency/hotspots), team ops capacity and on-call setup, deployment environment and compliance needs, budget range and hard vetoes"),
    "去 O 迁移评估": (
        "Oracle 版本与部署形态（单机/RAC/ADG）、强依赖特性清单（PL/SQL、DBLINK、分区、物化视图、AQ、VPD/OLS）、数据总量与停机窗口、性能基线关键指标、回退预案要求",
        "Oracle version and topology (single-instance/RAC/ADG), hard-dependency inventory (PL/SQL, DBLINKs, partitioning, materialized views, AQ, VPD/OLS), total data size and downtime window, key performance baseline metrics, rollback requirements"),
    "读扩展架构选型": (
        "写负载与峰值写入量、读/写比例、读一致性容忍度（能否接受秒级延迟）、RTO/RPO 目标、现有代理/中间件与连接池形态",
        "write load and peak write volume, read/write ratio, read-consistency tolerance (is seconds-level lag acceptable), RTO/RPO targets, existing proxy/middleware and connection-pooling setup"),
    "KV / 文档库选型": (
        "访问模式（点查/范围扫描/聚合占比）、一致性与事务需求（单文档原子 vs 多文档事务）、数据模型偏好（文档/KV/宽列）、运维偏好（托管 vs 自建）",
        "access patterns (point lookup vs range scan vs aggregation mix), consistency and transaction needs (single-document atomicity vs multi-document transactions), data-model preference (document/KV/wide-column), ops preference (managed vs self-hosted)"),
    "离线数据仓库": (
        "数据规模与年增速、ETL/调度现状与 T+1 时效要求、查询复杂度（宽表关联层数）与并发数、SQL 方言依赖（Hive/Spark SQL 等）",
        "data size and annual growth, current ETL/scheduling setup and T+1 SLA, query complexity (join depth) and concurrency, SQL dialect dependencies (Hive/Spark SQL etc.)"),
    "实时数仓": (
        "实时性要求（秒级/分钟级）、写入吞吐（每秒行数）与数据源、查询并发与复杂度、exactly-once 语义要求",
        "freshness requirement (seconds vs minutes), write throughput (rows/sec) and data sources, query concurrency and complexity, exactly-once semantics requirements"),
    "交互式 BI 与即席查询": (
        "并发用户/查询数、查询模式（固定报表 vs 即席探索占比）、数据新鲜度要求、现有 BI 工具",
        "concurrent users/queries, query mix (canned reports vs ad-hoc exploration), data freshness needs, existing BI tools"),
    "湖仓一体": (
        "现有湖存储与表格式（Iceberg/Hudi/Delta）、批流一体需求、数据治理与权限要求、对存算分离运维的接受度",
        "existing lake storage and table format (Iceberg/Hudi/Delta), batch-streaming unification needs, data governance and access-control requirements, appetite for storage-compute-separated operations"),
    "嵌入式与单机分析": (
        "数据规模上限、部署形态（嵌入进程/单机服务/桌面应用）、查询语言偏好（SQL/Python）、与现有系统的集成方式",
        "data size ceiling, deployment shape (embedded in-process / single-node service / desktop app), query language preference (SQL/Python), integration with existing systems"),
    "RAG 向量库选型": (
        "向量规模与维度、召回率硬要求、标量过滤+向量混合检索需求、数据更新频率、P99 延迟要求",
        "vector scale and dimensions, hard recall requirements, scalar-filter plus vector hybrid search needs, data update frequency, P99 latency requirements"),
    "专用向量库 vs 通用库 AI 扩展": (
        "现有数据库与已用 AI 扩展、RAG 规模预期（向量数/增速）、团队学习意愿、是否接受多一套运维体系",
        "existing database and AI extensions in use, expected RAG scale (vector count/growth), team learning appetite, willingness to operate one more system"),
}
_ANCHOR_ZH = "用交互式选择题逐题提问"
_ANCHOR_EN = "interactive multiple-choice questions"
for _t in AI_TEMPLATES:
    _qz, _qe = Q_FOCUS.get(_t["title_zh"], ("", ""))
    if _qz and _ANCHOR_ZH in _t["prompt_zh"]:
        _t["prompt_zh"] = _t["prompt_zh"].replace(
            _ANCHOR_ZH, _ANCHOR_ZH + "（提问时优先覆盖：" + _qz + "）", 1)
    if _qe and _ANCHOR_EN in _t["prompt_en"]:
        _t["prompt_en"] = _t["prompt_en"].replace(
            _ANCHOR_EN, _ANCHOR_EN + " (prioritize asking about: " + _qe + ")", 1)

GROUPS = [
    ("oltp", "通用选型", "General",
     "覆盖 OLTP 与通用场景的选型：多候选库全面对比、去 O 迁移、读扩展架构、KV 与文档库。",
     "Covers OLTP and general scenarios: head-to-head comparison of candidates, migrating off Oracle, read-scaling architecture, KV/document selection, and single-database deep dives."),
    ("olap", "OLAP 选型", "OLAP",
     "OLAP 不是一种数据库，而是一类负载；选型前先对号入座。下面按业务形态分成五个子领域：离线数仓（T+1 批量）、实时数仓（秒级~分钟级）、交互式 BI 与即席查询（亚秒、高并发）、湖仓一体（开放格式、存算分离）、嵌入式分析（单机零运维）。同一款产品在不同子领域里可能是神器也可能是灾难——先选子领域，再选产品。",
     "OLAP is not one database but a class of workloads — pick your sub-domain first. Five sub-domains below: batch warehouse (T+1), real-time warehouse (seconds-to-minutes), interactive BI and ad-hoc queries (sub-second, high concurrency), lakehouse (open formats, storage-compute separation), embedded analytics (single-node, zero-ops). The same product can be a gem in one sub-domain and a disaster in another."),
    ("aidb", "AI 数据库选型", "AI databases",
     "AI 数据库是一个衍生新领域，不等于给老数据库贴 AI 标签：它有自己独立的评价维度——向量索引算法与召回率、标量过滤加向量混合检索、十亿级扩展、embedding 流水线。下面三个模板分别覆盖：RAG 场景的向量库选型、专用向量库 vs 通用库 AI 扩展（如 PG、OceanBase、ES 的向量能力）的取舍线、混合检索与召回质量的深水区诊断。",
     "AI databases are a derivative new field, not a relabeling of old databases: they have their own evaluation dimensions — vector index algorithms and recall, scalar-filter plus vector hybrid search, billion-scale expansion, the embedding pipeline. Three templates below: vector DB selection for RAG, the trade-off line between dedicated vector DBs and AI extensions of general databases (e.g. vector support in PG, OceanBase, ES), and deep diagnosis of hybrid search and recall quality."),
]


def advisor_page_html(products):

    opts_a, opts_b = [], []
    for prod in products:
        nm = html.escape(prod["name"])
        v = html.escape(prod["name"], quote=True)
        opts_a.append('<option value="%s"%s>%s</option>' % (v, " selected" if prod["name"] == "OceanBase" else "", nm))
        opts_b.append('<option value="%s"%s>%s</option>' % (v, " selected" if prod["name"] == "TiDB" else "", nm))
    _extra = ["Pinecone", "Elasticsearch", "Neo4j"]
    _extra_opts = "".join('<option value="%s">%s</option>' % (html.escape(x, quote=True), html.escape(x)) for x in _extra)
    _core_a, _core_b = "".join(opts_a), "".join(opts_b)
    sel_a_zh = ('<optgroup label="本站深度档案（%d 款）">%s</optgroup>'
                '<optgroup label="更多热门库（暂无本站档案）">%s</optgroup>') % (len(products), _core_a, _extra_opts)
    sel_b_zh = ('<optgroup label="本站深度档案（%d 款）">%s</optgroup>'
                '<optgroup label="更多热门库（暂无本站档案）">%s</optgroup>') % (len(products), _core_b, _extra_opts)
    sel_a_en = ('<optgroup label="Profiled on this site (%d)">%s</optgroup>'
                '<optgroup label="More popular databases (no profile yet)">%s</optgroup>') % (len(products), _core_a, _extra_opts)
    sel_b_en = ('<optgroup label="Profiled on this site (%d)">%s</optgroup>'
                '<optgroup label="More popular databases (no profile yet)">%s</optgroup>') % (len(products), _core_b, _extra_opts)
    pk_zh = """
<div class="subnav">
  <a href="#pk">多库 PK</a>
  <a href="#grp-oltp">通用选型</a>
  <a href="#grp-olap">OLAP 选型</a>
  <a href="#grp-aidb">AI 数据库选型</a>
</div>
<h2 id="pk"><span data-zh="多库 PK" data-en="Head-to-head">多库 PK</span></h2>
<p>选 2-4 款数据库，一键生成多库对比提示词，直接发给 AI。顶部选了对比库后，这里会自动使用已选库（下拉框会被禁用）；没选时用下面的下拉框，默认已选中 OceanBase 和 TiDB。</p>
<p id="pk-note" class="pk-note" hidden></p>
<div class="pk-row">
  <select id="pk-a" class="pk-select" aria-label="数据库 A">%s</select>
  <span class="pk-vs">VS</span>
  <select id="pk-b" class="pk-select" aria-label="数据库 B">%s</select>
</div>
<div class="ai-btn-row">
  <button type="button" class="ai-btn ai-copy" data-pkact="copy"><span data-zh="复制提示词" data-en="Copy prompt">复制提示词</span></button>
  <button type="button" class="ai-btn" data-pkact="chatgpt">ChatGPT <span aria-hidden="true">\u2197</span></button>
  <button type="button" class="ai-btn" data-pkact="grok">Grok <span aria-hidden="true">\u2197</span></button>
  <button type="button" class="ai-btn" data-pkact="claude">Claude <span aria-hidden="true">\u2197</span></button>
</div>
""" % (sel_a_zh, sel_b_zh)
    pk_en = """
<div class="subnav">
  <a href="#pk">Head-to-head</a>
  <a href="#grp-oltp">General</a>
  <a href="#grp-olap">OLAP</a>
  <a href="#grp-aidb">AI databases</a>
</div>
<h2 id="pk"><span data-zh="多库 PK" data-en="Head-to-head">多库 PK</span></h2>
<p>Pick 2-4 databases and generate a comparison prompt for your AI in one click. If you have selected databases in the compare tray at the top, they are used automatically (the dropdowns are disabled); otherwise use the dropdowns below. OceanBase vs TiDB is preselected.</p>
<p id="pk-note-en" class="pk-note" hidden></p>
<div class="pk-row">
  <select id="pk-a-en" class="pk-select" aria-label="Database A">%s</select>
  <span class="pk-vs">VS</span>
  <select id="pk-b-en" class="pk-select" aria-label="Database B">%s</select>
</div>
<div class="ai-btn-row">
  <button type="button" class="ai-btn ai-copy" data-pkact="copy"><span data-zh="复制提示词" data-en="Copy prompt">复制提示词</span></button>
  <button type="button" class="ai-btn" data-pkact="chatgpt">ChatGPT <span aria-hidden="true">\u2197</span></button>
  <button type="button" class="ai-btn" data-pkact="grok">Grok <span aria-hidden="true">\u2197</span></button>
  <button type="button" class="ai-btn" data-pkact="claude">Claude <span aria-hidden="true">\u2197</span></button>
</div>
""" % (sel_a_en, sel_b_en)

    def render_card(t):
        cand = t.get("cand_mode") or ""
        cand_attrs = ""
        if cand:
            cand_attrs = (' data-cand="%s" data-hint-zh="%s" data-hint-en="%s"'
                          % (cand,
                             html.escape(t["candidates_hint_zh"], quote=True),
                             html.escape(t["candidates_hint_en"], quote=True)))
        return (
            '<div class="prompt-card"%s>\n'
            '  <h3><span data-zh="%s" data-en="%s">%s</span></h3>\n'
            '  <p class="prompt-use"><span data-zh="%s" data-en="%s">%s</span></p>\n'
            '  <pre class="prompt-text lang-zh">%s</pre>\n'
            '  <pre class="prompt-text lang-en" hidden>%s</pre>\n'
            '  <div class="ai-btn-row">\n'
            '    <button type="button" class="ai-btn ai-copy" data-act="copy"><span data-zh="复制提示词" data-en="Copy prompt">复制提示词</span></button>\n'
            '    <button type="button" class="ai-btn" data-act="chatgpt">ChatGPT <span aria-hidden="true">\u2197</span></button>\n'
            '    <button type="button" class="ai-btn" data-act="grok">Grok <span aria-hidden="true">\u2197</span></button>\n'
            '    <button type="button" class="ai-btn" data-act="claude">Claude <span aria-hidden="true">\u2197</span></button>\n'
            '  </div>\n'
            '</div>' % (
                cand_attrs,
                t["title_zh"], t["title_en"], t["title_zh"],
                t["use_zh"], t["use_en"], t["use_zh"],
                t["prompt_zh"], t["prompt_en"],
            )
        )

    sections = []
    for gid, tzh, ten, izh, ien in GROUPS:
        g = [render_card(x) for x in AI_TEMPLATES if x.get("group", "oltp") == gid and x["title_zh"] != "单库深挖"]
        sections.append(
            '<h2 id="grp-%s"><span data-zh="%s" data-en="%s">%s</span></h2>\n'
            '<p class="grp-intro"><span data-zh="%s" data-en="%s">%s</span></p>\n%s'
            % (gid, tzh, ten, tzh, izh, ien, izh, "\n".join(g)))
    sections_html = "\n".join(sections)

    zh_head = """
<div class="hero hero-slim">
  <h1><span data-zh="AI选型" data-en="AI Selection">AI选型</span></h1>
  <p>不替你做决定，也不假装智能：选一个提示词模板，场景已按通用推荐值预填好，一键跳转到你自己的 ChatGPT、Grok 或 Claude 账号里生成对比。</p>
</div>
<section class="doc-section">
<h2>用法</h2>
<div class="howto">
  <div class="howto-step"><span class="n">1</span><h4>选一个提示词模板</h4><p>上面可以直接多库 PK（2-4 款）；下面 12 个模板分三组：通用选型 4 个、OLAP 选型 5 个、AI 数据库选型 3 个。顶栏的「对比」托盘选好库后，提示词里的候选库会自动填入已选产品。</p></div>
  <div class="howto-step"><span class="n">2</span><h4>场景已预填，可直接用</h4><p>每个模板的场景都已按通用推荐值填好：不改可直接点按钮出结果；按你的实际情况改一改，结果会更准；删掉某一行，AI 会针对该项向你提问。</p></div>
  <div class="howto-step"><span class="n">3</span><h4>一键跳转外部 AI</h4><p>点 ChatGPT / Grok / Claude，提示词会自动填入新对话的输入框；若未自动填入，用"复制提示词"按钮手动粘贴。</p></div>
</div>
<div class="neutral-note">
  <strong>为什么这样更中立？</strong>推理发生在你自己的 AI 账号里：本站不经手你的业务信息，也不替你预设答案。每份模板都写死了几条纪律——结论标注证据等级、严格区分"查证为无"与"未找到证据"、不做综合总分与排名；信息不足时不许编造，必须先交互式逐题提问（一次只问一个问题，每题给出带字母编号的选项，你只需回复字母即可作答），而且不同模板问的方向不一样（去 O 问 Oracle 强依赖、向量库问召回率与延迟、诊断类先问诊再下结论）；候选库横跨不同领域时不许硬对比，先确认你的真实诉求。但请注意：AI 的回答仍需对照本站档案交叉验证，模型也会一本正经地编造。
</div>
"""
    en_head = """
<div class="hero hero-slim">
  <h1><span data-zh="AI选型" data-en="AI Selection">AI选型</span></h1>
  <p>No decisions made for you, no fake intelligence: pick a prompt template — the scenario comes pre-filled with generic recommended defaults — and jump to your own ChatGPT, Grok, or Claude account to generate the comparison.</p>
</div>
<section class="doc-section">
<h2>How it works</h2>
<div class="howto">
  <div class="howto-step"><span class="n">1</span><h4>Pick a prompt template</h4><p>Use head-to-head above for a one-click 2-4 database comparison; the 12 templates below come in three groups: 4 general, 5 OLAP, 3 AI database. Once you pick databases in the compare tray at the top, the candidate slots in each prompt are filled in automatically.</p></div>
  <div class="howto-step"><span class="n">2</span><h4>Scenario pre-filled, ready to use</h4><p>Each template comes with generic recommended defaults: use as-is for instant results, edit to match your reality for better results, or delete a line and the AI will ask you about that item.</p></div>
  <div class="howto-step"><span class="n">3</span><h4>Jump to an external AI</h4><p>Click ChatGPT / Grok / Claude and the prompt is pre-filled into a new chat. If it is not pre-filled, use the "Copy prompt" button and paste it manually.</p></div>
</div>
<div class="neutral-note">
  <strong>Why is this more neutral?</strong> The reasoning happens inside your own AI account: this site never sees your business details and never pre-bakes an answer for you. Every template hard-codes a set of rules — tag claims with evidence levels, strictly separate "verified absent" from "no evidence found", no aggregate scores or rankings; when information is missing the model must not invent facts but first ask you interactive multiple-choice questions, one at a time (one key question per turn, each with lettered options you answer by simply replying with the letter), with different question focuses per template (Oracle hard dependencies for migration assessments, recall and latency for vector DBs, a doctor-like history before diagnosing); and it must not force a comparison across different domains without first confirming what you actually need. One caution: still cross-check the AI's answer against this site's profiles. Models can hallucinate with a straight face.
</div>
"""
    zh_tail = """
<h2>本站内置 AI 功能</h2>
<p>直接在本站内对话的 AI 顾问仍在规划中（当前状态：待接入）。它必须满足：真实大模型调用、每条建议引用本站档案并原样携带证据等级、不确定就明说不知道、不替你做决定、回答可审计。在那之前，请用上面的模板与你自己的 AI 账号完成选型分析。</p>
</section>
"""
    en_tail = """
<h2>Built-in AI on this site</h2>
<p>An AI advisor that chats with you directly on this site is still planned (current status: pending integration). It must meet these bars: real large-model calls, every suggestion citing this site's profiles with evidence levels carried over unchanged, explicit "I don't know" under uncertainty, never deciding for you, and auditable answers. Until then, use the templates above with your own AI account.</p>
</section>
"""
    # 提示词卡片本身已是双语（内含 lang-zh/lang-en），只渲染一次；不要放进 lang_block 导致中英文各重复一份
    body = (lang_block(zh_head + pk_zh, en_head + pk_en)
            + sections_html
            + lang_block(zh_tail, en_tail))
    return page_shell("DB 选型参考 - AI选型", "DB Compare - AI Selection", body, active="advisor")

# 静态资源
# ---------------------------------------------------------------------------

CSS = """/* DB 选型参考站：浅色、干净、中立 */
:root{
  --bg:#f7f8fa; --card:#ffffff; --ink:#1f2430; --muted:#6b7280;
  --line:#e5e7eb; --accent:#1d4ed8; --accent-soft:#eff4ff;
  --green:#15803d; --green-bg:#ecfdf3; --amber:#b45309; --amber-bg:#fffbeb;
  --red:#b91c1c; --red-bg:#fef2f2; --slate:#475569; --slate-bg:#f1f5f9;
  --gray:#6b7280; --gray-bg:#f3f4f6;
  --radius:12px; --max:1180px;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans SC","Source Han Sans SC",system-ui,"Segoe UI",Roboto,sans-serif;
  line-height:1.75;font-size:16px}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.86em;background:var(--slate-bg);padding:.1em .35em;border-radius:6px}
pre{background:#0f172a;color:#e2e8f0;padding:14px 16px;border-radius:10px;overflow:auto;font-size:.85em}
pre code{background:none;padding:0;color:inherit}
blockquote{border-left:4px solid var(--line);margin:1em 0;padding:.4em 1em;color:var(--muted);background:var(--card);border-radius:0 8px 8px 0}
hr{border:none;border-top:1px solid var(--line);margin:1.6em 0}

/* 顶栏 */
.topbar{background:var(--card);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:50}
.topbar-inner{max-width:var(--max);margin:0 auto;padding:0 20px;height:60px;display:flex;align-items:center;gap:24px}
.brand{font-weight:800;font-size:18px;color:var(--ink);white-space:nowrap}
.brand:hover{text-decoration:none}
.brand-mark{color:var(--accent)}
.mainnav{display:flex;gap:4px;flex:1}
.mainnav a{color:var(--muted);padding:8px 14px;border-radius:8px;font-size:15px}
.mainnav a:hover{background:var(--accent-soft);color:var(--accent);text-decoration:none}
.mainnav a.active{color:var(--accent);font-weight:700;background:var(--accent-soft)}
.nav-select{display:none}
.lang-btn{margin-left:auto;border:1px solid var(--line);background:var(--card);border-radius:999px;padding:7px 18px;font-size:14px;cursor:pointer;color:var(--ink)}
.lang-btn:hover{border-color:var(--accent);color:var(--accent)}
.page{max-width:var(--max);margin:0 auto;padding:28px 20px 60px}
.footer{border-top:1px solid var(--line);background:var(--card);color:var(--muted);font-size:13px;text-align:center;padding:18px 20px}

/* hero */
.hero{text-align:center;padding:36px 10px 10px}
.hero h1{font-size:34px;margin:.2em 0;letter-spacing:.02em}
.hero-slim h1{font-size:28px}
.hero-sub{font-size:17px;color:var(--muted)}
.hero-note{font-size:14px;color:var(--muted);max-width:760px;margin:0 auto}
.disclaimer{background:#fffbeb;border:1px solid #fde68a;border-radius:var(--radius);padding:14px 18px;margin:18px auto;max-width:900px;font-size:15px;text-align:left}

/* 场景案例库入口 */
.cases-cta{max-width:900px;margin:22px auto 0;text-align:center}
.cases-cta a{display:inline-block;border:1px solid #bfdbfe;background:#eff6ff;border-radius:999px;padding:10px 26px;font-size:15px;color:#1d4ed8;text-decoration:none}
.cases-cta a:hover{background:#dbeafe}

/* 客户经验卡片 */
.fav-list{display:grid;gap:18px}
.fav-card{border:1px solid var(--line);border-radius:var(--radius);background:var(--card);padding:18px 20px;overflow-wrap:anywhere}
.fav-card h3{margin:0 0 12px;font-size:18px}
.fav-tag{display:inline-block;font-size:12px;font-weight:700;border-radius:999px;padding:2px 10px;margin-right:8px;vertical-align:2px}
.fav-tag-kernel .fav-tag{background:#dbeafe;color:#1d4ed8}
.fav-tag-eco .fav-tag{background:#dcfce7;color:#15803d}
.fav-tag-policy .fav-tag{background:#e0e7ff;color:#4338ca}
.fav-tag-pitfall .fav-tag{background:#ffedd5;color:#c2410c}
.fav-tag-pitfall{border-color:#fdba74}
.fav-fields{margin:0;display:grid;gap:10px}
.fav-field{display:grid;grid-template-columns:110px 1fr;gap:12px}
.fav-field dt{font-weight:700;font-size:14px;color:var(--muted)}
.fav-field dd{margin:0;font-size:15px;line-height:1.65}
.disclaimer-bar{background:#fffbeb;border:1px solid #fde68a;border-radius:var(--radius);padding:12px 16px;font-size:14px;margin-bottom:4px}

/* 场景案例库 */
.case-intro{max-width:900px;margin:6px auto 0;color:var(--muted);font-size:15px}
.case-filters{max-width:1000px;margin:18px auto}
.case-filter-row{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin:8px 0}
/* 多维筛选（电影网站式） */
.cf-row{display:flex;gap:10px;margin:10px 0;align-items:flex-start}
.cf-label{flex:0 0 56px;font-size:14px;font-weight:700;color:var(--muted);padding-top:7px;text-align:right}
.cf-chips{display:flex;gap:8px;flex-wrap:wrap;flex:1}
.cf-chips-col{flex:1;display:flex;flex-direction:column;gap:8px}
.cf-dbgroup{display:flex;gap:10px;align-items:flex-start;flex-wrap:wrap}
.cf-dbgroup-label{flex:0 0 auto;font-size:12px;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:3px 10px;margin-top:4px;white-space:nowrap}
.cf-dbgroup .cf-chips{flex:1}
.cf-n{font-style:normal;font-size:11px;background:#e2e8f0;color:#475569;border-radius:999px;padding:0 7px;margin-left:6px;line-height:18px}
.chip.on .cf-n{background:rgba(255,255,255,.25);color:#fff}
.cf-search{flex:1;max-width:420px;border:1px solid var(--line);border-radius:999px;padding:7px 16px;font-size:14px;background:var(--card);color:var(--ink)}
.cf-active{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:12px 0;padding:10px 14px;background:#f8fafc;border:1px dashed var(--line);border-radius:var(--radius);font-size:13px}
.cf-active-label{color:var(--muted);font-weight:700}
.cf-pill{border:1px solid var(--line);background:#fff;border-radius:999px;padding:3px 8px 3px 12px;font-size:13px;cursor:pointer;color:var(--ink)}
.cf-pill b{margin-left:6px;color:#94a3b8;font-weight:400}
.cf-pill:hover b{color:#dc2626}
.cf-clear{border:none;background:none;color:#2563eb;font-size:13px;cursor:pointer;padding:3px 8px}
.case-empty{max-width:1000px;margin:24px auto;text-align:center;color:var(--muted);font-size:15px;padding:32px 0}
/* 案例来源引用列表 */
.case-refs{margin-top:14px;border-top:1px solid var(--line);padding-top:10px}
.case-refs-title{font-size:13px;font-weight:700;color:var(--muted);margin-bottom:6px}
.case-refs ol{margin:0;padding-left:22px;font-size:13px;color:var(--muted);display:grid;gap:4px}
.case-refs a{color:#2563eb;word-break:break-all}
.chip{border:1px solid var(--line);background:var(--card);border-radius:999px;padding:6px 16px;font-size:14px;cursor:pointer;color:var(--ink)}
.chip.on{background:var(--ink);color:#fff;border-color:var(--ink)}
.case-count{text-align:center;color:var(--muted);font-size:14px}
.case-list{display:grid;gap:20px;max-width:1000px;margin:0 auto}
.case-card{border:1px solid var(--line);border-radius:var(--radius);background:var(--card);padding:20px 22px;overflow-wrap:anywhere}
.case-card h3{margin:0 0 10px;font-size:19px}
.case-type{display:inline-block;font-size:12px;font-weight:700;border-radius:999px;padding:2px 10px;margin-left:8px;vertical-align:2px}
.case-anti .case-type{background:#fee2e2;color:#b91c1c}
.case-pro .case-type{background:#dcfce7;color:#15803d}
.case-tags{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}
.case-tag{font-size:12px;background:#f1f5f9;color:#475569;border-radius:999px;padding:2px 10px}
.case-fields{margin:0;display:grid;gap:10px}
.case-field{display:grid;grid-template-columns:96px minmax(0,1fr);gap:12px}
.case-field dt{font-weight:700;font-size:14px;color:var(--muted)}
.case-field dd{margin:0;font-size:15px;line-height:1.65}
.case-meta{font-size:14px;color:var(--muted);margin:14px 0 0}
.case-meta a{color:#1d4ed8}
.case-verify{margin-left:12px;font-size:13px}

/* 筛选与卡片 */
.filter-bar{display:flex;gap:10px;justify-content:center;margin:26px 0;flex-wrap:wrap}
.filter-btn{border:1px solid var(--line);background:var(--card);border-radius:999px;padding:8px 20px;font-size:15px;cursor:pointer;color:var(--ink)}
.filter-btn b{font-weight:700;color:var(--muted);margin-left:4px;font-size:13px}
.filter-btn.active{background:var(--ink);color:#fff;border-color:var(--ink)}
.filter-btn.active b{color:#cbd5e1}
.card-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:20px;display:flex;flex-direction:column;gap:10px;transition:box-shadow .15s}
.card:hover{box-shadow:0 6px 24px rgba(15,23,42,.08)}
.card h3{margin:0;font-size:20px}
.card-one{color:var(--muted);font-size:14.5px;margin:0;flex:1}
.card-link{font-size:14px;font-weight:600}
.cat{display:inline-block;font-size:12px;font-weight:700;border-radius:999px;padding:3px 12px;letter-spacing:.03em}
.cat-oltp{background:#e0edff;color:#1d4ed8}
.cat-kvdoc{background:#fef3c7;color:#b45309}
.cat-olap{background:#e8f7ee;color:#15803d}
.cat-aidb{background:#f3e8ff;color:#7c3aed}
.domain-h{font-size:21px;margin:28px 0 14px;display:flex;align-items:center;gap:10px}
.domain-sec:first-of-type .domain-h{margin-top:6px}
.domain-n{font-size:13px;color:var(--muted);font-weight:600}
.cmp-toolbar{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin:14px 0 4px}
.cmp-filter-bar{display:flex;gap:8px;flex-wrap:wrap;margin:0}
.copy-btn{flex:none;border:1px solid var(--line);background:#fff;border-radius:999px;padding:6px 16px;font-size:13.5px;cursor:pointer;color:var(--ink);white-space:nowrap}
.copy-btn:hover{border-color:var(--accent);color:var(--accent)}
.cmp-result-bar{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin:8px 0 6px}
.cmp-result-actions{display:flex;gap:8px;flex-wrap:wrap}
.cmp-visible-count{color:var(--muted);font-size:13px}
.cmp-filter-btn{border:1px solid var(--line);background:#fff;border-radius:999px;padding:6px 16px;font-size:14px;cursor:pointer;color:var(--ink)}
.cmp-filter-btn.active{background:var(--ink);color:#fff;border-color:var(--ink)}

.tag{display:inline-block;font-size:12px;color:var(--muted);background:var(--slate-bg);border-radius:6px;padding:2px 8px;margin:0 6px 6px 0}

/* 文档节 */
.doc-section{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:26px 30px;margin:22px 0;overflow-wrap:anywhere}
.doc-section h2{font-size:22px;margin:0 0 14px;padding-bottom:10px;border-bottom:2px solid var(--accent-soft)}
.doc-section h3{font-size:18px;margin:1.4em 0 .6em}
.doc-section h4{font-size:16px;margin:1.2em 0 .5em}
.table-wrap{overflow-x:auto;margin:1em 0}
table{border-collapse:collapse;width:100%;font-size:14.5px;background:#fff}
th,td{border:1px solid var(--line);padding:9px 12px;text-align:left;vertical-align:top}
thead th{background:var(--slate-bg);white-space:nowrap}
tbody tr:nth-child(even){background:#fafbfc}

/* 徽章 */
.ev{display:inline-block;font-size:12px;font-weight:700;border-radius:6px;padding:2px 9px;margin:0 3px;white-space:nowrap;vertical-align:1px}
.ev-official{background:#dbeafe;color:#1d4ed8}
.ev-vendor{background:#ffedd5;color:#c2410c}
.ev-tested{background:#dcfce7;color:#15803d}
.ev-consensus{background:#e0e7ff;color:#4338ca}
.ev-tbd{background:#e5e7eb;color:#4b5563}
.legend{margin:14px 0;font-size:14px;color:var(--muted)}
.legend-label{font-weight:700;color:var(--ink)}

/* 结论色标 */
.verdict{display:inline-block;font-size:12.5px;font-weight:700;border-radius:999px;padding:3px 12px;margin:2px 4px 2px 0;white-space:nowrap}
.v-yes{background:var(--green-bg);color:var(--green)}
.v-partial{background:var(--amber-bg);color:var(--amber)}
.v-no{background:var(--red-bg);color:var(--red)}
.v-neutral{background:var(--slate-bg);color:var(--slate)}
.v-tbd{background:var(--gray-bg);color:var(--gray)}

/* 产品页 */
.profile-hero{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:28px 30px;margin-bottom:8px}
.profile-hero h1{margin:.3em 0;font-size:32px}
.back{font-size:14px}
.meta-row{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:8px 0}
.oneliner{font-size:17px;color:var(--ink);border-left:4px solid var(--accent);padding-left:14px;margin:14px 0 4px}
.dim-item{border:1px solid var(--line);border-radius:10px;padding:16px 20px;margin:14px 0;background:#fff}
.dim-item h3{margin:0 0 8px;font-size:17px}
.dim-num{display:inline-block;min-width:26px;height:26px;line-height:26px;text-align:center;background:var(--ink);color:#fff;border-radius:8px;font-size:13px;margin-right:8px}
.dim-body{font-size:15px}
.dim-body p{margin:.5em 0}
.dim-extra{border-style:dashed}
.dim-missing{color:var(--muted);font-style:italic}
.fallback-note{background:var(--amber-bg);border:1px solid #fde68a;border-radius:10px;padding:12px 18px;margin:14px 0}

/* 对比表 */
.cmp-wrap{border:1px solid var(--line);border-radius:var(--radius);background:#fff;max-height:78vh;overflow:auto}
.cmp-table{font-size:13.5px;min-width:2800px}
.cmp-table thead th{position:sticky;top:0;z-index:5;background:var(--slate-bg);vertical-align:bottom;min-width:180px;max-width:220px}
.cmp-table .row-head{position:sticky;left:0;z-index:6;background:#fff;min-width:170px;max-width:200px;box-shadow:1px 0 0 var(--line)}
.cmp-table thead .row-head{z-index:7;background:var(--slate-bg)}
.dim-h-zh{display:block;font-size:13.5px}
.dim-h-en{display:block;font-weight:400;font-size:11.5px;color:var(--muted)}
html[lang="en"] .dim-h-zh{display:none}
html[lang="en"] .dim-h-en{font-size:13.5px;font-weight:600;color:inherit}
.cmp-cell{vertical-align:top}
.cell-main .snippet{color:var(--muted);font-size:13px;margin:.4em 0;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}
.cmp-cell.expanded .snippet{-webkit-line-clamp:unset}
.cmp-cell .full{margin-top:.5em;border-top:1px dashed var(--line);padding-top:.5em}
.cell-toggle{border:1px solid var(--line);background:#fff;border-radius:6px;font-size:12px;padding:3px 12px;cursor:pointer;color:var(--accent);margin-top:6px}
.cell-toggle:hover{background:var(--accent-soft)}

/* 顾问页 */
.advisor-status{background:var(--amber-bg);border:1px solid #fcd34d;border-radius:10px;padding:14px 18px;margin-bottom:18px;font-size:15px}
.status-dot{display:inline-block;width:10px;height:10px;border-radius:50%;background:var(--amber);margin-right:8px;animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}

@media (max-width:720px){
  .topbar-inner{gap:12px;padding:0 12px}
  .mainnav{display:none}
  .nav-select{display:block;flex:1;min-width:0;max-width:200px;padding:8px 10px;font-size:14px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--text)}
  .page{padding:18px 12px 48px}
  .doc-section,.profile-hero{padding:18px}
  .hero h1{font-size:26px}
}

/* AI选型 */
.howto{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:18px 0 22px}
.howto-step{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.howto-step .n{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:50%;background:var(--accent);color:#fff;font-weight:700;font-size:14px;margin-bottom:8px}
.howto-step h4{margin:0 0 6px;font-size:16px}
.howto-step p{margin:0;font-size:14px;color:var(--muted)}
.neutral-note{background:var(--green-bg);border:1px solid #86efac;border-radius:10px;padding:14px 18px;margin:0 0 26px;font-size:15px}
.prompt-card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin-bottom:18px}
.prompt-card h3{margin:0 0 4px;font-size:18px}
.prompt-use{margin:0 0 12px;color:var(--muted);font-size:14px}
.prompt-text{background:#0f172a;color:#e2e8f0;border-radius:8px;padding:14px 16px;white-space:pre-wrap;word-break:break-word;font-size:13.5px;line-height:1.7;max-height:340px;overflow:auto;margin:0;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.ai-btn-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
.ai-btn{border:1px solid var(--line);background:#fff;border-radius:8px;padding:8px 16px;font-size:14px;cursor:pointer;color:var(--ink)}
.ai-btn:hover{border-color:var(--accent);color:var(--accent);text-decoration:none}
.ai-copy{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600}
.ai-copy:hover{background:#1e40af;border-color:#1e40af;color:#fff}
.ai-dive-row{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:14px}
.ai-dive-label{font-size:14px;color:var(--muted)}
@media (max-width:720px){.howto{grid-template-columns:1fr}}
.pk-row{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:14px 0 4px}
.pk-select{font-size:15px;padding:8px 12px;border:1px solid var(--line);border-radius:8px;background:#fff;max-width:280px}
.pk-vs{font-weight:700;color:var(--muted)}
.subnav{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 22px}
.subnav a{border:1px solid var(--line);background:#fff;border-radius:999px;padding:6px 16px;font-size:14px;color:var(--ink)}
.subnav a:hover{border-color:var(--accent);color:var(--accent);text-decoration:none}
.grp-intro{color:var(--muted);font-size:14.5px;margin:0 0 16px;max-width:960px}



/* 全局对比托盘 */
.cmp-tray{position:relative}
.tray-btn{display:flex;align-items:center;gap:6px;border:1px solid var(--accent);background:var(--accent);color:#fff;border-radius:999px;padding:7px 16px;font-size:14px;font-weight:600;cursor:pointer;white-space:nowrap;box-shadow:0 2px 8px rgba(29,78,216,.28)}
.tray-btn:hover{background:#1e40af;border-color:#1e40af;color:#fff}
.tray-btn .tray-count{font-weight:700;font-size:13px;opacity:.95}
.tray-btn .tray-count i{font-style:normal;color:#fff}
.tray-btn.tray-empty{background:#ea580c;border-color:#ea580c;color:#fff;animation:trayPulse 2.6s ease-in-out infinite}
.tray-btn.tray-empty:hover{background:#c2410c;border-color:#c2410c;color:#fff}
.tray-btn.tray-empty .tray-count{color:#fff}
.tray-btn.tray-empty .tray-count i{color:#fff}
@keyframes trayPulse{0%,100%{box-shadow:0 2px 8px rgba(234,88,12,.35)}50%{box-shadow:0 2px 20px rgba(234,88,12,.65)}}
.tray-panel{position:absolute;right:0;top:calc(100% + 8px);width:340px;max-height:70vh;overflow:auto;background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:0 12px 40px rgba(15,23,42,.14);z-index:100;padding:14px 16px;text-align:left}
.tray-sec{font-size:12px;color:var(--muted);font-weight:700;margin:10px 0 6px}
.tray-sec:first-child{margin-top:0}
.tray-selected{display:flex;flex-wrap:wrap;gap:8px;min-height:28px}
.tray-empty{font-size:13px;color:var(--muted)}
.sel-chip{display:inline-flex;align-items:center;gap:6px;background:var(--accent-soft);color:var(--accent);border-radius:999px;padding:4px 6px 4px 12px;font-size:13px;font-weight:600}
.sel-chip button{border:none;background:none;color:var(--accent);cursor:pointer;font-size:15px;line-height:1;padding:2px 6px;border-radius:50%}
.sel-chip button:hover{background:#dbe7ff}
.tray-list{display:flex;flex-direction:column;gap:10px}
.tray-group-h{font-size:12px;color:var(--muted);font-weight:700;margin-bottom:4px}
.tray-item{display:flex;align-items:center;gap:8px;width:100%;text-align:left;border:1px solid var(--line);background:#fff;border-radius:8px;padding:6px 10px;font-size:13.5px;cursor:pointer;color:var(--ink);margin-bottom:4px}
.tray-item:hover{border-color:var(--accent)}
.tray-item.on{background:var(--accent-soft);border-color:var(--accent);color:var(--accent);font-weight:600}
.tray-item:disabled{opacity:.45;cursor:not-allowed}
.tray-item .tick{width:18px;text-align:center;flex:none}
.tray-clear{border:none;background:none;color:var(--muted);cursor:pointer;font-size:13px}
.tray-clear:hover{color:var(--red)}
.tray-sel-left{display:flex;gap:14px;align-items:center}
.tray-share{border:none;background:none;color:var(--accent);cursor:pointer;font-size:13px}
.tray-share:hover{text-decoration:underline}
.tray-sel-actions{display:flex;justify-content:space-between;align-items:center;margin:10px 0 2px}
.tray-checkout{display:inline-block;background:var(--accent);color:#fff;border:1px solid var(--accent);border-radius:999px;padding:7px 18px;font-size:14px;font-weight:600;text-decoration:none;white-space:nowrap}
.tray-checkout:hover{background:#1e40af;border-color:#1e40af;color:#fff}
/* 加入对比飞行动画 */
.fly-dot{position:fixed;left:0;top:0;z-index:9999;width:18px;height:18px;border-radius:50%;background:#ea580c;box-shadow:0 2px 12px rgba(234,88,12,.55);pointer-events:none}
.tray-btn.tray-pop{animation:trayPop .45s ease}
.tray-btn.tray-empty.tray-pop{animation:trayPop .45s ease,trayPulse 2.6s ease-in-out infinite}
@keyframes trayPop{0%{transform:scale(1)}40%{transform:scale(1.28)}100%{transform:scale(1)}}
/* 加入对比按钮 */
.card-top{display:flex;align-items:center;justify-content:space-between;gap:8px}
.addcmp-btn{border:1px solid var(--line);background:#fff;border-radius:999px;padding:4px 12px;font-size:12.5px;cursor:pointer;color:var(--muted);white-space:nowrap}
.addcmp-btn:hover{border-color:var(--accent);color:var(--accent)}
.addcmp-btn.on{background:var(--accent);border-color:var(--accent);color:#fff}
.ai-dive-row .addcmp-btn{border-radius:8px;padding:8px 16px;font-size:14px}
/* 对比页已选提示条 */
.sel-notice{display:flex;align-items:center;gap:10px;flex-wrap:wrap;background:var(--accent-soft);border:1px solid #c9dbff;border-radius:var(--radius);padding:10px 16px;margin:14px 0 4px;font-size:14px}
.sel-notice b{color:var(--accent)}
.sel-notice button{border:1px solid var(--line);background:#fff;border-radius:999px;padding:4px 14px;font-size:13px;cursor:pointer}
.sel-notice button:hover{border-color:var(--accent);color:var(--accent)}
.cmp-filter-btn.disabled{opacity:.4;cursor:not-allowed}
/* PK 提示 */
.pk-note{background:var(--accent-soft);border:1px solid #c9dbff;border-radius:10px;padding:10px 16px;font-size:14px;margin:12px 0;max-width:900px}
.pk-select.dimmed{opacity:.5}
@media (max-width:720px){
  .topbar-inner{flex-wrap:wrap;height:auto;padding:10px 16px;gap:12px}
  .tray-panel{position:fixed;left:12px;right:12px;top:64px;width:auto;max-height:60vh}
}

"""

# 档案页"用 AI 深挖这款"直接复用"单库深挖"模板的提示词（{{CANDIDATES}} -> {name}，由 aiDeepDive 运行时注入库名），避免两处文案分叉
_DEEPDIVE_TPL = next(t for t in AI_TEMPLATES if t["title_zh"] == "单库深挖")
def _js_sq(s):
    return s.replace("\\", "\\\\").replace("'", "\\'").replace("\r", "").replace("\n", "\\n")
_DIVE_ZH_JS = _js_sq(_DEEPDIVE_TPL["prompt_zh"].replace("{{CANDIDATES}}", "{name}"))
_DIVE_EN_JS = _js_sq(_DEEPDIVE_TPL["prompt_en"].replace("{{CANDIDATES}}", "{name}"))
JS = """(function () {
'use strict';

/* 导航顺序归一化：首页、维度对比、AI选型、场景案例、方法论。同步执行（nav 已解析），老页面无需重推即可收敛，无闪烁 */
(function () {
var nav = document.querySelector('nav.mainnav');
if (!nav) return;
var order = ['index.html', 'compare.html', 'advisor.html', 'cases.html', 'methodology.html'];
var links = nav.querySelectorAll('a'), byHref = {}, i;
for (i = 0; i < links.length; i++) byHref[links[i].getAttribute('href')] = links[i];
for (i = 0; i < order.length; i++) { if (byHref[order[i]]) nav.appendChild(byHref[order[i]]); }
/* 移动端下拉导航：跳转 */
var nsel = document.getElementById('nav-select');
if (nsel) nsel.addEventListener('change', function () { if (nsel.value) location.href = nsel.value; });
})();

/* ---------------- 语言 ---------------- */
var KEY = 'dbcompare-lang';
function getLang() {
var nav = '';
try { nav = (navigator.language || '').toLowerCase(); } catch (e) {}
var dflt = nav.indexOf('zh') === 0 ? 'zh' : 'en';
try { return localStorage.getItem(KEY) || dflt;}
catch (e) { return dflt;}
}
function escHtml(s) {
return String(s).replace(/[&<>"']/g, function (c) {
return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c];
});
}
function paintLabels(lang) {
var lab = document.querySelectorAll('[data-zh]');
for (var k = 0; k < lab.length; k++) {
var el = lab[k];
el.textContent = (lang === 'zh')? el.getAttribute('data-zh'): el.getAttribute('data-en');
}
}

/* ---------------- AI 跳转 / 复制（顶层作用域：PK 按钮与档案页深挖按钮都在 DOMContentLoaded 之外调用） ---------------- */
var AI_URLS = {
chatgpt: 'https://chatgpt.com/?q=',
grok: 'https://grok.com/?q=',
claude: 'https://claude.ai/new?q='
};
function aiOpenService(service, prompt) {
var base = AI_URLS[service];
if (!base ||!prompt) return;
window.open(base + encodeURIComponent(prompt), '_blank', 'noopener');
}
function flashCopy(btn, msg) {
var span = btn.querySelector('span') || btn;
var old = span.textContent;
span.textContent = msg;
setTimeout(function () { span.textContent = old;}, 1200);
}
function copyPromptText(text, btn) {
function done(ok) {
flashCopy(btn, getLang() === 'zh'? (ok? '已复制': '复制失败'): (ok? 'Copied': 'Copy failed'));
}
if (navigator.clipboard && navigator.clipboard.writeText) {
navigator.clipboard.writeText(text).then(function () { done(true);}, function () { done(false);});
} else {
var ta = document.createElement('textarea');
ta.value = text;
ta.style.position = 'fixed';
ta.style.opacity = '0';
document.body.appendChild(ta);
ta.select();
try { document.execCommand('copy'); done(true);}
catch (e) { done(false);}
document.body.removeChild(ta);
}
}
/* 对比页：一键复制当前可见对比结果为 Markdown（尊重领域/已选筛选与当前语言） */
function htmlToPlain(root) {
var out = [];
function walk(n) {
if (n.nodeType === 3) { out.push(n.nodeValue); return;}
if (n.nodeType !== 1) return;
var tag = n.tagName.toLowerCase(), i;
if (tag === 'br') { out.push('\\n'); return;}
if (tag === 'li') out.push('- ');
for (i = 0; i < n.childNodes.length; i++) walk(n.childNodes[i]);
if (tag === 'p' || tag === 'div' || tag === 'li' ||
tag === 'h1' || tag === 'h2' || tag === 'h3' || tag === 'h4' || tag === 'tr') out.push('\\n');
}
walk(root);
return out.join('').replace(/[ \t\xa0　]+/g, ' ').replace(/ *\\n */g, '\\n').replace(/\\n{3,}/g, '\\n\\n');
}
function cmpCellText(cell, lang) {
var blk = cell.querySelector('.lang-block.lang-' + lang);
if (!blk) return {verdict: '', body: ''};
var v = blk.querySelector('.verdict');
var verdict = v? v.textContent.trim(): '';
var full = blk.querySelector('.full'), src;
if (full && full.innerHTML.trim()) {
src = full.cloneNode(true);
} else {
src = document.createElement('div');
var sn = blk.querySelector('.snippet');
if (sn) src.appendChild(sn.cloneNode(true));
}
var chips = src.querySelectorAll('.verdict'), i;
for (i = 0; i < chips.length; i++) chips[i].parentNode.removeChild(chips[i]);
return {verdict: verdict, body: htmlToPlain(src).trim()};
}
function buildCompareMarkdown() {
var lang = getLang(), zh = lang === 'zh', i, r;
var rows = [], all = document.querySelectorAll('.cmp-table > tbody > tr');
for (i = 0; i < all.length; i++) if (all[i].style.display !== 'none') rows.push(all[i]);
var ths = document.querySelectorAll('.cmp-table > thead th'), dims = [];
for (i = 1; i < ths.length; i++) {
var ds = ths[i].querySelector(zh? '.dim-h-zh': '.dim-h-en');
dims.push(ds? ds.textContent.trim(): ths[i].textContent.trim());
}
var names = rows.map(function (row) {
var s = row.querySelector('.row-head [data-zh]');
return s? (zh? s.getAttribute('data-zh'): s.getAttribute('data-en')): '';
});
var dt = new Date();
var dstr = dt.getFullYear() + '-' + ('0' + (dt.getMonth() + 1)).slice(-2) + '-' + ('0' + dt.getDate()).slice(-2);
var L = [];
L.push(zh? '# 数据库维度对比': '# Database Comparison');
L.push('> ' + (zh? '产品': 'Products') + '：' + names.join(zh? '、': ', ') +
'（' + rows.length + (zh? ' 款': ' products') + '）｜' +
(zh? '维度': 'Dimensions') + '：' + dims.length + '｜' +
(zh? '导出': 'Exported') + '：' + dstr);
L.push('> ' + (zh? '来源 db-compare-site；本对比不做综合总分、不做排名。'
: 'Source: db-compare-site; no aggregate scores, no rankings.'));
L.push('');
for (i = 0; i < dims.length; i++) {
L.push('## ' + (i + 1) + '. ' + dims[i]);
L.push('');
for (r = 0; r < rows.length; r++) {
var cells = rows[r].querySelectorAll('td.cmp-cell');
if (i >= cells.length) continue;
var cm = cmpCellText(cells[i], lang);
L.push('**' + names[r] + '**' + (cm.verdict? ' —— ' + cm.verdict: ''));
if (cm.body) L.push(cm.body);
L.push('');
}
}
return L.join('\\n').replace(/\\n{3,}/g, '\\n\\n').trim() + '\\n';
}
function cardPromptText(card) {
var pre = card.querySelector('.prompt-text.lang-' + getLang());
if (!pre) pre = card.querySelector('.prompt-text');
return pre? pre.textContent: '';
}

/* ---------------- 全局对比选型：顶栏托盘，跨页持久（localStorage），最多 4 款 ---------------- */
var SEL_KEY = 'dbcompare-selection';
var MAX_SEL = 4;
function catalog() { return window.DB_CATALOG || [];}
function prodName(slug) {
var c = catalog();
for (var i = 0; i < c.length; i++) if (c[i].slug === slug) return getLang() === 'zh'? c[i].name: (c[i].name_en || c[i].name);
return slug;
}
function getSelection() {
var out = [];
try {
var raw = localStorage.getItem(SEL_KEY);
var arr = raw? JSON.parse(raw): [];
var ok = {}, c = catalog(), i, j;
for (i = 0; i < c.length; i++) ok[c[i].slug] = 1;
for (j = 0; j < arr.length && out.length < MAX_SEL; j++) {
if (ok[arr[j]] && out.indexOf(arr[j]) < 0) out.push(arr[j]);
}
} catch (e) {}
return out;
}
function selNames() {
var s = getSelection(), r = [], i;
for (i = 0; i < s.length; i++) r.push(prodName(s[i]));
return r;
}
function toggleSelect(slug) {
var sel = getSelection();
var i = sel.indexOf(slug);
if (i >= 0) { sel.splice(i, 1);}
else {
if (sel.length >= MAX_SEL) return 'full';
sel.push(slug);
}
try { localStorage.setItem(SEL_KEY, JSON.stringify(sel));} catch (e) {}
applySelection();
return 'ok';
}
function clearSelection() {
try { localStorage.removeItem(SEL_KEY);} catch (e) {}
var _nb = document.getElementById('cmp-sel-names');
if (_nb) _nb.textContent = '';
applySelection();
}

function renderTray() {
var lang = getLang(), sel = getSelection(), i, k;
var count = document.getElementById('cmp-count');
if (count) count.textContent = sel.length;
var trayBtn = document.getElementById('cmp-tray-btn');
if (trayBtn) trayBtn.classList.toggle('tray-empty', sel.length === 0);
var box = document.getElementById('cmp-selected');
if (box) {
if (!sel.length) {
box.innerHTML = '<span class="tray-empty" data-zh="还没选，去点卡片上的「＋ 对比」" data-en="Nothing yet — hit “+ Compare” on a card"></span>';
} else {
var h = '';
for (i = 0; i < sel.length; i++) {
h += '<span class="sel-chip">' + escHtml(prodName(sel[i])) +
'<button type="button" data-unsel="' + sel[i] + '" aria-label="remove">×</button></span>';
}
box.innerHTML = h;
}
}
var list = document.getElementById('cmp-list');
if (list) {
var domains = window.DB_DOMAINS || {};
var order = ['oltp', 'kvdoc', 'olap', 'aidb'];
var c = catalog(), h2 = '';
for (var d = 0; d < order.length; d++) {
var dk = order[d];
var dn = domains[dk]? (lang === 'zh'? domains[dk].zh: domains[dk].en): dk;
var items = '';
for (k = 0; k < c.length; k++) {
var _dm = c[k].domains || [c[k].domain];
if (_dm.indexOf(dk) < 0) continue;
var on = sel.indexOf(c[k].slug) >= 0;
var dis = (!on && sel.length >= MAX_SEL)? ' disabled': '';
items += '<button type="button" class="tray-item' + (on? ' on': '') +
'" data-sel-toggle="' + c[k].slug + '"' + dis + '>' +
'<span class="tick">' + (on? '✓': '＋') + '</span>' + escHtml(c[k].name) + '</button>';
}
if (items) h2 += '<div class="tray-group"><div class="tray-group-h">' + escHtml(dn) + '</div>' + items + '</div>';
}
list.innerHTML = h2;
}
paintLabels(lang);
var coBar = document.getElementById('cmp-sel-actions');
if (coBar) {
coBar.hidden = sel.length === 0;
var coLab = document.getElementById('cmp-checkout-label');
if (coLab) coLab.textContent = (lang === 'zh'? '去对比（' + sel.length + ' 款）→': 'Compare (' + sel.length + ') →');
var coLink = document.getElementById('cmp-checkout');
if (coLink) coLink.href = 'compare.html?sel=' + sel.join(',');
}
}

function paintAddCmpButtons() {
var lang = getLang(), sel = getSelection();
var btns = document.querySelectorAll('[data-addcmp]');
for (var i = 0; i < btns.length; i++) {
var on = sel.indexOf(btns[i].getAttribute('data-addcmp')) >= 0;
btns[i].classList.toggle('on', on);
var lab = btns[i].querySelector('.addcmp-label');
if (lab) lab.textContent = on
? (lang === 'zh'? '✓ 已选': '✓ Selected')
: (lang === 'zh'? '＋ 对比': '＋ Compare');
}
}

/* 加入对比：飞入托盘动画（电商加购风格），落袋后才真正选中 */
var _flying = {};
function flyToTray(fromEl, done) {
var trayBtn = document.getElementById('cmp-tray-btn');
if (!trayBtn || !fromEl || window.matchMedia('(prefers-reduced-motion: reduce)').matches) { done(); return;}
var r1 = fromEl.getBoundingClientRect(), r2 = trayBtn.getBoundingClientRect();
var x0 = r1.left + r1.width / 2, y0 = r1.top + r1.height / 2;
var x1 = r2.left + r2.width / 2, y1 = r2.top + r2.height / 2;
var dot = document.createElement('div');
dot.className = 'fly-dot';
dot.style.transform = 'translate(' + x0 + 'px,' + y0 + 'px) translate(-50%,-50%)';
document.body.appendChild(dot);
var dur = 620, t0 = null;
function frame(ts) {
if (!t0) t0 = ts;
var t = Math.min(1, (ts - t0) / dur);
var x = x0 + (x1 - x0) * t;
var y = y0 + (y1 - y0) * t - Math.sin(t * Math.PI) * 110;
var s = 1 - .55 * t;
dot.style.transform = 'translate(' + x + 'px,' + y + 'px) translate(-50%,-50%) scale(' + s + ')';
dot.style.opacity = String(1 - .25 * t);
if (t < 1) requestAnimationFrame(frame);
else { dot.remove(); popTray(); done();}
}
requestAnimationFrame(frame);
}
function popTray() {
var b = document.getElementById('cmp-tray-btn');
if (!b) return;
b.classList.remove('tray-pop');
void b.offsetWidth;
b.classList.add('tray-pop');
setTimeout(function () { b.classList.remove('tray-pop');}, 500);
}

/* 对比页：有选择时只显示已选产品行，并禁用领域筛选 */
var cmpDomain = 'all';
/* 对比页：表格上方工具条的可见数量提示（复制范围 = 当前可见行 × 维度） */
/* URL 分享：?sel=slug1,slug2 —— 打开时校验后覆盖本地选择（?sel= 空值=清空） */
function applySelFromUrl() {
var m = /[?&]sel=([^&#]*)/.exec(window.location.search || '');
if (!m) return;
var valid = {}, c = catalog(), i;
for (i = 0; i < c.length; i++) valid[c[i].slug] = 1;
var raw = m[1];
try { raw = decodeURIComponent(raw.replace(/\+/g, ' ')); } catch (e) {}
var out = [], seen = {}, s, parts = raw.split(',');
for (i = 0; i < parts.length && out.length < MAX_SEL; i++) {
s = parts[i].trim().toLowerCase();
if (s && valid[s] && !seen[s]) { seen[s] = 1; out.push(s); }
}
try { localStorage.setItem(SEL_KEY, JSON.stringify(out)); } catch (e2) {}
}
function buildShareUrl() {
var base = (window.location.href || '').split('#')[0].split('?')[0];
return base + '?sel=' + getSelection().join(',');
}
function shareSelection(btn) {
var lang = getLang(), sel = getSelection();
if (!sel.length) {
flashCopy(btn, lang === 'zh'? '先选几款数据库': 'Select databases first');
return;
}
copyPromptText(buildShareUrl(), btn);
}
function updateCmpCount() {
var el = document.getElementById('cmp-visible-count');
if (!el) return;
var rows = document.querySelectorAll('.cmp-table > tbody > tr'), n = 0, i;
for (i = 0; i < rows.length; i++) if (rows[i].style.display !== 'none') n++;
var ths = document.querySelectorAll('.cmp-table > thead th');
var dims = ths.length > 0 ? ths.length - 1 : 0;
el.textContent = getLang() === 'zh'
? '当前可见：' + n + ' 款 × ' + dims + ' 维'
: 'Showing: ' + n + ' products × ' + dims + ' dimensions';
}
function applyCompareFilter() {
var rows = document.querySelectorAll('.cmp-table > tbody > tr');
if (!rows.length) return;
var sel = getSelection(), i, r;
var fbtns = document.querySelectorAll('.cmp-filter-btn');
var notice = document.getElementById('cmp-sel-notice');
if (sel.length) {
for (r = 0; r < rows.length; r++) {
rows[r].style.display = (sel.indexOf(rows[r].getAttribute('data-slug')) >= 0)? '': 'none';
}
for (i = 0; i < fbtns.length; i++) {
fbtns[i].classList.add('disabled');
fbtns[i].setAttribute('disabled', 'disabled');
}
if (notice) {
notice.hidden = false;
var nb = document.getElementById('cmp-sel-names');
if (nb) nb.textContent = selNames().join(getLang() === 'zh'? '、': ', ');
}
} else {
for (i = 0; i < fbtns.length; i++) {
fbtns[i].classList.remove('disabled');
fbtns[i].removeAttribute('disabled');
}
for (r = 0; r < rows.length; r++) {
var _dd = (rows[r].getAttribute('data-domains') || '').split(' ');
rows[r].style.display = (cmpDomain === 'all' || _dd.indexOf(cmpDomain) >= 0)? '': 'none';
}
if (notice) notice.hidden = true;
}
updateCmpCount();
}

/* PK 下拉框：中英文各一对，按当前语言取可见的那对 */
function pkSelects() {
var en = getLang() !== 'zh';
return [document.getElementById(en? 'pk-a-en': 'pk-a'), document.getElementById(en? 'pk-b-en': 'pk-b')];
}
function pkNoteEl() {
return document.getElementById(getLang() !== 'zh'? 'pk-note-en': 'pk-note');
}
/* AI 选型页 PK 区：选了 ≥2 款就用已选库，否则用下拉框 */
function paintPkNote() {
var note = pkNoteEl();
var _pp = pkSelects(), sa = _pp[0], sb = _pp[1];
if (!note ||!sa ||!sb) return;
var sel = getSelection(), lang = getLang();
if (sel.length >= 2) {
sa.disabled = true; sb.disabled = true;
sa.classList.add('dimmed'); sb.classList.add('dimmed');
var names = selNames().join(lang === 'zh'? '、': ', ');
note.hidden = false;
note.textContent = lang === 'zh'
? '已选 ' + sel.length + ' 款（' + names + '），下面按钮将直接用它们生成对比提示词；清空选择可恢复手动下拉框。'
: sel.length + ' selected (' + names + '). The buttons below will generate the comparison prompt from them; clear the selection to use the dropdowns again.';
} else {
sa.disabled = false; sb.disabled = false;
sa.classList.remove('dimmed'); sb.classList.remove('dimmed');
note.hidden = true;
note.textContent = '';
}
}

/* 提示词特化：把 {{CANDIDATES}} 替换为已选库名（无选择时显示通用填写提示） */
function specializePrompts() {
var lang = getLang(), sel = getSelection(), names = selNames();
var cards = document.querySelectorAll('.prompt-card[data-cand]');
for (var i = 0; i < cards.length; i++) {
var card = cards[i];
var mode = card.getAttribute('data-cand');
var hint = card.getAttribute(lang === 'zh'? 'data-hint-zh': 'data-hint-en') || '';
var repl;
if (mode === 'single') {
repl = (sel.length === 1)? (''): hint;
} else if (mode === 'first') {
repl = sel.length? names[0]: hint;
} else {
repl = sel.length? names.join(lang === 'zh'? '、': ', '): hint;
}
var pres = card.querySelectorAll('.prompt-text');
for (var j = 0; j < pres.length; j++) {
var pre = pres[j];
if (pre._raw === undefined) pre._raw = pre.textContent;
if (pre._raw.indexOf('{{CANDIDATES}}') >= 0) {
pre.textContent = pre._raw.split('{{CANDIDATES}}').join(repl);
}
}
}
}

function refreshDynamicText() {
renderTray();
paintAddCmpButtons();
paintPkNote();
specializePrompts();
updateCmpCount();
}
function applySelection() {
renderTray();
applyCompareFilter();
paintPkNote();
specializePrompts();
paintAddCmpButtons();
}

function apply(lang) {
document.documentElement.setAttribute('lang', lang === 'zh'? 'zh-CN': 'en');
var _t = document.querySelector('title[data-title-en]');
if (_t) document.title = lang === 'zh'? _t.getAttribute('data-title-zh'): _t.getAttribute('data-title-en');
var zhEls = document.querySelectorAll('.lang-zh');
for (var i = 0; i < zhEls.length; i++) zhEls[i].hidden = (lang!== 'zh');
var enEls = document.querySelectorAll('.lang-en');
for (var i = 0; i < enEls.length; i++) enEls[i].hidden = (lang!== 'en');
paintLabels(lang);
var btn = document.getElementById('lang-toggle');
if (btn) btn.textContent = (lang === 'zh')? 'EN': '中文';
try { localStorage.setItem(KEY, lang);} catch (e) {}
refreshDynamicText();
}

/* 多库 PK 提示词（N = 2/3/4）；无选择时走下拉框的旧模板 */
var PK_ZH = '你是一名中立的数据库架构顾问，不代表任何厂商。请基于公开资料，对{a}和{b}做一次双库 PK 对比。输出要求：1. 按这 47 个维度逐项对比：静态加密 / TDE、TLS / 传输加密、审计、认证与权限、备份恢复、可观测性、连接模型、事务与隔离级别、复制与一致性、扩展方式、兼容性、许可证与商业模式、中文资料丰富度、性能与延迟特征、合规与认证、成熟度与社区生态、标杆用户、生态工具链、云托管与 Serverless、数据接入与摄入、外部数据访问、CDC 与下游同步、TTL 与数据生命周期管理、在线 DDL 与 Schema 演进、多租户与资源隔离、跨地域多活、高可用架构与 RTO/RPO、行级安全与数据脱敏、JSON 与半结构化能力、全文检索能力、存储效率与压缩、开源协议与厂商锁定风险、查询优化器与计划稳定性、参数调优与自治能力、静默数据损坏防护、存储过程/触发器/过程语言、约束与数据完整性、分析 SQL 完备性、被遗忘权与数据擦除、数据血缘与目录集成、存算分离 vs 存算一体、多模能力、FinOps 成本可观测性、驱动与多语言生态、物化视图、支持跨云、热点数据更新能力。2. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；严格区分"查证为无"和"未找到证据"，不要把没查到的写成不支持。3. 每款给出：最适合的场景、最可能踩的三个坑（从机制层面解释，并说明在什么负载或故障下会触发）。4. 不做综合总分、不排名，只给带条件的判断，格式为"如果……那么……"。5. 需要我的业务场景信息才能下结论时，主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。如果候选库属于不同领域（如 OLTP 与向量库），不要硬对比：先交互式逐题确认我的真实诉求与对比口径（每题给出带字母编号的选项，我只需回复字母即可作答），再决定是对比还是纠正选型方向。6. 用中文回答。（建议：把本站这两款产品的档案页内容贴在下面，作为分析的起点）';
var PK_EN = 'You are a neutral database architecture advisor, not affiliated with any vendor. Do a head-to-head comparison of {a} vs {b} based on public information. Requirements: 1. Compare dimension by dimension across these 47 dimensions: data-at-rest encryption / TDE, TLS / transport encryption, auditing, authentication & authorization, backup & recovery, observability, connection model, transactions & isolation levels, replication & consistency, scaling, compatibility, license & business model, Chinese-language resources, performance & latency, compliance & certifications, maturity & community, notable adopters, ecosystem tooling, managed & serverless, data ingestion, external data access, CDC & downstream, TTL & data lifecycle, online DDL & schema evolution, multi-tenancy & resource isolation, cross-region active-active, HA & RTO/RPO, row-level security & masking, JSON & semi-structured, full-text search, storage efficiency & compression, OSS license & lock-in risk, optimizer & plan stability, tuning & autonomy, silent corruption protection, stored procedures & triggers, constraints & integrity, analytical SQL, right to erasure, data lineage & catalog, storage-compute architecture, multi-model, FinOps & cost observability, drivers & clients, materialized views, multi-cloud support, hotspot update handling. 2. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified; strictly distinguish "verified absent" from "no evidence found". 3. For each: best-fit scenarios and the three most likely production pitfalls, explained at the mechanism level with trigger conditions. 4. No aggregate total score and no ranking; conditional verdicts only, in "if..., then..." form. 5. When you need my scenario details for a conclusion, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts. If the candidates belong to different domains (e.g. OLTP vs vector DB), do not force a comparison: first interactively confirm what I actually need and the right basis of comparison, one question at a time with lettered options I can answer by replying with the letter, then decide whether to compare or to correct the selection direction. 6. Answer in English. (Tip: paste the profile pages on this site for both products below as a starting point.)';
function pkPromptN(lang, names) {
var n = names.length, i, list = '', sep = (lang === 'zh')? '、': ', ';
for (i = 0; i < n; i++) list += (i? sep: '') + names[i];
if (lang === 'zh') {
var kind = n === 2? '双库 PK': n + ' 库';
return '你是一名中立的数据库架构顾问，不代表任何厂商。请基于公开资料，对' + list + '做一次' + kind + '对比。' +
'输出要求：1. 按这 47 个维度逐项对比：静态加密 / TDE、TLS / 传输加密、审计、认证与权限、备份恢复、可观测性、连接模型、事务与隔离级别、复制与一致性、扩展方式、兼容性、许可证与商业模式、中文资料丰富度、性能与延迟特征、合规与认证、成熟度与社区生态、标杆用户、生态工具链、云托管与 Serverless、数据接入与摄入、外部数据访问、CDC 与下游同步、TTL 与数据生命周期管理、在线 DDL 与 Schema 演进、多租户与资源隔离、跨地域多活、高可用架构与 RTO/RPO、行级安全与数据脱敏、JSON 与半结构化能力、全文检索能力、存储效率与压缩、开源协议与厂商锁定风险、查询优化器与计划稳定性、参数调优与自治能力、静默数据损坏防护、存储过程/触发器/过程语言、约束与数据完整性、分析 SQL 完备性、被遗忘权与数据擦除、数据血缘与目录集成、存算分离 vs 存算一体、多模能力、FinOps 成本可观测性、驱动与多语言生态、物化视图、支持跨云、热点数据更新能力。' +
'2. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；严格区分"查证为无"和"未找到证据"，不要把没查到的写成不支持。' +
'3. 每款给出：最适合的场景、最可能踩的三个坑（从机制层面解释，并说明在什么负载或故障下会触发）。' +
'4. 不做综合总分、不排名，只给带条件的判断，格式为"如果……那么……"。' +
'5. 需要我的业务场景信息才能下结论时，主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。如果候选库属于不同领域（如 OLTP 与向量库），不要硬对比：先交互式逐题确认我的真实诉求与对比口径（每题给出带字母编号的选项，我只需回复字母即可作答），再决定是对比还是纠正选型方向。6. 用中文回答。' +
'（建议：把本站这几款产品的档案页内容贴在下面，作为分析的起点）';
}
var kindEn = n === 2? 'head-to-head': n + '-way';
return 'You are a neutral database architecture advisor, not affiliated with any vendor. Do a ' + kindEn + ' comparison of ' + list + ' based on public information. ' +
'Requirements: 1. Compare dimension by dimension across these 47 dimensions: data-at-rest encryption / TDE, TLS / transport encryption, auditing, authentication & authorization, backup & recovery, observability, connection model, transactions & isolation levels, replication & consistency, scaling, compatibility, license & business model, Chinese-language resources, performance & latency, compliance & certifications, maturity & community, notable adopters, ecosystem tooling, managed & serverless, data ingestion, external data access, CDC & downstream, TTL & data lifecycle, online DDL & schema evolution, multi-tenancy & resource isolation, cross-region active-active, HA & RTO/RPO, row-level security & masking, JSON & semi-structured, full-text search, storage efficiency & compression, OSS license & lock-in risk, optimizer & plan stability, tuning & autonomy, silent corruption protection, stored procedures & triggers, constraints & integrity, analytical SQL, right to erasure, data lineage & catalog, storage-compute architecture, multi-model, FinOps & cost observability, drivers & clients, materialized views, multi-cloud support, hotspot update handling. ' +
'2. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified; strictly distinguish "verified absent" from "no evidence found". ' +
'3. For each: best-fit scenarios and the three most likely production pitfalls, explained at the mechanism level with trigger conditions. ' +
'4. No aggregate total score and no ranking; conditional verdicts only, in "if..., then..." form. ' +
'5. When you need my scenario details for a conclusion, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts. If the candidates belong to different domains (e.g. OLTP vs vector DB), do not force a comparison: first interactively confirm what I actually need and the right basis of comparison, one question at a time with lettered options I can answer by replying with the letter, then decide whether to compare or to correct the selection direction. 6. Answer in English. ' +
'(Tip: paste the profile pages on this site for these products below as a starting point.)';
}

/* ---------------- 事件绑定 ---------------- */
document.addEventListener('DOMContentLoaded', function () {
apply(getLang());
var btn = document.getElementById('lang-toggle');
if (btn) btn.addEventListener('click', function () {
apply(getLang() === 'zh'? 'en': 'zh');
});
// index filter: by domain, hide empty domain sections
var fbtns = document.querySelectorAll('.filter-btn');
var cards = document.querySelectorAll('.card');
var dsecs = document.querySelectorAll('.domain-sec');
for (var i = 0; i < fbtns.length; i++) {
fbtns[i].addEventListener('click', function () {
for (var j = 0; j < fbtns.length; j++) fbtns[j].classList.remove('active');
this.classList.add('active');
var f = this.getAttribute('data-filter');
for (var c = 0; c < cards.length; c++) {
cards[c].style.display = (f === 'all' || cards[c].getAttribute('data-domain') === f)? '': 'none';
}
for (var s = 0; s < dsecs.length; s++) {
var any = false;
var cs = dsecs[s].querySelectorAll('.card');
for (var k = 0; k < cs.length; k++) {
if (cs[k].style.display!== 'none') { any = true; break;}
}
dsecs[s].style.display = any? '': 'none';
}
});
}
// compare page: filter product rows by domain (disabled while a selection is active)
var cfbtns = document.querySelectorAll('.cmp-filter-btn');
for (var i2 = 0; i2 < cfbtns.length; i2++) {
cfbtns[i2].addEventListener('click', function () {
if (this.hasAttribute('disabled')) return;
for (var j2 = 0; j2 < cfbtns.length; j2++) cfbtns[j2].classList.remove('active');
this.classList.add('active');
cmpDomain = this.getAttribute('data-filter');
applyCompareFilter();
});
}
// compare expand
document.addEventListener('click', function (ev) {
var t = ev.target;
if (t && t.classList && t.classList.contains('cell-toggle')) {
var cell = t.closest('.cmp-cell');
var block = t.closest('.lang-block');
if (!cell || !block) return;
var full = block.querySelector('.full');
var snippet = block.querySelector('.snippet');
var open = cell.classList.toggle('expanded');
if (full) full.hidden =!open;
if (snippet) snippet.hidden = open;
var label = open
? (getLang() === 'zh'? '收起': 'Collapse')
: (getLang() === 'zh'? '展开': 'Expand');
t.textContent = label;
}
});
// 全局对比选型：托盘开关 / 卡片按钮 / 面板内选择 / 清空（事件委托，面板内容是动态渲染的）
document.addEventListener('click', function (ev) {
var t = ev.target;
if (!t ||!t.closest) return;
var add = t.closest('[data-addcmp]');
if (add) {
var _slug = add.getAttribute('data-addcmp');
var _sel = getSelection();
if (_sel.indexOf(_slug) < 0 && _sel.length >= MAX_SEL) {
flashCopy(add, getLang() === 'zh'? '最多选 4 款': 'Up to 4');
} else if (_sel.indexOf(_slug) < 0) {
if (!_flying[_slug]) {
_flying[_slug] = true;
flyToTray(add, function () { _flying[_slug] = false; toggleSelect(_slug);});
}
} else {
toggleSelect(_slug);
}
return;
}
var un = t.closest('[data-unsel]');
if (un) { toggleSelect(un.getAttribute('data-unsel')); return;}
var tg = t.closest('[data-sel-toggle]');
if (tg) { if (!tg.disabled) toggleSelect(tg.getAttribute('data-sel-toggle')); return;}
if (t.closest('#cmp-clear') || t.closest('#cmp-sel-clear')) { clearSelection(); return;}
var cpc = t.closest('#cmp-copy');
if (cpc) { copyPromptText(buildCompareMarkdown(), cpc); return;}
var shl = t.closest('#cmp-share');
if (shl) { shareSelection(shl); return;}
var panel = document.getElementById('cmp-panel');
var trayBtn = t.closest('#cmp-tray-btn');
if (trayBtn && panel) {
var open = panel.hidden;
panel.hidden =!open;
trayBtn.setAttribute('aria-expanded', open? 'true': 'false');
return;
}
if (panel &&!panel.hidden &&!t.closest('.cmp-tray')) panel.hidden = true;
});
document.addEventListener('keydown', function (ev) {
if (ev.key === 'Escape') {
var panel = document.getElementById('cmp-panel');
if (panel &&!panel.hidden) panel.hidden = true;
}
});
// AI 选型：提示词卡片跳转外部 AI（读取的是特化后的文本）
document.addEventListener('click', function (ev) {
var t = ev.target;
if (!t ||!t.closest) return;
var b = t.closest('.ai-btn[data-act]');
if (!b) return;
var card = b.closest('.prompt-card');
if (!card) return;
var act = b.getAttribute('data-act');
var text = cardPromptText(card);
if (act === 'copy') copyPromptText(text, b);
else aiOpenService(act, text);
});
// 多库 PK：一键生成对比提示词（优先用托盘已选库，否则用下拉框）
document.addEventListener('click', function (ev) {
var t = ev.target;
if (!t ||!t.closest) return;
var b = t.closest('.ai-btn[data-pkact]');
if (!b) return;
var lang = getLang(), sel = getSelection(), tpl;
if (sel.length >= 2) {
tpl = pkPromptN(lang, selNames());
} else {
var _pp2 = pkSelects(), sa = _pp2[0], sb = _pp2[1];
var an = sa? sa.value: '';
var bn = sb? sb.value: '';
if (!an ||!bn) {
flashCopy(b, lang === 'zh'? '请先选两款库': 'Pick two first');
return;
}
tpl = (lang === 'zh'? PK_ZH: PK_EN).split('{a}').join(an).split('{b}').join(bn);
}
var act = b.getAttribute('data-pkact');
if (act === 'copy') copyPromptText(tpl, b);
else aiOpenService(act, tpl);
});
applySelFromUrl();
applySelection();
});

// 档案页"用 AI 深挖这款"：全局函数，供行内 onclick 调用
var DIVE_ZH = '__DIVE_ZH__';
var DIVE_EN = '__DIVE_EN__';
window.aiDeepDive = function (service, btn) {
var row = (btn && btn.closest)? btn.closest('.ai-dive-row'): null;
var name = row? row.getAttribute('data-product'): '';
var tpl = getLang() === 'zh'? DIVE_ZH: DIVE_EN;
var base = AI_URLS[service];
if (!base) return;
window.open(base + encodeURIComponent(tpl.split('{name}').join(name)), '_blank', 'noopener');
};
})();
"""
JS = JS.replace("__DIVE_ZH__", _DIVE_ZH_JS).replace("__DIVE_EN__", _DIVE_EN_JS)


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main():
    if not SRC.is_dir():
        print("profiles 目录不存在: %s" % SRC, file=sys.stderr)
        sys.exit(1)
    (SITE / "assets").mkdir(parents=True, exist_ok=True)
    products = []
    for slug in SLUGS:
        zh_p = SRC / (slug + ".md")
        en_p = SRC / (slug + ".en.md")
        if not zh_p.exists() or not en_p.exists():
            print("缺少档案文件: %s" % slug, file=sys.stderr)
            sys.exit(1)
        products.append(build_product(slug))

    # 客户经验 + 场景案例库数据
    _slugs = [p["slug"] for p in products]
    fav_index, fav_titles = build_fav_index(_slugs)
    prod_by_slug = {p["slug"]: p for p in products}
    cases = load_cases()

    outputs = {}
    global _CATALOG_SCRIPT
    _CATALOG_SCRIPT = (
        "window.DB_CATALOG=%s;window.DB_DOMAINS=%s;"
        % (json.dumps([{"slug": p["slug"], "name": p["name"], "name_en": p["name_en"], "domain": p["domain"], "domains": p["domains"]}
                       for p in products], ensure_ascii=False),
           json.dumps({d: {"zh": zh, "en": en} for d, zh, en in DOMAINS}, ensure_ascii=False)))
    outputs["index.html"] = apply_badges(index_page_html(products, n_cases=len(cases)))
    for p in products:
        outputs["profile-%s.html" % p["slug"]] = apply_badges(profile_page_html(p))
    outputs["cases.html"] = apply_badges(cases_page_html(cases, prod_by_slug, fav_index, fav_titles))
    cmp_body, cmp_cells = compare_page_html(products)
    # 分片数量随内容大小变化，先删旧分片避免残留（如 cmp-32.js 之后不再生成时）
    for _old in (SITE / "assets").glob("cmp-*.js"):
        _old.unlink()
    cmp_scripts = _write_cmp_shards(outputs, cmp_cells)
    outputs["compare.html"] = apply_badges(page_shell(
        "DB 选型参考 - 维度对比", "DB Compare - Compare", cmp_body, active="compare", tail_scripts=cmp_scripts))
    outputs["methodology.html"] = apply_badges(methodology_page_html())
    outputs["advisor.html"] = apply_badges(advisor_page_html(products))

    for name, content in outputs.items():
        (SITE / name).write_text(content, encoding="utf-8")
    (SITE / "assets" / "style.css").write_text(CSS, encoding="utf-8")
    (SITE / "assets" / "app.js").write_text(JS, encoding="utf-8")

    print("构建完成，输出文件：")
    for name in list(outputs) + ["assets/style.css", "assets/app.js"]:
        print("  -", name)
    n_fb = sum(len(p["fallbacks"]) for p in products)
    print("解析回退命中：%d 处" % n_fb)
    for p in products:
        for f in p["fallbacks"]:
            print("    [%s] %s" % (p["slug"], f))
    n_full = sum(1 for p in products if not p["dims_fallback_zh"] and not p["dims_fallback_en"])
    print("维度完整解析：%d / %d 产品（双语 47 维无回退）" % (n_full, len(products)))
    n_fav, n_fav_cards = 0, 0
    for p in products:
        zc, ec = get_fav_cards(p["slug"])
        if zc or ec:
            n_fav += 1
            n_fav_cards += max(len(zc), len(ec))
    print("客户经验：%d / %d 产品有内容，共 %d 张卡片" % (n_fav, len(products), n_fav_cards))
    print("场景案例：%d 个" % len(cases))
    for c in cases:
        for ps in _split_list(c["zh"]["fields"].get("相关产品", "")):
            if ps == "无":
                continue
            if ps not in prod_by_slug:
                print("    [案例 %s] 相关产品未知 slug: %s" % (c["slug"], ps))
        for rc in _split_list(c["zh"]["fields"].get("相关能力", "")):
            if rc == "无":
                continue
            if ":" in rc or "：" in rc:
                ps, nm = re.split(r"[:：]", rc, maxsplit=1)
                if fav_lookup(fav_index, ps.strip(), nm.strip()) is None:
                    print("    [案例 %s] 相关能力未匹配: %s" % (c["slug"], rc))


if __name__ == "__main__":
    main()
