# How long do territory-specific entry regimes last?

**Experiment, not the canon.** Issue: [#20](https://github.com/uncovering-world/travel-regions-extraction/issues/20) (release stability).

## Question

Under CR-W (R044) a part of a country becomes a region when entry to it follows other rules than the rest: a regional visa exemption, a special-area permit, separate immigration control. Such regimes appear, change and end, and nobody contests them. The [release stability proposal](../../docs/proposals/release-stability.md) offers four policies for when a regime enters and leaves a release; its recommendation (a regime must be in force at two consecutive yearly cut-offs) rests on a handful of examples.

Measured here, on regimes that started in 2000 or later, including those that have ended: for a policy that admits a regime only after it has been in force at N consecutive yearly cut-offs (N = 1, 2, 3),

1. how many regimes would have entered a release and left again within five years,
2. how many years real, lasting regimes would be held back, and
3. whether early endings are announced in advance (a stated expiry date, a pilot).

No proposal is assumed; the four options of the release stability proposal are the candidates. Profile: none; no cells are produced.

## Related

R031, R044 (G-TIME); Q008, Q010; [settling-rule back-test](../settling-rule/README.md), which answered the same question for contested control; the regimes collected for the [world Stage 1 draft](../stage1-world-draft/README.md).

## What would change our mind

Written before any data was collected. Known beforehand, from the 105 regimes of the world Stage 1 draft: of 54 in force with a known start year, six are at most two years old and nine at most five; 41 of 105 are marked as changed within ten years, but that mark mixes changes of detail with regimes appearing and ending, and the collection holds only three regimes that have ended.

1. **A plain snapshot is enough** if fewer than a tenth of new regimes end or are suspended within two years of starting.
2. **One extra cut-off is justified** if a fifth or more end or are suspended within two years; **two** if the share that ends between the second and the third year is still about as high.
3. **Waiting is the wrong tool** if most early endings were announced when the regime started (a stated expiry, a pilot). Then the rule's own stated duration says more than its age.
4. **A regime that ends should leave slowly** if suspended regimes commonly come back within two years (Jeju's waiver was suspended from February 2020 to June 2022); if they rarely do, exit can mirror entry.

The collection will be biased towards regimes that still exist and towards well-documented countries; how each regime was found is recorded so the bias can be described.

## Method

```bash
python3 experiments/regime-lifetimes/run.py
```

- **Data.** `inputs/regimes.csv`: 59 regimes collected from sources on 2026-10-03 by research agents, 39 from the leads of the world Stage 1 draft and 20 from searches for ended regimes. Every start, end, resumption and stated expiry carries its source and a quoted passage; the collectors' check found all 150 passages in the saved source texts. **Not checked again here**: the passages were not re-opened, and that a date follows from its passage was not read row by row. Evidence: 20 primary, 39 secondary. Six rows are local border traffic schemes for border residents.
- **Measure.** Year precision. For the 55 regimes that started in 2000 or later: years from start to the first ending or suspension. The closures of early 2020 are one shock, so every count is given with and without them.
- **Policy.** A regime enters a release once it has been in force at N consecutive year-end cut-offs; counted: how many enter, and how many of those end or are suspended within five years of entering.

## Result

| | All endings | Without the 2020 closures |
|---|---|---|
| Ended or suspended, of 55 | 23 | 12 |
| within the starting year or the next | 6 | 4 |
| within 2 years | 6 | 4 |
| within 5 years | 12 | 6 |
| within 10 years | 17 | 9 |

| Cut-offs N | Enter | Leave within 5 years of entering | without the 2020 closures | Too recent to tell |
|---|---|---|---|---|
| 1 | 53 | 10 | 4 | 0 |
| 2 | 45–47 | 7 | 2 | 4 |
| 3 | 41–43 | 9 | 3 | 8 |

- The four early endings outside 2020 are three area restrictions withdrawn within months (Chittagong Hill Tracts 2015, northern Sri Lanka 2014–15, Gilgit-Baltistan 2017) and one border card whose issuance was paused for nine months. None had a stated expiry.
- Ten regimes had a stated expiry or were pilots; most outlived it (the Kaliningrad 72-hour visa "experiment" ran from 2002 to 2016, the one-year exclusion of Manipur, Mizoram and Nagaland for fourteen years). For 43 it is unknown.
- Sixteen suspensions, twelve of them in 2020; ten resumed, after 0 to 4 years, most after 2 to 3.

## Conclusion

A proposal, not a rule.

1. *Met, narrowly.* Outside 2020, 4 of 55 new regimes (7%) ended or were suspended within two years, under the tenth set beforehand. A plain snapshot would have admitted four regimes that left within five years; a second cut-off halves that to two at the price of a year's delay for all. The collection under-counts ended regimes, so the true share is higher by an unknown amount.
2. *Not met.* Nothing supports a third cut-off: it admits no fewer short-lived regimes than the second.
3. *Not met.* Early endings were not announced, and stated expiries were mostly outlived: a rule's stated duration is a poor guide.
4. *Met.* Suspended regimes usually come back within two to four years, so a suspension should not remove a boundary at once.

The sample is small and biased towards regimes that still exist and towards well-documented countries.

## Status

Concluded 2026-10-03.
