# Status

Updated: 2026-11-19.

## Focus

A first Stage 1 release of the canon for Track Your Regions. The rules for Stage 1 are decided (D038–D074 in [decisions.md](decisions.md), R045–R060 in [spec.md](spec.md)); the [draft release package](../experiments/release-draft/README.md) is built from them and can be inspected on a local map ([tools/map-viewer](../tools/map-viewer/)). Stage 2 comes after the first release (#28).

Track Your Regions now works with the canon directly: its session for the revised catalogue model (TYR #2634) sends requests and defects by cross-session message. Its list of requests is local to TYR (`docs/local/research/2634-method/v9/canon-requests.md` in that repository). TYR has adopted D049: a trip's date picks the release of its year, so no dated attribution periods are needed. Catalogue points for R060 are a read-only snapshot under `~/tyr-exports/`; OSM extracts come from the dev stack's keeper (the Syncer session), one batched request per planet pass.

## Done on 2026-11-19

- D074 / R060 adopted: a small piece of geometry is fixed by hand only where a traveller does something there.
- The uncommitted work of 2026-10-05 is committed: the Cooch Behar enclave exchange, the Chong-Kara transfer, D073 in the render, and the list of real exclaves.
- D073 corrected in practice (a note on D073): only strips move, i.e. parts with no point more than 2 km from their edge. Before this, Ayia Napa and Paralimni were given to Dhekelia and Kodinar to Junagadh. The list of moved and kept parts is computed at full precision and shipped as `release/cut_off_D073.csv` (TYR request 3).
- Antarctica reads AQ under every point of view (D040).
- Northern Cyprus is OSM's outline; GADM's ZNC is bound to Cyprus, so Nicosia south of the Green Line is Cyprus.
- Research: [boundary providers beyond GADM and OSM](research/2026-11-19-boundary-providers.md).

## Waiting for the owner

- The open questions that remain: Q015, Q016, Q018, Q019, Q020, Q013.
- Bir Tawil: whether a party's stated boundary attributes land to a neighbour under its view (TYR no longer needs it).
- Stable keys for the five de facto states and for retired ISO codes (TYR request 6). TYR uses `x-abkhazia` … and `x-cs-1993` meanwhile.

## Active

- [Expedition regions](../experiments/expedition-regions/README.md): the owner keeps uninhabited, barely reachable territories as regions with a mark a consumer may leave out of totals; the candidate definition is being tested on 20 regions.
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

Finish the expedition-region test and put the definition to the owner. Then add the islands GADM lacks, clear the open items above, cut a first release candidate and answer TYR's remaining requests.
