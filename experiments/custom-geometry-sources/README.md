# Sources for the canon's own geometries

**Experiment, not the canon.** Open question [Q013](../../docs/open-questions.md); issue [#22](https://github.com/uncovering-world/travel-regions-extraction/issues/22).

## Question

The [GADM binding](../gadm-binding/README.md) left three groups of places that GADM 4.1 cannot represent as the canon needs:

- **A.** 20 regions with no whole GADM unit (zones, leases, unclaimed pockets, South Ossetia, East Jerusalem, Western Sahara west of the berm, the southern Kurils, Socotra…);
- **B.** 6 places GADM gives to another country than their holder (Siachen, Demchok, Bhutan's north-western valleys, Kalapani, Halayib, Bir Tawil);
- **C.** 21 small places GADM has no polygon for (islets and reefs).

For each place, which ready-made polygon exists: a feature of Natural Earth v5.1.2 (public domain, already pinned), an OpenStreetMap relation, a Commons map file? How many would have to be digitised from a treaty or map document? No geometry is fetched or compared.

## Related

R047; D042, D056; Q013; [outline-source survey](../outline-sources/README.md).

## What would change our mind

Written before the first run.

1. **Natural Earth can be the default custom layer** if it has a feature for most places of all three groups (all but about five). Then the procedure is "Natural Earth polygon, replaced by a more detailed source only where one is pinned and reviewed".
2. **OpenStreetMap has to be the default** if Natural Earth lacks many places that OpenStreetMap has.
3. **Digitising from documents is a real workload** if more than about five places have no polygon in any source.

## Method

```bash
python3 experiments/custom-geometry-sources/run.py
```

`inputs/places.csv` lists the 47 places (A 20, B 6, C 21) with the Natural Earth disputed-area features that represent them, chosen by the features' own names (`experiments/gadm-binding/outputs/disputed_points.csv`). Each place's Wikidata item is the Natural Earth feature's `WIKIDATAID`, else the item reviewed in the [outline-source survey](../outline-sources/README.md); its OpenStreetMap relation (P402) and Commons map (P3896) are read from Wikidata.

## Result

| Group | Places | Natural Earth polygon | Only OpenStreetMap or Commons | No source |
|---|---|---|---|---|
| A — regions with no GADM unit | 20 | 14 | 2 (Gornja Siga, Socotra) | 4 (Koalou, Rukwanzi–Semliki, the Dniester Security Zone, Varosha) |
| B — land GADM gives to another country | 6 | 6 | 0 | 0 |
| C — places GADM has no polygon for | 21 | 21 | 0 | 0 |
| **Total** | **47** | **41** | **2** | **4** |

27 of the 41 Natural Earth places also have an OpenStreetMap relation, nine a Commons map.

## Conclusion

1. *Met.* Natural Earth has a polygon for 41 of 47 places, including every place of groups B and C. It is the edition the registry already uses (R045), public domain and pinned.
2. *Not met.* OpenStreetMap is needed only for Gornja Siga and Socotra.
3. *Met, small.* Four places — Koalou, Rukwanzi–Semliki, the Dniester Security Zone, Varosha — have no polygon anywhere; their outlines are in agreements and maps that have to be found and digitised.

Natural Earth is drawn at 1:10 million: near the edge of a small place a visit point can fall on the wrong side. Whether to prefer a more detailed source where one exists is the owner's choice.

## Status

Concluded 2026-10-04.
