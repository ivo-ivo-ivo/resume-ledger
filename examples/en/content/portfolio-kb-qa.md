---
template: portfolio
title: Case study · Knowledge-base Q&A: making RAG releasable with a test set
out: build/portfolio-kb-qa.html
lang: en
---

# Case study · Knowledge-base Q&A: making RAG releasable with a test set

## Overview

Took a knowledge-base Q&A product for support teams from zero to its first paying customer in about 5 months at an AI startup in the support space, then to biweekly releases and 40+ paying customers. The work that mattered was not wiring up a model; it was turning "does it answer correctly" into a metric that could be measured, regressed and used as a release gate: a 150-question test set drawn from real tickets, retrieval hit rate from 74% in v1 to 93% after three optimisation rounds, and a 28% relative drop in human escalation at pilot customers. I owned discovery, PRD, test-set design, the knowledge-base and retrieval approach, and acceptance; fine-tuning and serving were done by the ML team, onboarding by the delivery team.

| Item | Detail |
| --- | --- |
| Project | Knowledge-base Q&A for support and success teams, B2B |
| Timeline | Kickoff month 1; first paying customer month 5; biweekly releases since |
| My role | Discovery, PRD, test-set design and labelling, retrieval approach, acceptance, pilot design |
| Team | Core team; ML team for fine-tuning and serving; delivery team for onboarding |
| Headline results | Hit rate 74% to 93%; escalation down 28% relative at pilots; 40+ paying customers |

## What changed

| Dimension | Before | After | Evidence |
| --- | --- | --- | --- |
| Release decision | Demo a few questions, ship if it looks fine | 150-question weekly regression; no release below the previous hit rate | Eval log |
| Wrong answers | Found via customer complaints | Low-confidence escalation; one-click agent correction, admin-reviewed before entering the knowledge base | HITL design |
| Customer value | Feature demos | Escalation down 28% relative at 6 pilots | 4 weeks before vs after |

## Problem and goals

The first customer trial ran two weeks before anyone noticed that roughly half the answers missed. There was no test set that could reproduce the failures, so optimisation was guesswork.

| Problem | Success criterion | Result |
| --- | --- | --- |
| Quality not measurable | A fixed test set; every change regressed against it | 150 questions, weekly |
| Low retrieval hit rate | A defined metric that keeps improving | 74% to 93% |
| No fallback on bad answers | Low confidence does not answer; agents can correct | HITL shipped |
| Customers see no value | Before/after at pilots | Escalation down 28% relative |

## Design and trade-offs

**Test set first, then optimisation.** 150 questions sampled from 4 customers' anonymised tickets; I labelled the target passage for each with customer-success. Definition: questions with a known target passage as the denominator, target passage in the top results as the numerator. Written as "retrieval hit rate", never "accuracy": in support, accuracy reads as answer correctness, a different metric this project did not measure separately.

**A first choice I reversed.** v1 used fixed-length chunks and plain vector search: 74%. Round one swapped the embedding model: under 2 percentage points gain, dropped. Round two moved to structure-aware chunks (question, answer, applicable product kept together) plus hybrid keyword + vector search. Round three added reranking and per-product-line partitioning. 93% after three rounds. Lesson: chunking moved the metric more than the embedding model did.

**Pragmatic calls.**
- Low confidence escalates rather than "answers as best it can": one extra escalation beats one wrong answer
- Agent corrections do not go live on their own; an admin reviews them first
- Multi-turn stays out of scope and on the roadmap: one correct single-turn answer beats one wrong multi-turn exchange

## Deep dive: how the test set became the release gate

| Step | Practice |
| --- | --- |
| Sampling | 4 customers' anonymised tickets, stratified by product line, 150 questions covering head and tail |
| Labelling | Target passage and acceptable answer points per question; double-labelled by me and customer-success, disagreements settled by the customer |
| Regression | Full run after any retrieval or knowledge-base structure change; compared with the previous release |
| Gate | No release below the previous hit rate; changes caused by new knowledge recorded separately |
| Upkeep | About 25 new questions per quarter, stale items retired, size held near 150 |

## Evaluation and rollout

| Stage | Practice | Question answered |
| --- | --- | --- |
| Offline | 150-question set, weekly | Is this release better than the last |
| Pilot comparison | 6 customers, 4 weeks before vs after, escalation rate | Do customers see value |
| General | Biweekly releases | Ongoing |

**Limits of the numbers.** Hit rate is a retrieval metric, not answer correctness. The escalation drop is a before/after at 6 pilots, not a controlled experiment. 40+ counts paying customers only.

## Human in the loop and compliance

- Low-confidence threshold adjustable per customer
- One-click corrections, admin-reviewed before entering the knowledge base
- Customer data isolated per tenant; test-set sampling under anonymisation agreements

## Results

| Metric | Definition | Value |
| --- | --- | --- |
| Retrieval hit rate | 150-question test set | 74% to 93% |
| Escalation rate | 6 pilots, 4 weeks each side, relative | down 28% |
| Paying customers | latest month, trials excluded | 40+ |
| Time to first paying customer | kickoff to go-live | about 5 months |

## Decision log

| Stage | Decision | Alternative | Basis |
| --- | --- | --- | --- |
| Month 2 | Build the test set before optimising | Tune directly | Optimisation without a test set cannot be reproduced |
| Month 3 | Drop the embedding-model swap, change chunking | Keep swapping models | Under 2 percentage points |
| Month 6 | Low confidence escalates | Let the model try | A wrong answer costs more than an escalation |
| Month 9 | Multi-turn out of this phase | Build in parallel | Single-turn hit rate not yet stable |

## Retrospective

**What worked**: test set before optimisation; the metric was defined as hit rate from day one; corrections are reviewed before they go live.

**What I would change**: 150 questions is small and thin on the tail; the pilot comparison had no control group, so customer process changes are mixed into the 28%; the first trial could have been caught in days with a test set instead of two weeks.

## Stack

| Layer | Technology |
| --- | --- |
| Knowledge | Structure-aware chunking, hybrid keyword + vector search, reranking, per-product-line partitioning |
| Model | LLM behind a gateway, vendor swappable; fine-tuning owned by the ML team |
| Evaluation | 150-question set, regression script, hit-rate dashboard |
| Delivery | Multi-tenant isolation; onboarding by the delivery team |

## Next steps

| Priority | Item | Status |
| --- | --- | --- |
| 1 | AI ticket triage | pilot at 3 customers |
| 2 | Multi-turn conversation, automatic ticket creation | planned |
| 3 | Grow the test set to several hundred, stratified by customer | planned |

## FAQ

| Question | Answer |
| --- | --- |
| Is 93% accuracy | No, retrieval hit rate; answer correctness is a separate metric this project did not measure |
| Is the 28% drop an experiment result | No, a before/after at 6 pilots without a control group |
| Who built it | Core team; evaluation and retrieval approach were mine, fine-tuning and serving the ML team's, onboarding the delivery team's |
| Biggest mistake | No test set before the first trial; two weeks to notice half the answers missed |
