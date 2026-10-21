#!/usr/bin/env python3
"""Reconcile every number in a content file against the ledger.

usage: python check_numbers.py content/<version>.md
(1) each number in the content must exist in a ledger row (Figures or Fact column) whose scope
    allows this content type (resume / portfolio / both);
(2) a number backed only by status=planned rows is flagged;
(3) banned wordings (ledger Banned column + rules.md "Banned wordings" section) must not appear.
Skips years, dates, times and bare integers <= 12 without a unit. Exit 1 on any failure.
"""
import re, sys
from pathlib import Path
from _ledger import project_root, parse_ledger

NUM = re.compile(r"(?<![A-Za-z\d])\d[\d,\.]*\s*[%+]?\s*(?:万|亿|k|K|M|B|x|X|倍|TB|GB|T|pp|个百分点)?(?![A-Za-z])")
YEAR = re.compile(r"^(19|20)\d\d(?:[\.\-/年]\d{1,2})?$")

def norm(s):
    s = s.replace("，", ",").replace("％", "%").replace("＋", "+")
    return re.sub(r"\s+", "", s).replace(",", "")

def tokens(text):
    body = re.sub(r"^---.*?---", "", text, count=1, flags=re.S)
    body = re.sub(r"`[^`]*`", "", body)
    # strip contact lines, dates and times before tokenising
    body = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", " ", body)
    body = re.sub(r"\+?\(?\d[\d\s\-()]{6,}\d", " ", body)   # phone-like runs
    body = re.sub(r"\b\d{1,2}[:：]\d{2}\b", " ", body)
    body = re.sub(r"\b(19|20)\d\d\s*[\.\-/年]?\s*(\d{1,2}\s*月?)?(\s*\d{1,2}\s*日?)?", " ", body)
    out = set()
    for m in NUM.finditer(body):
        t = m.group(0).strip()
        if re.match(r"^\d+(\.\d+)?$", t) and float(t) <= 12:
            continue
        out.add(norm(t))
    return sorted(out)

def ledger_numbers(rows, scope):
    ok, planned = set(), set()
    for _, c in rows:
        if c[7] not in ("both", scope):
            continue
        nums = {norm(m.group(0)) for col in (c[3], c[2], c[4]) for m in NUM.finditer(col)}
        (planned if c[8] == "planned" else ok).update(nums)
    return ok, planned

def banned_list(root, rows):
    items = set()
    for _, c in rows:
        for part in re.split(r"[;；]", c[5]):
            if part.strip():
                items.add(part.strip())
    rules = root / "rules.md"
    if rules.exists():
        sec = re.search(r"^##\s*(禁用写法|Banned wordings).*?(?=^##|\Z)",
                        rules.read_text(encoding="utf-8"), re.S | re.M)
        if sec:
            items |= {l[1:].strip() for l in sec.group(0).splitlines() if l.startswith("-")}
    return {b for b in items if b and not b.startswith(("(", "（"))}

def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = Path(sys.argv[1]).resolve()
    root = project_root(path.parent)
    text = path.read_text(encoding="utf-8")
    fm = re.match(r"^---\n(.*?)\n---", text, re.S)
    m = re.search(r"^template:\s*(\S+)", fm.group(1), re.M) if fm else None
    scope = "portfolio" if m and m.group(1).startswith("portfolio") else "resume"
    _, rows = parse_ledger(root / "ledger" / "facts.md")
    ok, planned = ledger_numbers(rows, scope)
    toks = tokens(text)
    def covered(t, pool):
        core = t.rstrip("+")
        return any(core == p.rstrip("+") for p in pool)
    missing = [t for t in toks if not covered(t, ok | planned)]
    from_planned = [t for t in toks if not covered(t, ok) and covered(t, planned)]
    hits = [b for b in banned_list(root, rows) if b in text]
    print(f"scope: {scope}   numbers in content: {len(toks)}   ledger figures usable: {len(ok)}")
    print("numbers not in ledger:", missing or "none")
    print("numbers only backed by planned rows:", from_planned or "none")
    print("banned wording hits:", hits or "none")
    sys.exit(1 if (missing or from_planned or hits) else 0)

if __name__ == "__main__":
    main()
