import maplibregl, { type GeoJSONSource, type MapGeoJSONFeature } from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import "./style.css";

/** Properties of a region feature, as written by experiments/release-draft/export_viewer_data.py. */
interface RegionProps {
  id: string;
  name: string;
  country: string;
  country_code: string;
  basis: string;
  evidence: string;
  open: string;
  povs: Record<string, string>;
  units: string[];
  wikidata_id: string;
  color?: string;
  differs?: boolean;
}

interface OwnProps {
  place: string;
  region: string;
  rank: string;
  whose_line: string;
  publisher: string;
  licence: string;
}

type FC<P> = GeoJSON.FeatureCollection<GeoJSON.Geometry, P>;

const CANON = "canon";
const $ = <T extends HTMLElement>(id: string) => document.getElementById(id) as T;

/** A stable colour per country code: hue from a hash, lightness by whether the region is a whole ISO entry. */
function colour(code: string, iso: boolean): string {
  let h = 0;
  for (const c of code) h = (h * 31 + c.charCodeAt(0)) % 360;
  return `hsl(${h} 52% ${iso ? 72 : 55}%)`;
}

const isIso = (id: string) => /^[A-Z]{2}$/.test(id);

function esc(s: unknown): string {
  return String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]!);
}

/** The file's JSON, or null when it is missing (Vite answers a missing file with index.html and status 200). */
async function load<T>(path: string): Promise<T | null> {
  try {
    const response = await fetch(path);
    if (!response.ok || !(response.headers.get("content-type") ?? "").includes("json")) return null;
    return (await response.json()) as T;
  } catch (error) {
    console.error(`could not read ${path}`, error);
    return null;
  }
}

function bounds(geometry: GeoJSON.Geometry): maplibregl.LngLatBounds {
  const b = new maplibregl.LngLatBounds();
  const walk = (c: unknown): void => {
    if (Array.isArray(c) && typeof c[0] === "number") b.extend(c as [number, number]);
    else if (Array.isArray(c)) c.forEach(walk);
  };
  if ("coordinates" in geometry) walk(geometry.coordinates);
  return b;
}

async function main(): Promise<void> {
  const regions = await load<FC<RegionProps>>("/data/regions.geojson");
  const own = await load<FC<OwnProps>>("/data/own_geometries.geojson");
  if (!regions) {
    $("summary").innerHTML =
      "No data. Run <code>experiments/release-draft/export_viewer_data.py</code> first (see README).";
    return;
  }
  const byId = new Map(regions.features.map((f) => [f.properties.id, f]));
  const povNames = Object.keys(regions.features[0]?.properties.povs ?? {}).sort();

  const povSelect = $<HTMLSelectElement>("pov");
  povSelect.innerHTML = [`<option value="${CANON}">the canon's attribution</option>`]
    .concat(povNames.map((p) => `<option value="${p}">Natural Earth, ${p}'s point of view</option>`))
    .join("");
  $("names").innerHTML = regions.features
    .map((f) => `<option value="${esc(f.properties.name)}">${esc(f.properties.id)}</option>`)
    .join("");

  const map = new maplibregl.Map({
    container: "map",
    center: [20, 25],
    zoom: 1.6,
    renderWorldCopies: false,
    style: {
      version: 8,
      sources: {
        osm: {
          type: "raster",
          tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
          tileSize: 256,
          maxzoom: 12,
          attribution: "© OpenStreetMap contributors",
        },
      },
      layers: [
        { id: "background", type: "background", paint: { "background-color": "#dbe4ea" } },
        { id: "osm", type: "raster", source: "osm", layout: { visibility: "none" }, paint: { "raster-opacity": 0.45 } },
      ],
    },
  });
  map.addControl(new maplibregl.NavigationControl(), "top-left");
  map.addControl(new maplibregl.ScaleControl(), "bottom-left");

  /** Colour each region by its country under the chosen point of view, and mark where it differs from the canon. */
  function recolour(pov: string): void {
    for (const f of regions!.features) {
      const p = f.properties;
      const code = pov === CANON ? p.country_code || p.country || p.id : p.povs[pov] || "?";
      const canonCode = p.povs.__canon_a3 ?? "";
      p.color = colour(code, isIso(p.id));
      p.differs = pov !== CANON && canonCode !== "" && code !== canonCode;
    }
    (map.getSource("regions") as GeoJSONSource | undefined)?.setData(regions!);
  }

  let hovered: string | null = null;
  let pinned: string | null = null;

  function show(id: string | null): void {
    const f = id ? byId.get(id) : undefined;
    if (!f) {
      $("info").innerHTML = '<p class="muted">Hover over a region; click to pin it.</p>';
      return;
    }
    const p = f.properties;
    const pov = povSelect.value;
    const values = Object.entries(p.povs).filter(([k]) => !k.startsWith("__"));
    const counts = new Map<string, number>();
    values.forEach(([, v]) => counts.set(v, (counts.get(v) ?? 0) + 1));
    const majority = [...counts.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] ?? "";
    const differing = values.filter(([, v]) => v !== majority);
    const owns = own?.features.filter((o) => o.properties.region === p.id) ?? [];
    $("info").innerHTML = `
      <h2>${esc(p.name)} ${pinned === p.id ? '<span class="pin">(pinned)</span>' : ""}</h2>
      <table>
        <tr><td>id</td><td><code>${esc(p.id)}</code></td></tr>
        <tr><td>country</td><td>${esc(p.country)} ${p.country_code ? `<code>${esc(p.country_code)}</code>` : ""}</td></tr>
        ${pov !== CANON ? `<tr><td>under ${esc(pov)}</td><td><code>${esc(p.povs[pov])}</code></td></tr>` : ""}
        <tr><td>points of view</td><td>most: <code>${esc(majority)}</code>${
          differing.length ? "<br>differ: " + differing.map(([k, v]) => `<span class="tag">${esc(k)} → ${esc(v)}</span>`).join("") : ""
        }</td></tr>
        <tr><td>basis</td><td>${esc(p.basis)}</td></tr>
        <tr><td>evidence</td><td>${esc(p.evidence)}</td></tr>
        ${p.open ? `<tr><td>open</td><td>${esc(p.open)}</td></tr>` : ""}
        ${p.wikidata_id ? `<tr><td>Wikidata</td><td><a href="https://www.wikidata.org/wiki/${esc(p.wikidata_id)}" target="_blank" rel="noreferrer">${esc(p.wikidata_id)}</a></td></tr>` : ""}
        <tr><td>made of</td><td>${p.units.map((u) => `<code>${esc(u)}</code>`).join("<br>")}</td></tr>
        ${owns.map((o) => `<tr><td>own geometry</td><td>${esc(o.properties.place)}: rank ${esc(o.properties.rank)}, ${esc(o.properties.whose_line)} <span class="muted">(${esc(o.properties.licence)})</span></td></tr>`).join("")}
      </table>`;
  }

  function focus(id: string): void {
    const f = byId.get(id);
    if (!f) return;
    pinned = id;
    map.fitBounds(bounds(f.geometry), { padding: 40, maxZoom: 8, duration: 600 });
    show(id);
  }

  map.on("load", () => {
    map.addSource("regions", { type: "geojson", data: regions, promoteId: "id" });
    map.addLayer({
      id: "fill",
      type: "fill",
      source: "regions",
      paint: {
        "fill-color": ["get", "color"],
        "fill-opacity": ["case", ["boolean", ["feature-state", "dim"], false], 0.15, 0.85],
      },
    });
    map.addLayer({
      id: "borders",
      type: "line",
      source: "regions",
      paint: { "line-color": "#3a4352", "line-width": 0.5 },
    });
    map.addLayer({
      id: "differs",
      type: "line",
      source: "regions",
      filter: ["==", ["get", "differs"], true],
      layout: { visibility: "none" },
      paint: { "line-color": "#6a1b9a", "line-width": 2 },
    });
    if (own) {
      map.addSource("own", { type: "geojson", data: own });
      map.addLayer({
        id: "own",
        type: "line",
        source: "own",
        paint: { "line-color": "#111", "line-width": 1.2, "line-dasharray": [2, 1.5] },
      });
    }
    map.addLayer({
      id: "hover",
      type: "line",
      source: "regions",
      paint: {
        "line-color": "#b3261e",
        "line-width": ["case", ["boolean", ["feature-state", "hover"], false], 2.5, 0],
      },
    });
    recolour(CANON);
    $("summary").textContent =
      `${regions.features.length} regions` + (own ? `, ${own.features.length} own geometries` : "") + ". Click a region to pin and zoom.";
  });

  map.on("mousemove", "fill", (e) => {
    const f = e.features?.[0] as MapGeoJSONFeature | undefined;
    const id = (f?.properties?.id as string | undefined) ?? null;
    if (id === hovered) return;
    if (hovered) map.setFeatureState({ source: "regions", id: hovered }, { hover: false });
    hovered = id;
    if (hovered) map.setFeatureState({ source: "regions", id: hovered }, { hover: true });
    map.getCanvas().style.cursor = "pointer";
    if (!pinned) show(hovered);
  });
  map.on("mouseleave", "fill", () => {
    if (hovered) map.setFeatureState({ source: "regions", id: hovered }, { hover: false });
    hovered = null;
    map.getCanvas().style.cursor = "";
    if (!pinned) show(null);
  });
  map.on("click", (e) => {
    const f = map.queryRenderedFeatures(e.point, { layers: ["fill"] })[0];
    if (f?.properties?.id) focus(f.properties.id as string);
    else {
      pinned = null;
      show(null);
    }
  });

  povSelect.addEventListener("change", () => {
    recolour(povSelect.value);
    if (pinned) show(pinned);
  });
  $<HTMLInputElement>("search").addEventListener("change", (e) => {
    const q = (e.target as HTMLInputElement).value.trim().toLowerCase();
    const hit = regions.features.find((f) => f.properties.name.toLowerCase() === q || f.properties.id.toLowerCase() === q)
      ?? regions.features.find((f) => f.properties.name.toLowerCase().includes(q));
    if (hit) focus(hit.properties.id);
  });
  $<HTMLInputElement>("nonIso").addEventListener("change", (e) => {
    const on = (e.target as HTMLInputElement).checked;
    for (const f of regions.features) map.setFeatureState({ source: "regions", id: f.properties.id }, { dim: on && isIso(f.properties.id) });
  });
  $<HTMLInputElement>("own").addEventListener("change", (e) => {
    if (map.getLayer("own")) map.setLayoutProperty("own", "visibility", (e.target as HTMLInputElement).checked ? "visible" : "none");
  });
  $<HTMLInputElement>("differ").addEventListener("change", (e) => {
    map.setLayoutProperty("differs", "visibility", (e.target as HTMLInputElement).checked ? "visible" : "none");
  });
  $<HTMLInputElement>("osm").addEventListener("change", (e) => {
    map.setLayoutProperty("osm", "visibility", (e.target as HTMLInputElement).checked ? "visible" : "none");
  });
}

void main();
