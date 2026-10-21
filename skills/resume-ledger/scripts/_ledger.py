"""shared helpers: locate ledger table, parse rows, next id."""
import re
from pathlib import Path

NCOLS = 11
ID_RE = re.compile(r"^F(\d{3,})$")

def project_root(start="."):
    p = Path(start).resolve()
    for q in [p, *p.parents]:
        if (q / "ledger.yaml").exists():
            return q
    raise SystemExit("ERROR: no ledger.yaml found in this directory or its parents; run init.py first")

def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]

def parse_ledger(path):
    """returns (lines, rows) where rows = list of (line_index, cells)"""
    lines = path.read_text(encoding="utf-8").split("\n")
    rows = []
    for i, l in enumerate(lines):
        if l.startswith("| F"):
            c = split_row(l)
            if len(c) >= NCOLS and ID_RE.match(c[0]):
                rows.append((i, c))
    return lines, rows

def last_id(rows):
    ids = [int(ID_RE.match(c[0]).group(1)) for _, c in rows]
    return max(ids) if ids else 0

def table_end(lines):
    start = next((i for i, l in enumerate(lines) if l.startswith("| ID")), None)
    if start is None:
        raise SystemExit("ERROR: facts table header '| ID' not found")
    i = start
    while i + 1 < len(lines) and lines[i + 1].startswith("|"):
        i += 1
    return i + 1
