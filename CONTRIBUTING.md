# Contributing

Three rules, then the usual.

1. **Never commit a real resume, ledger, transcript or JD.** Examples are fictional and must stay that way. CI greps for local paths; reviewers grep for names.
2. **Change `SKILL.md` only with a trigger eval.** Run `evals/trigger-eval.json` before and after; paste the two trigger rates into the pull request.
3. **Change a script only with a test.** `tests/run.py` must pass on macOS and Linux; add a case for every new flag or failure mode.

Setup:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install markdown pypdf
python tests/run.py
```

Scope of `SKILL.md`: keep it under two screens. New guidance goes into `references/<lang>/`, in both languages, written independently rather than translated.

Ledger format: 11 columns, fixed order. A column change is a breaking change and needs a migration note in `CHANGELOG.md`.
