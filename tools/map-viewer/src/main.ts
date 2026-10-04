import maplibregl, { type GeoJSONSource, type MapGeoJSONFeature } from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import "./style.css";

interface Source {
  url: string;
  label: string;
}

/** A fact a region rests on, with its sources and the passage quoted from them. */
interface Fact {
  field: string;
  value: string;
  quote: string;
  evidence: string;
  sources: Source[];
}

/** A special place or a marker that lies in a region (R046). */
interface Inside {
  id: string;
  name: string;
  what: string;
  why: string;
  where: string;
  wikidata_id?: string;
  link?: string;
}

/** Properties of a region feature, as written by experiments/release-draft/export_viewer_data.py. */
interface RegionProps {
  id: string;
  name: string;
  country: string;
  country_code: string;
  basis: string;
  why: string;
  rules: { id: string; url: string; title: string }[];
  status: string;
  evidence: string;
  evidence_text: string;
  open: string;
  povs: Record<string, string>;
  facts: Fact[];
  carved: { id: string; name: string; how: string }[];
  inside?: Inside[];
  inside_count: number;
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
  source_url: string;
  notes: string;
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
  const places = await load<FC<Inside & { region: string }>>("/data/places.geojson");
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
  if (import.meta.env.DEV) (window as unknown as { map: maplibregl.Map }).map = map; // for checks from the console
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
  recolour(CANON); // before the source exists, so the large file is tiled once, not twice

  let hovered: string | null = null;
  let pinned: string | null = null;

  function show(id: string | null): void {
    const f = id ? byId.get(id) : undefined;
    if (!f) {
      $("info").innerHTML = '<p class="muted">Hover over a region; click it to pin the details and follow their links.</p>';
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
    const seen = new Set<string>();
    const ownLines = owns.filter((o) => !seen.has(o.properties.place) && seen.add(o.properties.place));
    const link = (url: string, text: string) =>
      url ? `<a href="${esc(url)}" target="_blank" rel="noreferrer">${esc(text)}</a>` : esc(text);
    const sourceLinks = (sources: Source[]) =>
      sources.filter((s) => s.url).map((s, i) => link(s.url, `[${i + 1}]`)).join(" ");
    const host = (url: string) => { try { return new URL(url).hostname.replace(/^www\./, ""); } catch { return url; } };
    const inside = p.inside ?? [];
    $("info").innerHTML = `
      <h2>${esc(p.name)} ${pinned === p.id ? '<span class="pin">(pinned)</span>' : ""}</h2>
      <p class="muted">${esc(p.country)}${p.id !== p.country_code ? ` · <code>${esc(p.id)}</code>` : ""}${
        p.wikidata_id ? ` · ${link(`https://www.wikidata.org/wiki/${p.wikidata_id}`, p.wikidata_id)}` : ""}</p>

      <h3>Why it is a region</h3>
      <p>${esc(p.why)}</p>
      ${p.status ? `<p><b>In the canon:</b> ${esc(p.status)}</p>` : ""}
      <p class="rules">${p.rules.map((r) => link(r.url, `${r.id} ${r.title}`)).join(" · ")}</p>
      <p class="muted">Evidence: ${esc(p.evidence_text)}.</p>
      ${p.open ? `<p class="warn">Still open: ${esc(p.open)}</p>` : ""}

      ${p.facts.length ? `<h3>Facts it rests on</h3><ul class="facts">${p.facts.map((f) => `
        <li><b>${esc(f.field)}:</b> ${esc(f.value)} ${sourceLinks(f.sources)}
          ${f.quote ? `<details><summary>quote${f.sources[0]?.url ? ` from ${esc(host(f.sources[0].url))}` : ""}</summary><blockquote>${esc(f.quote)}</blockquote></details>` : ""}
        </li>`).join("")}</ul>` : ""}

      ${inside.length ? `<h3>Special places and notes in it</h3><ul class="facts">${inside.map((s) => `
        <li><b>${esc(s.name)}</b> <span class="tag ${s.what === "note" ? "note" : "special"}">${esc(s.what)}</span>${
          s.wikidata_id ? ` ${link(`https://www.wikidata.org/wiki/${s.wikidata_id}`, s.wikidata_id)}` : ""}<br><span class="muted">${esc(s.why)}${
          s.where !== "inside" ? ` (${esc(s.where)}${s.link === "close" ? "; approximate point" : ""})` : s.link === "close" ? " (approximate point)" : ""}</span></li>`).join("")}</ul>` : ""}

      ${p.carved.length ? `<h3>Separate regions linked to it</h3><ul class="facts">${p.carved.map((c) => `
        <li><a href="#" data-region="${esc(c.id)}">${esc(c.name)}</a> <span class="muted">— ${esc(c.how)}</span></li>`).join("")}</ul>` : ""}

      <h3>Points of view</h3>
      <p>Most say <code>${esc(majority)}</code>${pov !== CANON ? `; ${esc(pov)} says <code>${esc(p.povs[pov])}</code>` : ""}.${
        differing.length ? "<br>Differ: " + differing.map(([k, v]) => `<span class="tag">${esc(k)} → ${esc(v)}</span>`).join("") : ""}</p>

      ${ownLines.length ? `<h3>Own outline</h3><ul class="facts">${ownLines.map((o) => `
        <li>${esc(o.properties.place)}: ${link(o.properties.source_url, o.properties.publisher)}, the line of ${esc(o.properties.whose_line)}
          <span class="muted">(rank ${esc(o.properties.rank)}, ${esc(o.properties.licence)})</span>
          ${o.properties.notes ? `<br><span class="muted">${esc(o.properties.notes)}</span>` : ""}</li>`).join("")}</ul>` : ""}

      <details class="tech"><summary>Made of (substrate units)</summary>${p.units.map((u) => `<code>${esc(u)}</code>`).join("<br>")}</details>`;
    $("info").querySelectorAll<HTMLAnchorElement>("a[data-region]").forEach((a) =>
      a.addEventListener("click", (e) => {
        e.preventDefault();
        focus(a.dataset.region!);
      }),
    );
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
    if (places) {
      map.addSource("places", { type: "geojson", data: places });
      map.addLayer({
        id: "places",
        type: "circle",
        source: "places",
        paint: {
          "circle-radius": ["interpolate", ["linear"], ["zoom"], 1, 3, 6, 6],
          "circle-color": ["case", ["==", ["get", "what"], "note"], "#1d4ed8", "#c2410c"],
          "circle-stroke-color": "#fff",
          "circle-stroke-width": 1,
        },
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
    $("summary").textContent = "Drawing regions…";
    map.once("idle", () => {
      $("summary").textContent =
        `${regions.features.length} regions` + (own ? `, ${own.features.length} own geometries` : "") +
      (places ? `, ${places.features.length} special places and notes on the map` : "") + ". Click a region to pin and zoom.";
    });
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

  const popup = new maplibregl.Popup({ closeButton: false, closeOnClick: false, maxWidth: "320px" });
  map.on("mousemove", "places", (e) => {
    const p = e.features?.[0]?.properties as (Inside & { region: string }) | undefined;
    if (!p) return;
    map.getCanvas().style.cursor = "pointer";
    popup.setLngLat(e.lngLat).setHTML(
      `<b>${esc(p.name)}</b> <span class="tag ${p.what === "note" ? "note" : "special"}">${esc(p.what)}</span><br>` +
      `<span class="muted">${esc(p.why)}</span><br><span class="muted">in ${esc(byId.get(p.region)?.properties.name ?? p.region)}</span>`,
    ).addTo(map);
  });
  map.on("mouseleave", "places", () => popup.remove());
  $<HTMLInputElement>("places").addEventListener("change", (e) => {
    if (map.getLayer("places")) map.setLayoutProperty("places", "visibility", (e.target as HTMLInputElement).checked ? "visible" : "none");
  });
  $<HTMLInputElement>("withPlaces").addEventListener("change", (e) => {
    const on = (e.target as HTMLInputElement).checked;
    $<HTMLInputElement>("nonIso").checked = false;
    for (const f of regions.features) map.setFeatureState({ source: "regions", id: f.properties.id }, { dim: on && !f.properties.inside_count });
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
    $<HTMLInputElement>("withPlaces").checked = false;
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
