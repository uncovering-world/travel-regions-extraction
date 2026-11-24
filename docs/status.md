# Status

Updated: 2026-11-23.

## Focus

A first Stage 1 release of the canon for Track Your Regions. The rules for Stage 1 are decided (D038–D083 in [decisions.md](decisions.md), R045–R064 in [spec.md](spec.md)); the [draft release package](../experiments/release-draft/README.md) is built from them and can be inspected on a local map ([tools/map-viewer](../tools/map-viewer/)). Stage 2 comes after the first release (#28).

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
- D077 amends R062: where the CLDR plain name has a qualifier ("SAR", " - "), the short or variant form is used — Hong Kong, Macao, Congo (DRC), Congo (Republic); D080 adds a bracketed second name at the end (Myanmar).
- D078 / R063 adopted (TYR request 33): ground two GADM units of different regions both draw goes to the region with the longer shared border; amended by D079: the substrate is cleaned as a coverage (snap 1e-7°, longest border, gap 0) and the release states the recipe; on GADM 4.1 all 2,353 strips are sub-millimetre lenses that snapping removes. Our own render does not clean yet.
- D081 / R064 adopted (2026-11-23): land World Polygons 11.4 draws and GADM 4.1 does not goes to the region it borders longest, else to the region of its World Polygons country code; unmatched pieces are listed. The [missing-land experiment](../experiments/missing-land/README.md) found 88,219 such pieces, 11,903 km². D083 (2026-11-23): only pieces of at least 0.01 km² are added. The build is `experiments/release-draft/added_land_D081.py`; GADM 4.1 leaves a 16.5 km² hole over central Dublin with 21 catalogue points. World run of 2026-11-23: 554,407 pieces, 155,552 km² added to 236 regions; after mapping the Coral Sea Islands to AU and deciding Banc du Geyser (TF), Conejo (HN) and an Abu Musa islet by R051 with evidence, 4 pieces (48 km²) stay undecided: Minerva Reefs and Imia/Kardak (World Polygons 'Heipethes Islands'), which have no holder in our sources; TYR takes them as gaps named in the release notes (2026-11-24). Of 529 catalogue points in no GADM unit, 113 now fall in added land, 14 lie on islets under the floor, 402 lie in water in both sources.
- D082 amends D079 / R063 (2026-11-23): the cleaned coverage is the one-window result, computable in longitude windows with the seams cleaned again (TYR's measurement: one window needs 60–80 GB; five windows fit in 14 GB).
- Release format: cut-off points at 7 decimals; `geometry/` rebuilt from scratch with a per-file `sources.csv`; `manifest.json` `status` is `draft` or `release`.

## Waiting for the owner

- The open questions that remain: Q015, Q016, Q018, Q019, Q020, Q013.
- Bir Tawil: whether a party's stated boundary attributes land to a neighbour under its view (TYR no longer needs it).
- Stable keys for the five de facto states and for retired ISO codes (TYR request 6). TYR uses `x-abkhazia` … and `x-cs-1993` meanwhile.

## Active

- TYR requests: done on 2026-11-22 — 20 (`no_country_basis`), 11 lease part (`lessee`, `lease_until`), 33 (D078/D079, substrate cleaning), 34 (cut-off points inside their piece), 35 (a holder for every licence). Open: 22 (Stage 1 cells as rows, a `stage1_cell` column at Stage 2), 6 (keys for reused codes), the rest of 11 (D049's lapsed-rule mark and D043 (5)'s fighting flag have no computed facts yet). TYR will measure a world-wide `ST_CoverageClean` window on GADM 4.1.

- Release draft (#22), open items:
  - D081 built (`added_land_D081.py`); Minerva Reefs and Imia/Kardak stay undecided until a holder is sourced; TYR needs no country per view for special places (its rule O1: the land counts for the holder under every view); the added land is joined into the release draft (`membership.csv` precedence 3, `manifest.json` `added_land`, the 4 undecided pieces in `gaps.csv`); Roca Partida is not in World Polygons and needs another source;
  - Western Sahara under Morocco's view (needs Morocco's claim to the whole territory as a sourced register fact);
  - Hans Island (is the 2022 agreement in force?): the Folketing consented on 19 December 2023 (ft.dk, B 14, 2023-24 session, timetable; read through en.wikipedia Hans Island, revision 1386274128, 2026-11-22); Greenland's Inatsisartut approved it on 31 May 2023 (naalakkersuisut.gl); Canada's ratification and the date of entry into force are not found (Global Affairs Canada's treaty database was unavailable on 2026-11-22). Uninhabited, 1.3 km²: kept with GL until entry into force is confirmed;
  - Vélez de la Gomera and the Chafarinas (D045: own geometries into ES);
  - 45 unexplained fragments in the display check, mostly real exclaves to list in `inputs/known_fragments.csv`;
  - near Pyla a 0.6 km² part of Cyprus moved to Dhekelia by D073: a village area under R060, to be checked by hand;
  - the Okpara villages and the far plots of the Baikonur lease, as before.
- Known GADM defects for Stage 2, reported by TYR: Lake Erie filed wholly under Ohio (TIGER/Line splits it), Uttarakhand and Himachal Pradesh listed three times each, a Ukrainian unit named "?".
- Long term: a canon for every year from 2000 ([#30](https://github.com/uncovering-world/travel-regions-extraction/issues/30)).

## Next step

Answer TYR's open requests and settle a rule for GADM's overlaps. Then add the islands GADM lacks, clear the open items above, cut a first release candidate and answer TYR's remaining requests.
