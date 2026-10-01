# -*- coding: utf-8 -*-
"""一次性迁移：27 个老产品的 54 个 profile md，追加 3 个数据集成新维度。
不删除任何内容，只在 dims 节末尾追加；重编号；节标题 19 -> 22。
databricks/snowflake 已有 22 维，跳过。
"""
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent
sys.path.insert(0, str(SITE))
from build import split_dim_items, _dim_name_and_rest_h3, _dim_name_and_rest_list
from new_dims_data2 import NEW_DIMS2, CONTENT2

PROFILES = SITE.parent / "profiles"
SKIP = {"databricks", "snowflake"}
DIM_ORDER = [d["key"] for d in NEW_DIMS2]

def find_dims_section(lines):
    start = None
    for i, ln in enumerate(lines):
        if not re.match(r"^##\s+", ln):
            continue
        low = ln.lower()
        if ("硬维度" in ln or "hard dimensions" in low
                or "固定题库" in ln or "fixed question battery" in low):
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if re.match(r"^##\s+", lines[i]):
            end = i
            break
    return start, start + 1, end

def is_item_header(style, line):
    s = line.strip()
    if style == "h3":
        return bool(re.match(r"^###\s+", line))
    if style == "numbered":
        return bool(re.match(r"^\d{1,2}[.)]\s+\*\*", s))
    if style == "bullet":
        return bool(re.match(r"^[-*+]\s+\*\*", s))
    return False

def render_new_item(style, lang, n, dim, entry):
    v, p, b = entry["v"], entry["p"], entry["b"]
    zh_name, en_name = dim["zh"], dim["en"]
    if lang == "zh":
        if style == "h3":
            return "### %d. %s——%s（%s）\n\n%s\n" % (n, zh_name, v, p, b)
        if style == "numbered":
            return "%d. **%s**：**%s**（%s）。\n\n%s\n" % (n, zh_name, v, p, b)
        return "- **%s**：**%s**（%s）。\n\n%s\n" % (zh_name, v, p, b)
    else:
        if style == "h3":
            return "### %d. %s — %s (%s)\n\n%s\n" % (n, en_name, v, p, b)
        if style == "numbered":
            return "%d. **%s**: **%s** (%s).\n\n%s\n" % (n, en_name, v, p, b)
        return "- **%s**: **%s** (%s).\n\n%s\n" % (en_name, v, p, b)

def renumber(lines, style):
    n = 0
    out = []
    for ln in lines:
        if style == "h3":
            m = re.match(r"^(###\s+)\d+([.)、]\s*)", ln)
            if m:
                n += 1
                ln = "%s%d%s%s" % (m.group(1), n, m.group(2), ln[m.end():])
        elif style == "numbered":
            m = re.match(r"^(\d{1,2})([.)]\s+\*\*)", ln.strip())
            if m and is_item_header(style, ln):
                n += 1
                lstripped = ln.lstrip()
                ln = ln[: len(ln) - len(lstripped)] + "%d%s%s" % (n, m.group(2), lstripped[m.end():])
        out.append(ln)
    return out, n

def migrate_file(path):
    lang = "en" if path.stem.endswith(".en") else "zh"
    slug = re.sub(r"\.en$", "", path.stem)
    if slug in SKIP:
        return "SKIPPED-NEW"
    if slug not in CONTENT2:
        return "NO-DATA"
    lines = path.read_text(encoding="utf-8").split("\n")
    sec = find_dims_section(lines)
    if not sec:
        return "NO-DIMS-SECTION"
    title_i, body_start, body_end = sec
    # 节标题 19 -> 22
    lines[title_i] = re.sub(r"\b19\b", "22", lines[title_i])
    body = lines[body_start:body_end]
    items, extras, style, intro = split_dim_items(body)
    # 追加 3 个新条目（节末）
    if not body or body[-1].strip() != "":
        body.append("")
    # 当前最大编号
    _, cur_n = renumber(body, style)
    for dim in NEW_DIMS2:
        key = dim["key"]
        entry = CONTENT2[slug][key][lang]
        cur_n += 1
        body.extend(render_new_item(style, lang, cur_n, dim, entry).split("\n"))
    # 重编号
    body, final_n = renumber(body, style)
    lines[body_start:body_end] = body
    path.write_text("\n".join(lines), encoding="utf-8")
    return f"OK-{final_n}"

def main():
    files = sorted(PROFILES.glob("*.md"))
    # 排除备份目录（glob 只在 profiles 下，不含子目录）
    results = {}
    for f in files:
        # 跳过 .en 的 stem 处理已在 migrate_file 内
        r = migrate_file(f)
        results[r] = results.get(r, 0) + 1
        if not r.startswith("OK"):
            print(f"  {f.name}: {r}")
    print("Results:", results)
    migrated = results.get("OK-22", 0)
    print(f"migrated {migrated} files with 22 dims")
    # 验证
    bad = []
    for f in files:
        slug = re.sub(r"\.en$", "", f.stem)
        if slug in SKIP:
            continue
        text = f.read_text(encoding="utf-8")
        # 数维度条目
        if f.stem.endswith(".en"):
            cnt = len(re.findall(r"^[-*+]\s+\*\*", text, re.M))
        else:
            cnt = len(re.findall(r"^###\s+\d+", text, re.M))
        # 只检查 dims 节内的（粗略：全文）
        if cnt < 22:
            bad.append((f.name, cnt))
    if bad:
        print("BAD:", bad)
    else:
        print("ALL OK - all have 22 dims")

if __name__ == "__main__":
    main()
