"""Deterministic open-world pairwise evaluation."""

from __future__ import annotations

from dataclasses import dataclass

from .model import (
    ComparisonInput,
    DataBlocker,
    DataBlockerKind,
    EvaluatorOutput,
    EvaluatorResult,
    FactualUnitReference,
    ModelBlocker,
    Profile,
    RuleDerivation,
    SignatureEquality,
    TravellerWitness,
)
from .signatures import assess_signature, signatures_equal


HARD_WITNESS_DIMENSIONS = frozenset(
    {
        "acceptable_identity_document",
        "admission_decision_scope",
        "document_scope",
        "hard_permits",
        "protected_area_permit",
        "relevant_hard_permits",
        "visa_requirement",
        "visa_scope",
        "visa_territorial_validity",
    }
)
OUT_OF_SCOPE_TRAVELLERS = frozenset({"diplomatic_mission", "military_mission", "work", "migration"})
ACCEPTED_EVIDENCE_STATUSES = frozenset({"verified", "supported"})


@dataclass(frozen=True)
class WitnessAssessment:
    accepted: tuple[TravellerWitness, ...]
    rejected: tuple[tuple[str, str], ...]
    data_blockers: tuple[DataBlocker, ...]
    applied_rules: tuple[str, ...]


def _assess_witnesses(comparison: ComparisonInput) -> WitnessAssessment:
    accepted: list[TravellerWitness] = []
    rejected: list[tuple[str, str]] = []
    blockers: set[DataBlocker] = set()
    rules: set[str] = set()
    for witness in sorted(comparison.witnesses, key=lambda item: item.id):
        rules.update(("R007", "R008"))
        if witness.scope != "R007":
            rejected.append((witness.id, "outside territorial R007 scope"))
            continue
        if witness.traveller_scope in OUT_OF_SCOPE_TRAVELLERS:
            rejected.append((witness.id, "outside civilian short-stay traveller scope"))
            continue
        if witness.dimension not in HARD_WITNESS_DIMENSIONS:
            rejected.append((witness.id, "dimension is not a profile hard territorial dimension"))
            continue
        if witness.decision_a is None or witness.decision_b is None or witness.decision_a == witness.decision_b:
            rejected.append((witness.id, "does not contain two different decisions"))
            continue
        bad_evidence = tuple(
            ref
            for ref in witness.evidence_refs
            if ref in comparison.evidence
            and comparison.evidence[ref].status not in ACCEPTED_EVIDENCE_STATUSES
        )
        if witness.status != "verified" or bad_evidence:
            refs = bad_evidence or witness.evidence_refs
            blocker_ids = tuple(f"{ref}.status" for ref in bad_evidence)
            if not blocker_ids:
                blocker_ids = (f"{witness.id}.evidence_status",)
            for blocker_id in blocker_ids:
                blockers.add(
                    DataBlocker(
                        blocker_id,
                        tuple(refs),
                        kind=DataBlockerKind.VERIFICATION_STATUS,
                    )
                )
            rejected.append((witness.id, "evidence status is not verified"))
            continue
        accepted.append(witness)
    return WitnessAssessment(
        accepted=tuple(accepted),
        rejected=tuple(rejected),
        data_blockers=tuple(sorted(blockers)),
        applied_rules=tuple(sorted(rules)),
    )


def must_separate(
    a: FactualUnitReference,
    b: FactualUnitReference,
    profile: Profile,
    evidence: dict[str, object] | None = None,
    *,
    comparison: ComparisonInput | None = None,
) -> tuple[RuleDerivation, ...]:
    """Return sufficient split derivations; endpoints are explicit for the public predicate."""
    del a, b, evidence
    if comparison is None:
        return ()
    derivations: list[RuleDerivation] = []
    witness_assessment = _assess_witnesses(comparison)
    for witness in witness_assessment.accepted:
        derivations.append(
            RuleDerivation("R007", EvaluatorResult.MUST_SEPARATE, witness.evidence_refs)
        )
    jurisdiction_verified = bool(comparison.jurisdiction_evidence_refs) and all(
        ref in comparison.evidence and comparison.evidence[ref].status == "verified"
        for ref in comparison.jurisdiction_evidence_refs
    )
    if (
        profile in {Profile.P2, Profile.P3}
        and comparison.jurisdiction_difference is True
        and jurisdiction_verified
    ):
        derivations.append(
            RuleDerivation(
                "R011",
                EvaluatorResult.MUST_SEPARATE,
                comparison.jurisdiction_evidence_refs,
            )
        )
    return tuple(sorted(set(derivations)))


def hard_compatible(
    a: FactualUnitReference,
    b: FactualUnitReference,
    profile: Profile,
    evidence: dict[str, object] | None = None,
    *,
    comparison: ComparisonInput | None = None,
) -> bool:
    del evidence
    if comparison is not None and must_separate(a, b, profile, comparison=comparison):
        return False
    a_signature = assess_signature(a, profile)
    b_signature = assess_signature(b, profile)
    return (
        a_signature.complete
        and b_signature.complete
        and signatures_equal(a, b, profile) is SignatureEquality.TRUE
    )


def _explanation(
    result: EvaluatorResult,
    *,
    accepted_witnesses: tuple[TravellerWitness, ...],
    rejected_witnesses: tuple[tuple[str, str], ...],
    data: tuple[str, ...],
    model: tuple[str, ...],
) -> str:
    if result is EvaluatorResult.RULE_CONFLICT:
        base = "Applicable normative derivations require incompatible terminal outcomes."
    elif result is EvaluatorResult.MUST_SEPARATE:
        if accepted_witnesses:
            ids = ", ".join(item.id for item in accepted_witnesses)
            base = f"Verified hard territorial witness certificate accepted: {ids}."
        else:
            base = "Independently verified final admission jurisdictions differ under R011."
    elif result is EvaluatorResult.MODEL_UNRESOLVED:
        base = "Undefined model predicates can change the outcome: " + ", ".join(model) + "."
        if data:
            base += " Data blockers also recorded: " + ", ".join(data) + "."
    elif result is EvaluatorResult.DATA_UNKNOWN:
        base = "Concrete data blockers prevent the required assessment: " + ", ".join(data) + "."
    elif result is EvaluatorResult.HARD_COMPATIBLE:
        base = (
            "Both Stage 1 profile signatures are complete and equal, with no applicable "
            "mandatory-separation certificate."
        )
    else:
        base = "No sufficient split certificate or complete equal signature is available."
    if rejected_witnesses:
        details = "; ".join(f"{item}: {reason}" for item, reason in rejected_witnesses)
        base += " Rejected witness candidates: " + details + "."
    return base


def evaluate(comparison: ComparisonInput, profile: Profile) -> EvaluatorOutput:
    a_signature = assess_signature(comparison.a, profile)
    b_signature = assess_signature(comparison.b, profile)
    equality = signatures_equal(comparison.a, comparison.b, profile)
    witness_assessment = _assess_witnesses(comparison)

    rules = set(witness_assessment.applied_rules)
    evidence_refs: set[str] = set()
    data_blockers = {
        blocker
        for blocker in comparison.data_blockers
        if profile in blocker.profiles
    }
    data_blockers.update(witness_assessment.data_blockers)
    data_blockers.update(a_signature.data_blockers)
    data_blockers.update(b_signature.data_blockers)
    if profile in {Profile.P2, Profile.P3} and comparison.jurisdiction_difference is True:
        jurisdiction_verified = bool(comparison.jurisdiction_evidence_refs) and all(
            ref in comparison.evidence and comparison.evidence[ref].status == "verified"
            for ref in comparison.jurisdiction_evidence_refs
        )
        if not jurisdiction_verified:
            data_blockers.add(
                DataBlocker(
                    "final_admission_jurisdiction.evidence_status",
                    comparison.jurisdiction_evidence_refs,
                    frozenset({Profile.P2, Profile.P3}),
                )
            )
    model_blockers = {
        blocker
        for blocker in comparison.model_blockers
        if profile in blocker.profiles
    }
    model_blockers.update(a_signature.model_blockers)
    model_blockers.update(b_signature.model_blockers)

    explicit_derivations = tuple(sorted(comparison.derivations))
    terminal_requirements = {item.requires for item in explicit_derivations}
    if {
        EvaluatorResult.MUST_SEPARATE,
        EvaluatorResult.HARD_COMPATIBLE,
    }.issubset(terminal_requirements):
        result = EvaluatorResult.RULE_CONFLICT
        rules.update(item.rule for item in explicit_derivations)
        for item in explicit_derivations:
            evidence_refs.update(item.evidence_refs)
    else:
        split_derivations = must_separate(
            comparison.a,
            comparison.b,
            profile,
            comparison=comparison,
        )
        if split_derivations:
            result = EvaluatorResult.MUST_SEPARATE
            rules.update(item.rule for item in split_derivations)
            for item in split_derivations:
                evidence_refs.update(item.evidence_refs)
        elif model_blockers:
            result = EvaluatorResult.MODEL_UNRESOLVED
            if profile is Profile.P3:
                rules.add("R010")
        elif data_blockers:
            result = EvaluatorResult.DATA_UNKNOWN
        elif hard_compatible(comparison.a, comparison.b, profile, comparison=comparison):
            result = EvaluatorResult.HARD_COMPATIBLE
            rules.update(("R008", "R009"))
            evidence_refs.update(a_signature.evidence_refs)
            evidence_refs.update(b_signature.evidence_refs)
        else:
            result = EvaluatorResult.SEPARATION_NOT_PROVEN

    if result is EvaluatorResult.DATA_UNKNOWN:
        for blocker in data_blockers:
            evidence_refs.update(blocker.evidence_refs)

    accepted_witnesses = (
        witness_assessment.accepted if result is EvaluatorResult.MUST_SEPARATE else ()
    )
    if result in {
        EvaluatorResult.RULE_CONFLICT,
        EvaluatorResult.MUST_SEPARATE,
        EvaluatorResult.HARD_COMPATIBLE,
        EvaluatorResult.SEPARATION_NOT_PROVEN,
    }:
        output_data_blockers: set[DataBlocker] = set()
        output_model_blockers: set[ModelBlocker] = set()
    elif result is EvaluatorResult.DATA_UNKNOWN:
        output_data_blockers = data_blockers
        output_model_blockers = set()
    else:
        output_data_blockers = data_blockers
        output_model_blockers = model_blockers
    data_ids = tuple(sorted({item.id for item in output_data_blockers}))
    model_ids = tuple(sorted({item.id for item in output_model_blockers}))
    return EvaluatorOutput(
        comparison_id=comparison.id,
        profile=profile,
        result=result,
        applied_rules=tuple(sorted(rules)),
        witnesses=tuple(sorted(item.id for item in accepted_witnesses)),
        signature_a_complete=a_signature.complete,
        signature_b_complete=b_signature.complete,
        signature_equal=equality,
        blocked_by_data=data_ids,
        blocked_by_model=model_ids,
        evidence_refs=tuple(sorted(evidence_refs)),
        explanation=_explanation(
            result,
            accepted_witnesses=accepted_witnesses,
            rejected_witnesses=witness_assessment.rejected,
            data=data_ids,
            model=model_ids,
        ),
    )
