# Notes on regimes.csv (collected 2026-10-03)

59 regimes, 150 quotes. Scratch data for experiments/regime-lifetimes; nothing here is adopted or verified beyond
"the quote is in the fetched page". Collected in three batches (A: East/South-East Asia, B: South/Central Asia, Middle East,
Africa, C: Europe, Russia, Americas, Oceania); batches A and B were collected by subagents and then read through, not
re-researched. Build files: `part-A/B/C.jsonl` -> `merge.py` -> `regimes.csv`; `selfcheck.py` verifies it.

## Files
- `regimes.csv` - the dataset. `sources.tsv` - cited URL -> saved text in `pages/`. `pages/*.raw` - raw downloads.
- `selfcheck.py` - every quote must be a substring of the saved text of its source after collapsing whitespace runs
  (HTML stripping inserts spaces/newlines; nothing else is normalised). Result: 59 regimes, 150 quotes, 0 failures.
- Wikipedia is cited only by `oldid`; two OLD revisions are used on purpose because current pages have dropped the history
  (Visa policy of Russia, Nov 2020; Visa policy of China, Jan 2020). Pages that blocked a direct fetch were read through the
  Wayback Machine (`web.archive.org/web/2id_/...`): the snapshot date was not checked, so "in force" quotes from such pages
  are "as of the snapshot", not as of 2026.

## Counts
- Ended or interrupted: 27 = 9 abolished, 2 replaced by a national rule, 16 suspended (10 of these later resumed, 6 not).
- Stated expiry / pilot / "temporary" at start: 10 yes, 3 no, 46 unknown (no passage found either way).
- In force 2026: 28 yes, 13 no, 18 unknown. Evidence: 20 primary, 39 secondary.
- 4 regimes started before 2000 and are included for an end/suspension in 2000+ (Norfolk Island, Torres Strait,
  Ceuta/Melilla, Kuril visa-free visits). 39 of 59 came from the seed list, 20 from own leads / searches.

## How ended regimes were searched for
1. Old Wikipedia revisions of "Visa policy of X" (regional schemes described in the present tense, with dates).
2. Targeted web searches for known types of ending: pilot stopped, scheme folded into a national e-visa, exemption or
   parole rescinded, permit requirement lifted or re-imposed, separate immigration control abolished, treaty terminated.
3. Per-country leads from memory used only as search terms (Kaliningrad 72-hour visa, Guam/CNMI parole, Norfolk Island,
   Kuril exchanges, Sri Lanka northern clearance, Pakistan NOC, India PAP relaxations, Colombia border card, Oyapock card).
Bias: countries with English/Russian/Spanish/French press and official gazettes online are over-represented (RU 11, CN 7,
US 4); short-lived local schemes in poorly documented countries are almost certainly missing. Regimes still in force are
easier to find than ended ones, but ended ones were searched for on purpose, so their share here (27/59) is NOT an estimate
of the real share.

## Coding choices that matter for the analysis
- **COVID**: 12 of the 16 suspensions are COVID closures (5 China rows, Jeju, Taiwan offshore permits, 3 Russian regional
  e-visas, Torres Strait, Oyapock card; the other four are political or administrative: Poland-Kaliningrad 2016,
  Latvia-Russia 2022, Ceuta/Melilla 2021, Colombia border card 2018; Kuril visits also stopped then but only the 2022 termination is sourced). They are one
  global shock, not 13 independent events.
- **Russian regional e-visas** (Far East 2017, Kaliningrad 2019, St Petersburg 2019): coded `suspended` 2020-03-18 with no
  resumption; they were never resumed as regional schemes and were superseded by the national e-visa (in law from
  2021-01-01, issued from 2023-08-01). They could equally be coded `replaced_by_national_rule`.
- **Mergers and successors are not endings**: Belarus Brest and Grodno zones (merged Nov 2019), the Guam-only Visa Waiver
  Program -> Guam-CNMI VWP (2009), CNMI parole for PRC nationals -> EVS-TAP (2025), China 72h -> 144h -> 240h transit
  areas (one row) are recorded as continuing regimes with the change in `notes`.
- **Partial suspensions**: for the Colombia border card and the Oyapock card what stopped was the ISSUANCE of cards; for
  Taiwan's offshore landing permits the interruption is practical (ferries stopped, PRC travel ban), not a repeal.
- **Local border traffic** rows (6) apply to border residents only, not to travellers in general - filter on
  `regime_kind=local_border_traffic` if that is out of scope. Five more Schengen agreements with sourced start months
  (Hungary-, Slovakia-, Poland-, Romania-Ukraine; Romania-Moldova) are in the same quoted sentence and were left out to
  avoid flooding the set with one type.
- `in-ladakh-ilp-domestic` concerns Indian citizens (inner line permit), not foreigners.
- `stated_expiry_or_pilot=yes` cases that did NOT end at the stated date: India Manipur/Mizoram/Nagaland relaxation
  ("initially one year", ran 14 years), Andaman relaxation (to 31.12.2022, still exempt), Greek 2012 pilot (to 30 Sep 2012,
  renewed at least to 2018-19), Greek 2024 Visa Express, Algeria southern VOA ("exceptional and temporary"), Bhutan SDF
  waiver, Yangyang, Muan, Shanghai cruise pilot, Kaliningrad 72-hour "experiment" (ran 2002-2016).

## Weak or unverified
- Start dates resting on thin evidence: Norfolk Island (year in the Act's title only), Kaliningrad 72h visa (year only),
  Syria AANES/Semalka (date of the crossing, not of a permit rule), Ladakh ILP 2017 (one Wikipedia sentence), Phu Quoc 2005
  (number of the decision), Hainan and Guangdong group schemes ("since 2000" in press/tourism-board text), Tongrim/Sinuiju,
  Libya Benghazi, the two Belarus zones (Wikipedia only), Ukraine Crimea permit (approval date, not entry into force).
- `in_force_2026=no` for several ended rows is the ending text itself (Pakistan, Sri Lanka, Russia parole, Kuril,
  Kaliningrad 72h), not a 2026 reading; no reinstatement was found, but none was searched for systematically.
- No end found, and status unknown, for: Yangyang and Muan group schemes (last sourced extensions to 2025-05-31 and
  2025-03-31), Greek 2012 pilot, Latvia-Belarus and Latvia-Russia traffic, Chukotka-Alaska visits, Crimea special permit,
  Rapa Nui (2026 status not fetched), Colombia border card, Okinawa multiple visa, Batam/Bintan/Karimun, Nakhchivan, Karabakh.
- Okinawa multiple-entry visa is borderline: the visa admits to all Japan, only the first visit is tied to Okinawa.
- Guilin: the 2020 suspension / 2023 resumption notices name a "Guangxi" ASEAN group policy; treated as the same scheme.

## Contradictions
- With the seed (`crw_scopes.csv`):
  - Hainan group scheme: Xinhua (2018) says since 2000 with five countries added in 2010; seed says 2010.
  - Chukotka-Alaska: pinned Wikipedia says the 1989 agreement came into force on 2015-07-17; seed says "1989; renewed 2015".
  - Iraq Kurdistan: no merger into the federal e-visa confirmed; the KRG portal still issues e-visas; Wikipedia contradicts itself.
  - Batam/Bintan/Karimun: Perpres signed 2024-08-29; implementing circular dated 2024-10-08.
  - Sinuiju/Tongrim: Wikipedia implies 2014; seed says 2015.
  - Andaman: current official text lists 29 islands, not 30 (plus 11 day-visit islands, to 31.12.2027).
  - Ceuta/Melilla: Middle East Monitor dates the suspension of the local exemption to May 2021; the seed says "after 2020"
    (border closed March 2020 - closure date not quoted here).
- Between sources:
  - Latvia-Belarus local border traffic: "since 2011" vs "from February 2012" in two Wikipedia pages.
  - Latvia-Russia: Interfax reports suspension from 2022-08-01; current Wikipedia still describes it in the present tense.
  - Yangyang start: MOJ release 2022-06-01 vs an embassy notice giving 2023-03-15 (apparently copied from the Muan notice).
  - Sri Lanka 2014 clearance: 10 vs 15 October 2014. Semalka handover: 15 vs 16 April 2026.
  - Kuril termination: TASS dateline 5 Sept 2022; search snippets say the resolution is of 3 Sept.

## Dropped (no sourced start date, or out of scope)
- No sourced start: Mexico northern border zone FMM exemption (blogs say it ended Sept 2015), Guam-only VWP and CNMI's own
  immigration control (ended 2009-11-28; start not fetched for the latter, the former continues as GCVWP), Japan Tohoku
  multiple visa, Rason, Pakistan's older AJK/Chitral NOC regime (abolished 2019-03-26), Sri Lanka's earlier clearance
  (lifted 2011-07-04), Tajikistan GBAO permit, Egypt Sinai stamp, Iran Kish/Qeshm, Jordan Aqaba, Sudan permits, Socotra,
  Tibet permit closures, Laos Golden Triangle, Myanmar permit areas.
- Out of scope: COVID-only schemes (e.g. Phuket sandbox), Donbas contact-line passes (wartime measure), Transnistria's
  2023 restriction on Ukrainian men (nationality rule of an unrecognised authority), Ascension e-visa (procedure change,
  not a new regime), Belarus visa-free entry through airports (country-wide).
- Not searched at all: Kazakhstan/Kyrgyzstan border zones, Saudi Arabia (Medina), Oman/UAE, Morocco/Western Sahara,
  Ethiopia, Sikkim, Lakshadweep, Nepal area openings, Malaysia, Thailand, Philippines, Cambodia, Mongolia, most of Latin
  America, the Caribbean and the Pacific.
