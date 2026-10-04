# Discovery of territory-specific entry rules

A part of a country becomes a region of the canon when entry to it follows its own rule (R044, R056, R055 in [docs/spec.md](../../docs/spec.md)). The rules themselves are kept here: `census.csv` (one row per rule, first collected for the world Stage 1 draft, whose own input copy stays as it was) and `facts.csv` (what the text of each rule says, every value with its source and a verbatim passage; `verify_facts.py` re-opens the sources and writes `VERIFICATION.md`). Under "no witness, no boundary" a rule missing from the census gives no region and no warning, so the census needs a repeatable way to find what it lacks. This folder is that way, built like the [discovery for disputed areas](../disputed-areas/UPDATING.md).

| File | Edited by | Content |
|---|---|---|
| `sources.json` | `discover.py --latest` | The navbox "Visa policy by country" and every linked "Visa policy of …" article, each pinned to a revision |
| `places.json` | `discover.py` | Wikidata answers for the places the articles link (coordinates, class, country); kept between runs |
| `candidates.csv`, `DISCOVERY.md` | `discover.py` only | One candidate per (article, place) where a sentence with an entry-rule word names a place of that country; the list of candidates not yet accounted for |
| `discovery-map.csv` | hand (and `--prefill`) | For every candidate: census row ids, or `ignore` with a reason, or empty (not yet looked at) |
| `census.csv` | hand | The census of territory-specific entry rules |
| `facts.csv`, `VERIFICATION.md` | hand / `verify_facts.py` | What each rule's text says, with sources and passages; the result of re-opening them |
| `cache/` | `discover.py` | Downloads; not committed |

A candidate is only a lead: a sentence that mentions a place near words such as visa-free, permit, restricted, transit or immigration control. Most leads are airports, border crossings or ports named in country-wide rules. Whether a lead is a rule that makes a region is decided by reading the rule's own text, as [UPDATING.md](UPDATING.md) describes. Nothing is entered from memory.

## State

See `DISCOVERY.md`. First run 2026-10-03: 183 articles read, 432 candidates, 58 mapped by name to the census, 374 not yet looked at; 33 of the census's 116 rows are reached by some candidate.

## Verification state (2026-10-04)

`verify_facts.py` found 256 of 319 passages in their sources; 26 were not found and 37 sources could not be read (see `VERIFICATION.md`). Almost all of the 26 are in PDFs (laws and ordinances: Lakshadweep, San Andrés, Rapa Nui, Macquarie Island, Saint Helena, Tristan da Cunha, Matsu) where the text layer breaks lines or words differently from the quote, and a few are pages that have changed since they were read. They are kept, marked unverified here, because removing them would change regions on a reading failure rather than on evidence; each needs a check by hand or a better source.
