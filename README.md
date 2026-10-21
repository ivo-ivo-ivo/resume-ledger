# resume-ledger

Resumes, JD-targeted variants and portfolio case studies built from a **fact ledger**, so every number in a document traces back to a source the candidate confirmed. An Agent Skill, usable in Claude Code, Codex CLI, Gemini CLI, Cursor and any tool that reads `SKILL.md`. Chinese and English.

Most "AI resume" tools start from the job description and write toward it. This one starts from what actually happened, records it with its definition and source, and only then writes, and a script refuses any draft whose numbers are not in the ledger.

## How it works

1. `init` creates a private project: ledger, rules, content, registry. Nothing of yours is stored in this repository.
2. The agent interviews you in rounds. Every new fact needs a definition, a source, your own role boundary and a status (live / pilot / planned). Conflicts between what you said now and earlier are surfaced, never resolved silently.
3. Facts are appended with `fact_add.py` (next ID, no duplicates). You fill `rules.md`: red-line words, banned and allowed wordings, a redaction map.
4. Content lives in one Markdown file per version. A JD-targeted version starts from a hit map: requirement → ledger rows → hit / partial / gap. Gaps are not padded.
5. `check.py` builds HTML and PDF, reconciles every number against the ledger, scans for red-line words and formatting, and reads the page count back. Nothing is "done" until all three pass.
6. Blind copies are derived, never hand-edited. Versions are registered with outcomes, the only feedback loop.

Portfolios follow the same rule with one twist: their wording is independent of the resume, but every figure still needs a ledger row with scope `portfolio`.

## Compatibility

| Tool | Install path | Status |
| --- | --- | --- |
| Claude Code | plugin marketplace or `npx skills add` | install verified; triggering eval in progress (see `evals/`) |
| Codex CLI, Cursor, Gemini CLI, Copilot, Windsurf and others on the Agent Skills standard | `npx skills add` into `.agents/skills/` | installs by the standard; not individually verified |
| Web chats without a shell | paste `SKILL.md` and references as instructions | degraded mode described in `SKILL.md`; not verified |

Status: v0.1. Report what works or breaks in your tool via an issue.

## Install

```bash
npx skills add ivo-ivo-ivo/resume-ledger          # any agent on the Agent Skills standard
claude plugin marketplace add ivo-ivo-ivo/resume-ledger && claude plugin install resume-ledger@resume-ledger
gemini extensions install https://github.com/ivo-ivo-ivo/resume-ledger
```

Requirements: Python 3.10+, `pip install markdown pypdf` (use a venv on macOS), Chrome / Chromium / Edge for PDF export. Without a shell, the skill falls back to a manual mode and says so.

## Three-minute start

```bash
S=<path to skills/resume-ledger/scripts>
python3 $S/init.py --lang en --name "Your Name" --dir ~/my-resume
cd ~/my-resume
python3 $S/fact_add.py --topic Role --fact "..." --number "..." --definition "..." --source "user 2026-10-16"
python3 $S/check.py content/general.md
```

Or just tell your agent "help me write a resume for this JD" and let the skill drive.

## Examples

Two complete, fictional walkthroughs: [`examples/zh`](examples/zh/README.md) (小张) and [`examples/en`](examples/en/README.md) (Maya Chen). Each plants five common slips in the first interview round and shows how the conflict check and the number check catch them.

## Privacy

Your ledger is personal data. `init.py` writes a `.gitignore` that keeps transcripts out of git; keep the whole project directory private. The skill never copies your facts into its own folder.

## Licence

Code MIT; documentation, references and examples CC BY 4.0. See `LICENSE` and `LICENSE-docs`.

中文说明见 [README.zh.md](README.zh.md)。
