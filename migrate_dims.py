# -*- coding: utf-8 -*-
"""一次性迁移：54 个 profile md
1. 删除“大版本升级 / Major-version upgrades”维度条目；
2. 在 dims 节末尾追加 6 个新维度（按各文件原有风格 h3/numbered/bullet）；
3. 重编号；4. 节标题 14 -> 19。
运行前自动备份到 profiles.bak-<date>。
"""
import re
import shutil
import sys
from datetime import date
from pathlib import Path

SITE = Path(__file__).resolve().parent
sys.path.insert(0, str(SITE))
from build import split_dim_items, _dim_name_and_rest_h3, _dim_name_and_rest_list  # noqa: E402
from new_dims_data import NEW_DIMS, CONTENT  # noqa: E402

PROFILES = SITE.parent / "profiles"
TARGET_ZH = "大版本升级"
TARGET_EN = "Major-version upgrades"

DIM_ORDER = [d["key"] for d in NEW_DIMS]


def find_dims_section(lines):
    """返回 (节标题行号, 节体起, 节体止)。节体止 = 下一个 ## 标题行（不含）。
    兼容多种标题写法：硬维度/Hard dimensions（大小写不敏感）、固定题库/Fixed question battery。"""
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


def is_upgrade_dim(name, lang):
    """判断维度名是否为“大版本升级”维度，兼容多种写法：
    大版本升级 / Major-version upgrades / Major version upgrades / Major-Version Upgrade"""
    if lang == "en":
        low = name.lower()
        return "major" in low and "upgrade" in low
    return TARGET_ZH in name


def header_name(style, line, lang):
    if style == "h3":
        name, _ = _dim_name_and_rest_h3(line)
    else:
        name, _ = _dim_name_and_rest_list(line)
    return name or ""


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
    lines = path.read_text(encoding="utf-8").split("\n")
    sec = find_dims_section(lines)
    if not sec:
        return "NO-DIMS-SECTION"
    title_i, body_start, body_end = sec
    # 节标题 14 -> 19：标题行中的独立数字 14 即为维度数，统一替换为 19
    # 兼容：固定题库 14 项 / 14 维必答 / Fixed 14-Question Battery / 14 mandatory dimensions 等
    lines[title_i] = re.sub(r"\b14\b", "19", lines[title_i])
    body = lines[body_start:body_end]
    items, extras, style, intro = split_dim_items(body)
    # 找目标条目行号（兼容多种写法）
    header_idx = [i for i, ln in enumerate(body) if is_item_header(style, ln)]
    drop = None
    for hi in header_idx:
        if is_upgrade_dim(header_name(style, body[hi], lang), lang):
            drop = hi
            break
    if drop is None:
        return "TARGET-NOT-FOUND"
    # 删除：从 header 到下一个 header（或节末）
    pos = header_idx.index(drop)
    drop_end = header_idx[pos + 1] if pos + 1 < len(header_idx) else len(body)
    del body[drop:drop_end]
    # 追加 6 个新条目（节末）
    if not body or body[-1].strip() != "":
        body.append("")
    for key in DIM_ORDER:
        dim = next(d for d in NEW_DIMS if d["key"] == key)
        entry = CONTENT[slug][key][lang]
        # render_new_item 返回多行字符串，必须拆成行再 extend，否则 split_dim_items/renumber 无法按行解析
        body.extend(render_new_item(style, lang, 0, dim, entry).split("\n"))
    body, count = renumber(body, style)
    # bullet 风格无编号，count=0；用解析复核
    lines[body_start:body_end] = body
    path.write_text("\n".join(lines), encoding="utf-8")
    # 复核
    items2, _, style2, _ = split_dim_items(body)
    names = [it["name"] for it in items2 if not it.get("_note")]
    unmatched_note = [it["name"][:20] for it in items2 if it.get("_note")]
    return "OK style=%s items=%d dropped=1 added=6" % (style2, len(names))


def main():
    bak = PROFILES.parent / ("profiles.bak-%s" % date.today().isoformat())
    if bak.exists():
        shutil.rmtree(bak)
    shutil.copytree(PROFILES, bak)
    print("backup ->", bak)
    files = sorted(PROFILES.glob("*.md"))
    report = {}
    for p in files:
        if p.stem.endswith(".en"):
            continue
        for q in (p, p.parent / (p.stem + ".en.md")):
            if not q.exists():
                report[q.name] = "MISSING"
                continue
            report[q.name] = migrate_file(q)
    bad = {k: v for k, v in report.items() if not v.startswith("OK")}
    print("migrated %d files" % len(report))
    for k, v in sorted(report.items()):
        if not v.startswith("OK"):
            print("  !!", k, v)
    if bad:
        print("FAILURES:", len(bad))
        sys.exit(1)
    print("ALL OK")


if __name__ == "__main__":
    main()
