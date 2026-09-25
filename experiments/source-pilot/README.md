# From source to explanation: the first pilot

Date of reading: 13 September 2026. [Task](https://github.com/uncovering-world/travel-regions-extraction/issues/3).

We checked how to gather material for mandatory boundaries on three familiar pairs. This is a research package, **not a new canon and not finished separation certificates**. Earlier data and rules were not changed.

## What came out

| Dossier | Practical result | What cannot be claimed yet |
|---|---|---|
| [Denmark and Greenland](cases/greenland.md) | A concrete comparison candidate on visa coverage was found; exemptions for residence permits were examined separately. | That all the evidence for an automatic mandatory separation is ready. |
| [European France and Réunion](cases/reunion.md) | The ordinary Schengen visa, special multiple-entry visas and exemption grounds were separated. | That every Schengen visa holder needs an additional visa. |
| [Tibet and ordinary Chinese territory](cases/tibet.md) | Information on travel to Tibet and China's general permit procedure were kept apart. | That these permits are identical, or that every permit zone automatically forms a region. |

Details and direct links to sources are in the dossiers. **No pair was declared compatible for lack of a finished proof of difference.**

## Why these cases

The selection tests three difficulties of collection: the territorial effect of a document, exceptions, and the ambiguous nature of a permit. It follows existing research questions, not an expected attractive map. It is not a representative sample of the world; it cannot be used to estimate the share of hard territories or the cost of world coverage.

In the geographic part, eight pages were read out of the ten addresses tried; two addresses could not be retrieved. This counts reading targets, not HTTP requests, tokens or person-hours. New pages were opened for specific questions about nationality, the ordinary visa and exceptions; there was no bulk collection. At the user's additional request, a separate [survey of existing aggregators and passport matrices](aggregators.md) was prepared; its pages are not part of these ten geographic sources.

## How the material is organised

- `cases/` — explanations for a human reader: the question, what was found, the limits of the conclusion, the next step.
- [sources.json](sources.json) — what was read and when, who published it, where to find confirmation, short quotations and limitations. Access errors are kept.
- [observations.json](observations.json) — individual statements and their sources, research inferences, the description of the candidate traveller and open checks.
- [dossier-template.md](dossier-template.md) — a repeatable format for the next dossier, not a local backlog.
- [validate.py](validate.py) — an offline integrity check of the package. It is **not a new evaluator** and not a legal check.

Short excerpts and research notes are stored here, not full archived copies of pages. Checksums protect these local materials from unnoticed change but do not prove that the websites are unchanged. Publication, reading and effective dates are kept apart. `null` means "not established", not "the rule has always applied".

## What we learned about the process

A single "visa required" flag is not enough; a chain is needed: document and traveller class → the document's effect in the territory → exceptions → source and period of validity. Information for one side of a comparison cannot automatically be carried over to the other.

Three outcomes of the work differ: **a source was read**, **a narrow statement is supported by text**, **the whole conclusion about a boundary is verified**. This pilot has the first two; the third is not claimed. Another AI or a confident answer does not replace checking the source and its applicability.

The existing code accepts only the last, strongest level — prepared proofs of all required conditions. Passing our records to it as `verified` would be wrong. So there is no automatic converter to production input here, and old evaluator results were not renamed.

## The next small step

Continuation: an [in-depth audit of Denmark / Greenland](audits/greenland-2026-09-13.md). The legislative text was found, the traveller class was refined and a list of exceptions compiled; the original register of the first iteration is kept.

No finished production certificate is claimed yet. The next step is to bring the **Denmark–Greenland dossier** to one verified proof of a difference in the territorial validity of a visa: confirm the remaining exceptions for the given class, the rule's effect on the chosen date and the exact disjoint scope of the comparison. Digitising the boundary is separate work; its absence should not be confused with the absence of a textually defined scope of the rule.

This does not require studying every visa in the world first. The result is one reference dossier that a reviewer can reproduce from the stored material. If a specific condition is not confirmed, we keep the gap rather than change the rule to make the pilot succeed. After that, the same format can be used to judge which part of the work to give to AI.

## Checks

```bash
python3 experiments/source-pilot/validate.py
python3 -m pytest -q
(cd experiments/source-pilot && sha256sum --check --quiet checksums.sha256)
(cd experiments/q001 && sha256sum --check --quiet checksums.sha256)
```

The package does not change the normative specification, does not adopt the separateness of an admission authority as a ground for a boundary and does not develop a destination partition. The old Q001 stays frozen. New observations belong to the reading of 13 September, not retroactively to the old snapshot.
