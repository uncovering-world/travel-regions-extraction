# How we work

The owner and the agent work on the canon together, in conversation. [AGENTS.md](../AGENTS.md) holds the invariants; this page says where results go.

## Choosing the means

Questions differ, so the path differs. Pick what the question needs, and switch when it turns out to need something else:

- **Owner's decision** — the question is a product or modelling preference and the options are already clear.
- **Discussion** — options, generic predicates and counterexamples need to be laid out first.
- **Desk research** — facts or outside practice are missing (`ctr-research`).
- **Experiment** — the answer depends on how a rule behaves over many cases or on data (`ctr-experiment`).
- **Code** — a tool is needed to build or check something.

None of these is a mandatory step before another. A decision can follow a single conversation; an experiment can end without any decision.

## Where results land

| Result | Place | Marking |
|---|---|---|
| Adopted rule, decision or question closure | `docs/spec.md` (R), `docs/decisions.md` (D), `docs/open-questions.md` (Q) | Only after the owner's explicit decision; next free ID; never renumbered (`ctr-decide`) |
| Proposal awaiting a decision | the conversation; if long or worth keeping, `docs/proposals/<slug>.md` or a comment on the related issue | "Proposal, not adopted"; after the decision, marked adopted (with its D ID) or rejected |
| Research note worth keeping | `docs/research/YYYY-MM-DD-<slug>.md` | Sources with dates; fact vs inference; unverified marked |
| Experiment | `experiments/<slug>/` with a `README.md` | Question, what would change our mind, method, result, conclusion, status |
| Review or analysis of the project | `docs/reviews/` | Non-normative |
| Where we are | `docs/status.md` | Updated at the end of each piece of work; live items only |
| Work spanning sessions | GitHub issues, Status on org project 3 | See below |

Frozen baselines (`experiments/q001/`, `experiments/source-pilot/`) are never edited; new evidence gets its own place.

## Issues

- Open an issue for work that spans sessions or must not be forgotten; quick questions stay in `docs/status.md`.
- Body sections follow the [Task form](../.github/ISSUE_TEMPLATE/task.yml): Description / Requirements / Additional Information. English, concise, no boilerplate.
- Native fields: Type, Priority and Size always; Theme and AI fit when obvious.
- Board Status: New → Backlog → In progress → In review → Done.
- To pause work, close the issue as *not planned* with a comment that says why and when to reopen it. Finished work is closed as *completed* with links to the commits or artifacts.
- #4 is the only epic: the roadmap.

## Git

Small conventional commits (`type(scope): subject`) straight to `main`, pushed right away. Never force-push.
