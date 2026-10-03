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

## Status

Planned (2026-10-04).
