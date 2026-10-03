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

Fields and allowed values are defined at the top of `build.py`. The `kind` of an area is one of: `own_regime`, `lease_or_base`, `de_facto_state`, `occupied_or_annexed`, `paper_claim`, `islets_for_maritime_zone`, `line_position`, `no_agreed_boundary`, `unclaimed`, `resolved_recently`; their meaning is in [UPDATING.md](UPDATING.md).

Every manual fact carries the passage of its source that it rests on (`quote`), so it can be checked by re-opening the source; `verify_quotes.py` does that. Evidence levels: `primary` (the official or legal text itself), `secondary` (a reputable secondary source, including Wikipedia at a pinned revision), `machine` (read by `refresh_machine.py`). Facts written from memory are not admitted.

## Commands

From the repository root:

```bash
python3 data/disputed-areas/refresh_machine.py --date YYYY-MM-DD   # re-read Natural Earth and Wikidata
python3 data/disputed-areas/discover.py                            # candidates from the pinned lists; what is not yet in the register
python3 data/disputed-areas/verify_quotes.py                       # re-open sources and check the quoted passages
python3 data/disputed-areas/build.py                               # validate and regenerate derived files
python3 data/disputed-areas/build.py --check                       # what the tests run
```

Both scripts are deterministic: the same inputs give byte-identical outputs. Natural Earth is pinned to a version and checked by checksum; Wikidata is live, so a refresh records the date it was read and any change shows up in `git diff`.

## State

See `REPORT.md` (facts) and `DISCOVERY.md` (candidates). The list of 210 areas came from a first census that was largely written from an agent's memory; its facts were removed and are being re-entered from sources with quoted passages.
