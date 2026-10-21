---
name: resume-ledger
description: Write, tailor and maintain resumes / CVs, JD-targeted versions, blind copies and portfolio case studies from a fact ledger, so every number traces to a source the user confirmed. Use this skill whenever the user mentions a resume, CV, 简历, 履历, job description, JD, 岗位, 投递, cover letter, portfolio, 作品集, case study, interview prep, 面试, or asks to "make my experience sound better", even if they only paste an old resume or a job post. Supports zh and en.
allowed-tools: Bash(python3:*) Bash(python:*) Read Write Edit
---

# resume-ledger

Resumes built from a **fact ledger**, not from memory. Never write a number you cannot point to in the ledger, and never put a fact in the ledger before the user has confirmed it. Scripts verify; you ask and write.

## Where things are

- **This skill's files**: the directory that contains this SKILL.md. Scripts are in `<skill-dir>/scripts/`, templates in `<skill-dir>/templates/`, references in `<skill-dir>/references/`. Resolve `<skill-dir>` from the path you read this file at (for a Claude Code plugin it is `${CLAUDE_PLUGIN_ROOT}/skills/resume-ledger`). Call scripts as `python3 <skill-dir>/scripts/<name>.py`.
- **The user's project**: a separate directory created by `init.py`, with `ledger.yaml` at its root. Scripts find it by walking up from the current directory. Never write the user's facts, transcripts or drafts into the skill directory.

## How big is the task

- **Wording only** (rephrase a bullet, fix grammar, shorten a paragraph, no number touched): answer directly, apply `rules.md` if a project exists, no pipeline.
- **Anything with a number, a new version, a JD, a portfolio, or a first resume**: full workflow below.
- **Unsure**: ask one question, then decide.

## Five principles

1. **Facts before prose.** Nothing enters a resume or portfolio until it is a ledger row with a source.
2. **Numbers carry their definition.** A figure without scope (what is counted, over what period, relative or absolute) is not a fact yet.
3. **Scripts verify, the model asks.** Number reconciliation, red-line scans, IDs and registry rows are scripts; do not do them by hand or in your head.
4. **One source file per version; derived outputs are never hand-edited.**
5. **The user owns every decision.** Confirm before overwriting a version, editing or removing a fact, or sending anything out. Report every failure verbatim; never patch silently.

## Project layout (created by `init.py`)

```
<project>/
  ledger.yaml            # lang, name, chrome path
  ledger/facts.md        # the fact ledger, rows F001…
  ledger/transcripts/    # raw user statements by date; git-ignored
  rules.md               # red-line words, banned/allowed wordings, redaction map
  decisions.md           # the user's writing decisions
  content/*.md           # one file per version; front matter template/title/out/lang
  build/                 # generated html/pdf
  registry.md            # versions: target, pages, where sent, feedback
  interview/             # JD hit maps and Q&A prep (template provided)
```

## Workflow

### 0. Find or create the project
If no `ledger.yaml` exists in the current directory or above, run `python3 <skill-dir>/scripts/init.py --lang zh|en --name "<name>" --dir <path>`. It also checks Python packages and Chrome and reports what is missing. Do not ask the user to create files by hand.

### 1. Collect facts
Two entry points, same rule: a fact is written only after the user confirms its **definition, source, their own role boundary, and status** (live / pilot / planned).

- **From an existing resume or notes the user pastes**: treat it as a transcript. Save it under `ledger/transcripts/`, extract candidate facts into a list, then confirm them in rounds. Numbers from an old resume are candidates, not facts.
- **From an interview**: rounds of at most 10 questions, must-have first, options to tick where possible. The first round asks the skeleton: timeline, scope of the first version, mechanism, how results were measured, metric definitions, compliance / human-in-the-loop, who did what.

Before the next round run a **conflict check**: new statements against existing ledger rows and against earlier statements in this session. Show both versions of every conflict and ask which stands. Never pick for the user. If the same disagreement survives two rounds, stop and ask for material instead.

Write with `fact_add.py` (prints the last ID, appends the next, refuses duplicates). Correct with `fact_edit.py --id F0xx ...` (keeps the old value in the source column). Never edit the ledger table by hand. Read `references/<lang>/workflow.md` for the full protocol.

### 2. Rules
`rules.md` has four sections scripts read by heading: red-line words, banned wordings, allowed wordings, redaction map. The user fills them; offer starters per language, never invent industry terms for them.

### 3. Write content
- One Markdown file per version in `content/`; front matter `template` (resume-zh | resume-en | portfolio), `title`, `out`, `lang`.
- A **JD-targeted version** starts from a hit map (`interview/HITMAP-template.md`): each requirement → ledger rows → hit / partial / gap. A gap stays a gap; a partial hit is written as what it is.
- A number appears at most twice in one resume (summary + one body line); the same figure keeps the same definition in every version. Relative vs absolute is always stated.
- **Portfolio case studies**: de-identified, wording independent of the resume, every figure still backed by a ledger row with scope `portfolio` or `both`. Structure and checklist in `references/<lang>/portfolio.md`. Flagship ≤ 8 pages, short case ≤ 3.
- Phrasing rules in `references/<lang>/writing-rules.md`.

### 4. Build and check
```
python3 <skill-dir>/scripts/check.py content/<version>.md        # build → check_numbers → scan; stops at the first failure
```
Step by step: `build.py` (md → html → pdf, needs Chrome; `--no-pdf` for html only), `check_numbers.py` (every number must be in the ledger; numbers backed only by planned rows are flagged; banned wordings are caught), `scan.py` (red-line words, punctuation, spacing; `--portfolio` adds the user's name, emails, phones, real dates). A version is done only when all three pass and you have read the PDF page count back to the user.

### 5. Register and derive
`registry_add.py --version <v> --target <t> --source <src → out> --pages <n>` (refuses duplicates). Blind copies: `derive.py content/<version>.md` (applies the redaction map, replaces the user's name, drops contact lines, fails if a mapped term survives), then build and check the derived file like any other. Record where each version went and what came back; that registry is the only feedback loop.

### 6. Interview prep
For a targeted version, write `interview/<jd>-prep.md` from `references/<lang>/interview-prep.md`: each likely question → answer points → ledger IDs.

## Degraded mode (no shell)
If scripts cannot run: keep the ledger as a Markdown table; before presenting any draft, list every number in it with its ledger ID; scan the draft against `rules.md` by reading and print the hits; say plainly that the checks were manual. Never claim a script-level check passed.

## Known limits
Bare integers up to 12 are not reconciled by the script (make sure they are in the ledger anyway). English units such as "weeks" are not parsed as units. The red-line scan catches listed words, not indirect identification.

## Language
Output language follows `lang` in `ledger.yaml`. Punctuation, spacing and phrasing rules are per language in the references. This file stays in English; references and examples exist in zh and en.

## References
- `references/<lang>/workflow.md` — interview protocol, conflict check, number rules
- `references/<lang>/writing-rules.md` — phrasing, what counts as a stretched number, what to delete
- `references/<lang>/portfolio.md` — case-study structure and de-identification checklist
- `references/<lang>/interview-prep.md` — hit map and Q&A prep format
- `<repo>/examples/<lang>/` — a complete fictional walkthrough that passes its own checks
