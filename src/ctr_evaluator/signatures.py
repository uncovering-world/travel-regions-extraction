"""Hard-signature completeness and equality predicates."""

from __future__ import annotations

from .model import (
    DataBlocker,
    DimensionState,
    FactualUnitReference,
    ModelBlocker,
    Profile,
    SignatureAssessment,
    SignatureEquality,
)


P1_DIMENSIONS = (
    "admission_decision_scope",
    "visa_scope",
    "document_scope",
    "relevant_hard_permits",
)
P2_DIMENSIONS = P1_DIMENSIONS + ("final_admission_jurisdiction",)
P3_DIMENSIONS = P2_DIMENSIONS + ("identity_discriminator",)

PROFILE_DEFINITIONS: dict[Profile, dict[str, object]] = {
    Profile.P1: {
        "name": "regime_only",
        "version": "q001-0.1.1",
        "traveller_scope_ref": "R007",
        "hard_dimensions": list(P1_DIMENSIONS),
    },
    Profile.P2: {
        "name": "jurisdiction",
        "version": "q001-0.1.1",
        "traveller_scope_ref": "R007",
        "hard_dimensions": list(P2_DIMENSIONS),
    },
    Profile.P3: {
        "name": "jurisdiction_plus_identity",
        "version": "q001-0.1.1",
        "traveller_scope_ref": "R007",
        "hard_dimensions": list(P3_DIMENSIONS),
    },
}


def _base_token(unit: FactualUnitReference, profile: Profile) -> str | None:
    if profile in unit.complete_tokens:
        return unit.complete_tokens[profile]
    if profile is Profile.P2 and Profile.P1 in unit.complete_tokens:
        return unit.complete_tokens[Profile.P1]
    if profile is Profile.P3:
        return unit.complete_tokens.get(Profile.P2)
    return None


def assess_signature(unit: FactualUnitReference, profile: Profile) -> SignatureAssessment:
    direct_token = unit.complete_tokens.get(profile)
    base_token = _base_token(unit, profile)

    if direct_token is not None:
        required: tuple[str, ...] = ()
    elif profile is Profile.P1 and base_token is not None:
        required = ()
    elif profile is Profile.P2 and base_token is not None:
        required = ("final_admission_jurisdiction",)
    elif profile is Profile.P3 and base_token is not None:
        required = ("identity_discriminator",)
    else:
        required = {
            Profile.P1: P1_DIMENSIONS,
            Profile.P2: P2_DIMENSIONS,
            Profile.P3: P3_DIMENSIONS,
        }[profile]

    explicit_extra = tuple(
        name
        for name in sorted(unit.dimensions)
        if name == "route_dependent_hard_decisions" and name not in required
    )
    required = required + explicit_extra

    values: list[object] = []
    evidence_refs: set[str] = set()
    data_blockers: set[DataBlocker] = set()
    model_blockers: set[ModelBlocker] = set()
    complete = profile not in unit.incomplete_reasons

    if base_token is not None:
        values.append(("synthetic_complete_token", base_token))

    for name in required:
        dimension = unit.dimensions.get(name)
        if dimension is None:
            complete = False
            continue
        evidence_refs.update(dimension.evidence_refs)
        if not dimension.complete:
            complete = False
        if dimension.blocker_id:
            blocker = DataBlocker(dimension.blocker_id, dimension.evidence_refs)
            if dimension.state is DimensionState.UNRESOLVED_MODEL_SEMANTICS:
                model_blockers.add(ModelBlocker(dimension.blocker_id))
            else:
                data_blockers.add(blocker)
        if dimension.complete:
            values.append((name, dimension.semantic_value()))

    semantic_value = tuple(values) if complete else None
    return SignatureAssessment(
        complete=complete,
        semantic_value=semantic_value,
        evidence_refs=tuple(sorted(evidence_refs)),
        data_blockers=tuple(sorted(data_blockers)),
        model_blockers=tuple(sorted(model_blockers)),
    )


def signature_complete(unit: FactualUnitReference, profile: Profile) -> bool:
    return assess_signature(unit, profile).complete


def signatures_equal(
    a: FactualUnitReference, b: FactualUnitReference, profile: Profile
) -> SignatureEquality:
    a_signature = assess_signature(a, profile)
    b_signature = assess_signature(b, profile)
    if not a_signature.complete or not b_signature.complete:
        return SignatureEquality.UNKNOWN
    if a_signature.semantic_value == b_signature.semantic_value:
        return SignatureEquality.TRUE
    return SignatureEquality.FALSE
