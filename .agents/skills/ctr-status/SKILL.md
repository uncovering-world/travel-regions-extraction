---
name: ctr-status
description: Use when a session on the Canonical Travel Regions repository starts, when the owner asks where the project stands or what to do next, or when a piece of work has ended and progress should be saved for the next session.
---

# Orient and save progress

`docs/status.md` is the hand-off between sessions: focus, decisions waiting for the owner, active experiments, next step. It lists only what is live — history lives in git, `docs/decisions.md` and closed issues.

## Orient

1. Read `docs/status.md`.
2. `git status -sb` — uncommitted work and commits not yet pushed. Then `git log --oneline "$(git log -1 --format=%h -- docs/status.md)"..HEAD` — what happened since the status was last saved.
3. `gh issue list --repo uncovering-world/travel-regions-extraction --state open --json number,title,updatedAt --limit 50`. For every issue the status cites, check that it is open and that its title still matches the item.
4. Read board Status only when the status lists active work or something may be In progress (`ctr-issue`, `references/project.graphql`).
5. Answer briefly: current focus; what waits for the owner's decision; active experiments; **one** recommended next step and why. Name at most the three most consequential mismatches between status, repository and tracker, and offer the rest.

A recommendation is not a start signal — wait for the owner to pick. Uncommitted or unpushed work that this session did not create: report it and ask before committing it.

## Save progress

At the end of a piece of work, or when asked:

1. Rewrite `docs/status.md` in place, one screen at most: date, focus, pending decisions (with issue links), active experiments (path and state), next step. Drop finished items instead of marking them done.
2. Commit `docs(status): <what changed>` and push.

## Common mistakes

- Reporting from memory instead of reading the files and the tracker.
- Turning the status into a backlog or a changelog.
- Leaving the status stale after a decision or an experiment concluded.
