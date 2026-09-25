---
name: ctr-issue-select
description: Inspect the live Canonical Travel Regions GitHub backlog and recommend the next bounded ticket by phase, dependencies, priority, capacity and AI fit. Use for choosing work or backlog status, not automatically starting or mutating issues.
---

# Select the next useful issue

Read [AGENTS.md](../../../AGENTS.md) and [docs/workflow.md](../../../docs/workflow.md), especially mission-directed selection and current phase limits. Selection is read-only unless triage or execution was also requested. Do not claim/assign tickets, change Status or create follow-ups for a list/recommendation request.

## Read live state

Read both query files fully before running them from the repo root:

```bash
gh api graphql --paginate --slurp -F query=@.agents/skills/ctr-issue-select/references/issues.graphql
gh api graphql --paginate --slurp -F query=@.agents/skills/ctr-issue-select/references/project.graphql
```

The first reads this repository's issues and native metadata; the second reads project **3** only. Join by full issue URL, not issue number across repositories. Both paginate their outer connection. Nested connections expose `pageInfo`: if any is truncated, retrieve that connection's remaining pages before deciding that metadata or blockers are absent. Native `issueDependenciesSummary.blockedBy` counts open blockers even if their node list is incomplete.

Reconcile **every** open repo issue against the board; report missing placement and metadata. An archived project item is not an active Backlog placement: surface it for triage, do not select it from a stale Status. If either read fails, explicitly describe the unavailable fields. An unreadable board is not an empty board; unknown Status or blockers cannot make work eligible. Read an applicable milestone's full counts separately if reporting progress; an open-only issue query is not a closed count.

For shortlisted issues, read the full body and current discussion:

```bash
gh issue view NUMBER --repo uncovering-world/travel-regions-extraction --json body,comments,issueType,parent,subIssues,blockedBy,milestone,assignees,url
gh api --paginate repos/uncovering-world/travel-regions-extraction/issues/NUMBER/comments
```

The REST comments read covers discussions longer than a CLI summary. Read dependency resolutions and linked artifacts, not just closed flags. Check recent associated PRs before claiming the work is unstarted. Confirm premises against current repository state.

## Recommend, do not take over

Apply the workflow's selection order: current user request; current phase; actual blockers; Status; AI fit/capacity; applicable milestone; Priority; justified goal contribution and bounded effort. Exclude Epics, active/review work and missing metadata from the ready shortlist. Offer decomposition/triage as such; do not quietly execute the umbrella. Stage 2 and world-partition tasks remain out of phase regardless of priority. A Pair or Human-led ticket is not an autonomous pick.

Recommend one issue with its artifact, goal contribution, scope, tests and any remaining decision. Briefly identify the most relevant excluded alternative and why when it aids the choice. If none is ready, name the smallest missing triage/decision instead of inventing a fact-gathering task. Re-read the chosen ticket immediately before starting if the user also authorized execution; then use the delivery skill.
