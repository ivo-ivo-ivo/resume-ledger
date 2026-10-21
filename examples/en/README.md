# Example · Maya Chen (fictional)

A complete walkthrough: two interview rounds to a ledger, rules, a general resume, a JD-targeted version, a blind copy, a case study and interview prep. Person, companies and numbers are invented to demonstrate the method.

| File | What to look at |
| --- | --- |
| `ledger/transcripts/2026-10-02.md` | Round one plants five common slips: collaborators counted as reports, trials counted as customers, "accuracy" used for hit rate, a pilot called launched, relative and absolute mixed |
| `ledger/transcripts/2026-10-04.md` | How the conflict check asks, how the user corrects, how corrections land as ledger rows |
| `ledger/facts.md` | 21 rows, each with definition, banned wording, source, scope, status |
| `jd/aipm.md` → `interview/aipm-hitmap.md` → `content/aipm-targeted.md` | Hit map before the targeted version; a partial hit is written as "collaborates", not padded |
| `content/portfolio-kb-qa.md` | Case study: wording independent of the resume, every figure still in the ledger (scope portfolio); round three exists because the check caught two unrecorded figures |
| `checks.txt` | Real `check.py` output for all four content files |

```bash
S=<skill path>/scripts
python $S/check.py content/aipm-targeted.md   # needs Chrome; --no-pdf for HTML only
python $S/derive.py content/aipm-targeted.md  # blind copy
```
