---
name: ctr-decide
description: Use when the owner makes a normative choice about the canon — adopting or rejecting a rule, convention or proposal, narrowing or closing an open question — or asks for the options behind such a choice to be laid out; also when asked to "record" or "save" a finding that implies a rule.
---

# Prepare and record decisions

Normative text lives only in `docs/spec.md` (R), `docs/decisions.md` (D) and `docs/open-questions.md` (Q); `docs/partition-architecture.md` summarises them. Nothing becomes normative until the owner says so explicitly in the conversation.

## A finding is not a decision

Results of research, experiments or reviews go where findings live — the experiment README, a research note, `docs/status.md` or an issue comment — marked as proposals. An owner's "ok, save it" about a finding is not adoption: save the finding there, then ask whether the rule it implies is adopted. New D entries carry only `accepted`, `rejected` or `deferred`; the older `tentative` entries are history, not a place for new proposals.

## Preparing a decision

Lay out, in the conversation (or in `docs/proposals/<slug>.md` if long or worth keeping):

- the question and which consumer requirement or open question it serves;
- the options, each stated as a **generic predicate over data** — never as a list of territory names;
- counterexamples and what each option does to them (`data/adversarial-test-set.csv`, `experiments/`, known cases); consequences for named territories are expectations until checked against a source;
- effects on accepted constraints (e.g. D004–D007) and on existing R/D/Q items;
- a recommendation.

## Recording an adopted decision

1. Record only what the owner decided. Details you add to make the rule operational are proposals: list them and get an OK before committing. A parameter left open becomes a new Q.
2. Read the related issue with its comments, and every R/D/Q item the decision touches. Also grep the normative documents for the decision's key terms — conflicting clauses are not always linked by ID.
3. Next free IDs — never renumber or reuse:
   - D: `grep -n '^### D0' docs/decisions.md`; R: `grep -n '^### R0' docs/spec.md`; Q: `grep -n '^## Q0' docs/open-questions.md`
   - V checks: the checks table in `docs/spec.md`; T rows: the last `test_id` in `data/adversarial-test-set.csv`
   - Confirm the candidate is unused: `git grep -n '<ID>'` and `gh pr list --repo uncovering-world/travel-regions-extraction`.
4. `docs/decisions.md`: a new entry with English labels **Decision / Rationale / Rules / Counterarguments / Status / Basis**. Status `accepted`; Basis "owner decision, YYYY-MM-DD", with links to the proposal, issue or experiment.
5. `docs/spec.md` and `docs/open-questions.md`: add R items. Amend a partly overridden item in place and tag it `amended by Dxxx`. A wholly replaced item keeps its text and gains a status note linking to its replacement. Where a clause elsewhere no longer holds, append a dated note naming it. Narrow or close Q items, giving the reason.
6. Bump the version header of each changed normative document. The evaluator's `SPEC_VERSION` and its test change only if the evaluated core (R044) changes.
7. Update summaries that no longer hold: `docs/partition-architecture.md`, `README.md`, the "Current state" bullet in `AGENTS.md`, `docs/status.md`. Mark a proposal file adopted with its D ID.
8. If the rule is testable, add tests or new adversarial rows in English; do not rewrite existing rows' expectations. Run validation (AGENTS.md).
9. Commit only your paths — `git commit -m "docs(spec): adopt Dxxx — <short>" -- <paths>` — and push. If a path you must change carries unrelated uncommitted edits, ask first. Comment on the related issue; close it if its outcome is reached.

A rejected or deferred option is recorded as a D entry with status `rejected` or `deferred` when its reasoning is worth keeping.

## Red flags

- Writing "accepted" because an experiment or research pointed that way — the owner has not decided yet.
- Encoding an exception for a named territory. If the owner wants one, it is an explicit convention with rationale, scope and citation (Q011).
- Rewriting frozen historical artifacts (`experiments/q001/`, `experiments/source-pilot/`) to fit a new rule.
- New public text in a language other than English.
