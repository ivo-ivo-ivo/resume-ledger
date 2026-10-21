#!/usr/bin/env python3
"""Scan a built HTML (or a Markdown source) for red-line words and formatting slips.

usage: python scan.py build/<version>.html [--portfolio]
Red-line words come from rules.md "## 红线词" / "## Red-line words" (placeholder lines are skipped)
plus the user's name from ledger.yaml when --portfolio is given (portfolios are de-identified).
zh checks: half-width punctuation after CJK, missing space between CJK and ASCII.
en checks: double spaces, space before punctuation.
Both: email addresses and phone-like numbers inside a portfolio.
Exit 1 on red-line or identifier hits; formatting issues are reported but do not fail.
"""
import re, sys
from pathlib import Path
from _ledger import project_root

def strip_html(s):
    s = re.sub(r"<style.*?</style>", "", s, flags=re.S)
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"&[a-z]+;", " ", s)

def words_from_rules(root):
    rules = root / "rules.md"
    if not rules.exists():
        return []
    sec = re.search(r"^##\s*(红线词|Red-line words).*?(?=^##|\Z)", rules.read_text(encoding="utf-8"), re.S | re.M)
    if not sec:
        return []
    out = []
    for l in sec.group(0).splitlines():
        if not l.startswith("-"):
            continue
        w = l[1:].strip()
        if w.startswith(("（示例）", "(example)")) or not w:
            continue
        out.append(w)
    return out

def context(text, w, n=18):
    i = text.find(w)
    return text[max(0, i - n): i + len(w) + n].replace("\n", " ")

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    p = Path(sys.argv[1]).resolve()
    portfolio = "--portfolio" in sys.argv
    root = project_root(p.parent)
    raw = p.read_text(encoding="utf-8")
    text = strip_html(raw) if p.suffix == ".html" else re.sub(r"^---.*?---", "", raw, count=1, flags=re.S)
    cfg = dict(re.findall(r"^(\w+):\s*\"?([^\"\n]+)\"?", (root / "ledger.yaml").read_text(encoding="utf-8"), re.M))
    lang = cfg.get("lang", "en")
    words = words_from_rules(root)
    if portfolio and cfg.get("name"):
        words.append(cfg["name"])
    hits = [(w, context(text, w)) for w in words if w in text]
    ident = []
    if portfolio:
        ident += [("email", m) for m in re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text)]
        ident += [("phone", m) for m in re.findall(r"\+?\(?\d[\d\s\-()]{6,}\d", text)]
        ident += [("date", m) for m in re.findall(r"(?<!\d)20\d\d[-./年]\d{1,2}", text)]
    fmt = []
    if lang == "zh":
        fmt += [("half-width punctuation after CJK", m) for m in re.findall(r"[\u4e00-\u9fff][,.;:!?]", text)]
        fmt += [("missing space CJK/ASCII", m) for m in re.findall(r"[\u4e00-\u9fff][A-Za-z0-9%]|[A-Za-z0-9%][\u4e00-\u9fff]", text)]
    else:
        fmt += [("double space", m) for m in re.findall(r"\S  +\S", text)]
        fmt += [("space before punctuation", m) for m in re.findall(r"\w [,.;:!?]", text)]
    print(f"file: {p.name}   lang: {lang}   red-line words loaded: {len(words)}")
    print("red-line hits:", "none" if not hits else "")
    for w, c in hits:
        print(f"  {w!r}  …{c}…")
    if portfolio:
        print("identifier hits:", ident[:10] or "none")
    print("formatting:", "none" if not fmt else f"{len(fmt)} issue(s)")
    for k, m in fmt[:15]:
        print(f"  {k}: {m!r}")
    sys.exit(1 if (hits or ident) else 0)

if __name__ == "__main__":
    main()
