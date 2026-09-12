"""S1-core-v1: evaluate explicit CR-W proofs, never historical Q001 assertions.

Evidence-backed gates are normalized proof attestations, not inferred legal facts.
The producer must justify every conjunct of each gate in R044. This module checks
the proof envelope; it does not research law, extract geometry or build a partition.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
import json
from typing import Any, Mapping

from .loaders import InputError


PROFILE = "S1-core-v1"
SCHEMA_VERSION = "s1-core-input-v1"
SPEC_VERSION = "0.3.0-draft"
EVALUATOR_VERSION = "s1-core-1.0.0"
TRAVELLER_SCOPE = "civilian-short-stay-v1"
GATES = ("G-SCOPE", "G-CONTEXT", "G-HARD", "G-TIME", "G-EVIDENCE")
HARD_DIMENSIONS = (
    "accepted_travel_document",
    "visa_eta_admission_authorisation_requirement",
    "territorial_authorisation_validity",
    "entry_eligibility_or_prohibition",
    "civilian_stay_conditions_duration_or_termination",
    "permission_to_enter_or_be_present_in_territorial_scope",
    "independently_applicable_legal_entry_or_exit_route_obligation",
)


def _object(value: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise InputError(f"{path}: expected object")
    return value


def _text(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{path}: expected nonempty string")
    return value


def _date(value: Any, path: str) -> date:
    try:
        return date.fromisoformat(_text(value, path))
    except ValueError as exc:
        raise InputError(f"{path}: expected ISO date") from exc


def _array(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        raise InputError(f"{path}: expected array")
    return value


def _known(value: Any) -> bool:
    if value is None or value == "unknown" or value == "" or value == [] or value == {}:
        return False
    if isinstance(value, dict):
        return all(_known(v) for v in value.values())
    if isinstance(value, list):
        return all(_known(v) for v in value)
    return True


@dataclass
class _Assessment:
    data: set[str] = field(default_factory=set)
    model: set[str] = field(default_factory=set)
    refs: set[str] = field(default_factory=set)

    def include(self, other: _Assessment) -> None:
        self.data.update(other.data)
        self.model.update(other.model)
        self.refs.update(other.refs)


class _Proofs:
    def __init__(self, raw: Mapping[str, Any], as_of: date):
        self.records = _object(raw.get("evidence", {}), "evidence")
        self.as_of = as_of

    def evidence(
        self, refs: Any, scopes: tuple[str, ...], context: str, path: str,
        assessment: _Assessment,
    ) -> bool:
        refs = _array(refs, f"{path}.evidence_refs")
        if not refs:
            assessment.data.add(f"{path}.evidence_missing")
            return False
        valid = True
        covered_scopes: set[str] = set()
        for ref in sorted({_text(ref, path) for ref in refs}):
            assessment.refs.add(ref)
            record = self.records.get(ref)
            if record is None:
                assessment.data.add(f"{ref}.missing")
                valid = False
                continue
            record = _object(record, ref)
            if record.get("status") != "verified":
                assessment.data.add(f"{ref}.status")
                valid = False
            provenance = ("source_ref", "locator", "source_competence")
            if any(not isinstance(record.get(key), str) or not record[key].strip() for key in provenance):
                assessment.data.add(f"{ref}.provenance")
                valid = False
            if "valid_from" not in record:
                assessment.data.add(f"{ref}.validity")
                valid = False
            else:
                start = _date(record["valid_from"], f"{ref}.valid_from")
                end = record.get("valid_to")
                end = _date(end, f"{ref}.valid_to") if end is not None else None
                if (end is not None and end <= start) or not (start <= self.as_of and (end is None or self.as_of < end)):
                    assessment.data.add(f"{ref}.validity")
                    valid = False
            source_scopes = _array(record.get("scopes", []), f"{ref}.scopes")
            contexts = _array(record.get("contexts", []), f"{ref}.contexts")
            source_scopes = {_text(item, f"{ref}.scopes") for item in source_scopes}
            if not source_scopes.intersection(scopes) or not (context in contexts or "all" in contexts):
                assessment.data.add(f"{ref}.applicability")
                valid = False
            else:
                covered_scopes.update(source_scopes)
            if record.get("traveller_scope") != TRAVELLER_SCOPE:
                assessment.data.add(f"{ref}.traveller_scope")
                valid = False
        if not set(scopes).issubset(covered_scopes):
            assessment.data.add(f"{path}.scope_coverage")
            valid = False
        return valid

    def gate(
        self, raw: Any, scopes: tuple[str, ...], context: str, path: str,
        assessment: _Assessment,
    ) -> bool:
        proof = _object(raw, path)
        state = proof.get("state", "unknown")
        if state == "model_unresolved":
            assessment.model.add(path)
            return False
        if state == "unknown":
            assessment.data.add(path)
            return False
        if state not in {"proven_true", "proven_false"}:
            raise InputError(f"{path}: invalid gate state")
        verified = self.evidence(proof.get("evidence_refs", []), scopes, context, path, assessment)
        return verified and state == "proven_true"

    def decision(
        self, raw: Any, scope: str, context: str, path: str, assessment: _Assessment,
    ) -> tuple[bool, str | None]:
        decision = _object(raw, path)
        state = decision.get("state", "unknown")
        if state == "unresolved_model_semantics":
            assessment.model.add(path)
            return False, None
        if state == "unknown":
            assessment.data.add(path)
            return False, None
        if state not in {"known_value", "known_absence", "not_applicable"}:
            raise InputError(f"{path}: invalid decision state")
        if state == "known_value" and not _known(decision.get("value")):
            assessment.data.add(f"{path}.value")
            return False, None
        if state == "not_applicable" and not decision.get("rationale"):
            assessment.data.add(f"{path}.rationale")
            return False, None
        valid = self.evidence(decision.get("evidence_refs", []), (scope,), context, path, assessment)
        value = decision.get("value") if state == "known_value" else decision.get("rationale") if state == "not_applicable" else None
        # JSON distinguishes false from 0; provenance and display labels are not values.
        semantic = json.dumps([state, value], sort_keys=True, allow_nan=False)
        return valid, semantic


def evaluate_core(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Evaluate a versioned normalized proof bundle; return no region assignments."""
    raw = _object(raw, "input")
    for key, required in (("schema_version", SCHEMA_VERSION), ("profile", PROFILE), ("traveller_scope", TRAVELLER_SCOPE)):
        if raw.get(key) != required:
            raise InputError(f"{key}: expected {required}; historical P1/P2/P3 inputs require a separate gate audit")
    comparison_id = _text(raw.get("comparison_id"), "comparison_id")
    as_of = _date(raw.get("as_of"), "as_of")
    scopes = _object(raw.get("scopes"), "scopes")
    a, b = (_text(scopes.get(side), f"scopes.{side}") for side in ("a", "b"))
    if a == b:
        raise InputError("G-SCOPE: cannot certify separation/equality of two disjoint scopes using the same scope ID")
    proofs = _Proofs(raw, as_of)
    assessment = _Assessment()
    accepted: list[str] = []
    rejected: list[str] = []
    certificate_ids: set[str] = set()
    for cert in _array(raw.get("certificates", []), "certificates"):
        cert = _object(cert, "certificate")
        cid = _text(cert.get("id"), "certificate.id")
        if cid in certificate_ids:
            raise InputError(f"duplicate certificate id: {cid}")
        certificate_ids.add(cid)
        current = _Assessment()
        if cert.get("dimension") not in HARD_DIMENSIONS:
            rejected.append(f"{cid}: outside accepted hard dimensions")
            continue
        context = _object(cert.get("context", {}), f"{cid}.context")
        if context.get("purpose") in {"work", "settlement", "diplomatic_mission", "military_mission"} or cert.get("rule_kind") in {"incident", "emergency", "event", "named_individual"}:
            rejected.append(f"{cid}: outside class-based standing civilian scope")
            continue
        valid = True
        if cert.get("status") != "verified":
            current.data.add(f"{cid}.status")
            valid = False
        for key, expected in (("traveller_scope", TRAVELLER_SCOPE), ("as_of", raw["as_of"]), ("scope_a", a), ("scope_b", b)):
            if cert.get(key) != expected:
                current.data.add(f"{cid}.{key}")
                valid = False
        if (context.get("purpose") != "civilian_short_stay"
                or not isinstance(context.get("id"), str) or not context["id"]
                or not isinstance(context.get("attributes"), dict) or not context["attributes"]
                or context.get("class_basis") != "class_rule"
                or not isinstance(context.get("trip_class"), str) or not context["trip_class"]):
            current.data.add(f"{cid}.context")
            valid = False
        if cert.get("rule_kind") not in {"standing_class_rule", "constitutive_rule"}:
            current.data.add(f"{cid}.rule_kind")
            valid = False
        context_id = str(context.get("id", "missing"))
        gates = _object(cert.get("gates", {}), f"{cid}.gates")
        for gate in GATES:
            valid = proofs.gate(gates.get(gate, {}), (a, b), context_id, f"{cid}.{gate}", current) and valid
        left_ok, left = proofs.decision(cert.get("decision_a", {}), a, context_id, f"{cid}.decision_a", current)
        right_ok, right = proofs.decision(cert.get("decision_b", {}), b, context_id, f"{cid}.decision_b", current)
        if valid and left_ok and right_ok and left != right:
            accepted.append(cid)
        else:
            rejected.append(f"{cid}: no proved CR-W discontinuity through all gates")
        assessment.include(current)

    signatures = _object(raw.get("signatures", {}), "signatures")
    signature_values: list[dict[str, str | None]] = []
    signature_complete: list[bool] = []
    for side, scope in (("a", a), ("b", b)):
        sig = signatures.get(side)
        values: dict[str, str | None] = {}
        complete = False
        if sig is not None:
            sig = _object(sig, f"signatures.{side}")
            coverage = sig.get("coverage", {})
            complete = proofs.gate(coverage, (scope,), "all", f"signatures.{side}.coverage", assessment)
            dimensions = _object(sig.get("dimensions", {}), f"signatures.{side}.dimensions")
            for dimension in HARD_DIMENSIONS:
                ok, value = proofs.decision(dimensions.get(dimension, {}), scope, "all", f"signatures.{side}.{dimension}", assessment)
                values[dimension] = value
                complete = complete and ok
        signature_values.append(values)
        signature_complete.append(complete)
    equal: bool | str = "unknown"
    if all(signature_complete):
        equal = signature_values[0] == signature_values[1]
    if accepted and equal is True:
        assessment.data.add("certificate_signature.source_conflict")
        result = "data_unknown"
    elif accepted:
        result = "must_separate"
    elif assessment.model:
        result = "model_unresolved"
    elif assessment.data:
        result = "data_unknown"
    elif equal is True:
        result = "hard_compatible"
    else:
        result = "separation_not_proven"
    return {
        "comparison_id": comparison_id,
        "profile": PROFILE,
        "profile_version": "1",
        "spec_version": SPEC_VERSION,
        "evaluator_version": EVALUATOR_VERSION,
        "traveller_scope": TRAVELLER_SCOPE,
        "as_of": raw["as_of"],
        "result": result,
        "applied_rules": ["CR-W", "R044"] if result == "must_separate" else [],
        "witnesses": sorted(accepted) if result == "must_separate" else [],
        "signature": {"a_complete": signature_complete[0], "b_complete": signature_complete[1], "equal": equal},
        "blocked_by_data": sorted(assessment.data) if result in {"data_unknown", "model_unresolved"} else [],
        "blocked_by_model": sorted(assessment.model) if result == "model_unresolved" else [],
        "evidence_refs": sorted(assessment.refs),
        "rejected_certificates": sorted(rejected),
    }
