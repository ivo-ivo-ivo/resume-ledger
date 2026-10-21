# Workflow and interview protocol (en)

## Order of work

1. Initialise the project (`init.py`).
2. Collect facts with the interview protocol below; write each confirmed fact with `fact_add.py`.
3. The user fills `rules.md`: red-line words, banned wordings, allowed wordings, redaction map.
4. Write content: `content/<version>.md`, one file per version.
5. Build and check: `check.py` runs build → number reconciliation → scan; read the PDF page count back to the user.
6. Register with `registry_add.py`; record where it was sent and what came back.

## Interview protocol

Goal: turn what the user remembers into ledger rows, each with a definition, a source, a role boundary and a status. The model asks and organises; it does not conclude on the user's behalf.

**Rounds**
- At most 10 questions per round; must-have first, nice-to-have last; offer tickable options rather than chains of follow-ups.
- Round one asks the skeleton questions: timeline, scope of the first version, mechanism, evaluation method, metric definitions, compliance and human-in-the-loop, division of labour.
- Read the ledger before asking; never re-ask what is already recorded.

**Four things every new fact needs** (missing one = not written)
1. Definition: numerator and denominator, period, relative or absolute, scope.
2. Source: date of the statement, document, system export.
3. Role boundary: what the user did, who did the rest.
4. Status: live / pilot / planned.

**Conflict check before the next round**
- Compare new statements against existing ledger rows and against earlier statements in this session. For each conflict, show both versions and ask which stands.
- Never pick for the user; never silently keep one.
- If the same disagreement survives two rounds, stop and ask for material instead of asking a third time.

**Common practice is an option, never a fact**
- When the user asks "what do people usually do", list the common approaches so they can tick what matches.
- The tick goes into the ledger; the listed options do not. What the user did not do is "not done in v1, listed under next steps", which reads as more credible than claiming it.

**Exit condition**
- Skeleton answered, conflicts cleared: present a narrative plan (sections and the source of each) and write the body only after the user agrees.

## Number rules

- A figure appears at most twice in one resume: once in the summary, once in the body.
- Relative or absolute must be stated: "improved by 20%" fails; "+20% relative" or "+20 percentage points" passes.
- Facts with status planned may only appear under "next steps"; `check_numbers.py` flags numbers backed only by planned rows.
- Bare integers up to 12 are not reconciled by the script; the model must still make sure they exist in the ledger.

## Portfolio vs resume

- Portfolios are de-identified; their wording may differ from the resume, but every number still needs a ledger row with scope portfolio or both.
- Flagship case study ≤ 8 pages, short case ≤ 3; planned items go under "next steps", never into results.
- The two documents must be able to explain each other: if the resume says "3 direct reports" and the portfolio says "core team", the user must be able to bridge that in an interview.
