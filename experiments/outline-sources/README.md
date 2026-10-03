# Where the outlines of Stage 1 regions can come from

**Experiment, not the canon.** Open question [Q013](../../docs/open-questions.md); issue [#22](https://github.com/uncovering-world/travel-regions-extraction/issues/22).

## Question

The [Stage 1 list](../stage1-list/README.md) names 322 regions but draws none. R047 says an outline is a line the parties state and that the substrate is extended with a custom geometry where it has no fitting unit; Q013 asks how such geometries are sourced, pinned and versioned. Before choosing, measure what is available:

1. For each region, which ready-made outline exists in a pinned, openly licensed dataset: Natural Earth 10m (the edition the registry already uses), GADM (Track Your Regions' current substrate), or an OpenStreetMap boundary relation?
2. How many regions have no outline in any of them, and of what kind are they?
3. How are the regions tied to those datasets: by an identifier the dataset itself publishes (ISO code, Natural Earth feature id, a Wikidata property), or only by name?

No geometry is fetched or compared here; this is a coverage count. Profile: `S1-product-v1`.

## Related

R028, R030, R045, R047; D042; Q013, Q014; consumer contract C6 (not tied to one substrate).

## What would change our mind

Written before the first run.

1. **Natural Earth plus GADM is enough** if together they cover all but a handful of regions (fewer than about 10), and those few are small places a custom geometry can hold. Then the design is "dataset first, custom geometry as the exception".
2. **OpenStreetMap is needed** if a substantial group (about 10 or more) has an outline only there. Its licence (ODbL, share-alike) then becomes a question for the owner and for Track Your Regions.
3. **Identifiers are not enough** if many regions can be tied to a dataset only by name. Then the tie itself must become a maintained, reviewed input, as the ties from the register to conflicts are.
4. If a region kind (detached islands, zones with no single holder, unclaimed land) has no outline anywhere, that kind needs its own procedure for custom geometries.

## Method

```bash
python3 experiments/outline-sources/run.py
```

- **Ties to Wikidata.** ISO entries through the `WIKIDATAID` of the Natural Earth 10m admin-0 feature with that ISO code; registry cells and small features through the Natural Earth disputed-area feature; register areas through the register's `wikidata_id` where it has one. The other 44 regions by a Wikidata name search whose answers are kept in `inputs/name_ties.csv`; all 44 were reviewed by label and description on 2026-10-04 and twelve were corrected (e.g. Labuan resolved to a district in Indonesia, Gorno-Badakhshan to the Soviet-era oblast).
- **Sources per item.** Natural Earth v5.1.2 10m admin-0 (map units, countries, disputed areas) and admin-1 (states and provinces) by their `WIKIDATAID`; GADM and OpenStreetMap through the item's Wikidata properties P8714 (GADM ID) and P402 (OpenStreetMap relation ID).
- **What it does not show.** That a source has a polygon for the item, not that the polygon matches the region's stated outline. GADM coverage is measured only through Wikidata, which records a GADM ID for 97 of the 249 ISO entries: this is a gap in Wikidata, not evidence that GADM lacks the rest. A direct GADM check needs GADM's own files.

## Result

320 regions (the Stage 1 list after the Antarctica correction). Three have no Wikidata item at all (the Koalou zone, the Dniester Security Zone, the UNDOF area of separation).

| Kind of region | Regions | Natural Earth polygon | OpenStreetMap relation | None of the three |
|---|---|---|---|---|
| ISO 3166-1 entries | 249 | 249 | 247 | 0 |
| Entry rules (incl. held areas) | 32 | 26 | 30 | 1 |
| Registry cells | 10 | 10 | 7 | 0 |
| Residents test (islets, paper claims, zones) | 21 | 15 | 12 | 6 |
| Leased areas with their own access rule | 6 | 2 | 2 | 3 |
| Unclaimed land | 2 | 1 | 2 | 0 |

Without a Natural Earth polygon and without a GADM ID on Wikidata: 17 regions. Seven of them have an OpenStreetMap relation (Diego Garcia, Gornja Siga, Nakhchivan, Mount Athos, Minicoy, Phu Quoc, Socotra); ten have none (Koalou, Moldauhafen, Rukwanzi–Semliki, the Russian ranges in Kazakhstan, the Spratly Islands, Tiwinza, the Dniester Security Zone, the UNDOF area, Varosha, Rapa Nui as the special territory).

## Conclusion

Against what was written beforehand:

1. *Not met.* Natural Earth with GADM (as far as Wikidata shows) leaves 17 regions, not fewer than ten. Natural Earth alone covers every ISO entry and every registry cell, and 26 of 32 entry-rule regions.
2. *Borderline.* Seven regions have an outline only in OpenStreetMap, close to the threshold of ten.
3. *Met.* 44 of 71 regions that are not ISO entries could be tied only by name, and twelve name searches were wrong. Ties are a maintained, reviewed input.
4. *Met.* Leased areas and zones with no single holder are the kinds without outlines; their outlines are lease and ceasefire lines published in treaty annexes and maps, so they need a procedure for custom geometries from such documents.

What this supports: a layered design — Natural Earth for countries, registry cells and many first-level units; OpenStreetMap relations (pinned by version) or GADM units for smaller units; a custom geometry digitised from a cited document for the ten with nothing. Which layer is the canon's reference geometry, and whether OpenStreetMap's share-alike licence is acceptable, are the owner's choices (Q013).

## Status

Concluded 2026-10-04.
