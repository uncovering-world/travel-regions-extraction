# How long does a change of control take to settle?

**Experiment, not the canon.** Issue: [#20](https://github.com/uncovering-world/travel-regions-extraction/issues/20) (release stability).

## Question

The owner agreed in principle that a contested strip goes with whoever administers it, and asked how long such control must last before the canon follows it — a short military presence (Ukrainian forces in Sudzha, August 2024 to March 2025) must not count. Candidates on the table: 2 years (owner), 5 years (NomadMania's minimum for disputed populated territory), 1 year (one release interval). The owner also proposed an intermediate status for territories in flux, reviewed after the waiting time.

Empirically: when control over a territory changes by force, how long is it before one can tell that the change will last? For a waiting time T:

- what share of such changes has already ended before T (and is correctly kept out of the canon), and
- of those still in place at T, what share ends within the following ten years (the canon would have followed and then had to go back)?

No proposal is assumed. The experiment uses military occupations as the observable: they have recorded start and end years. It says nothing about legality.

## Related

R015, R024, R031, R044 (G-TIME); Q007, Q008; [release stability proposal](../../docs/proposals/release-stability.md); register kinds `occupied_or_annexed`, `de_facto_state`, `line_position`, `no_agreed_boundary` in [data/disputed-areas](../../data/disputed-areas/README.md).

## What would change our mind

Written before the first run.

1. **Two years is enough** if most occupations that end do so within about two years, and of those that reach two years few (under about a fifth) end within the following ten.
2. **Five years is the defensible wait** if a substantial share (about a third or more) of those that reach two years still end before five, while few of those that reach five end within the following ten.
3. **No waiting time works** if the share that ends in the following ten years is about the same whatever the age already reached. Then time alone does not separate settled from unsettled, and an "unsettled" status has to rest on something else (hostilities over, an agreed line).
4. World-war occupations (starting 1914–1918 and 1939–1945) may behave differently from the rest; they are reported separately, and the post-1945 pattern is the one that matters for the canon.

## Method

`run.py` (Python ≥ 3.11, standard library). From the repository root:

```bash
python3 experiments/control-duration/run.py
```

- **Source.** Wikipedia's "List of military occupations" at revision 1377366365 (read 2026-10-03), fetched through the MediaWiki API into `cache/`; the checksum of the fetched page is in `outputs/summary.json`. The list covers occupations since the Hague Convention of 1907: 207 rows with start and end years, of which 77 start in 1946 or later. It is a tertiary source compiled by editors; its rows are not a designed sample and several rows can belong to one war.
- **Duration.** Only years are given, so the measure is the span `end year − start year`; the true duration is within a year of it. "Reaches T" means a span of at least T. Occupations in the list's "ongoing" table are counted as continuing in 2026.
- **Annexations.** For the eleven occupations since 1946 that the list marks as subsequently annexed, the listed end year is the year of annexation, not necessarily the end of control. `inputs/annexed_outcomes.csv` records for each, with a source and the passage it rests on, whether the annexing state still holds the territory. Seven do (Junagadh, Hyderabad, Tibet, Dadra and Nagar Haveli, Goa, Aksai Chin, southern Vietnam) and are counted as continuing; four do not (the West Bank under Jordan, East Timor, Kuwait, the districts around Nagorno-Karabakh) and end in the listed year.
- **Estimates.** Shares that take continuing cases into account are product-limit (Kaplan–Meier) estimates in whole years.
- Eras are reported separately: occupations starting in 1914–1918 and 1939–1945 (world wars), other occupations before 1946, and those starting in 1946 or later, which the conclusions use.

## Result

Occupations starting in 1946 or later: 77, of which 52 ended and 25 continue.

| Waiting time T | Already ended before T | Of those that reach T: end within the next 5 years | … within the next 10 years |
|---|---|---|---|
| 1 year | 17% | 32% | 40% |
| 2 years | 32% | 18% | 30% |
| 3 years | 36% | 15% | 26% |
| 5 years | 43% | 7% | 17% |
| 10 years | 47% | 11% | 31% |

- **A burst, then a trickle.** Of the 52 that ended, 25 ended with a span of 0 or 1 year. The other 27 endings are spread over spans of 2 to 32 years, about one per year of age; long occupations also end (Sinai after 15 years, southern Lebanon 18, Czechoslovakia 21, East Timor 24, Syria in Lebanon 29).
- **What ends between two and nine years** is, in this list, military intervention without annexation: Russia in northern Ukraine and Ukraine in Russia's border oblasts (the Sudzha case; a span of 2 at year resolution, seven months in fact), Perevi, India in Sri Lanka, Ethiopia in Somalia, the Congo war, Mauritania's part of Western Sahara, Turkey's zones in northern Syria.
- **Annexation predicts permanence better than age does.** Of the eleven annexations since 1946, one (Kuwait) was undone within a year; none of the other ten ended before 19 years, and seven are still held. Among occupations without annexation, 38% of those that reach two years end within the following ten, and 23% of those that reach five.
- **World wars differ.** Occupations starting in 1914–1918 have a median span of 3 years and those starting in 1939–1945 of 4: they end when the war ends.

Per-row data are in `outputs/occupations.csv`.

## Conclusion

Against "what would change our mind":

1. *Two years is enough?* Partly. Waiting two years removes the burst — about a third of all cases. But of those that reach two years, 30% still end within ten years (18% within five), above the fifth set beforehand.
2. *Five years?* The first condition is not met: only about 16% of those that reach two years end before five. Waiting five years instead of two halves the chance of a reversal in the following five years (18% to 7%) and costs three more years of delay for the majority that lasts.
3. *No waiting time works?* In the strict sense, yes: at no age does the chance of ending become negligible, and it is higher again for cases that have lasted ten years (31%) than for those that have lasted five. Time separates episodes from arrangements; it does not certify permanence.
4. The post-1945 pattern is the relevant one.

What this supports:

- **A waiting time earns most of its value in the first two years.** Beyond that, each further year of waiting buys little.
- **The kind of arrangement matters more than its age.** Formal incorporation that survives its first year has almost always lasted decades; military presence without it keeps ending at any age. This supports a test of kind (a standing civil arrangement, not a military operation) alongside any waiting time, rather than a longer waiting time alone.
- **An intermediate "unsettled" status is justified**: for the first years the outcome is genuinely open, and even later a settled attribution can change — which a release then records as an ordinary change.

What it does not support: any claim about legality, or a precise threshold. The sample is small, the rows are editors' units, and the year resolution blurs exactly the one-to-two-year range.

## Second question (added 2026-10-03, before running it)

The owner pointed to the public conflict statistics as a second source. The Uppsala Conflict Data Program (UCDP) records, for every year since 1946, each armed conflict involving a state that caused at least 25 battle-related deaths, and says whether the conflict is over territory and which territory.

Question: after fighting over a territory stops, how long is it before one can tell that it will not resume? For a number of quiet years Q: of the territorial conflicts that have stayed quiet for Q years, what share becomes active again within the following ten?

What would change our mind:

1. If conflicts that have been quiet for two years rarely resume within the following ten (under about a fifth), two quiet years are a sound point for reviewing an unsettled area.
2. If the share is still high after two quiet years and drops clearly by five, five quiet years are the sound point.
3. If the share is about the same however long the quiet has lasted, quiet time does not tell settled from unsettled, and the status has to rest on the kind of ending (an agreement, a victory) instead.

Also reported, as context: how long episodes of fighting over territory last.

### Method (second question)

`run_conflicts.py` (Python ≥ 3.11, standard library), from the repository root:

```bash
python3 experiments/control-duration/run_conflicts.py
```

- **Source.** UCDP/PRIO Armed Conflict Dataset version 26.1 (conflict-years 1946–2025), downloaded from <https://ucdp.uu.se/downloads/> on 2026-10-03 into `cache/`; URL and checksum are in the script. Licence CC BY 4.0. Cite: Davies, Pettersson and Öberg (2026), "Organized violence 1989–2025, and violent political protests", *Journal of Peace Research*, doi:10.1093/jopres/xjag046; Gleditsch, Wallensteen, Eriksson, Sollenberg and Strand (2002), "Armed Conflict 1946–2001: A New Dataset", *Journal of Peace Research* 39(5).
- **Selection.** Conflicts whose incompatibility is over territory (alone or together with government): 199 conflicts, 1,586 conflict-years. A conflict is active in a year when it caused at least 25 battle-related deaths. One side is always a government; conflicts between non-state groups are not in this dataset.
- **Episodes.** A run of consecutive active years of one conflict is an episode; the years between two episodes are quiet years. Episodes still active in 2025 are left out of the recurrence figures; for the others, quiet time is counted to the next episode or to 2025. Shares are product-limit estimates in whole years.

### Result (second question)

335 episodes of fighting over territory have ended; 174 of them were followed by a new episode of the same conflict.

**How long the fighting lasts.** Half of the ended episodes lasted a single year, 64% at most two, 81% at most five.

**How often it resumes after Q quiet years:**

| Quiet years Q | Resumes within the next 5 years | … within the next 10 years | Interstate only, next 10 | Within states only, next 10 |
|---|---|---|---|---|
| 1 | 40% | 45% | 29% | 53% |
| 2 | 28% | 33% | 21% | 41% |
| 3 | 20% | 26% | 22% | 32% |
| 5 | 11% | 16% | 16% | 19% |
| 10 | 6% | 12% | 12% | 15% |

Two thirds of all resumptions come after one to three quiet years (113 of 174); three quarters within five.

Per-episode data are in `outputs/conflict_episodes.csv`, the figures in `outputs/conflicts_summary.json`.

### Conclusion (second question)

Outcome 2 of "what would change our mind": after two quiet years a third of territorial conflicts still resume within ten years — above the fifth set beforehand — and after five quiet years a sixth do. The risk falls steadily with quiet time and never reaches zero.

The two sources measure different things and agree closely: an occupation that has lasted two years ends within the next ten in about 30% of cases, and one that has lasted five in about 17%; a territorial conflict quiet for two years resumes within ten in 33%, and one quiet for five in 16%.

For the canon this supports:

- reviewing an unsettled area after **five** years if the aim is that roughly five in six accepted changes hold for the following decade; after **two** years roughly two in three do, after three about three in four;
- tying the review to **quiet** as well as to elapsed time: the dataset gives, for each territorial conflict and year, whether it was active, so "no active conflict over the area in the last T years" can be computed, not judged;
- using the same dataset as an alarm: an area linked to a conflict that becomes active has its control facts re-checked at the next release.

Limits: a conflict in this dataset is defined by the territory in dispute and the government involved, not by a map outline; resumption of fighting does not always mean a change of control; the year is the unit.

## Status

Concluded 2026-10-03 (both questions).
