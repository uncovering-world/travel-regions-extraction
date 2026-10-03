# Reference-registry rule — proposal

**Status: option A adopted on 2026-10-03 as [D038](../decisions.md#d038--no-region-crosses-a-country-boundary-under-a-supported-perspective) (R045), with ISO 3166-1 and the Natural Earth national points of view. Parameters: Antarctica unchanged ([D040](../decisions.md#d040--antarctica-is-one-stage-1-cell-divided-in-stage-2-by-access)); editions change only by decision ([D039](../decisions.md#d039--the-canon-is-pinned-to-stated-editions-of-its-reference-lists)); the rule sits in Stage 1. The recommended resolution rule (tie to the substrate) and a size floor are rejected ([D052](../decisions.md#d052--rejected-tying-small-disputed-areas-to-the-substrate-or-a-bare-area-threshold)); small areas are treated by kind (D044–D047). Open details: Q014.** Issue: [#19](https://github.com/uncovering-world/travel-regions-extraction/issues/19). Evidence: [experiments/stage1-world-draft](../../experiments/stage1-world-draft/README.md).

## Question

Requirement C2 of the [consumer contract](consumer-contract.md) says every region lies inside one country under every supported perspective. CR-W cannot guarantee that: it separates only places whose entry rules differ. Which rule does?

It serves C2 and C3, and the open questions Q006 (does a legal dispute preserve a separate identity) and Q011 (are explicit product conventions allowed).

## Options

| | Option | Predicate | What happens to the hard cases |
|---|---|---|---|
| A | **Reference registry** | Stage 1 refines every partition in a declared, versioned registry: for each declared partition P and each Stage 1 cell s, s lies inside exactly one class of P (or in its remainder). | Countries, microstates, overseas territories with their own ISO 3166-1 entry and perspective-dependent areas are separated by construction. |
| B | Adopt CR-J (independent admission competence) | Different final admission jurisdictions separate, even with equal rules. | Separates states and most dependencies, but needs a J1–J6 legal proof per pair; does not separate areas where perspectives disagree and the regime is the controller's (Golan, Aksai Chin). |
| C | Curated convention list | A named, cited list of territories kept separate. | Works for D004–D007 but is a list of names: the project's own rules reject it (R008, D036) unless Q011 allows it. |
| D | CR-W only (today) | — | D004–D007 remain accepted but underivable; microstates without an entry regime merge with neighbours. |

Option A needs no legal proof: the registry is a product declaration with an external source, checked by comparing with a hashed snapshot. It is name-blind relative to the registry. It adds boundaries only; CR-W continues to split inside registry cells.

## What the first experiment shows

Count-only run on ISO 3166-1 (249 entries) and Natural Earth v5.1.2 with its 31 national point-of-view attributions:

| Registry | Cells (features ≥ 100 km²) | Cells (no size floor) |
|---|---|---|
| ISO 3166-1 only | 249 | 249 |
| + Natural Earth default (de facto) | 259 | 265 |
| + all 31 points of view | 278 | 298 |

- **ISO 3166-1 alone is not enough.** It has no cell for Crimea, Kosovo, Northern Cyprus, Somaliland, Abkhazia, South Ossetia or the UK Sovereign Base Areas. D006 holds under it only by not saying anything about Crimea.
- **With all points of view, D004–D007 are derived**, with two caveats: the British Antarctic Territory lies inside AQ (R026 keeps Antarctica as one cell), and Akrotiri (78 km²) falls under a 100 km² floor while Dhekelia (102 km²) does not.
- **The points of view add 29 cells above the floor**: de facto states (Kosovo, Northern Cyprus, Somaliland, Abkhazia, South Ossetia, Nagorno-Karabakh, two areas of eastern Ukraine), large disputed areas (Crimea, Western Sahara west of the berm, the Kashmir sectors, Aksai Chin, Arunachal Pradesh, Golan Heights, Halayib is *not* among them because every point of view gives it to Egypt), and a few smaller ones (Abyei, the Ilemi triangle, the southern Kurils, Olivenza, East Jerusalem).
- **Transnistria is not separated**: every Natural Earth point of view, including Russia's, attributes it to Moldova. It would be a cell only through CR-W.
- **Natural Earth needs a resolution rule.** Twenty features are under 100 km² (reefs, river islets, the Spanish plazas, Hans Island). Without a floor they would be 20 more cells with no substrate unit to hold them.
- **Natural Earth's attributes are not clean.** Names of disputed features are often the administering country's ("India", "Georgia", "Ukraine", and "Greenland" for Hans Island), codes for "shown as disputed" are opaque (`B17`, `UUU`), and at least one value is an error (Barbados attributed to Uruguay in the Argentine column). None of this changed a cell above the floor, but cell names and the country attribute cannot be taken from these columns unchecked.
- **Five features equal a whole ISO entry** (Taiwan, Falkland Islands, South Georgia, Israel under three points of view, Western Sahara east of the berm) and add no cell; they only change which country the entry counts under.

## Parameters the owner would have to set

1. **Which perspectives.** ISO 3166-1 only (249), plus the de facto default (259), or plus the national points of view (278). The consumer's side of this is TYR #771.
2. **Resolution.** What happens to registry areas too small to be a region: a size floor, "must correspond to a substrate unit", or attach to a neighbour with a marker (TYR's draft rule P4 does the latter).
3. **Antarctica.** Whether claim sectors, which a registry of national points of view would introduce, override R026's single Antarctic cell. Proposed: they do not.
4. **Registry versioning.** A new edition of ISO 3166-1 or Natural Earth changes cells only through a decision, not automatically (ties to the release policy, #20).
5. **Where the rule sits.** In Stage 1, so Stage 2 can never cross a registry boundary.

## Effects on existing items if adopted

- New R item (registry refinement) and a new check; R009 and R039 amended (Stage 1 = coarsest partition refining the registry and satisfying CR-W); R016's clause that an ISO code never separates narrowed to ISO 3166-2 and other labels.
- D004–D007 become derivable (with the caveats above); D036's gap closes when the check passes.
- Q006 and Q011 narrow; a new open question holds the registry's composition.
- CR-J (Q001 residual) loses most of its motivation: the cases it was meant for have their own ISO 3166-1 entries.
- The adversarial set gains rows for microstates and perspective-dependent areas.

## Recommendation

Adopt option A with all Natural Earth national points of view plus ISO 3166-1, a resolution rule tied to the substrate (an area that no substrate unit can represent is attached to the administering cell and marked), Antarctica unchanged, and registry editions changing only by decision. Use Natural Earth for the attribution of areas, not for names.
