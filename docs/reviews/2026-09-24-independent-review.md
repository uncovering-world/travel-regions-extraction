# Independent project review — 2026-09-24

**Status: input material, not a normative document.** Nothing here is adopted. A proposal becomes a rule only through an explicit owner decision recorded in [decisions.md](../decisions.md) and [spec.md](../spec.md). The owner asked for an independent judgement: is the project adequate for its purpose — the region canon for Track Your Regions (TYR) — and has the work gone too deep into detail?

Method: re-read spec, decisions, open questions, the Q001 rule review, the 93-row adversarial set and the source pilot; extracted what TYR needs from a canon (TYR planning documents; issues #587, #766, #768, #770, #771, #786). In parallel: three research threads (literature on regionalization; practice of standards and travel lists; a stress test of CR-W against real territorial entry regimes) and an independent reviewer who did not know the author's conclusions. TYR #786 was treated as one input, not as the yardstick.

## Conclusion

Depth itself is not the mistake. The method — start from the problem statement, write rules as predicates, test them against counterexamples, keep "unknown" distinct from "no" — is sound and has already paid off. The problem is that the consumer (TYR) is missing from the problem statement, and the depth went into legal-grade proof of facts before anyone checked that the rules produce a good partition.

## What is done well

- Rules as predicates with counterexamples, name-blindness (V010), open-world semantics.
- Two stages with the invariant "Stage 2 refines Stage 1" — the right *construction* order.
- CR-W finds genuine travel regions that ISO 3166-1 lacks: Zanzibar, Rapa Nui, Galápagos, Sabah, Sarawak, Jeju, Hainan, Phu Quoc, Guam/Northern Marianas (Appendix C).
- D031 (local restricted zones are overlays) and Q004 (customs is separate from admission; Åland correctly does not split).
- Bitemporal facts and an identifier lifecycle (R031–R032).

## Six problems

### P1. The consumer is missing from the problem statement

TYR's basic functions — counting countries, regions within a country, a per-user choice for disputed territories — require every canon region to lie inside one country under every supported perspective. The spec has no such requirement; R016 explicitly calls an ISO code, recognition and a separate stamp insufficient; CR-J is not adopted; identity is excluded.

Consequences:
- San Marino, Monaco, Liechtenstein and the Vatican have no entry regime of their own — CR-W will not separate them. None is in the adversarial set.
- The Germany/France boundary depends on finding a witness inside Schengen (Q001 C001 under P1: `data_unknown`).
- Golan Heights, Aksai Chin: the regime is the controller's and splitting on a dispute is forbidden (D035), so a region may straddle a border drawn by Syria's or India's perspective.
- D004–D007 are accepted but underivable (D036).

Practice: none of the surveyed systems derives territorial status from first principles (Appendix B). The standpoint literature recommends keeping conflicting perspectives separately tagged.

**Proposal (not adopted):** a Stage 1 rule of a different kind — *the canon refines every partition in a declared, versioned reference registry* (ISO 3166-1 plus selected Natural Earth point-of-view layers). It is a product declaration with an external source, not a factual claim. It derives D005–D007, almost all of D004, every country boundary and the microstates; Q006/#19 close and CR-J (#18) mostly loses its purpose. The D010 objection ("a registry cannot justify itself") does not apply: the justification is the product requirement to count visits by country.

### P2. CR-W: sound idea, three general holes

Stress test on 15 cases: it fires in 14. Artefacts come from:
1. transit (China's 240-hour regime: boundaries down to prefecture level, redrawn repeatedly since 2013);
2. scopes anchored to a port, terminal or distance band (the 25-mile Border Crossing Card zone in the US; ferry-terminal schemes);
3. no stability (Russia's regional e-visas 2017–2023: splits that appeared and vanished).

D032 ("one witness, no frequency threshold") is not the culprit — it is what separates Hainan and Jeju. Proposed general fixes: compare trips to a destination, transit is not a witness; the scope must be a territorial unit named by the rule, otherwise it is an overlay; stability is handled at release level (P4). Whole-territory permits (Tibet, Jan Mayen, Indian PAP states) need an explicit convention (Q005 allows one).

Fact verification belongs where sources disagree: no published legal instrument was found for Tibet; sources on the Kurdistan Region of Iraq conflict. The pilot's full audit went to Greenland ≠ Denmark, where the answer is not in doubt.

None of the 20 verified cases is in the adversarial set: about 90% of it is overseas and disputed territories; zero sub-national visa programmes, zero microstates, three rows of interior granularity.

### P3. Open world without a product default

Splitting needs one witness; merging needs proof of equality across all 7 dimensions for all contexts. In Q001, `hard_compatible` occurs 0 times in 147 results. Under these semantics Stage 1 never completes, and by R041 Stage 2 cannot start without it. TTWA, DEGURBA and NUTS work closed-world with parameters. **Proposal:** a product Stage 1 profile — within a registry cell there is no boundary without a CR-W witness, and the result is marked provisional; `S1-core-v1` stays as the strict research definition.

### P4. No release stability policy

G-TIME: a new rule applies immediately, so the canon follows visa policy directly; 11 of the 15 regimes checked changed within 10 years. Practice: NUTS amends at most every 3 years and ignores changes of ≤1% of population, with correspondence tables; ISO never reuses a code for 50 years; TCC and NomadMania never delete entries. **Proposal:** separate "facts at date t" from "canon release", with a minimum interval, entry/exit conditions for a boundary, a de-minimis threshold and correspondence tables.

### P5. Development order and pairwise-only evaluation

Stage 2 produces most cells and carries all the vagueness; vague and fiat boundaries have no fact of the matter — formalisation only fixes a chosen reading. Successful precedents (TTWA, DEGURBA): a small published rule set, iteration, whole-partition metrics. The project has not built a single partition. Stage 1 decisions are irreversible (R041), yet cannot be judged without seeing Stage 2.

Direction for Stage 2: three questions (is it a region; one region or two; where is the boundary) with named parameters; a per-cell admissibility condition instead of a target count (max-p); administrative units first (NUTS Art. 3); thresholds plus bounded written exceptions (NomadMania ≤ 8+2; the NUTS island clause) — which also answers Q011; validation against the cores of reference lists rather than exact boundaries.

### P6. Process heavier than the work

7 epics and 25 issues with authorisation boilerplate, 3 skills, an AI cost study for 50/500/5000 dossiers, a review protocol without a reviewer, a frozen P1/P2/P3 evaluator path. The first issue that builds any partition (#22) sits seven steps down the blocker chain.

## What depth belongs where

| Layer | Before | Proposed |
|---|---|---|
| Rules as predicates with counterexamples | deep | keep |
| Invariants: coverage, disjointness, time, IDs | present | keep; add a release policy |
| Proof of facts | legal-grade everywhere | "cited" by default; full audit where sources disagree |
| Stage 2 | forbidden | design and experiments |
| Evaluation | pairwise | whole partition |
| Process | epics and gates | a few live issues |

## Proposals for decision

1. Write TYR's requirements as R items with tests: one point — one region; a region's country under the chosen perspective; number of regions per country; a visit survives changes; explainability.
2. The reference-registry rule (P1).
3. CR-W amendments (transit, scope, stability) and a whole-territory permit convention; extend the adversarial set.
4. A product Stage 1 profile and a cited world draft; whole-partition metrics; comparison with TCC.
5. Stage 2 design and experiments on 5–12 countries; write its contract after the first runs.

---

## Appendix A. Literature

- Bittner & Smith (2003), A theory of granular partitions, *Foundations of GIScience*, doi:10.1201/9780203009543.ch7 — partition quality is a set of whole-partition properties; exhaustiveness is relative to a declared domain and resolution.
- Bittner & Smith (2001), Granular partitions and vagueness, FOIS, doi:10.1145/505168.505197 — a canon is one chosen crisp reading of vague names.
- Smith & Varzi (2000), Fiat and bona fide boundaries, *PPR* 60(2), doi:10.2307/2653492 — political and visa boundaries are fiat; ownership of the line itself is a convention.
- Gómez Álvarez & Bennett (2017), Classification, individuation and demarcation of forests, COSIT, doi:10.4230/LIPIcs.COSIT.2017.8 — three separate questions with explicit parameters; threshold vagueness differs from conceptual vagueness.
- Gómez Álvarez & Rudolph (2021), Standpoint Logic, FOIS, doi:10.3233/FAIA210367 — conflicting standpoints are kept separately rather than unified.
- Montello et al. (2003), Where's downtown?, *Spatial Cognition and Computation* 3(2–3), doi:10.1080/13875868.2003.9683761 — agreement on cores, disagreement at edges.
- Openshaw (1984), *The Modifiable Areal Unit Problem*, CATMOG 38 — aggregation has no rules; a partition is correct only relative to a declared purpose.
- Duque, Anselin & Rey (2012), The max-p-regions problem, *J. Regional Science* 52(3), doi:10.1111/j.1467-9787.2011.00743.x — a per-cell condition instead of a target number of regions.
- Guo (2008), REDCAP, *IJGIS* 22(7), doi:10.1080/13658810701674970 — whole-partition metrics for comparing regionalizations.
- UNWTO (2019), *Tourism Definitions*, doi:10.18111/9789284420858 — "destination" has no scale.
- Raun, Ahas & Tiru (2016), *Tourism Management* 57, doi:10.1016/j.tourman.2016.06.006; Tenkanen et al. (2017), *Sci. Reports* 7:17615, doi:10.1038/s41598-017-18007-4 — travel data are biased; they can inform but not define.
- Coombes & ONS (2015), *Travel to Work Areas*, CURDS RR2015/05 — "no single theoretically correct algorithm"; alternatives compared on partition metrics.
- *Applying the Degree of Urbanisation* (2021), doi:10.1787/4bc1c502-en; endorsed by the UN Statistical Commission in 2020 — a global method on a few parameters.
- Grüninger & Fox (1995), competency questions; Noy & McGuinness (2001), Ontology Development 101; Presutti et al. (2009), eXtreme Design — every commitment traces to a question or a test; iterative development.

## Appendix B. Practice of standards and lists

- **TCC** (330): separately administered territories count; non-contiguous parts if population > 100,000; islands ≥ 200 miles away or > 100,000 people; disputed areas with a historical identity count separately. https://travelerscenturyclub.org/territory-status
- **NomadMania** (1,301 under the 2022 rules, 1,381 after May 2026): a formula over area, population, World Heritage sites, ethnic fractionalisation, GDP and arrivals; thresholds for islands and enclaves; the committee may deviate for at most 8+2 countries with written justification; rules reviewed every 2 years; regions are never deleted. https://nomadmania.com/static/nm.rules.regions.pdf
- **MTP** (~1,500): splitting criteria are not published. https://mtp.travel/lists-explained/uncountries
- **Wikivoyage**: the 7±2 rule; regions at one level neither overlap nor leave gaps; "legal divisions don't necessarily make for reasonable travel divisions"; disputed areas by actual control. https://en.wikivoyage.org/wiki/Wikivoyage:Geographical_hierarchy
- **ISO 3166-1**: names and membership come from UN lists; a deleted code is not reused for 50 years. https://www.iso.org/iso-3166-country-codes.html
- **NUTS** (Regulation 1059/2003): administrative units are the first criterion; population bands (NUTS-1 3–7M, NUTS-2 0.8–3M, NUTS-3 150–800k); amendments at most every 3 years; changes of ≤ 1% of population are not amendments; an island clause. https://www.legislation.gov.uk/eur/2003/1059/pdfs/eur_20031059_2019-11-13_en.pdf
- **DEGURBA**: uniform thresholds on a 1 km² grid worldwide; the 2026 edition changed parameters — the method is versioned.
- **Natural Earth**: de facto boundaries by default with disputed areas marked; point-of-view layers since v5.0.0 (December 2021), 31 countries plus ISO; 246–258 countries depending on the perspective. https://www.naturalearthdata.com/about/disputed-boundaries-policy/
- **OSM** — "on the ground" rule; **Google** — ground truth, then UN/ISO, then local law; **Mapbox** — a `worldview` field.
- **Apps** (been, Visited and others): a UN 193 or ISO ~250 base plus toggles for disputed territories.

Common patterns: territorial status is delegated to an external authority; disputes are de facto boundaries plus claim layers; thresholds come with bounded written exceptions; administrative units come first; change is governed explicitly; a named body interprets the criteria.

## Appendix C. CR-W stress test (as of 2026-09-24)

| Case | Regime | Changes | CR-W split | Sensible? |
|---|---|---|---|---|
| Jeju (KR) | 30 days visa-free for the island only | excluded-country list changed 2018; paused 2020–2022 | yes | yes |
| Hainan (CN) | 30 days visa-free for 61 countries, Hainan only | 2018, 2024, 2026; the nationwide visa-free list absorbed most countries | yes (e.g. US citizens) | yes, but fragile |
| Phu Quoc (VN) | 30 days visa-free for all on direct arrival | legal basis 2005, 2014, 2020; unit renamed 2025 | yes | yes |
| China, 240-hour transit | stay limited to permitted areas of 24 provinces | 2013, 2016, 2024, 2025, 2026 | yes, many, down to prefectures | no (artefact) |
| Russia, regional e-visas | e-visa valid in the region of entry | 2017, 2019; replaced by a unified e-visa in 2023 | historically, not now | mostly an era artefact |
| Rapa Nui (CL) | max 30 days, FUI form, Chilean nationals included; Law 21.070 | since 2018 | yes | yes |
| Galápagos (EC) | TCT card, max 60 days per year | stable since 2015; fee raised 2024 | yes | yes |
| Sabah, Sarawak (MY) | own immigration control, incl. for Peninsular residents | since 1963; Labuan checks since 2022 | yes | yes |
| India, PAP/RAP | Arunachal and Sikkim whole-state; Manipur, Mizoram, Nagaland PAP reimposed 17 Dec 2024 | 2018, 2024, 2025 | yes, several | yes at state level; island lists are overlays |
| Tibet | TTB permit for foreigners | no legal instrument found | yes, if it counts as a standing rule | yes |
| Svalbard / Jan Mayen | outside Schengen / permission for every visit | stable | yes / depends on the permit convention | yes |
| Kurdistan Region of Iraq | own KRG visa | 2021–2025; sources conflict | yes | yes, boundary contested |
| Mount Athos (GR) | diamonitirion, quotas, women barred | stable | yes | yes |
| Réunion and other DOMs (FR) | Schengen visa not valid | low | yes | yes |
| Åland (FI) | tax border only, admission as in Finland | since 1995 | no | correct negative |
| Guam and Northern Marianas (US) | own visa waiver programme | — | yes | yes |
| Zanzibar (TZ) | mandatory local travel insurance since 1 Oct 2024 | 2024 | yes | yes |
| US Border Crossing Card zone | 25 miles (75 in Arizona) | — | yes | no (artefact) |
| Batam, Bintan, Karimun (ID) | 4 days for Singapore PRs via designated terminals | 2024 | unclear | likely artefact |

Key sources: https://en.nia.gov.cn/n147418/n147463/c183412/content.html (China transit), https://msgg.gob.cl/wp/2018/08/01/nueva-ley-para-rapa-nui-los-requisitos-para-visitar-o-residir-en-la-isla/ (Rapa Nui), https://www.gobiernogalapagos.gob.ec/preguntas-y-respuestas-frecuentes-control-migratorio-tct/ (Galápagos), https://www.imi.gov.my/index.php/en/main-services/travel-documents/document-in-lieu-of-internal-travel-document-2/ (Sabah/Sarawak), https://tz.usembassy.gov/alert-mandatory-insurance-required-for-travel-to-zanzibar-september-25-2024/ (Zanzibar), https://www.dhs.gov/guam-cnmi-visa-waiver-program (Guam). Not confirmed from primary sources: the Tibet legal instrument, current practice in the Kurdistan Region, and a stay restriction for Batam.
