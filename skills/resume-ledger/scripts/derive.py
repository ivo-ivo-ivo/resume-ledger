#!/usr/bin/env python3
"""Derive a redacted (blind) copy of a content file. Never edit derived files by hand.

usage: python derive.py content/<version>.md [--suffix blind]
Substitutions: rules.md "## 脱敏替换" / "## Redaction map" lines of the form `- old => new`,
plus the user's name from ledger.yaml -> "候选人" (zh) / "Candidate" (en).
Lines containing an email or phone number are dropped. Output: content/<version>-<suffix>.md
with `out` rewritten to the matching build path.
"""
import re, sys
from pathlib import Path
from _ledger import project_root

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1]).resolve()
    suffix = sys.argv[sys.argv.index("--suffix") + 1] if "--suffix" in sys.argv else "blind"
    root = project_root(src.parent)
    cfg = dict(re.findall(r"^(\w+):\s*\"?([^\"\n]+)\"?", (root / "ledger.yaml").read_text(encoding="utf-8"), re.M))
    subs = []
    rules = root / "rules.md"
    if rules.exists():
        sec = re.search(r"^##\s*(脱敏替换|Redaction map).*?(?=^##|\Z)", rules.read_text(encoding="utf-8"), re.S | re.M)
        if sec:
            for l in sec.group(0).splitlines():
                m = re.match(r"^-\s*(.+?)\s*=>\s*(.+?)\s*$", l)
                if m:
                    subs.append((m.group(1), m.group(2)))
    if cfg.get("name"):
        subs.append((cfg["name"], "候选人" if cfg.get("lang") == "zh" else "Candidate"))
    text = src.read_text(encoding="utf-8")
    kept = []
    dropped = 0
    for line in text.split("\n"):
        if re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", line) or re.search(r"\+?\(?\d[\d\s\-()]{6,}\d", line):
            dropped += 1
            continue
        kept.append(line)
    out = "\n".join(kept)
    for a, b in subs:
        out = out.replace(a, b)
    out = re.sub(r"^(out:\s*)(.+?)(\.html)\s*$", lambda m: f"{m.group(1)}{m.group(2)}-{suffix}{m.group(3)}", out, count=1, flags=re.M)
    dst = src.with_name(f"{src.stem}-{suffix}{src.suffix}")
    dst.write_text(out, encoding="utf-8")
    left = [a for a, _ in subs if a in out]
    print(f"derived: {dst.relative_to(root)}   substitutions: {len(subs)}   lines dropped: {dropped}")
    if left:
        sys.exit(f"ERROR: still present after substitution: {left}")

if __name__ == "__main__":
    main()
