---
name: ctr-issue-create
description: Create, refine or decompose GitHub issues for Canonical Travel Regions with goal-linked acceptance criteria, native metadata and dependencies. Use for ticket creation or backlog triage, not ticket execution or geographic research.
---

# Create a Canonical Travel Regions issue

Read repository [AGENTS.md](../../../AGENTS.md) and [docs/workflow.md](../../../docs/workflow.md). The target is only `uncovering-world/travel-regions-extraction`, project **3**. Read the [Task form](../../../.github/ISSUE_TEMPLATE/task.yml) before drafting. Commands run from the repository root.

## Establish the task

Understand the requested outcome and identify its contribution to the canon. Read the relevant current R/D/Q sections and repository anchors. Search existing open **and closed** GitHub issues and recent related PRs; do not duplicate work or assert a premise from a title alone. Read matching issue bodies and comments before deciding to update or create. Do not collect new geography merely to flesh out a ticket.

Separate a missing fact, missing model predicate, product-regression conflict, implementation defect and process enabler. Research should ask a discriminating question with a valid negative outcome. Do not bake CR-J adoption, a desired region list or Stage 2 work into acceptance as though already authorized.

Use the form's Description / Requirements / Additional Information structure in neutral English. Include scope/non-goals, concrete artifact, validation, goal contribution and relevant R/D/Q links. Model questions remain in `docs/open-questions.md`; ticket IDs are GitHub numbers, not new Q IDs. State unknown costs rather than inventing a price.

Propose or set native Type, Priority, Size, Theme and AI fit using **current** org options. Use area labels only. Determine genuine parent/blocker relationships; do not turn “related” into “blocked by”. For an Epic, create bounded slices only when decomposition is requested; preserve already created sub-issues and inherited blockers. Do not generate a whole roadmap from one task.

## Publish only what was requested

An explicit request to create the scoped ticket is authorization to create it. A request for a draft is not. Ask for direction only if an unresolved scope, cost or product choice materially changes the ticket; otherwise use a disclosed, conservative assumption. Ticket creation never authorizes its implementation or a paid pilot.

1. Create with explicit `--repo`, `--type`, `--body-file` and applicable labels/hierarchy. Use an ephemeral draft, not a committed ticket mirror. After an uncertain create response, search for the created issue before retrying.
2. Set the four native issue fields using the verified org schema and the issue-field-values endpoint described in the workflow. Set only the requested values; leave unrelated metadata alone.
3. Add the issue to project 3 and set New if it needs triage, otherwise Backlog. Do not change project 2 or shared field definitions. Add a milestone only if it already exists and applies.
4. Read back body, type, fields, hierarchy and project Status. Report partial failures accurately and repair only the failed operation on the same issue. If an Epic slice was created, confirm its native parent and update only the relevant parent acceptance reference, preserving other text.

Return the issue URL, bounded outcome, metadata actually set and remaining blockers. Do not start the research just because the ticket now exists.
