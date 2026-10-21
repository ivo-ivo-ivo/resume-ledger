# Changelog

## 0.1.0 · 2026-10-16

First public release.

- Agent Skill `resume-ledger`: fact ledger, interview protocol with conflict check, JD hit map, portfolio method, blind copies, version registry.
- Scripts: `init`, `fact_add`, `fact_edit`, `build` (md → html → pdf via Chrome), `check_numbers`, `scan`, `derive`, `registry_add`, `check`.
- Templates for zh and en resumes and portfolios; scaffold projects; hit-map template.
- Two complete fictional examples (小张, Maya Chen), each passing its own checks.
- Verified: install via `npx skills add` and via Claude Code plugin marketplace; PDF export on macOS with Chrome. Not yet verified: triggering evals, Codex and Cursor plugin manifests, no-shell degraded mode.

Breaking changes: none (first release). The ledger table has 11 fixed columns; adding or reordering columns breaks the scripts.
