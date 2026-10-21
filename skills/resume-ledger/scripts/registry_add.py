#!/usr/bin/env python3
"""Add a row to registry.md. Refuses a duplicate version name.

usage: python registry_add.py --version V --target T --source S [--date YYYY-MM-DD]
       [--notes N] [--pages P] [--sent-to X] [--feedback F]
"""
import argparse, datetime, sys
from _ledger import project_root

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True)
    ap.add_argument("--target", required=True)
    ap.add_argument("--source", required=True, help="e.g. content/x.md → build/x.html / .pdf")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    for k in ["notes", "pages", "sent-to", "feedback"]:
        ap.add_argument("--" + k, default="")
    a = ap.parse_args()
    root = project_root()
    p = root / "registry.md"
    lines = p.read_text(encoding="utf-8").split("\n")
    if any(l.startswith(f"| {a.version} |") for l in lines):
        sys.exit(f"ERROR: version `{a.version}` already registered")
    row = "| " + " | ".join([a.version, a.date, a.target, a.source, a.notes, a.pages,
                            getattr(a, "sent_to"), a.feedback]) + " |"
    hdr = next((i for i, l in enumerate(lines) if l.startswith("| ")), None)
    if hdr is None:
        sys.exit("ERROR: registry table not found")
    i = hdr
    while i + 1 < len(lines) and lines[i + 1].startswith("|"):
        i += 1
    lines.insert(i + 1, row)
    p.write_text("\n".join(lines), encoding="utf-8")
    print(row)

if __name__ == "__main__":
    main()
