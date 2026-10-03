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

## Method

`run.py` (Python ≥ 3.11, standard library). From the repository root:

```bash
python3 experiments/settling-rule/run.py
```

Sources, pinned with URL, version and checksum in `inputs/sources.json` and fetched into `cache/`:

- **Seizures by states.** The Modern Conquest dataset v3.0 (Dan Altman; replication files of *Taking Territory: The Persistence of Conquest Since 1945*), conquest attempts 1918–2024. A conquest attempt is a military seizure of disputed territory "with the intention to assume lasting control", recognised by a sovereignty claim and a fixed position; raids, interventions and peacekeeping are excluded (codebook). Used: the 78 initial attempts from 1946 on whose outcome is coded (the 2022 invasion of Ukraine is not), with the year of seizure, the year the territory was lost (`HELDUNTIL`) and how (`LOSSTYPE`).
- **Breakaway entities.** Table 2 of Florea 2020, "Rebel governance in de facto states" (*EJIR* 26(4), p. 1016): 40 de facto states 1945–2016 with year of emergence, year and type of disappearance, transcribed in `inputs/defacto_states.csv`. Every entity in it existed for at least 24 months by definition, and the table ends in 2016.
- **Years of fighting.** UCDP/PRIO Armed Conflict Dataset v26.1: a year is not quiet for an area if a linked conflict over territory has a conflict-year (25 or more battle-related deaths).
- **Links from areas to conflicts.** A seizure is linked to every interstate conflict over territory in which the two states are primary parties on opposite sides (by country code, automatically). `inputs/links.csv` adds, by conflict id and with the basis stated, the conflicts UCDP codes against a non-state side: Western Sahara, East Timor and the breakaway entities. 49 of 78 seizures and 35 of 40 entities have a link; for the rest every year counts as quiet.

The rule is applied year by year (`simulate`): the year of the seizure never counts; each later full calendar year adds one to the clock if quiet and sets it to zero if not; the canon accepts the new holder in the year the clock reaches T; after that, fighting is only a flag. The same is run with all years treated as quiet ("plain clock") for comparison.

Not modelled, and why it matters:

- The rule's other guards. The conquest dataset's definition stands in for "asserts the area as its own". Nothing stands in for "a standing civil arrangement", which can only delay acceptance.
- The return path. A retake years later by the earlier holder (Azerbaijan in 2016, 2020, 2022 and 2023) is a new seizure in the dataset and waits T here; under the rule it would be taken over at once.
- Precision. Years only: "T" means between T and T+1 years of holding.
- The link by pair of states is coarse: all fighting between India and Pakistan over Kashmir stops the clock for Siachen and for the Rann of Kutch alike. UCDP codes some wars as being about government, not territory (southern Sudan 1983–2004), so their years count as quiet.

## Result

Outputs: `outputs/summary.json` (all counts and case lists), `outputs/seizures.csv`, `outputs/breakaways.csv`, `outputs/showcase.csv` (year-by-year tracks for the cases named in `inputs/showcase.csv`).

**Seizures by states, 1946–2024** (78; 44 ended, 34 still held). They ended 0 years after the seizure year in 26 cases, 1 year in 7, 2 in 2, 3 in 2, and then after 6, 9, 9, 15, 15, 24 and 29 years.

| T | Accepted | Later undone | of which by force | Ended before acceptance | Still unsettled at the end of 2024 | Unsettled territory-years |
|---|---|---|---|---|---|---|
| 1 | 45 | 11 | 3 | 33 | 0 | 82 |
| 2 | 42 | 9 | 2 | 35 | 1 | 130 |
| 3 | 39 | 7 | 1 | 37 | 2 | 197 |
| 5 | 35 | 6 | 1 | 38 | 5 | 286 |
| 10 | 26 | 2 | 0 | 42 | 10 | 486 |

**Breakaway entities, 1945–2016** (40; 12 reintegrated, 4 became states, 24 alive in 2016).

| T | Accepted | Later reintegrated by force | by agreement | Became states | Ended before acceptance | Still unsettled in 2016 | Unsettled territory-years |
|---|---|---|---|---|---|---|---|
| 1 | 32 | 3 | 5 | 4 | 4 | 4 | 241 |
| 2 | 29 | 2 | 5 | 3 | 6 | 5 | 305 |
| 3 | 25 | 1 | 4 | 3 | 8 | 7 | 371 |
| 5 | 20 | 1 | 3 | 2 | 10 | 10 | 444 |
| 10 | 17 | 1 | 3 | 1 | 11 | 12 | 593 |

**What each step in T decides differently** (accepted at the shorter wait, not at the longer):

| Step | Accepted changes it avoids that were later undone | Areas it leaves unsettled that are still held |
|---|---|---|
| 1 → 2 | Sumdorong Chu (India 1984, lost by force 1986); Ras Doumeira (Eritrea 2008, mediated withdrawal 2010); Tamil Eelam (accepted 2002 after one quiet year, defeated 2009) | Azawad; Nagorno-Karabakh retaken in 2023 |
| 2 → 3 | Buraimi (Saudi Arabia 1952, expelled 1955); Hanish Islands (Eritrea 1995, arbitration 1998); Chechnya (accepted 1993, reintegrated by force 1999); Eastern Slavonia (accepted 1997, reintegrated by agreement 1998) | Mindanao; Gaza; Farukh (2022) |
| 3 → 5 | East Timor (accepted 1991 after three quiet years; Indonesia withdrew in 1999); Gagauzia (accepted 1994, reintegrated by agreement 1995) | Ladakh (part, 2020); al-Fashaga (2020); areas retaken by Azerbaijan in 2020; Karen State; Palestine; Cyrenaica |
| 5 → 10 | Preah Vihear (Thailand 1953, ICJ ruling 1962); Sinai (Israel 1967, handed back by 1982); Thule Island (Argentina 1976, retaken 1982); Sumdorong Chu (China 1986, mutual pullback 1995) | Crimea; Siachen; the Bhutanese valleys held by China since 2015; Doumeira (2017); Nagorno-Karabakh (never ten quiet years in a row between 1991 and its retaking in 2023); Casamance |

**Accepted changes undone by force, both sets together:** four at T=2 (Buraimi, Thule Island, Chechnya, Anjouan), two at T=3 and at T=5 (Thule Island, Anjouan), one at T=10 (Anjouan, accepted 2007 and retaken 2008).

**The two clocks.** At T=2 the quiet-years clock gives a different acceptance year than the plain one for 6 of 78 seizures (among them Western Sahara: 1991, not 1977; Sinai: 1972, not 1969; East Timor: 1990, not 1977) and for 25 of 40 breakaway entities. With the plain clock every entity in Florea's table is accepted at T=2 and sixteen later end, six of them by force.

**The picture at the end of 2024.** Among the areas still held, T = 1, 2 and 3 leave nothing unsettled except areas Azerbaijan retook in 2022–2023, which the rule's return path takes over at once. T=5 also leaves the part of Ladakh held by China since 2020 and al-Fashaga (Sudan, 2020) unsettled, both due at the end of 2025 if still held and quiet. T=10 leaves in addition Crimea (seven quiet years, then fighting since 2022), Siachen (never ten quiet years in a row), the valleys China holds in Bhutan (2015) and Doumeira (2017).

## Conclusion

A proposal for the owner's decision, not a rule.

Against what was written beforehand:

1. *Not met as written.* Raising T from 2 to 5 removes three later-undone acceptances among seizures by states (Buraimi, Hanish Islands, East Timor), not fewer than three. Two of the three are already removed at T=3.
2. *Met.* Undoing by force is rare after acceptance: 2 of 42 at T=2, 1 of 39 at T=3. The others ended by ruling, agreement or withdrawal 1 to 13 years after acceptance (and one island sank). No waiting time anticipates those; they need the path for agreed changes.
3. *Not met; one T is tenable.* With the quiet-years clock, breakaway entities accepted at T=2 were later reintegrated in 7 of 29 cases, seizures by states undone in 9 of 42. Without the clock the entities would look far worse.
4. *Largely met.* For T from 1 to 3 the picture at the end of 2024 is the same; T=5 differs by two border areas for one more year.
5. *Met for breakaway entities, limited for seizures.* The link from areas to conflict records has to be a maintained input of the register.

What the record supports:

- **T=1 is too short**: it accepts six changes that force later undid (three seizures, three entities), one of them in the year after acceptance.
- **The step from 2 to 3 is the last that removes reversals by force** (Buraimi, Chechnya). From 3 on, an accepted change was undone by force twice in eighty years, the same two cases at T=3 and T=5.
- **Steps beyond 3 buy little and cost more**: T=5 adds two years of unsettled status to every accepted change to avoid two changes that ended by agreement; T=10 leaves Crimea and Siachen unsettled and never accepts Nagorno-Karabakh in its thirty-two years.
- **The numbers are small.** Each step rests on two to four cases, year precision shifts cases across a boundary, and each population comes from one author's dataset. The record separates 1 from 3 and 3 from 10 clearly; it does not separate 2 from 3 sharply.

It does not show that any waiting time makes a change final, and it says nothing on legality.

## Status

Concluded 2026-10-03.
