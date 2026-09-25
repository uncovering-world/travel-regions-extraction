# GitHub workflow

This is the repository's operational workflow, not a normative change to the regional model. [AGENTS.md](../AGENTS.md) supplies current phase limits; [spec.md](spec.md) owns the geographic rules.

## Sources of truth

- [Issues](https://github.com/uncovering-world/travel-regions-extraction/issues): the only task register. No committed local ticket copies, status ledgers or duplicate backlog.
- [Canonical Travel Regions project 3](https://github.com/orgs/uncovering-world/projects/3): Status for this repository's issues, with a Workflow board view. The project was created private; do not change its visibility without a request. Track Your Regions/project 2 is separate and must not be modified by this workflow.
- GitHub-native issue metadata: type, Priority, Size, Theme, AI fit, parent/sub-issues, blocked-by and milestone. Do not duplicate these as board-local fields or priority/status labels.
- [Open questions](open-questions.md): unresolved model semantics with Q IDs. An issue links to a question and delivers a bounded investigation; closing that issue does not automatically close Q001 or adopt a new rule.
- Repository artifacts: reviewed analysis, source-grounded evidence, code, tests and decisions. A temporary issue draft or API response is not another source of truth and should not be committed.

This borrows the task shape and native-metadata approach of [Track Your Regions](https://github.com/uncovering-world/track-your-regions/blob/main/CLAUDE.md), not its destination/curation heuristics, release sequencing, infrastructure or permissions.

## Mission-directed work

Every ticket states the chain **deliverable → blocker or invariant → contribution to the canonical partition**. Distinguish a missing fact from a missing definition. A conceptual ambiguity usually calls for a small synthetic distinguishing experiment; it does not justify bulk geographic collection. Evidence work must identify the accepted rule/gate it enables and keep unresolved cases visible.

The current phase permits Stage 1 model/evidence/evaluator work and bounded process enablers. It does not permit Stage 2 development or a world partition. Later geometry, coverage and destination work needs an explicit phase decision, not a silent change in ticket priority. Keep the final exhaustive, disjoint, one-level goal visible without pretending the current pairwise evaluator already produces that output.

Useful progress includes an auditable CR-W gate, an explicitly narrowed model question, a regression/failure exposed with a general counterexample, or a repeatable evidence-production cost/quality measurement. Neither fewer unknowns obtained by assumption nor more completed tickets is a substitute.

## Issue shape and metadata

Use the [Task form](../.github/ISSUE_TEMPLATE/task.yml): **Description / Requirements / Additional Information**, with a neutral English title/body and checkable acceptance items. These are the same top-level sections used for tasks in Track Your Regions. Bug reports also state reproduction, expected/actual behavior and the affected revision in Description. A requirement is checkable from a PR, artifact or written decision, not from agreement with an intended map.

The body includes current repository anchors, goal contribution, deliverables, scope/non-goals, related R/D/Q IDs, dependencies and validation. State what would count as a negative research result. Do not quote informal chat or invent measurements, issue links or facts.

| Metadata | Semantics |
|---|---|
| Type | Task: research, model experiment, evidence audit, tooling or docs. Bug: behavior contradicts the accepted contract. Feature: a new capability. Epic: umbrella, decomposed into bounded sub-issues, never executed as one vague assignment. |
| Priority | Urgent / High / Medium / Low, using existing org options. Urgent means a demonstrated critical break/blocker, not merely an interesting topic. |
| Size | Tiny / Small / Medium / Large / X-Large; rough effort, not an execution-time promise. Split an oversized ticket before starting. |
| Theme | Reuse applicable existing org values such as Data & Sync, Map & Geo, Infra & CI or Docs. Do not alter the shared org schema to add a project-specific option without authorization. |
| AI fit | Agent-ready: bounded, testable task can finish without unmade product choices. Pair: maintainer choices expected during work. Human-led: normative adoption, budget/account approvals or human-led review. It describes this ticket, not whether its subject is AI. |
| Parent / blocked-by | Native relationships. A related Q ID is not a dependency issue. Never treat a cancelled/closed blocker as proof that its promised deliverable exists; read its resolution. |
| Milestone | Use an applicable existing milestone if there is one; do not create a roadmap or deadline by inference. |
| Labels | Area only. Existing `documentation` and repository-local `process` / `research` are enough initially; add further areas only when needed. |

Missing metadata means **untriaged**, not lowest priority, unblocked or Agent-ready. Estimate uncertain fields explicitly; do not present estimates as measurements.

## Lifecycle

Project Status values: **New → Backlog → In progress → In review → Done**.

- New: incoming or underspecified. Triage premise, scope, acceptance, fields and dependencies before Backlog.
- Backlog: scoped and triaged. It may still have blockers; status alone never makes it eligible.
- In progress: the authorized bounded work is active. Record a concise start/handoff comment when taking or handing off a ticket, not one comment per tool call.
- In review: deliverables and validation are available for review; unresolved product/budget choices stay explicit.
- Done: the issue's acceptance criteria are fulfilled and the deliverables are accessible in the agreed repository/PR or report. Research may validly finish with no-go. Code left only in an agent's worktree is not delivered. Close with completed/not-planned accurately; do not count not-planned as successful delivery.

Native open dependencies block selection regardless of Status. For non-issue blockers (budget, unavailable source, required human decision), use an explicit **Blockers** subsection in Additional Information and a handoff comment. Return paused work to Backlog when appropriate; do not leave it advertised as active indefinitely. A new dependency ticket requires normal creation authorization, not fabricated work.

An implementation request includes routine updates to its own issue and board status. A request to list/recommend is read-only. Creating a ticket does not authorize its execution. Ask only for choices that materially change scope; do not require a second confirmation for an explicitly requested, fully scoped issue creation.

## Selecting work

1. Respect the user's explicitly selected ticket or task. For a next-ticket request, fetch live issues and project Status using the selection skill's paginated queries. Surface off-board and untriaged issues; no missing metadata may masquerade as a ready backlog.
2. Exclude closed issues, Epics, In progress/In review work, open dependencies, explicit non-issue blockers and work outside the current phase. An Epic can be a decomposition proposal, not an automatic implementation. Unknown blocker/status information means uncertain eligibility.
3. Match AI fit and Size to the session. In autonomous mode, shortlist Agent-ready work only. Pair/Human-led work can be proposed for collaboration, not silently converted to autonomous work. Prefer an applicable active milestone, then Priority. Within that, explain which verified blocker the task removes; prefer a bounded smaller slice when value is comparable, and use issue number as the final neutral tie-break.
4. Read shortlisted issue bodies, comments, dependency resolutions and linked artifacts. Confirm the premise against current code/spec. A high-priority stale issue must be narrowed or re-triaged rather than implemented verbatim.
5. Recommend one ticket, its expected artifact and goal contribution, with any genuine prerequisite. Do not start, assign or change Status for a recommendation-only request. If nothing is eligible, identify the specific triage/decomposition/decision needed instead of starting Stage 2 or collecting arbitrary facts.

## GitHub operations

Use installed `gh` help to check supported options. The repository and board are explicit in every command. Initial diagnostics:

```bash
gh repo view uncovering-world/travel-regions-extraction --json nameWithOwner,hasIssuesEnabled
gh api orgs/uncovering-world/issue-types
gh api orgs/uncovering-world/issue-fields
gh project field-list 3 --owner uncovering-world --format json
```

Create a body in an ephemeral file with an editor/apply_patch and pass `--body-file`; do not interpolate untrusted issue text into a shell command. Example shapes below use `NUMBER`, `TITLE` and `/absolute/path/to/draft.md` as placeholders, not real resources:

```bash
gh issue create --repo uncovering-world/travel-regions-extraction --type Task --title 'TITLE' --body-file /absolute/path/to/draft.md
gh project item-add 3 --owner uncovering-world --url https://github.com/uncovering-world/travel-regions-extraction/issues/NUMBER
gh project item-edit 3 --owner uncovering-world --url https://github.com/uncovering-world/travel-regions-extraction/issues/NUMBER --field Status --value Backlog
```

Read current org field IDs and allowed option names before setting native issue fields. POST `repos/uncovering-world/travel-regions-extraction/issues/NUMBER/issue-field-values` with `{"issue_field_values":[{"field_id":ID,"value":"OPTION NAME"}]}` using `gh api --method POST --input /absolute/path/to/payload.json`. Only submit the fields being changed. Do not hardcode option IDs from another repository or create board-local duplicates. Read back the values with GET at the same endpoint. Use `gh issue edit --parent`, `--add-blocked-by` and `--milestone` for applicable relationships, and verify them.

Board placement, metadata writes and issue creation are separate operations. If a create times out, search recently created issues by body/title/author before retrying. If placement or field setting fails, retry that operation for the **existing issue**, never create another issue. Report what actually succeeded and the remaining repair; do not request token-scope changes silently. A failed board read means Status is unavailable, not that the board is empty. Selection can report issues in degraded read-only mode but cannot certify them ready.

No cron, paid AI worker, automatic assignment, mass issue generation or issue-body-triggered code execution is installed by this workflow. Commit/push/PR and deployment actions still need the user's relevant authorization.

## Evidence-producing and normative tickets

Evidence proposals need source versions/locators, applicability, dates, exceptions and distinct candidate/verified states. Schema validation and LLM confidence are not source entailment. Unknowns are valid outputs. Human verification is review of external evidence, not an oracle of preferred final regions.

A model ticket may recommend a rule with generic counterexamples and required spec patches. Adoption requires an explicit normative decision and matching spec/decision changes; research completion alone does not adopt CR-J, close residual Q questions or weaken D004–D007. A future paid pilot needs a separate scope and maximum-spend approval. Research comparing prices is not spending authorization.

## Skills and validation

The three project skills live under `.agents/skills/` so they travel with this repository. `AGENTS.md` routes to them and holds shared invariants; the skills hold only their specific workflow. Their creation follows the skill-creator guidance to avoid duplicate policy and unnecessary scaffolding. Repo-local discovery and progressive disclosure follow [official skills documentation](https://learn.chatgpt.com/docs/build-skills); project instruction discovery follows [official AGENTS.md documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md). If a skill does not appear, restart the session or read the linked file directly; no global install is required.

After a skill change, validate YAML frontmatter and optional UI metadata, local reference paths, the issue form and live read-only queries. When available, run the installed skill-creator's `scripts/quick_validate.py` for each skill. Also simulate selection for blocked, off-board, untriaged, stale, Epic, Pair-only and out-of-phase tickets; do not publish test issues. These checks verify packaging and workflow coverage, not guaranteed autonomous agent behaviour.

Use the repository checks in [AGENTS.md](../AGENTS.md) for delivery. Record outcomes on the ticket, link durable artifacts, distinguish implemented from proposed and leave an honest handoff. If the user has not requested publishing local changes, report that boundary rather than marking them delivered.
