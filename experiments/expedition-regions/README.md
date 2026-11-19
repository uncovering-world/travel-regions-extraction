# Expedition regions

## Question

The owner decided on 2026-11-19 that uninhabited, barely reachable territories stay regions, but carry a mark so that a consumer can leave them out of an overall count. The question raised by Track Your Regions was France's "k of 14", which counts Clipperton. Before the mark is adopted as a rule, does this candidate definition sort the real regions of the release draft well?

A region is an **expedition region** when both hold:

1. it has no permanent civilian population (staff of stations, bases or missions who rotate are not residents);
2. an ordinary visitor has no regular way in: no scheduled flight or ferry, and no regular landings from publicly sold cruises or tours. It is reached only by a private expedition under a permit, or by a scientific or military mission.

The mark changes no boundary and no count by itself. It is a fact about a region, with sources, which the consumer may use. Profile: the release draft (`S1-product-v1`).

## Related

The owner's decision of 2026-11-19 in the conversation, not yet recorded as a D entry. D040 (Antarctica), D041 and D046 (special places), D004–D005 (ISO entries as regions), D074 (which governs effort on geometry, not counting).

## What would change our mind

- **Rubbish in:** a region the definition marks although ordinary travellers do visit it, e.g. through scheduled expedition cruises sold to the public. That would mean "regular" is defined too narrowly.
- **Misses:** a region it does not mark although a traveller can in practice only reach it by a private, permit-based expedition. That would mean "regular" is defined too broadly.
- **Cases that cannot be decided from sources.** If many regions turn on a judgement the facts cannot settle (how regular is regular), the definition needs a measurable threshold, e.g. landings sold in at least two of the last three years.

## Method

Candidates are picked by a generic test, not by name: every region of `experiments/release-draft/release/regions.csv` whose Wikidata population (P1082, read 2026-11-19) is below 1,000, or that is a register area the register does not mark `inhabited: yes`. That gives 19 regions. Antarctica (AQ) is added by hand because it was named in the discussion. For each candidate, `inputs/facts.csv` records with a source and a quote: whether civilians live there permanently; scheduled transport; publicly sold cruises or tours that land (2023–2026); and the permit regime. `run.py` applies the definition and writes `outputs/summary.json`.

```bash
python3 experiments/expedition-regions/run.py
```

## Result

Run of 2026-11-19 (facts gathered by two research subagents; the sold landings on South Georgia and Jan Mayen were re-checked against the downloaded operator logs):

| Verdict | Regions |
|---|---|
| expedition | UM (every refuge closed to the public; Palmyra by special-use permit) |
| expedition, unconfirmed (no sold landing found 2023–2026) | BV, HM, TF, rule/fr-clipperton, area/gornja-siga |
| ordinary: sold landings, no residents | AQ, GS, rule/au-macquarie-island, rule/sj-jan-mayen |
| ordinary: scheduled transport | rule/sh-ascension (monthly charter flight) |
| ordinary: residents | PN, CC, VA, rule/sh-tristan-da-cunha |
| undecided: facts unknown | area/ankoko-island, area/bir-tawil, area/gazakh-exclaves, area/la-guera, area/shebaa-farms |

Findings that bear on the definition:

- The line between "expedition" and "ordinary" falls exactly at a publicly sold expedition cruise: Antarctica, South Georgia, Macquarie and Jan Mayen are uninhabited and have no scheduled transport, but expedition ships land paying passengers there each season (e.g. Oceanwide Expeditions at Salisbury Plain, South Georgia, 17 Dec 2025, and on Jan Mayen, 4 June 2025).
- A second kind of place falls under the definition by its letter but is not an expedition destination: closed military or border areas (Shebaa Farms, Ankoko, the Gazakh exclaves; also most of UM). No permit opens them to a visitor.
- For the disputed areas the sources rarely say anything about access; five of six stay undecided.
- The register marks Gornja Siga `closed`; a secondary source says Croatia has let people in on land since 6 August 2023. To be checked against a primary source.

## Conclusion

Pending the owner's choice on expedition cruises (see the conversation of 2026-11-19).

## Status

Running (2026-11-19).
