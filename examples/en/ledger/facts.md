# Fact ledger

One row per fact confirmed by the user. Append only with `scripts/fact_add.py`, never by hand. Scope: resume / portfolio / both. Status: live / pilot / planned; planned rows may only appear under "next steps", never as results.

| ID | Topic | Fact (allowed wording) | Figures | Definition | Banned wording | Source | Scope | Status | Verified | Review date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F001 | Profile | AI product manager, 6 years in product, 3 of them on LLM applications | 6 years; 3 years |  |  | user 2026-10-02 | resume | live | user |  |
| F002 | Education | BSc Computer Science, 2015–2019 | 2015–2019 |  |  | diploma | resume | live | user |  |
| F003 | Current·Role | A customer-support AI startup, Senior Product Manager (knowledge-base Q&A line), since Apr 2023 | Apr 2023 |  |  | user 2026-10-02; contract | resume | live | user |  |
| F004 | Current·Team | Directly manages 3 (2 PMs, 1 ops); a 7-person ML and engineering team collaborates but does not report to her | 3; 7 | 3 = direct reports; 7 = collaborators | led a team of 10 | user 2026-10-02 | resume | live | user |  |
| F005 | Current·Product | Knowledge-base Q&A for support teams, 40+ paying customers | 40+ | paying customers as of Sep 2026, trials excluded | over 100 customers | user 2026-10-02; CRM export 2026-09-30 | both | live | user |  |
| F006 | Current·Retrieval | Retrieval hit rate improved from 74% to 93% | 74%; 93% | 150-question test set from real support tickets; denominator = questions with a known target passage, numerator = target passage in top results; 74% = v1, 93% = after three optimisation rounds | accuracy 93%; recall | user 2026-10-02, confirmed 2026-10-04 after conflict; eval log | both | live | user |  |
| F007 | Current·Method | Retrieval optimisation: structure-aware chunking, hybrid keyword + vector search, reranking, per-product-line partitioning |  |  |  | user 2026-10-02 | both | live | user |  |
| F008 | Current·Escalation | Human-escalation rate down 28% relative at pilot customers | 28% | 6 pilot customers, 4 weeks before vs 4 weeks after, escalated chats ÷ total chats, relative | down 28 percentage points; all customers | user 2026-10-04; customer reports | both | live | user |  |
| F009 | Current·Eval | Built a 150-question regression test set, run weekly, used as the release gate | 150 | sampled from 4 customers' anonymised tickets; labelled by Maya with customer-success |  | user 2026-10-02 | both | live | user |  |
| F010 | Current·HITL | Low-confidence answers escalate to a human; agents can correct an answer in one click; corrections reach the knowledge base only after admin review |  |  |  | user 2026-10-02 | both | live | user |  |
| F011 | Current·Speed | First paying customer live about 5 months after kickoff; biweekly releases since | 5 months |  |  | user 2026-10-02; release log | both | live | user |  |
| F012 | Current·Renewal | First-year renewal rate 88% | 88% | customers signed in 2024 who renewed in 2025, by count |  | user 2026-10-04; finance | resume | live | user |  |
| F013 | Current·Ownership | Owned discovery, PRD, test-set design, knowledge-base and retrieval approach, acceptance; fine-tuning and serving by the ML team; onboarding by the delivery team |  |  | built entirely by me | user 2026-10-04 | both | live | user |  |
| F014 | Current·Planned | Multi-turn conversation and automatic ticket creation |  |  |  | user 2026-10-02 | both | planned | user |  |
| F015 | Current·Pilot | AI ticket triage piloting at 3 customers | 3 | pilot, not general availability | launched ticket triage | user 2026-10-04 after conflict | both | pilot | user |  |
| F016 | Previous·Role | A project-management SaaS company, Product Manager (AI features), Aug 2020 – Mar 2023 | Aug 2020 – Mar 2023 |  |  | user 2026-10-02; reference letter | resume | live | user |  |
| F017 | Previous·Summary | Meeting-summary feature, 150k+ monthly active users of the feature | 150k+ | feature MAU, not product MAU | product MAU 150k | user 2026-10-02; dashboard screenshot | resume | live | user |  |
| F018 | Previous·Triage | Support-ticket auto-classification, 90% accuracy on a 600-ticket labelled sample, manual review volume down 35% relative | 90%; 600; 35% | accuracy on labelled sample; review volume month before vs month after, relative | down 35 percentage points | user 2026-10-02, confirmed 2026-10-04 | resume | live | user |  |
| F019 | Previous·Conversion | Free-to-paid conversion up 12% relative after AI features shipped | 12% | quarter before vs quarter after, relative | up 12 percentage points; up 12% (unqualified) | user 2026-10-04 after conflict | resume | live | user |  |
| F020 | Current·Attempt | First optimisation round swapped the embedding model: under 2 percentage points gain, dropped | 2 percentage points | same 150-question set |  | user 2026-10-06 | portfolio | live | user |  |
| F021 | Current·EvalUpkeep | Test set topped up with about 25 new questions per quarter, stale items retired, size held near 150 | 25 |  |  | user 2026-10-06 | portfolio | live | user |  |
