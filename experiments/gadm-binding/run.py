#!/usr/bin/env python3
"""Bind the regions of the Stage 1 list to GADM 4.1 units by code or name (attributes only, no geometry). Q013.

GADM is read from the consumer's local copy (path in GADM, or the environment variable GADM_GPKG); its data are not
copied into this repository. Inputs: inputs/gadm_codes.csv ties GADM's own pseudo-countries (GID_0 such as ZNC or
Z07) to regions by GADM's NAME_0; inputs/reviewed.csv records reviewed decisions for name matches.

Run from the repository root: python3 experiments/gadm-binding/run.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import sqlite3
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
GADM = Path(os.environ.get("GADM_GPKG", REPO.parent / "track-your-regions" / "deployment" / "gadm_410.gpkg"))
GADM_SHA256 = "5a85ef31541c85e12eed7eabfebe59c88c05881367101696d86abef56bfb4ec2"
ISO = Path("/usr/share/iso-codes/json/iso_3166-1.json")


def read(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def fold(text: str) -> str:
    text = "".join(c for c in unicodedata.normalize("NFKD", text or "") if not unicodedata.combining(c)).casefold()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def short(name: str) -> str:
    """The place name without bracketed or comma-separated additions and generic unit words."""
    name = re.split(r"[(,]", name)[0]
    name = re.sub(r"\b(province|autonomous region|autonomous okrug|autonomous oblast|autonomous republic|"
                  r"autonomous district|region|island|islands|archipelago|state|county|territory|department|"
                  r"of the|of)\b", " ", name, flags=re.I)
    return fold(name)


def main() -> None:
    size = GADM.stat().st_size
    head = hashlib.sha256()
    with GADM.open("rb") as handle:  # hashing 2.7 GB takes a while; done once per run
        for block in iter(lambda: handle.read(1 << 24), b""):
            head.update(block)
    if head.hexdigest() != GADM_SHA256:
        print(f"WARNING: GADM sha256 {head.hexdigest()} differs from the recorded one")
    db = sqlite3.connect(f"file:{GADM}?mode=ro", uri=True)
    units = db.execute("select distinct GID_0, NAME_0, COUNTRY, GOVERNEDBY, SOVEREIGN, DISPUTEDBY, GID_1, NAME_1, "
                       "VARNAME_1, GID_2, NAME_2, VARNAME_2, GID_3, NAME_3 from gadm_410").fetchall()
    countries = {u[0]: u[1] for u in units}
    by_name: dict[tuple[str, str], set[tuple[str, str]]] = defaultdict(set)   # (GID_0, folded name) -> {(level, GID)}
    for g0, _, _, _, _, _, g1, n1, v1, g2, n2, v2, g3, n3 in units:
        for level, gid, names in ((1, g1, [n1] + (v1 or "").split("|")), (2, g2, [n2] + (v2 or "").split("|")),
                                  (3, g3, [n3])):
            for n in names:
                if gid and n and fold(n):
                    by_name[(g0, fold(n))].add((f"GID_{level}", gid))
    alpha3 = {c["alpha_2"]: c["alpha_3"] for c in json.loads(ISO.read_text())["3166-1"]}

    regions = read(REPO / "experiments" / "stage1-list" / "outputs" / "regions.csv")
    census = {r["id"]: r for r in read(REPO / "experiments" / "stage1-world-draft" / "inputs" / "crw_scopes.csv")}
    register = {r["area_id"]: r for r in read(REPO / "data" / "disputed-areas" / "registry.csv")}
    codes = {r["region"]: r for r in read(ROOT / "inputs" / "gadm_codes.csv")}
    reviewed = {r["region"]: r for r in read(ROOT / "inputs" / "reviewed.csv")} if (ROOT / "inputs" / "reviewed.csv").exists() else {}

    rows = []
    for r in regions:
        rid = r["id"]
        out = {"region": rid, "name": r["name"], "basis": r["basis"].split(":")[0].split(";")[0],
               "gadm_units": "", "level": "", "matched_by": "", "note": ""}
        if rid in reviewed:
            out.update({"gadm_units": reviewed[rid]["gadm_units"], "level": reviewed[rid]["level"],
                        "matched_by": "reviewed", "note": reviewed[rid]["note"]})
        elif rid in codes:
            out.update({"gadm_units": codes[rid]["gid_0"], "level": "GID_0", "matched_by": "GADM pseudo-country",
                        "note": f"GADM NAME_0 {countries.get(codes[rid]['gid_0'], '?')}"})
        elif r["basis"].startswith("ISO"):
            g0 = alpha3.get(rid, "")
            if g0 in countries:
                out.update({"gadm_units": g0, "level": "GID_0", "matched_by": "ISO alpha-3"})
            else:
                out["note"] = f"no GADM country {g0 or '(no alpha-3)'}"
        else:
            country = census[rid[5:]]["iso_code"] if rid.startswith("rule/") else ""
            names = {short(r["name"])}
            if rid.startswith("rule/"):
                names.add(short(census[rid[5:]]["name"]))
            names.discard("")
            g0s = [alpha3[country]] if country in alpha3 else list(countries)
            hits = sorted({h for g0 in g0s for n in names for h in by_name.get((g0, n), set())})
            if hits:
                top = min(int(level[-1]) for level, _ in hits)
                chosen = [gid for level, gid in hits if int(level[-1]) == top]
                out.update({"gadm_units": " ".join(chosen), "level": f"GID_{top}",
                            "matched_by": "exact name" + (" (several units)" if len(chosen) > 1 else ""),
                            "note": f"searched {sorted(names)}" + ("" if country else "; country not known, all searched")})
            else:
                out["note"] = f"no GADM unit named {sorted(names)}"
        rows.append(out)

    # GADM pseudo-countries and their place in the canon
    used = {u.split(".")[0] for row in rows for u in row["gadm_units"].split()}
    pseudo = [{"gid_0": g, "name_0": n} for g, n in sorted(countries.items())
              if not any(g == alpha3.get(a) for a in alpha3) and g not in used]

    (ROOT / "outputs").mkdir(exist_ok=True)
    with (ROOT / "outputs" / "bindings.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "gadm": {"file": GADM.name, "bytes": size, "sha256": GADM_SHA256, "countries": len(countries)},
        "regions": len(rows),
        "matched_by": dict(Counter(r["matched_by"] or "unbound" for r in rows).most_common()),
        "by_basis": {b: dict(Counter(r["matched_by"] or "unbound" for r in rows if r["basis"] == b).most_common())
                     for b in sorted({r["basis"] for r in rows})},
        "unbound": [f"{r['region']}: {r['note']}" for r in rows if not r["gadm_units"]],
        "several_units": [f"{r['region']}: {r['gadm_units']}" for r in rows if "several" in r["matched_by"]],
        "gadm_countries_not_used": [f"{p['gid_0']} {p['name_0']}" for p in pseudo],
    }
    (ROOT / "outputs" / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "by_basis"}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
