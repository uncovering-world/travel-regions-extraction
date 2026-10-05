# Claim activity: how recent must a claimant's official step be?

## Question

D070 makes a paper claim with resident civilians a region only while the claimant presses it, by an official step (a law, an official map, a case before a court, a protest or letter to an international body, a statement of its government) within the last N years; otherwise it is a special place. Q021 asks for N. Which N separates claims that are pressed today from dormant ones, without making a pressed claim flicker between region and special place across yearly releases (R055)?

Population: the register's areas of kind `paper_claim` whose `inhabited` is `yes` or unknown (33 on 2026-10-05). Profile: `S1-product-v1` (R057), with D064–D070.

## Related

D070, Q021; R051, R055; D067 (secondary sources allowed, marked), D068 (a claim counts until renounced by an act in force). Issue #22.

## What would change our mind

- If the gaps between consecutive official steps of claims that are plainly pressed (the claimant raises them every year at the UN, or maps them in law) are often longer than the N that excludes the plainly dormant claims, no single N separates them, and D070 needs a different test (for example a minimum count of steps, or the kind of step).
- If most claims cannot be dated (no official step found with a source), the test is not workable on the current evidence, whatever N is.
- If the result depends on a few steps of doubtful kind (a minister's remark, a parliamentary question), the list of steps that count must be narrowed before choosing N.

## Method

1. For each claim in the population, collect the claimant's official steps since 2000 (and the latest step before 2000 if none after), each with its date, kind, source URL and verbatim passage (`inputs/steps.csv`). Steps by the claimant's government, legislature, courts or official cartography only; statements by others about the claim do not count. Collected by research agents and reviewed; an unverified step is marked.
2. `run.py` computes, for each claim, the years with a step, the longest gap between consecutive steps, and the years since the latest step; and for N in 3, 5, 10, 15 and 20, the claims that are regions at each yearly release from 2005 to 2025 and the number of times each claim changes status between consecutive releases (flicker).
3. A good N keeps every claim with steps in most years a region at every release (no flicker) and makes the claims without a step for a long time special places.

Reproduce: `python3 experiments/claim-activity/run.py`

## Result

Pending.

## Conclusion

Pending.

## Status

Planned (2026-10-05).
