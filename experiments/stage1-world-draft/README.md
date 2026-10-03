# World Stage 1 draft

**Experiment, not the canon.** Cells here are a draft under proposals that are not adopted. Issue: [#22](https://github.com/uncovering-world/travel-regions-extraction/issues/22).

## Question

How many Stage 1 cells does the world have, and which, if Stage 1 is built as

1. **registry cells** — the coarsest partition that refines ISO 3166-1 and every Natural Earth point-of-view (POV) attribution, and
2. **CR-W splits** inside registry cells, taken at "cited" evidence level from a census of territory-specific entry regimes?

And how does the result move with each open choice: which perspectives are in the registry, and the pending CR-W amendments (transit, rule scope, whole-territory permits)?

Assumed proposals (none adopted): the reference-registry rule ([#19](https://github.com/uncovering-world/travel-regions-extraction/issues/19)); a product profile where a registry cell has no internal boundary without a CR-W witness and evidence is "cited" by default (#22); the CR-W amendments ([#17](https://github.com/uncovering-world/travel-regions-extraction/issues/17)) as parameters. Under the strict `S1-core-v1` none of these cells is certified.

The first run is count-only: a list of cells with their defining units, no geometry.

## Related

R009, R039, R041, R044; R014, D031, Q005 (permits and overlays); R027 (transit); D012 (non-contiguity does not split); D004–D007 (accepted product constraints); Q006, Q011. Consumer-contract proposal: [C2, C5](../../docs/proposals/consumer-contract.md).

## What would change our mind

Written before the first run.

1. **Is the registry enough for D004–D007?** If any accepted constraint is not derived by registry cells, the registry rule as proposed does not close #19 and needs another input or an explicit convention.
2. **Is Natural Earth usable as the perspective source?** If its POV attributes need more than a handful of documented corrections to give sensible cells, the registry needs another source or a curated list — which changes #19.
3. **How much does CR-W add?** If CR-W splits are under 5% of cells, Stage 1 is dominated by the registry, and legal-grade evidence work on CR-W has little effect on the partition; that supports "cited by default". If they are over 25%, evidence quality matters much more than the review assumed.
4. **Which amendment matters?** The amendment whose switch moves the total most should be decided first; if none moves it by more than a few cells, #17 can wait for Stage 2.
5. **Does the draft resemble a known list?** If the draft's cells that are parts of an ISO entry overlap poorly with the TCC entries that are parts of an ISO entry, either CR-W misses what travellers consider separate (work for Stage 2) or the reference list uses other criteria; either way the comparison says what Stage 2 must add. TCC is validation only; nothing is tuned toward it.

## Method

`run.py` (Python ≥ 3.11, standard library). From the repository root:

```bash
python3 experiments/stage1-world-draft/run.py
```

The first run downloads two Natural Earth files into `cache/`; their URLs, version and checksums are in `inputs/sources.json`.

**Registry cells.** Every ISO 3166-1 entry is a cell (`inputs/iso3166-1.csv`, 249 entries). A Natural Earth feature — a disputed area, or an entity without an ISO code — becomes a further cell when at least one perspective attributes it to something other than the ISO entry that administers it. Perspectives are Natural Earth's default attribution and its 31 national point-of-view columns. Features with the same administering entry and the same attribution under every perspective form one cell. Two generic rules keep the data's noise out: a feature covering at least 80% of its ISO entry is that entry, not a part of it; a cell under 100 km² is below the draft's resolution and is listed in `outputs/skipped.csv` instead.

**CR-W cells.** `inputs/crw_scopes.csv` is a census of 116 territory-specific entry regimes inside ISO entries, compiled on 2026-10-03 from official pages where they could be read and otherwise from secondary sources (mostly Wikipedia); its limits are described in `inputs/crw_scopes.notes.md`. Evidence is honest rather than strong: 9 rows rest on an official page, 92 on secondary sources, 15 are unconfirmed or conflicted, and 32 have an unclear current status. A scope becomes a cell when it is in force, its evidence is at least "cited", and it survives the profile's switches:

| Profile | Transit regimes | Scopes that are not a whole named unit | Whole-territory permits | Evidence | Status |
|---|---|---|---|---|---|
| `amended` (baseline) | off | off | on | cited | in force |
| `raw` | on | on | on | cited | in force |
| `amended_no_permits` | off | off | off | cited | in force |
| `amended_confirmed_only` | off | off | on | official page only | in force |
| `amended_any_evidence` | off | off | on | any | in force |
| `amended_incl_unclear_status` | off | off | on | cited | in force or unclear |

Customs-only and tax-only differences never split (Q004). Scopes the registry already separates are not counted twice.

**Reference list.** `inputs/tcc_parts.csv` holds the 96 entries of the Travelers' Century Club list (330 entries, as of January 2022; read 2026-10-03) that are parts of an ISO entry or span several, with the ground TCC appears to separate them on and, mapped by hand, the draft cell that corresponds. Validation only.

No geometry is built; cells are named by their defining units. The registry part attributes a disputed feature to the ISO entry of its default administrator, which is not always the entry that contains it geographically (Western Sahara west of the berm is listed under Morocco).

## Result

Outputs: `outputs/summary.json`, `outputs/cells.csv` (the baseline's 304 cells), `outputs/skipped.csv`.

**Registry**

| Perspectives declared | Cells ≥ 100 km² | No size floor | Floor at 1,000 km² |
|---|---|---|---|
| ISO 3166-1 only | 249 | 249 | 249 |
| + Natural Earth default | 259 | 265 | 256 |
| + 31 national points of view | 278 | 298 | 271 |

**With CR-W**

| Profile | CR-W cells | Total |
|---|---|---|
| `amended` (baseline) | 26 | 304 |
| `raw` — no amendments | 55 | 333 |
| `amended_no_permits` | 18 | 296 |
| `amended_confirmed_only` | 4 | 282 |
| `amended_any_evidence` | 28 | 306 |
| `amended_incl_unclear_status` | 42 | 320 |

The baseline's 26 CR-W cells: Jeju, Hainan, Phu Quoc, Kinmen, Matsu, Guilin and Xishuangbanna (tour-group exemptions), southern Mexico (the five states of the Regional Visitor Card) — visa exemptions; Rapa Nui, Galápagos, San Andrés — stay limits; Sabah, Sarawak, Zanzibar, Transnistria — separate immigration control; Puntland, Socotra, Ascension — own visa system; Tibet, Sikkim, Arunachal Pradesh, Gorno-Badakhshan, Chukotka, Mount Athos, Tristan da Cunha, Clipperton — whole-territory permits.

**Accepted constraints.** With all points of view the registry gives separate cells for Réunion (D005, own ISO entry), Crimea (D006; also separate from Russia, tentative D013), Western Sahara (D007, own entry, and the part west of the berm as a further cell) and the UK overseas territories with ISO entries (D004). Not derived: the British Antarctic Territory (inside AQ) and Akrotiri (78 km², under the floor; Dhekelia at 102 km² is a cell). With ISO 3166-1 only, there is no Crimea cell and no Sovereign Base Area cell.

**Against TCC.** Of the 96 TCC entries that are parts of ISO entries, 22 have a draft cell:

| Ground on which TCC lists the part | TCC entries | With a draft cell |
|---|---|---|
| De facto or disputed territory | 9 | 9 |
| Separated land (islands, exclaves) | 58 | 13 |
| Member of a federation or union (the emirates, England, Scotland …) | 15 | 0 |
| Continental division (Turkey in Europe, Egypt in Asia …) | 7 | 0 |
| Antarctic claim | 7 | 0 |

Twelve of the draft's 26 CR-W cells have no TCC entry: Phu Quoc, Kinmen, Matsu, Guilin, Xishuangbanna, southern Mexico, Puntland, Arunachal Pradesh, Gorno-Badakhshan, Chukotka, Mount Athos, Clipperton.

## Conclusion

Against "what would change our mind":

1. **The registry derives D004–D007 only with the national points of view**, and with two residual gaps (the Antarctic claim, and a Sovereign Base Area cut off by the size floor). ISO 3166-1 alone is not enough. This supports the registry proposal for #19 and shows that its resolution rule should not be a bare area threshold.
2. **Natural Earth is usable for attribution without hand corrections**, given two generic rules (whole-entry and resolution). It is not usable for names, and its point-of-view columns contain opaque codes and at least one error (see the [registry proposal](../../docs/proposals/reference-registry.md)).
3. **CR-W adds 26 cells, 8.6% of the baseline** — between the two thresholds set beforehand. Stage 1 is dominated by the registry; CR-W contributes the cells that matter most to travellers (Zanzibar, Sabah, Rapa Nui, Jeju …). Legal-grade proof for each of them would change little in the partition; where it matters is the scopes whose current status is unclear (16 more cells if all of them hold).
4. **The amendment that moves the total most is the scope rule**: requiring a whole named unit removes 28 scopes (border bands, site lists, parts of states), against 8 for the permit convention and 1 for transit (the transit regime is one scope here; as cells it would be dozens). Evidence matters as much: on official pages alone only 4 CR-W cells survive.
5. **The draft is not a TCC-like list, and Stage 1 should not try to be one.** It matches every TCC entry that rests on de facto control and the island entries that have their own entry regime, and none of the 15 federation members, 7 continental divisions or 45 islands and exclaves without a regime (Sicily, Hawaii, Tasmania, the Canaries, Kaliningrad). Those are what Stage 2 has to produce — by separated land, identity or weight, not by hard rules.

Further findings for #17:

- Three baseline cells look wrong as regions although they pass every proposed amendment: the five Mexican states of the Regional Visitor Card (one rule spanning several units, for four nationalities), and Guilin and Xishuangbanna (exemptions for organised tour groups). They suggest two more questions: whether a class defined by organised group travel is a civilian short-stay class in the sense of G-CONTEXT, and what cell a rule spanning several units creates.
- Clipperton (uninhabited, a few km²) shows that CR-W cells need the same resolution rule as registry cells.
- Several regimes changed kind within ten years (Andaman and Nicobar, Azad Kashmir, Gilgit-Baltistan went from whole-unit permits to partial ones), which ties #17 to the release policy (#20).

Nothing here is adopted. The cell list is a draft for discussion, built from secondary evidence.

## Status

Concluded 2026-10-03 (count-only run). Next: geometry and substrate binding for the baseline cells, in the [proposed release format](../../docs/proposals/output-format.md).
