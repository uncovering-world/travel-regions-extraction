# Release stability policy — proposal

**Status: proposal, not adopted.** Issue: [#20](https://github.com/uncovering-world/travel-regions-extraction/issues/20).

## Question

Under G-TIME (R044) a standing rule separates from the day it takes effect, and R031 has no notion of a release. A canon that follows entry rules directly would change whenever a visa policy changes: of the territory-specific regimes checked in the [2026-09-24 review](../reviews/2026-09-24-independent-review.md) (Appendix C), most changed within ten years. Track Your Regions needs regions that hold still (consumer contract [C7](consumer-contract.md)): progress numbers and curator edits should not move without a stated reason. Visits themselves are safe — TYR records them as points (TYR #768).

How do facts that change continuously become a canon that changes rarely?

## Proposal: two layers

1. **Facts at date t** stay as they are: bitemporal, with effective and recorded time (R031). CR-W is evaluated against them at any t. Nothing changes here.
2. **A release** is a published canon built for a cutoff date. Only releases reach the consumer. A release policy decides which factual changes become changes of the canon.

## Options for the release policy

| | Option | Entry of a new boundary | Exit of a boundary | Trade-off |
|---|---|---|---|---|
| A | **Snapshot** | In force at the cutoff | Not in force at the cutoff | Simple; a regime that happens to exist on the cutoff day enters even if it is a year old and ends next year |
| B | **Snapshot with hysteresis** | In force at two consecutive cutoffs | Absent at two consecutive cutoffs | A regime shorter than one interval never enters; every change is delayed by one release |
| C | **Announced duration** | In force at the cutoff and not announced to end before the next cutoff | Ended, or announced to end before the next cutoff | Uses what the rule itself says; needs no waiting, but many rules state no end date, so it falls back to A |
| D | **Never remove** (as TCC and NomadMania do) | As A or B | A boundary, once in a release, stays; the region is marked historical instead | Maximum stability for travellers; the canon accumulates cells that no rule supports any more |

Common to all options:

- **Interval.** Releases are at least 12 months apart. NUTS uses three years; visa regimes move faster than administrative reforms, and the product is young, so a shorter interval is proposed with the option to lengthen it.
- **De minimis.** A geometry correction that moves less than a stated share of a region's area (proposed 1%, as NUTS does for population) changes the geometry revision, not the region or its identifier (R032).
- **Identifiers** are never reused (R032). A split or merge creates new identifiers with `split_from` / `merged_from`.
- **Correspondence table.** Every release ships a table from the previous release's identifiers to its own, with the rule and input change behind each difference.
- **Registry editions** (ISO 3166-1, Natural Earth) change cells only at a release and only by decision ([registry proposal](reference-registry.md)).

## How the options behave on test cases

| Case | A | B | C | D |
|---|---|---|---|---|
| A new standing regime with no stated end (Rapa Nui 2018) | enters next release | enters one release later | enters next release | enters |
| A regime replaced after six years (Russia's regional e-visas, 2017–2023) | enters, then leaves | enters, then leaves, each one release later | enters, leaves | enters, stays as historical |
| A regime that exists for eight months between two cutoffs | may enter if a cutoff falls inside it | never enters | enters only if a cutoff falls inside it and no end is announced | as A or B |
| A programme renewed year by year with a stated expiry (China's unilateral visa-free list, currently to 31 Dec 2026) | witnesses appear and vanish with each renewal | changes delayed | never counts as lasting — a split that depends on it never enters | as chosen for entry |
| The witness class changes but the split stays (Hainan: which nationalities differ changes, the island stays distinct) | no change | no change | no change | no change |
| A suspended regime (Jeju, February 2020 to June 2022) | leaves and re-enters | leaves only if absent at two cutoffs | leaves if the suspension is open-ended | stays |

## Interaction with G-TIME

G-TIME stays as adopted: it says when a factual separation exists. The release policy is a product layer on top and does not add an age threshold to CR-W. A boundary held back by hysteresis is a true CR-W difference that the current release does not yet publish, and the release notes say so.

## Recommendation

Option B with a 12-month interval, the 1% de-minimis rule and correspondence tables; removed regions are kept in the correspondence table, not in the partition. B is the only option that keeps short-lived regimes out without asking for knowledge of the future, and its cost — a one-release delay — is small for a product where visits are points.

## What adoption would change

A new R item (releases and their policy) and a D entry; R031 gains a note that it describes facts, not releases; R032 gains the de-minimis rule; Q008 narrows (stability is handled at release level; classification of emergency measures stays open); Q010 narrows for the same reason.
