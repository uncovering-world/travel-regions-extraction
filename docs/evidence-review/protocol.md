# Reviewing CR-W evidence

Proposal version: `crw-review-v1-draft`, 14 September 2026. Task: [#12](https://github.com/uncovering-world/travel-regions-extraction/issues/12).

Status: a draft procedure; agreement with the maintainer on the reviewer's responsibility and competence has not yet been obtained. Nobody is appointed as a reviewer. The document does not certify geographic facts and does not adopt new canon rules.

The procedure serves [R044](../spec.md#r044--cr-w-proven-hard-territorial-traveldecision-discontinuity-accepted-d032), D032–D037 and the [current core contract](../../experiments/q001/stage1-core-adoption.md). Where they diverge, the normative documents take precedence. A worked example is the [Greenland walkthrough](greenland-walkthrough.md).

## What a review produces

The unit of review is a specific version of a proof: two scopes, one traveller class, one comparison date, one accepted hard dimension and the linked sources. The reviewer confirms that the conclusion follows from the sources and that every premise applies. The reviewer does not approve a desired list of regions.

For CR-W one admissible class is enough regardless of frequency. A successful review of one difference does not prove the completeness of other rules or the final placement of territories in the canon. The absence of a certificate does not mean `hard_compatible`: that requires a separate positive proof of full equality of all accepted hard dimensions on one S/t.

## Responsibility and competence — a proposal for agreement

| Role | Responsibility |
|---|---|
| Preparer, human or AI | Assembles a reproducible package, separates quotation from interpretation, lists exceptions and gaps; records the tools and versions used. Does not give its own AI conclusion the status `verified`. |
| Accountable reviewer, human | Personally reads the material sources, checks both sides and all gates, and signs the decision with an exact scope of responsibility. May involve a specialist for a specific premise, keeping the specialist's opinion and its limits. |
| Maintainer | Agrees the required competence or a specific reviewer, ensures the decision is recorded and the artifacts are accessible. Does not replace missing evidence with an administrative signature. Handles normative questions separately. |

Proposed minimum competence: the ability to read the material rules in the source language, or to check a translation with a competent participant; to trace territorial and temporal applicability, amendments and exceptions; to tell a legal rule from a guide or an advisory; to apply R044 and to check the provenance of a stored version. A job title, a degree or confidence do not by themselves confirm these abilities. Where competence on a specific point is lacking, that point stays open until a suitable specialist takes part.

The maintainer may review an AI-prepared dossier if they meet these requirements and personally check the sources. That is not external independent expertise. If one person both prepared a material legal conclusion and reviews it, this is recorded as self-review, and another competent person is proposed for the final confirmation of that conclusion. No automatic two-person requirement is introduced for AI-prepared material.

The record discloses participation in preparation, reliance on the same translation or retelling, possible conflicts of interest and the limits of competence. A second AI, several agreeing models, a schema check or a successful evaluator run is not human confirmation. The number of votes does not resolve a conflict between sources.

To settle #12 it is enough to accept this competence profile and division of responsibility, or to state changes. A specific person must be named and confirm their work before the first real `verified` signature; agreeing the profile does not by itself create such a signature.

## States and transitions

These are procedure states, not an extension of the evaluator's enum. `reviewed` is not passed to production as `verified`. Procedure states, the truth of individual premises and evaluator results are kept separately.

| Transition | Condition and record |
|---|---|
| New material → `candidate` | There is a package version, author/tool, scope/context/t, the claimed conclusion and a list of missing material. An AI extraction always starts here. |
| `candidate` → `reviewed` | A named person has completed a documented review of the stated extent. For each gate and both sides the finding and references are recorded; unchecked points are listed explicitly. Possible outcomes: ready for confirmation, insufficient data, conflict, refuted candidate, unresolved semantics. |
| `reviewed` → `verified` | The reviewer's responsibility is agreed; all five gates and both differing D are proven, sources and material exceptions are checked, and no conflicts relevant to the conclusion remain open. The signature contains the package version, the scope and the review date. |
| Corrected or updated package → new `candidate` | A change of source, class, scope, comparison date or material interpretation requires a new version and a review of the affected premises. An old signature is not carried over automatically. |

A verified narrow quotation may be accepted as a separate statement while the certificate as a whole remains `candidate` or `reviewed`. Accepting a quotation does not confirm the source's competence for the whole legal conclusion.

If an error is found in an already confirmed package, an immutable withdrawal or replacement record is created with the reason, the affected certificates and the interval. Such a package is excluded from new production builds until the problem is resolved; the historical version and result stay reproducible together with the withdrawal notice. A new rule after t does not automatically invalidate a correct review for an earlier t, but it does not allow its use for a new date either.

## What to keep before signing

For each material premise:

- The source identifier, the publisher and why it is competent for this particular statement; the official URL, version or edition, and an exact locator — article, page, section, table or paragraph.
- A stored version of the text used, accessible to the reviewer, with SHA-256 and a description of how it was obtained. For HTML, keep the material context, tables, footnotes and linked exceptions; a screenshot of the heading or a short quotation is not enough. For PDF, the edition used. An accessible immutable archive with an identifier and verifiable content is acceptable. A hash of a local retelling does not replace the stored source.
- The retrieval or observation time, the publication date and the proven interval of legal applicability, separately. The start of effect is not derived from the download date; an unknown end of the interval does not mean proven applicability on any future date.
- A short excerpt, a separate translation and interpretation, the exact statement and its limits, references to the territory and context. For OCR or translation, record the tool and version and a human check of the material passages against the original.
- The chain of applicable rules, amendments, transitional provisions and exceptions. For each exception, why it does or does not apply to the given class. "There are no other privileges" without checking the grounds is not enough.

Storing and publishing a source must respect access and permitted use: a public URL does not by itself prove the right to republish. If the full text cannot be published, state where it may be stored, the restrictions and how a reviewer can reproduce it; the public package states the limits of availability honestly. If a material version is unavailable for review, confirmation stays blocked. Circumventing restrictions and taking out new subscriptions are not part of the procedure.

## Checklist of the five gates

For each item record the premise, sources and locators, interpretation, the person who checked it, and the result: proven, refuted, unknown, conflict or unresolved semantics. A gate is proven only when all of its components are proven.

| Check | What the reviewer must establish |
|---|---|
| G-SCOPE | A and B are non-empty and disjoint; the same relevant effect is proven within each scope. A containing object is not compared with a part it contains as if they were disjoint territories. Geometry uncertainty is preserved. A textual definition can suffice when its extent is proven; a polygon is not required by itself. |
| G-CONTEXT | One `civilian-short-stay-v1`, one date, a coherent non-empty class and the same logical trip. All influencing documents, nationalities, residence permits, permits, history, duration and route conditions are stated, together with exceptions. No circular definition of "valid wherever needed". A named person or an actually successful trip is not required. |
| G-HARD | An accepted dimension is chosen; the difference has a territorial legal effect on entry, stay or exit. Names of authorities, claims, island/overseas labels and everyday logistics are not enough. An unclear permit/overlay distinction is kept as Q005/Q009 and not resolved by the territory's size. |
| G-TIME | The rule is in force at t and is a standing or constitutive class rule. It is not exclusively an incident, emergency or event measure. There is no age threshold for the rule. Amendments and the applicability of the edition are checked; an ambiguous classification is kept as Q008. |
| G-EVIDENCE | Both D and the exceptions relating to them are proven by competent sources applicable to the scope, context and t. Every material premise traces to a verified version and locator. Provisional, missing and conflicted material is not promoted to confirmed. |

Separately record the exact values of `decision_a` and `decision_b`, the chosen dimension and the proof that they differ semantically. The territorial coverage of a visa is not replaced by a guarantee of actual admission. `known_absence` requires positive proof; `not_applicable` requires a proven basis; the absence of text gives neither.

After human review a normaliser may prepare a separately versioned input under the existing contract. It keeps references to signatures and evidence and does not change their scope. A structure check and an `evaluate-core` run confirm technical conformance to the interface; they do not replace checking the facts. A partial audit is not exported as a full certificate. This document does not implement a normaliser or a new evaluator.

## Disagreements and stopping confirmation

1. Record the competing statements with exact source versions; check whether scope, class, date and dimension really coincide.
2. Check the competence of the sources, amendments and exceptions separately. Do not pick a convenient quotation or the newest URL without proof of applicability.
3. If a factual or legal dispute is not resolved by the sources, keep `conflict`/`unknown` and ask a competent person to check the relevant premise. The disagreement and its author stay in the history after resolution.
4. If the normative predicate itself is undefined, record `model_unresolved` with the corresponding Q. The reviewer does not adopt CR-J, new hard dimensions or exceptions by territory name.
5. Refuse to promote the affected proof to `verified`. A refuted candidate does not prove compatibility. An unrelated gap does not withdraw another certificate that is already sufficient and applicable.

## Minimum audit record

The record is kept next to the separately versioned proof. This is a documentation format; no new mandatory JSON schema is introduced.

| Field | Content |
|---|---|
| Identity | Review ID, procedure version, package version or manifest hash, comparison ID, model version, scopes A/B, traveller scope, class version, dimension and `as_of`. |
| Preparation | Author, date, AI/model/prompt/tool versions used or an honest `not_recorded`; links to the source material. Missing provenance is assessed explicitly, not invented. |
| Review responsibility | Name or stable account ID of the person, confirmation of participation, basis of competence, role in preparation, limits of independence, link to the maintainer's agreement. |
| Premise matrix | Each component of the five gates, both D and applicable exceptions; source/version/locator, finding, who checked it and open questions. |
| Outcome | Procedure state, review findings and reasons, the exact confirmed scope, the date, and a signature through an attributable review, comment, commit or signed record. A name generated by AI is not a signature. |
| History | Previous version, changes, disagreements and their resolution, withdrawal or replacement, dependent certificates and outputs, reasons for re-review. |

Triggers for re-review: a change in a material source or its availability, a new amendment or exception, a change of context, scope or t, a discovered translation or normalisation error, a conflict, or a change of the accepted contract. The affected extent is reviewed; unaffected references may be reused only with an explicit justification of their applicability to the new version.

## Completion boundary for #12

The task's artifacts are this procedure and the walkthrough of an existing dossier. Completion needs the maintainer's agreement on the competence and responsibility profile and publication of the materials in an agreed way. Closing #12 does not mean completing #13, the appearance of a certificate or the closure of residual Q items. No agreement has been recorded yet; the current walkthrough is an AI demonstration of the procedure.
