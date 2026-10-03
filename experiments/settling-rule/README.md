# Back-test of the settling rule for contested areas

**Experiment, not the canon.** Issue: [#20](https://github.com/uncovering-world/travel-regions-extraction/issues/20) (release stability).

## Question

The owner proposed a separate status for territories whose control is in flux, and asked for a stronger basis for the waiting time than "another list uses five years", and to see what different waiting times would do to the canon.

The rule under test (a proposal, not adopted):

- An area whose control passes by force to a party that asserts it as its own, or as a separate entity, becomes **unsettled**. The canon keeps the last settled attribution and says who holds the area.
- If control returns to the party the canon attributes the area to, the area is settled again and the canon never changed.
- If the new holder keeps the area for **T consecutive quiet years** — calendar years with no active armed conflict over it — the canon accepts the new holder.
- A change that the parties agree on, or that follows a ruling they accept, is taken over at once.

For T = 1, 2, 3, 5 and 10:

1. On the record since 1946, how many forcible changes of control would the canon have accepted, how many of those were later undone and how (by force, or by ruling, settlement or withdrawal), and for how long would areas have been unsettled?
2. Do seizures by states and breakaway entities behave alike?
3. Which concrete cases does each step in T decide differently?
4. What does the world look like at the 2026 release under each T?

Assumes: the state machine above (pending); the definition of "administers" agreed in principle on 2026-10-03 (the party controlling civilian access); one release per year reflecting the situation at the end of that year. No cells are produced; this is not a partition run.

## Related

Q007, Q008; R031; [release stability proposal](../../docs/proposals/release-stability.md); [control-duration experiment](../control-duration/README.md), which measured durations and recurrence but did not run a rule; register kinds `occupied_or_annexed` and `de_facto_state` in [data/disputed-areas](../../data/disputed-areas/README.md).

## What would change our mind

Written before the first run. Known beforehand: the literature review done for this question had already tabulated, in the same conquest dataset, how many years after the seizure territories were lost. Part 1 for seizures by states is therefore a re-computation under a stated convention, not a blind test. The quiet-years clock, the breakaway entities, the case lists and the 2026 picture had not been computed.

1. **Waiting longer than about two years is not supported for seizures by states** if raising T from 2 to 5 removes fewer than three later-undone acceptances since 1946 while every accepted change waits three years longer.
2. **A longer T is the wrong tool for late reversals** if acceptances undone by force are rare at every T ≥ 2 and the rest are undone by ruling, settlement or withdrawal. Those need the "agreed change" path, not more waiting.
3. **One T for both kinds is not supported** if breakaway entities are undone after acceptance markedly more often than seizures by states at the same T.
4. **The choice between 2 and 5 is not about today's map** if the 2026 picture is the same for every T in that range. Then it is about how fast the canon follows the next change.
5. **The link to conflict data is material** if the quiet-years clock and the plain years-since-seizure clock give different acceptance years for many of the linked cases. Then the link from areas to conflict records has to be a maintained input of the register.

Conventions fixed before the run:

- Year precision. With a seizure in year y, the canon accepts at the end of the first year in which the holder has held the area through T consecutive full calendar years after y, all of them quiet. The holder has then held it for between T and T+1 years.
- A year is not quiet if the linked conflict has a conflict-year in the UCDP/PRIO Armed Conflict Dataset (at least 25 battle-related deaths).
- Ways of losing a seized area, from the conquest dataset's LOSSTYPE: by force (1, 2), under pressure (3, 4), by ruling, settlement or withdrawal (5, 6, 7), other (8).

## Status

Planned (2026-10-03).
