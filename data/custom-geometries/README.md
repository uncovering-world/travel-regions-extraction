# The canon's own geometries

Outlines the canon needs where the substrate (GADM 4.1) cannot represent a place (R047, D059). By default these come from Natural Earth v5.1.2's disputed-areas layer and are referenced there by feature id; this folder holds only geometries that have no such source and had to be derived or digitised, each with its derivation, sources and licence in its GeoJSON properties.

| File | Place | How it was made | Licence |
|---|---|---|---|
| `koalou.geojson` | Koalou (Kourou) zone, Benin–Burkina Faso | The polygon of the overlap of the two countries' official national outlines (HDX COD-AB admin-0: Burkina Faso from the Institut Géographique du Burkina, Benin from SALB/OCHA) that contains the village; 64.2 km², 502 vertices, no vertex added by hand. It is the land both claim, i.e. the area between their claim lines (R047). Accepted by the owner on 2026-10-04 (D061). | CC BY-IGO (both inputs) |

The derivation was done once with a set operation outside this repository (see the file's properties); a script that reproduces it from the pinned inputs is still to be written.
