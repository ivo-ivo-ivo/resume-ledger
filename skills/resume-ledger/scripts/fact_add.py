#!/usr/bin/env python3
"""Append one fact to ledger/facts.md with the next ID. Never append by hand.

usage: python fact_add.py --topic T --fact F --source S [--number N] [--definition D]
       [--banned B] [--scope resume|portfolio|both] [--status live|pilot|planned]
       [--verified V] [--review YYYY-MM] [--dry-run]
Prints last ID and new ID. Refuses if an identical fact text already exists.
"""
import argparse, sys
from _ledger import project_root, parse_ledger, last_id, table_end

def main():
    ap = argparse.ArgumentParser()
    for k in ["topic", "fact", "source"]:
        ap.add_argument("--" + k, required=True)
    ap.add_argument("--number", default="")
    ap.add_argument("--definition", default="")
    ap.add_argument("--banned", default="")
    ap.add_argument("--scope", choices=["resume", "portfolio", "both"], default="both")
    ap.add_argument("--status", choices=["live", "pilot", "planned"], default="live")
    ap.add_argument("--verified", default="user")
    ap.add_argument("--review", default="")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    for v in vars(a).values():
        if isinstance(v, str) and "|" in v:
            sys.exit("ERROR: '|' is not allowed inside a cell")
    root = project_root()
    path = root / "ledger" / "facts.md"
    lines, rows = parse_ledger(path)
    dup = [c[0] for _, c in rows if c[2] == a.fact]
    if dup:
        sys.exit(f"ERROR: identical fact already exists: {dup}")
    lid = last_id(rows)
    nid = f"F{lid+1:03d}"
    row = "| " + " | ".join([nid, a.topic, a.fact, a.number, a.definition, a.banned,
                            a.source, a.scope, a.status, a.verified, a.review]) + " |"
    if not a.dry_run:
        lines.insert(table_end(lines), row)
        path.write_text("\n".join(lines), encoding="utf-8")
    print(f"last id: F{lid:03d}  ->  new id: {nid}" + ("  (dry run)" if a.dry_run else "  written"))
    print(row)

if __name__ == "__main__":
    main()
