#!/usr/bin/env python3
"""Render content/<version>.md -> HTML -> PDF.

usage: python build.py content/<version>.md [--no-pdf]
Front matter decides everything: template (resume-zh | resume-en | portfolio), title, out, lang.
HTML goes to `out`; PDF goes next to it with .pdf. Page count is printed and must be read back
to the user. Needs: pip install markdown pypdf; Chrome/Chromium/Edge path in ledger.yaml.
Exit 1 on any failure; never produces a partial artefact silently.
"""
import re, sys, subprocess, html as H
from pathlib import Path
from _ledger import project_root

HERE = Path(__file__).resolve().parent
TPL = HERE.parent / "templates"

def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    if not m:
        sys.exit("ERROR: front matter missing (template / title / out / lang)")
    fm = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip().strip('"')
    for k in ("template", "title", "out"):
        if k not in fm:
            sys.exit(f"ERROR: front matter lacks `{k}`")
    return fm, text[m.end():]

def read_cfg(root):
    cfg = {}
    for line in (root / "ledger.yaml").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(\w+):\s*(.+?)\s*$", line)
        if m:
            cfg[m.group(1)] = m.group(2).strip('"')
    return cfg

def page_count(pdf):
    try:
        from pypdf import PdfReader
        return len(PdfReader(str(pdf)).pages)
    except Exception:
        data = pdf.read_bytes()
        return len(re.findall(rb"/Type\s*/Page[^s]", data))

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1]).resolve()
    no_pdf = "--no-pdf" in sys.argv
    root = project_root(src.parent)
    cfg = read_cfg(root)
    fm, body = front_matter(src.read_text(encoding="utf-8"))
    css = TPL / f"{fm['template']}.css"
    if not css.exists():
        sys.exit(f"ERROR: unknown template `{fm['template']}` (no {css.name} in templates/)")
    try:
        import markdown
    except ImportError:
        sys.exit("ERROR: python-markdown not installed: pip install markdown")
    inner = markdown.markdown(body, extensions=["tables", "sane_lists", "attr_list"])
    lang = fm.get("lang", cfg.get("lang", "en"))
    doc = (f"<!DOCTYPE html><html lang=\"{lang}\"><head><meta charset=\"utf-8\">"
           f"<title>{H.escape(fm['title'])}</title><style>{css.read_text(encoding='utf-8')}</style>"
           f"</head><body><main class=\"{fm['template']}\">{inner}</main></body></html>")
    out = (root / fm["out"]).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    print(f"html: {out.relative_to(root)}")
    if no_pdf:
        return
    chrome = cfg.get("chrome", "NOT_FOUND")
    if chrome == "NOT_FOUND" or not chrome:
        sys.exit("ERROR: no Chrome configured in ledger.yaml (`chrome:`); PDF not produced. "
                 "Re-run with --no-pdf for HTML only.")
    pdf = out.with_suffix(".pdf")
    cmd = [chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
           f"--print-to-pdf={pdf}", out.as_uri()]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not pdf.exists():
        sys.exit(f"ERROR: Chrome failed (exit {r.returncode}):\n{r.stderr[-800:]}")
    print(f"pdf:  {pdf.relative_to(root)}")
    print(f"pages: {page_count(pdf)}")

if __name__ == "__main__":
    main()
