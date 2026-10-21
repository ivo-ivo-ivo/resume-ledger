#!/usr/bin/env python3
"""resume-ledger: create a project skeleton.

usage: python init.py --lang zh|en --name "Name" [--dir PATH]
Creates ledger.yaml, ledger/facts.md, ledger/transcripts/, rules.md, decisions.md,
content/, build/, registry.md, interview/, .gitignore. Detects Chrome for PDF export.
Exit codes: 0 ok, 2 project created but a dependency (Chrome, markdown, pypdf) is missing, 1 error.
"""
import argparse, os, shutil, sys, platform
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCAFFOLD = HERE.parent / "templates" / "scaffold"

CHROME_CANDIDATES = {
    "Darwin": [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ],
    "Linux": ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge"],
    "Windows": [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ],
}

def find_chrome():
    for c in CHROME_CANDIDATES.get(platform.system(), []):
        if os.path.isabs(c) and os.path.exists(c):
            return c
        p = shutil.which(c)
        if p:
            return p
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", choices=["zh", "en"], required=True)
    ap.add_argument("--name", required=True, help="display name used on rendered resumes")
    ap.add_argument("--dir", default=".")
    a = ap.parse_args()
    root = Path(a.dir).resolve()
    if (root / "ledger.yaml").exists():
        print(f"ERROR: {root/'ledger.yaml'} already exists; refusing to overwrite.")
        sys.exit(1)
    for d in ["ledger/transcripts", "content", "build", "interview"]:
        (root / d).mkdir(parents=True, exist_ok=True)
    src = SCAFFOLD / a.lang
    if not src.exists():
        print(f"ERROR: scaffold for lang={a.lang} not found at {src}")
        sys.exit(1)
    for f in ["ledger/facts.md", "rules.md", "decisions.md", "registry.md", "content/EXAMPLE-resume.md", "interview/HITMAP-template.md"]:
        dst = root / f
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src / f, dst)
    missing = []
    for mod in ("markdown", "pypdf"):
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    chrome = find_chrome()
    (root / "ledger.yaml").write_text(
        f"lang: {a.lang}\nname: \"{a.name}\"\nchrome: {chrome or 'NOT_FOUND'}\nout_dir: build\n"
        "privacy:\n  never_commit:\n    - ledger/transcripts/\n    - \"*.private.md\"\n",
        encoding="utf-8")
    gi = root / ".gitignore"
    existing = gi.read_text(encoding="utf-8") if gi.exists() else ""
    add = "\n".join(l for l in ["ledger/transcripts/", "*.private.md", "build/*.html"] if l not in existing)
    gi.write_text((existing.rstrip("\n") + "\n" + add + "\n").lstrip("\n"), encoding="utf-8")
    print(f"created project at {root} (lang={a.lang})")
    print(f"python packages: {'ok' if not missing else 'MISSING ' + ', '.join(missing) + '  -> pip install ' + ' '.join(missing)}")
    print(f"chrome: {chrome or 'NOT FOUND -> install Chrome/Chromium/Edge or set chrome: in ledger.yaml'}")
    if chrome and not missing:
        sys.exit(0)
    print("WARNING: project created, but PDF export will fail until the items above are fixed.")
    sys.exit(2)

if __name__ == "__main__":
    main()
