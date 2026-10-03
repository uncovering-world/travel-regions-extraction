# Binding Stage 1 regions to GADM units

**Experiment, not the canon.** Open question [Q013](../../docs/open-questions.md) (binding to substrate units); issue [#22](https://github.com/uncovering-world/travel-regions-extraction/issues/22).

## Question

Track Your Regions draws regions from GADM 4.1 (`gadm_410.gpkg`, see its `db/` scripts). For each of the 317 regions of the [Stage 1 list](../stage1-list/README.md):

1. Can it be written as a set of whole GADM units, and at which level?
2. Which regions cut through GADM units, or have no GADM unit at all, so that they need a custom geometry (D042, D056)?
3. Does a region's GADM country (`GID_0`) agree with the country the canon attributes it to, and where does GADM's own `GOVERNEDBY` / `SOVEREIGN` / `DISPUTEDBY` record differ?

Only attributes are read, no geometry: a match of names or codes is a candidate binding, not proof that outlines agree. GADM's data stay local (its licence forbids redistribution); only unit identifiers are written to this repository.

## Related

R028, R030, R045, R047; D042, D056; Q013; [outline-source survey](../outline-sources/README.md).

## What would change our mind

Written before the first run.

1. **GADM is a sufficient substrate for Stage 1** if all but a handful of regions bind to whole GADM units by code or exact name, and the rest are small places.
2. **Name matching is not enough** if more than about a tenth of the non-ISO regions match only by an ambiguous or approximate name; then bindings are a reviewed input, like the register's ties.
3. **GADM's country attribution conflicts with the canon** wherever a region's `GID_0` is not its canon country; if this happens for more than the known disputed areas, the canon cannot inherit GADM's country tree and must carry its own.

## Status

Planned (2026-10-04).
