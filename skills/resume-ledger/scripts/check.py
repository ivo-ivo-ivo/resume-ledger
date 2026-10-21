#!/usr/bin/env python3
"""One-shot: build + check_numbers + scan for a content file.

usage: python check.py content/<version>.md [--no-pdf]
Runs the three steps in order and stops at the first failure.
"""
import re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

def run(name, *args):
    print(f"== {name}")
    r = subprocess.run([sys.executable, str(HERE / name), *args])
    if r.returncode not in (0,):
        sys.exit(f"stopped at {name} (exit {r.returncode})")

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1]).resolve()
    extra = [a for a in sys.argv[2:] if a == "--no-pdf"]
    run("build.py", str(src), *extra)
    run("check_numbers.py", str(src))
    fm = re.match(r"^---\n(.*?)\n---", src.read_text(encoding="utf-8"), re.S).group(1)
    out = re.search(r"^out:\s*(.+)$", fm, re.M).group(1).strip()
    tpl = re.search(r"^template:\s*(\S+)", fm, re.M).group(1)
    root = src.parent.parent
    run("scan.py", str(root / out), *(["--portfolio"] if tpl.startswith("portfolio") else []))
    print("== all checks passed")

if __name__ == "__main__":
    main()
