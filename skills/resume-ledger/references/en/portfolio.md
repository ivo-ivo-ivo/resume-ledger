# Portfolio method (en)

A case study answers "how did you think, trade off and verify", not "what features shipped". One project per case, one core mechanism explained properly.

## Structure (flagship ≤ 8 pages, short ≤ 3)

Flagship: overview → what changed (before / after / evidence) → problem and goals (success criteria) → design and trade-offs (including one reversed first choice) → one deep dive → evaluation and rollout (with a "limits of the numbers" paragraph) → human in the loop and compliance → results → decision log → retrospective (what worked / what I would change) → stack → next steps and open problems → FAQ.
Short: context and problem → success criteria → design and key decisions → ownership boundary → results → retrospective.

A section readers remember: "a day in the life of one record", walking the mechanism end to end and naming the one step where AI appears.

## Three hard constraints
- Numbers come from deterministic systems; the model explains or rewrites. Every AI-influenced decision names who can confirm or overturn it.
- Say what is unfinished and risky before saying what succeeded; the "limits of the numbers" paragraph is mandatory.
- Planned items go under "next steps", never into results.

## Numbers
- Wording may differ from the resume, but every figure still needs a ledger row with scope portfolio or both; `check_numbers.py` reconciles against that scope.
- No real dates; relative months ("kickoff month 1") with the anchor stated in the overview.
- Before/after and experiment results are kept apart; say when there was no control group.

## De-identification checklist (walk it before sending)
- Names, employers, clients, partners
- Real dates, internal version numbers, system codenames
- Business-line names and counts, headcounts (write "core team")
- Scene details that imply the industry or region
- Vendor names (AI tools and model vendors excepted)
- Contact details
`scan.py --portfolio` catches the user's name, emails, phones and real dates; scene details are on you.

## Common failures
- A resume expanded: the same figures in a different order.
- Only wins: no reversed decision, no open problem; readers stop believing.
- Contradicting the resume without a bridge: "3 direct reports" there, "core team" here, with no way to explain both in an interview.
