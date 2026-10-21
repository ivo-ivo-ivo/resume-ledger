# Trigger evals

`trigger-eval.json` holds 20 realistic prompts: 10 that should activate the skill and 10 near-misses that share vocabulary (JD, resume, portfolio) but need something else. Run them with Anthropic's `skill-creator` description optimiser from inside Claude Code:

```bash
npx skills add anthropics/skills --skill skill-creator      # if not installed
# then, in Claude Code, ask: "run the trigger eval in evals/trigger-eval.json against skills/resume-ledger and optimise the description"
```

Record the resulting trigger rates in CHANGELOG.md with each description change. Add a prompt here whenever a real user says something that should have triggered and did not.
