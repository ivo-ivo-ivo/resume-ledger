#!/usr/bin/env python3
"""Three scenarios, no Chrome needed: init from scratch, examples pass their own checks, ledger append + conflict.
usage: python tests/run.py
"""
import subprocess, sys, tempfile, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = ROOT / "skills" / "resume-ledger" / "scripts"
PY = sys.executable
fails = 0

def run(args, cwd, expect=0):
    r = subprocess.run([PY, *args], cwd=cwd, capture_output=True, text=True)
    ok = (r.returncode == expect)
    global fails
    fails += 0 if ok else 1
    print(("PASS" if ok else "FAIL"), " ".join(str(a) for a in args[:2]), f"(exit {r.returncode}, expected {expect})")
    if not ok:
        print(r.stdout[-600:], r.stderr[-600:])
    return r

# 1. init from scratch, both languages; expect 0 (chrome) or 2 (no chrome)
for lang in ("zh", "en"):
    d = Path(tempfile.mkdtemp())
    r = subprocess.run([PY, S / "init.py", "--lang", lang, "--name", "T", "--dir", d], capture_output=True, text=True)
    ok = r.returncode in (0, 2) and (d / "ledger" / "facts.md").exists() and (d / ".gitignore").exists() and (d / "interview" / "HITMAP-template.md").exists()
    fails += 0 if ok else 1
    print("PASS" if ok else "FAIL", "init", lang, f"(exit {r.returncode})")
    shutil.rmtree(d)

# 2. examples pass their own checks (html only)
for ex in ("zh", "en"):
    e = ROOT / "examples" / ex
    for f in sorted((e / "content").glob("*.md")):
        run([S / "check.py", f, "--no-pdf"], cwd=e)
    shutil.rmtree(e / "build", ignore_errors=True)

# 3. ledger append, duplicate refusal, planned-number flag, banned wording
d = Path(tempfile.mkdtemp())
subprocess.run([PY, S / "init.py", "--lang", "en", "--name", "T", "--dir", d], capture_output=True)
run([S / "fact_add.py", "--topic", "x", "--fact", "served 500 customers", "--number", "500", "--source", "t", "--banned", "over 1000"], cwd=d)
run([S / "fact_add.py", "--topic", "x", "--fact", "served 500 customers", "--source", "t"], cwd=d, expect=1)
run([S / "fact_edit.py", "--id", "F001", "--number", "520", "--note", "recount"], cwd=d)
r = run([S / "fact_edit.py", "--id", "F999", "--number", "1"], cwd=d, expect=1)
run([S / "fact_add.py", "--topic", "y", "--fact", "launch in 40 countries", "--number", "40", "--source", "t", "--status", "planned"], cwd=d)
(d / "content" / "t.md").write_text("---\ntemplate: resume-en\ntitle: t\nout: build/t.html\nlang: en\n---\nServed 520 customers, over 1000 leads, live in 40 countries, 77% growth.\n", encoding="utf-8")
r = run([S / "check_numbers.py", d / "content" / "t.md"], cwd=d, expect=1)
want = ["77%", "40", "over 1000"]
ok = all(w in r.stdout for w in want)
fails += 0 if ok else 1
print("PASS" if ok else "FAIL", "check_numbers flags missing, planned and banned:", want)
shutil.rmtree(d)

print("\nRESULT:", "all passed" if fails == 0 else f"{fails} failure(s)")
sys.exit(1 if fails else 0)
