# Land GADM 4.1 does not draw

## Question

Which land does the release's substrate leave out? GADM 4.1 lacks some islands (Chichijima, Fatu Hiva, Rocas Atoll, Malpelo, San Pedro Mártir were found by hand on 2026-11-19, see [the boundary providers note](../../docs/research/2026-11-19-boundary-providers.md)). A traveller's pin on such land lies in no region. This experiment lists all of it at once, instead of one island at a time, so that the release can add what matters through own geometries (D062; an empty `donors` adds land only where GADM has none, D074 (4)).

Runs under the product profile `S1-product-v1`. Assumes no pending proposal.

## Related

D062, D074 (R060), D074 (4) (the land rule); issue #22 (release draft); `docs/status.md` (open item "islands GADM 4.1 does not draw").

## What would change our mind

- If the missing land is a handful of islands, they are added by hand as own geometries, as planned.
- If it is thousands of pieces with real area, adding them one by one is wrong, and a general rule is needed (the land source's attribution for land no unit draws). That is an owner's choice.
- If a missing piece lies near a catalogue point (R060's test: within 1 km), it must be added before the first release whatever its size.

## Method

Every polygon part of World Polygons 11.4 (layer `DoS_WP_11_4`, the land-only source pinned in `data/custom-geometries/sources.json`) of at least `MIN_KM2` is tested at a point inside it against GADM 4.1's units (the GeoPackage's R-tree, then point-in-polygon). Parts that no unit contains, and that no own geometry's land file covers, are missing land. Each is listed with its World Polygons country (`GENC_3`, `ISO_3166_1`), area and point, and the number of TYR catalogue points (`~/tyr-exports/real-points-2026-11-19.csv`, read only) within 1 km of it.

```bash
nice -n 10 flock ~/.cache/tyr-heavy.lock uv run --no-project --with shapely --with pyproj python experiments/missing-land/run.py
```

Outputs: `outputs/missing.csv` (every missing part) and `outputs/summary.json`.

## Result

(pending)

## Conclusion

(pending)

## Status

Running.
