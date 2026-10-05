# Claim activity: how recent must a claimant's official step be?

## Question

D070 makes a paper claim with resident civilians a region only while the claimant presses it, by an official step (a law, an official map, a case before a court, a protest or letter to an international body, a statement of its government) within the last N years; otherwise it is a special place. Q021 asks for N. Which N separates claims that are pressed today from dormant ones, without making a pressed claim flicker between region and special place across yearly releases (R055)?

Population: the register's areas of kind `paper_claim` whose `inhabited` is `yes` or unknown (36 on 2026-10-05; first written as 33 by mistake). Profile: `S1-product-v1` (R057), with D064–D070.

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

Run of 2026-10-05: 654 official steps for 34 of the 36 claims (`inputs/steps.csv`, collected by three research agents, every passage checked on its page; 2 claims of Libya have no step found at all). Coverage is uneven: the agents' shared web-search budget ran out, so some claims are under-collected (see each part's notes, kept outside the repository), and some rows only say that a dispute exists or come from weak speakers (interviews, a spokesman).

Test 1, a step in the last N years (`by_N` in `outputs/summary.json`): claims pressed at the 2025 release and status changes 2005–2025 — N=3: 26 and 63; N=5: 28 and 41; N=10: 30 and 25; N=15: 33 and 12; N=20: 33 and 11. Olivenza is pressed under every N: Portugal's defence minister said in September 2024 that the state does not recognise it as Spanish territory, and a ministry answered parliament on the nationality of people born there.

Test 2, steps in at least K distinct years of the last N (`frequency_test`): with N=10 and K=2, 26 claims are pressed at 2025; not pressed: Olivenza (one year with a step in 2016–2025), Ceuta and Melilla (Morocco: 2006, 2007, 2020, 2026, mostly interviews and a spokesman), North Korea claimed by the South (its own ISO entry anyway), Heglig, Ilemi, KaNgwane and Ingwavuma, Noktundo and the two Libyan claims. With K=3, also Junagadh, the Estonian claim, the Saudi–UAE border, the Republic of China's legacy claims and the 1949 no-man's-lands; with K=4, also Sakteng.

## Conclusion

A single "step within N years" does not separate Olivenza from pressed claims: a claimant that rarely acts can still make a statement in a given year. A frequency test does: steps in at least two distinct years of the last ten keeps every claim raised most years a region and makes Olivenza, Ceuta, Melilla and the long-silent claims special places. This is a proposal for Q021; it changes D070's test from "a step within N years" to "steps in K of the last N years", which is the owner's decision.

## Status

Concluded 2026-10-05 (first run); waiting for the owner's choice of the test.
