"""Rename the launcher's own name inside every language catalog's <source>/<translation>.

The English sources in the code changed, so each catalog needs the same text changed on both
sides of a message, otherwise Qt's (context, source) lookup misses and the string silently
falls back to English.

Deliberately NOT touched:
  - the import-format list ("Prism Launcher, PolyMC or MultiMC exported instances"), which
    names other launchers' formats and must stay accurate
  - the stale "Install a prismlauncher symlink to /usr/local/bin" pair, which already does not
    match the code (code uses %1); we do not invent sources
  - <oldsource>, <extracomment>, <name> (Qt contexts) and comments
"""
import re, pathlib, sys

APPLY = "--apply" in sys.argv
KEEP_HINTS = ("PolyMC", "MultiMC exported", "symlink to /usr/local/bin")
PAIRS = [("Prism Launcher", "WTF Launcher"), ("PrismLauncher", "WTFLauncher"), ("prismlauncher", "wtflauncher")]
TAGS = ("source", "translation")

total = {}
for p in sorted(pathlib.Path(".").glob("*.ts")):
    raw = orig = p.read_text(encoding="utf-8")
    counter = [0]
    for tag in TAGS:
        for old, new in PAIRS:
            pat = re.compile(rf"(<{tag}[^>]*>)([^<]*)(</{tag}>)")

            def repl(m, old=old, new=new):
                text = m.group(2)
                if old not in text or any(k in text for k in KEEP_HINTS):
                    return m.group(0)
                counter[0] += 1
                return m.group(1) + text.replace(old, new) + m.group(3)

            raw = pat.sub(repl, raw)
    changed = counter[0]
    if raw != orig:
        # 只做结构性自检（成对标签数量一致）；真正的正确性由 lrelease 编译验证
        for tag in TAGS:
            if len(re.findall(rf"<{tag}[^>]*>", raw)) != len(re.findall(rf"</{tag}>", raw)):
                print(f"跳过 {p.name}: {tag} 标签不成对")
                break
        else:
            total[p.name] = changed
            if APPLY:
                p.write_text(raw, encoding="utf-8", newline="\n")

print(("已改写 " if APPLY else "将改写 ") + f"{len(total)} 个文件，共 {sum(total.values())} 处")
print("样例:", list(total.items())[:6])
leftover = []
for p in sorted(pathlib.Path(".").glob("*.ts")):
    for m in re.finditer(r"<(?:source|translation)[^>]*>([^<]*(?:Prism Launcher|prismlauncher)[^<]*)</(?:source|translation)>",
                         p.read_text(encoding="utf-8", errors="ignore")):
        if not any(k in m.group(1) for k in KEEP_HINTS):
            leftover.append((p.name, m.group(1)[:60]))
print("非预期残留:", len(leftover), leftover[:4])
