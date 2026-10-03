# Register of disputed and special-status areas

Facts about land areas whose attribution to a country is contested, undefined or special: de facto states, occupied areas, buffer zones, leases, claimed territories, disputed islets, border-line disputes and areas with no agreed boundary.

**The register holds facts, not decisions.** Whether an area becomes a canon cell, a tickable special place or a marker on a boundary is decided by rules in [docs/spec.md](../../docs/spec.md) that read these facts. Changing one's mind means changing a rule, not this data.

## Files

| File | Edited by | Content |
|---|---|---|
| `areas.csv` | hand | One row per area: stable `area_id`, name, and the links that drive machine facts — `wikidata_id`, `natural_earth_id` (one or more Natural Earth `NE_ID` values, space-separated) |
| `facts.csv` | hand (manual rows), `refresh_machine.py` (machine rows) | One row per fact: area, field, value, sources, date read, evidence level, origin |
| `sources.csv` | hand | Sources and whether they can be read by machine |
| `registry.csv`, `pages/`, `REPORT.md` | `build.py` only | A summary table, one readable page per area, and the work list |
| `discovery-map.csv` | hand | For every candidate found by `discover.py`: the area(s) it corresponds to, or `ignore` with a reason |
| `candidates.csv`, `DISCOVERY.md` | `discover.py` only | Candidates from Wikipedia's list of territorial disputes and Natural Earth (both pinned), and the list of those not yet accounted for |
| `seed/` | — | The census the register was first filled from (2026-10-03) and the script that imported it |

Fields and allowed values are defined at the top of `build.py`. The `kind` of an area is one of: `own_regime`, `lease_or_base`, `de_facto_state`, `occupied_or_annexed`, `paper_claim`, `islets_for_maritime_zone`, `line_position`, `no_agreed_boundary`, `resolved_recently`; their meaning is in [UPDATING.md](UPDATING.md).

Evidence levels: `primary` (an official or legal source read directly), `secondary` (a reputable secondary source, including Wikipedia), `memory` (written from general knowledge, no source — to be replaced), `machine` (read by `refresh_machine.py`).

## Commands

From the repository root:

```bash
python3 data/disputed-areas/refresh_machine.py --date YYYY-MM-DD   # re-read Natural Earth and Wikidata
python3 data/disputed-areas/discover.py                            # candidates from the pinned lists; what is not yet in the register
python3 data/disputed-areas/build.py                               # validate and regenerate derived files
python3 data/disputed-areas/build.py --check                       # what the tests run
```

Both scripts are deterministic: the same inputs give byte-identical outputs. Natural Earth is pinned to a version and checked by checksum; Wikidata is live, so a refresh records the date it was read and any change shows up in `git diff`.

## State on 2026-10-03

210 areas from a multi-source census (Wikipedia's list of territorial disputes, a 2023 snapshot of the CIA World Factbook's disputes field, Natural Earth). No fact has primary evidence yet; about two thirds rest on memory only. The first census was compiled by an agent, not by the discovery script, so 143 of the 264 candidates are not yet matched to areas and 102 areas are not yet traced to a candidate; `DISCOVERY.md` lists both. `REPORT.md` is the work list for facts. How to work through it is in [UPDATING.md](UPDATING.md).
