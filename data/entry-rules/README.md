# Discovery of territory-specific entry rules

A part of a country becomes a region of the canon when entry to it follows its own rule (R044, R056, R055 in [docs/spec.md](../../docs/spec.md)). The rules themselves are kept in a census, `experiments/stage1-world-draft/inputs/crw_scopes.csv`, with the facts checked against their texts in `experiments/stage1-list/inputs/entry_rule_facts.csv`. Under "no witness, no boundary" a rule missing from the census gives no region and no warning, so the census needs a repeatable way to find what it lacks. This folder is that way, built like the [discovery for disputed areas](../disputed-areas/UPDATING.md).

| File | Edited by | Content |
|---|---|---|
| `sources.json` | `discover.py --latest` | The navbox "Visa policy by country" and every linked "Visa policy of …" article, each pinned to a revision |
| `places.json` | `discover.py` | Wikidata answers for the places the articles link (coordinates, class, country); kept between runs |
| `candidates.csv`, `DISCOVERY.md` | `discover.py` only | One candidate per (article, place) where a sentence with an entry-rule word names a place of that country; the list of candidates not yet accounted for |
| `discovery-map.csv` | hand (and `--prefill`) | For every candidate: census row ids, or `ignore` with a reason, or empty (not yet looked at) |
| `cache/` | `discover.py` | Downloads; not committed |

A candidate is only a lead: a sentence that mentions a place near words such as visa-free, permit, restricted, transit or immigration control. Most leads are airports, border crossings or ports named in country-wide rules. Whether a lead is a rule that makes a region is decided by reading the rule's own text, as [UPDATING.md](UPDATING.md) describes. Nothing is entered from memory.

## State

See `DISCOVERY.md`. First run 2026-10-03: 183 articles read, 432 candidates, 58 mapped by name to the census, 374 not yet looked at; 33 of the census's 116 rows are reached by some candidate.
