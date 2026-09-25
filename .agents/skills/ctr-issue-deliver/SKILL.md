---
name: ctr-issue-deliver
description: Execute an authorized Canonical Travel Regions GitHub ticket with scoped artifacts, evidence/model safeguards, validation and an honest issue/board handoff. Use when asked to work on a ticket; listing or creating a ticket alone does not trigger execution.
---

# Deliver one bounded ticket

Read [AGENTS.md](../../../AGENTS.md), [docs/workflow.md](../../../docs/workflow.md), the live issue body/comments/dependencies and the task's referenced current R/D/Q sections. Use [the adoption record](../../../experiments/q001/stage1-core-adoption.md) for current proof inputs and [implementation notes](../../../docs/evaluator-implementation.md) for evaluator work. Do not load the entire factual corpus for an unrelated task.

## Begin with an authorized outcome

Confirm that the user asked for execution, not merely creation or recommendation. Inspect the worktree, current implementation, linked PRs and last handoff; continue existing work rather than restarting. Check current phase, non-issue blockers and the actual outcome of closed dependencies. An Epic requires authorized decomposition; it is not one implementation ticket.

State the deliverable, non-goals, applicable rules/questions and validation. If the ticket conflicts with current accepted semantics, surface the conflict before changing them. A model-analysis request authorizes proposals, not normative adoption. An AI feasibility ticket authorizes its stated research, not a paid pilot, framework installation or bulk geographic collection.

For a runnable ticket, set In progress on project 3 and leave a concise start comment describing the bounded slice and any prior work being resumed. Preserve other assignments and do not imply someone else has approved the work. If status writing fails, report it without recreating the issue or blocking safe local progress.

## Work by task type

- **Model:** use general predicates and synthetic distinguishing cases; identify data versus conceptual gaps. Preserve accepted product regressions as explicit constraints without hardcoded answers. Proposed spec patches stay proposed unless adoption is explicitly requested.
- **Evidence:** only research the authorized scope. Preserve source versions/locators, effective versus retrieval time, exceptions and both sides of a claimed discontinuity. Candidate AI extractions are not verified. Source review is not a final-region oracle. Stage 1 certificates require every R044 gate; missing data and model ambiguity stay typed unknowns. Do not write over the frozen Q001 snapshot without explicit versioned-update scope.
- **Implementation:** preserve historical P1/P2/P3 behavior/results separately from current CR-W. Exercise the changed behavior and counterexamples; never reinterpret old results by renaming a profile.
- **Process/research:** implement only the requested enabler or report. Link its concrete downstream use; compare costs from current primary documentation when required, label estimates and do not run billable experiments without a cap and authorization.

Do not automatically create unrelated tickets or change org-wide configuration. When scope or approval is missing, leave a precise handoff and ask for the necessary decision. Continue safe independent portions where possible, but do not claim blocked acceptance items are complete.

## Verify and hand off

Run the relevant acceptance checks and the repository baseline in AGENTS.md. For protected-data work, inspect the diff and checksum results; do not repair an unintended factual modification by blessing its new checksum. Check deterministic artifact behavior without rewriting the historical results. Record commands, outcomes and checks not run; do not invent measurements or treat a syntax validator as proof of semantics.

Update the issue's acceptance checklist only for completed items and add a concise evidence-backed completion or blocker comment with artifact links. Preserve other contributors' body text; prefer a comment if ownership is uncertain. Move to In review when durable reviewable deliverables exist. Local-only changes remain a handoff, not Done. Commit/push/PR follow the current user's scope; do not infer standing permission from an earlier completed request.

Mark Done/close completed only after the agreed deliverables are accessible and the ticket's criteria truly hold. If the ticket includes maintainer acceptance, wait for it. No-go may complete research, but it must not pretend a production system was built. A residual Q question remains open unless its separate closure criterion and normative decision are fulfilled.

Final report: issue URL, delivered outcome, changed artifacts, checks, factual/normative changes, unresolved blockers and next safe step. Do not automatically begin the next ticket.
