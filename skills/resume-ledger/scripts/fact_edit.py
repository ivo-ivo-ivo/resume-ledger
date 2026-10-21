#!/usr/bin/env python3
"""Change one ledger row in place, keeping the old value in the source column.

usage: python3 fact_edit.py --id F012 [--fact F] [--number N] [--definition D] [--banned B]
       [--scope resume|portfolio|both] [--status live|pilot|planned] [--source S] [--review R]
       [--note "why"] [--dry-run]
At least one field must change. The previous fact/number/status text is appended to the
source column as "edited <date>: was <old>", so corrections stay traceable.
"""
import argparse, datetime, sys
from _ledger import project_root, parse_ledger, split_row

COLS = {"fact": 2, "number": 3, "definition": 4, "banned": 5, "source": 6, "scope": 7, "status": 8, "review": 10}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    for k in COLS:
        ap.add_argument("--" + k)
    ap.add_argument("--note", default="")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    changes = {k: getattr(a, k) for k in COLS if getattr(a, k) is not None}
    if not changes:
        sys.exit("ERROR: nothing to change")
    for v in list(changes.values()) + [a.note]:
        if "|" in v:
            sys.exit("ERROR: '|' is not allowed inside a cell")
    if "scope" in changes and changes["scope"] not in ("resume", "portfolio", "both"):
        sys.exit("ERROR: scope must be resume | portfolio | both")
    if "status" in changes and changes["status"] not in ("live", "pilot", "planned"):
        sys.exit("ERROR: status must be live | pilot | planned")
    root = project_root()
    path = root / "ledger" / "facts.md"
    lines, rows = parse_ledger(path)
    hit = [(i, c) for i, c in rows if c[0] == a.id]
    if len(hit) != 1:
        sys.exit(f"ERROR: id {a.id} found {len(hit)} times")
    i, cells = hit[0]
    old = {k: cells[COLS[k]] for k in ("fact", "number", "status") if k in changes and cells[COLS[k]] != changes[k]}
    for k, v in changes.items():
        cells[COLS[k]] = v
    if old:
        trail = "; ".join(f"{k} was: {v}" for k, v in old.items())
        stamp = f"edited {datetime.date.today().isoformat()}: {trail}" + (f" ({a.note})" if a.note else "")
        cells[6] = (cells[6] + "; " if cells[6] else "") + stamp
    row = "| " + " | ".join(cells) + " |"
    print(("dry run: " if a.dry_run else "updated: ") + row)
    if not a.dry_run:
        lines[i] = row
        path.write_text("\n".join(lines), encoding="utf-8")

if __name__ == "__main__":
    main()
