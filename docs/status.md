# Status

Updated: 2026-11-21.

## Focus

A first Stage 1 release of the canon for Track Your Regions. The rules for Stage 1 are decided (D038–D076 in [decisions.md](decisions.md), R045–R062 in [spec.md](spec.md)); the [draft release package](../experiments/release-draft/README.md) is built from them and can be inspected on a local map ([tools/map-viewer](../tools/map-viewer/)). Stage 2 comes after the first release (#28).

Track Your Regions now works with the canon directly: its session for the revised catalogue model (TYR #2634) sends requests and defects by cross-session message. Its list of requests is local to TYR (`docs/local/research/2634-method/v9/canon-requests.md` in that repository). TYR has adopted D049: a trip's date picks the release of its year, so no dated attribution periods are needed. Catalogue points for R060 are a read-only snapshot under `~/tyr-exports/`; OSM extracts come from the dev stack's keeper (the Syncer session), one batched request per planet pass.

## Done on 2026-11-19

- D074 / R060 adopted: a small piece of geometry is fixed by hand only where a traveller does something there.
- The uncommitted work of 2026-10-05 is committed: the Cooch Behar enclave exchange, the Chong-Kara transfer, D073 in the render, and the list of real exclaves.
- D073 corrected in practice (a note on D073): only strips move, i.e. parts with no point more than 2 km from their edge. Before this, Ayia Napa and Paralimni were given to Dhekelia and Kodinar to Junagadh. The list of moved and kept parts is computed at full precision and shipped as `release/cut_off_D073.csv` (TYR request 3).
- Antarctica reads AQ under every point of view (D040).
- Northern Cyprus is OSM's outline; GADM's ZNC is bound to Cyprus, so Nicosia south of the Green Line is Cyprus.
- Research: [boundary providers beyond GADM and OSM](research/2026-11-19-boundary-providers.md).

## Done on 2026-11-20–21

- D075 / R061 adopted: every region carries an access mark (ordinary, expedition, closed) in `regions.csv`; how to evidence closure is Q022. TYR counts expedition regions on a line of their own.
- Own outlines add only land where GADM has none: `geometry/land/<file>` (the outline intersected with World Polygons 11.4). Before this, Northern Cyprus, Somaliland and Essequibo gained their territorial sea.
- D076 / R062 adopted: every region has a `common_name` (CLDR 48 for coded regions, Wikipedia titles for descriptive area names; TYR request 23).
- Release format: cut-off points at 7 decimals; `geometry/` rebuilt from scratch with a per-file `sources.csv`; `manifest.json` `status` is `draft` or `release`.

## Waiting for the owner

- The open questions that remain: Q015, Q016, Q018, Q019, Q020, Q013.
- Bir Tawil: whether a party's stated boundary attributes land to a neighbour under its view (TYR no longer needs it).
- Stable keys for the five de facto states and for retired ISO codes (TYR request 6). TYR uses `x-abkhazia` … and `x-cs-1993` meanwhile.

## Active

- TYR requests from its round 12 (`v12/canon-requests.md` in TYR): 20 (a reason for each region with no country), 11 (a lease's lessee), 22 (Stage 1 cells as rows, a `stage1_cell` column at Stage 2). Also a gap of ours: the release states no rule for GADM's own overlaps between countries (BEN/TGO, GEO/RUS), which V001 forbids; asked TYR how its loader resolves them.

- Release draft (#22), open items:
  - islands GADM 4.1 does not draw: Chichijima and the Ogasawara Islands, Fatu Hiva, Rocas Atoll, Malpelo and San Pedro Mártir are in the pinned World Polygons 11.4; Japan's MLIT N03 would be rank 1 for Ogasawara; Roca Partida needs another source;
  - Western Sahara under Morocco's view (needs Morocco's claim to the whole territory as a sourced register fact);
  - Hans Island (is the 2022 agreement in force?);
  - Vélez de la Gomera and the Chafarinas (D045: own geometries into ES);
  - 45 unexplained fragments in the display check, mostly real exclaves to list in `inputs/known_fragments.csv`;
  - near Pyla a 0.6 km² part of Cyprus moved to Dhekelia by D073: a village area under R060, to be checked by hand;
  - the Okpara villages and the far plots of the Baikonur lease, as before.
- Known GADM defects for Stage 2, reported by TYR: Lake Erie filed wholly under Ohio (TIGER/Line splits it), Uttarakhand and Himachal Pradesh listed three times each, a Ukrainian unit named "?".
- Long term: a canon for every year from 2000 ([#30](https://github.com/uncovering-world/travel-regions-extraction/issues/30)).

## Next step

Answer TYR's open requests and settle a rule for GADM's overlaps. Then add the islands GADM lacks, clear the open items above, cut a first release candidate and answer TYR's remaining requests.
