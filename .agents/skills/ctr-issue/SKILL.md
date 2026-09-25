---
name: ctr-issue
description: Use when creating, updating, pausing or closing a GitHub issue of uncovering-world/travel-regions-extraction, or when reading or changing its Status on the Canonical Travel Regions board (org project 3).
---

# Issues and board

Repository `uncovering-world/travel-regions-extraction` (`R` below); board = org `uncovering-world` project **3**. Always pass `--repo` / `--owner`. Never touch the Track Your Regions repository or its project 2, and never change org-wide field definitions. All text in English. Temporary files go to `mktemp` or a scratch directory, never into the working tree.

An issue is for work that spans sessions or must not be forgotten; quick questions live in `docs/status.md`.

## Create

1. Search with distinctive terms: `gh issue list --repo R --state all --search "<terms> in:title" --json number,title,state`. Update an existing issue rather than duplicating it.
2. Body in a temp file, sections of `.github/ISSUE_TEMPLATE/task.yml`: **Description** (problem and why it matters), **Requirements** (checkboxes), **Additional Information** (related R/D/Q, dependencies, non-goals if useful). Concise, no boilerplate.
3. Create under the roadmap and keep the number:
   `url=$(gh issue create --repo R --type Task --title "<title>" --body-file "$body" --parent 4); n=${url##*/}`
   Type Bug only for a contract violation; #4 is the only Epic.
4. Board: `gh project item-add 3 --owner uncovering-world --url "$url"`, then
   `gh project item-edit 3 --owner uncovering-world --url "$url" --field Status --value Backlog`
   (New if scope is still unclear; In progress if starting now).
5. Native fields — `gh api orgs/uncovering-world/issue-fields` gives field ids and option names. Priority and Size always; AI fit when obvious; Theme options are the shared TYR product areas, so leave it unset for spec, decision and research work. Several fields go in one request; fields left out are not cleared; values are option **names**:
   `f=$(mktemp); echo '{"issue_field_values":[{"field_id":30515534,"value":"High"},{"field_id":46404581,"value":"Medium"}]}' > "$f"`
   `gh api --method POST repos/R/issues/$n/issue-field-values --input "$f"`
6. Only real dependencies: `gh issue edit $n --repo R --add-blocked-by <m>`.
7. Read back: `gh api repos/R/issues/$n/issue-field-values --jq '.[] | "\(.issue_field_name)=\(.single_select_option.name)"'` and `gh issue view $n --repo R --json issueType,parent,projectItems`.
8. If the issue is a live item, link it from `docs/status.md`.

If a create call fails or times out, search for the issue before retrying — never create a duplicate.

## Progress, pause, close

- Comment when something durable happens: a result, a decision, a blocker. Not per step.
- Tick requirement boxes that are actually met.
- Done: `gh issue close $n --repo R --reason completed --comment "<what, with links to commits or artifacts>"`.
- Pause: `--reason "not planned"` with a comment saying why and when to reopen.

## Reading the whole board

From the repository root:
`gh api graphql --paginate --slurp -F query=@.agents/skills/ctr-issue/references/issues.graphql` (open issues with fields, parents, blockers)
`gh api graphql --paginate --slurp -F query=@.agents/skills/ctr-issue/references/project.graphql` (board items with Status)
Join them by issue URL. `--paginate` follows only the outer connection. A failed board read means Status is unknown, not that the board is empty.
