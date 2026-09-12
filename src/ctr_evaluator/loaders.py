"""Load synthetic fixtures and the current Q001 factual snapshot."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable, Mapping

from .model import (
    ComparisonInput,
    DataBlocker,
    DataBlockerKind,
    DatasetBundle,
    DimensionState,
    EvidenceRecord,
    EvaluatorResult,
    FactualUnitReference,
    HardSignatureDimension,
    ModelBlocker,
    Profile,
    RuleDerivation,
    TravellerWitness,
)


class InputError(ValueError):
    """Raised when evaluator input violates the executable contract."""


def _evaluator_result(value: object) -> EvaluatorResult:
    """Parse a terminal outcome, accepting the pre-0.2 input spelling only."""
    normalized = "hard_compatible" if value == "may_merge" else str(value)
    return EvaluatorResult(normalized)


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InputError(f"cannot load {path}: {exc}") from exc


def _unique_by_id(records: Iterable[Mapping[str, Any]], label: str) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    for record in records:
        identifier = record.get("id")
        if not isinstance(identifier, str) or not identifier:
            raise InputError(f"{label} record has no stable id")
        if identifier in result:
            raise InputError(f"duplicate {label} id: {identifier}")
        result[identifier] = record
    return result


def _evidence_records(raw: Iterable[Mapping[str, Any]]) -> dict[str, EvidenceRecord]:
    records = _unique_by_id(raw, "evidence")
    return {
        identifier: EvidenceRecord(
            id=identifier,
            status=str(record.get("evidence_status", record.get("status", "unknown"))),
            source_refs=tuple(sorted(set(record.get("source_refs", [])))),
            observed_as_of=record.get("observed_as_of"),
        )
        for identifier, record in records.items()
    }


def _fact_dimension(
    name: str,
    raw: Mapping[str, Any] | None,
    evidence: Mapping[str, EvidenceRecord],
) -> HardSignatureDimension:
    if not raw or raw.get("value") is None or raw.get("value") == "unknown":
        return HardSignatureDimension(name, DimensionState.UNKNOWN)
    refs = tuple(sorted(set(raw.get("evidence_refs", []))))
    status = raw.get("status")
    refs_verified = bool(refs) and all(
        ref in evidence and evidence[ref].status == "verified" for ref in refs
    )
    if status == "supported" and refs_verified:
        return HardSignatureDimension(
            name=name,
            state=DimensionState.KNOWN_VALUE,
            value=raw["value"],
            evidence_refs=refs,
        )
    return HardSignatureDimension(name, DimensionState.UNKNOWN, evidence_refs=refs)


def _load_q001_unit(
    raw: Mapping[str, Any], evidence: Mapping[str, EvidenceRecord]
) -> FactualUnitReference:
    admission = raw.get("admission", {})
    visa = raw.get("visa_and_documents", {})
    permits = raw.get("permits", {})
    dimensions = {
        "admission_decision_scope": _fact_dimension(
            "admission_decision_scope", admission.get("territorial_scope"), evidence
        ),
        "visa_scope": _fact_dimension("visa_scope", visa.get("visa_scope"), evidence),
        "document_scope": _fact_dimension("document_scope", visa.get("document_scope"), evidence),
        "relevant_hard_permits": _fact_dimension(
            "relevant_hard_permits", permits.get("territorial_permits"), evidence
        ),
        "final_admission_jurisdiction": _fact_dimension(
            "final_admission_jurisdiction", admission.get("final_admission_authority"), evidence
        ),
        "identity_discriminator": HardSignatureDimension(
            "identity_discriminator",
            DimensionState.UNRESOLVED_MODEL_SEMANTICS,
            blocker_id="Q001.identity",
        ),
    }
    return FactualUnitReference(id=str(raw["id"]), dimensions=dimensions)


def _jurisdiction_refs(
    a_raw: Mapping[str, Any],
    b_raw: Mapping[str, Any],
    evidence: Mapping[str, EvidenceRecord],
) -> tuple[str, ...]:
    refs: set[str] = set()
    for raw in (a_raw, b_raw):
        admission = raw.get("admission", {})
        for field_name in ("final_admission_authority", "independent_final_decision"):
            field = admission.get(field_name, {})
            for ref in field.get("evidence_refs", []):
                if ref in evidence and evidence[ref].status == "verified":
                    refs.add(ref)
    return tuple(sorted(refs))


def load_q001(q001_dir: str | Path = "experiments/q001") -> DatasetBundle:
    root = Path(q001_dir)
    evidence_doc = _read_json(root / "evidence.json")
    evidence = _evidence_records(evidence_doc.get("evidence", []))

    raw_units: dict[str, Mapping[str, Any]] = {}
    for path in sorted((root / "facts").glob("*.json")):
        raw = _read_json(path)
        identifier = raw.get("id")
        if not isinstance(identifier, str) or not identifier:
            raise InputError(f"fact file has no id: {path}")
        if identifier in raw_units:
            raise InputError(f"duplicate factual unit id: {identifier}")
        raw_units[identifier] = raw
    units = {
        identifier: _load_q001_unit(raw, evidence)
        for identifier, raw in raw_units.items()
    }

    comparisons_doc = _read_json(root / "comparisons.yaml")
    raw_comparisons = _unique_by_id(comparisons_doc.get("comparisons", []), "comparison")
    comparisons: list[ComparisonInput] = []
    for comparison_id in sorted(raw_comparisons):
        raw = raw_comparisons[comparison_id]
        if not re.fullmatch(r"C\d{3}", comparison_id):
            raise InputError(f"malformed comparison id: {comparison_id}")
        a_id, b_id = raw.get("a"), raw.get("b")
        if a_id not in units or b_id not in units:
            raise InputError(f"{comparison_id}: unknown endpoint")
        witnesses = tuple(
            TravellerWitness(
                id=f"{comparison_id}.W{index:03d}",
                scope="R007",
                dimension=str(item.get("decision_dimension", "")),
                decision_a=item.get("decision_a"),
                decision_b=item.get("decision_b"),
                status=str(item.get("status", "unknown")),
                evidence_refs=tuple(item.get("evidence_refs", [])),
                traveller_scope="civilian_short_stay",
            )
            for index, item in enumerate(raw.get("witnesses", []), 1)
        )
        jurisdiction_raw = raw.get("questions", {}).get("independent_admission_jurisdiction")
        jurisdiction_difference = jurisdiction_raw if isinstance(jurisdiction_raw, bool) else None
        model_questions = set(raw.get("model_questions", []))
        model_blockers: list[ModelBlocker] = []
        if "Q004" in model_questions:
            model_blockers.append(ModelBlocker("Q004"))
        model_blockers.append(ModelBlocker("Q001.identity", frozenset({Profile.P3})))
        if "Q006" in model_questions:
            model_blockers.append(ModelBlocker("Q006", frozenset({Profile.P3})))
        data_blockers: list[DataBlocker] = []
        for item in raw.get("evaluator_data_blockers", []):
            try:
                blocker_profiles = frozenset(Profile(value) for value in item["profiles"])
                blocker_kind = DataBlockerKind(item["kind"])
                blocker_id = str(item["id"])
            except (KeyError, TypeError, ValueError) as exc:
                raise InputError(
                    f"{comparison_id}: malformed evaluator_data_blockers entry"
                ) from exc
            if not blocker_profiles or not blocker_id:
                raise InputError(
                    f"{comparison_id}: evaluator data blocker requires id and profiles"
                )
            refs = tuple(sorted(set(item.get("evidence_refs", []))))
            if any(ref not in evidence for ref in refs):
                raise InputError(
                    f"{comparison_id}: evaluator data blocker references unknown evidence"
                )
            data_blockers.append(
                DataBlocker(
                    blocker_id,
                    refs,
                    blocker_profiles,
                    blocker_kind,
                )
            )
        if jurisdiction_difference is None:
            for jurisdiction_profile in (Profile.P2, Profile.P3):
                if not any(
                    jurisdiction_profile in blocker.profiles for blocker in data_blockers
                ):
                    data_blockers.append(
                        DataBlocker(
                            "final_admission_jurisdiction",
                            profiles=frozenset({jurisdiction_profile}),
                        )
                    )
        comparisons.append(
            ComparisonInput(
                id=comparison_id,
                a=units[str(a_id)],
                b=units[str(b_id)],
                witnesses=witnesses,
                evidence=evidence,
                data_blockers=tuple(data_blockers),
                model_blockers=tuple(model_blockers),
                jurisdiction_difference=jurisdiction_difference,
                jurisdiction_evidence_refs=_jurisdiction_refs(
                    raw_units[str(a_id)], raw_units[str(b_id)], evidence
                ),
                disputed_identity_relevant="Q006" in model_questions,
            )
        )

    fixture_doc = _read_json(root / "evaluator-fixtures.yaml")
    return DatasetBundle(
        spec_version=str(fixture_doc["spec_version"]),
        dataset_snapshot=str(comparisons_doc.get("snapshot", "unknown")),
        q001_dir=str(root),
        comparisons=tuple(comparisons),
    )


_DIMENSION_ALIASES = {
    "hard_permits": "relevant_hard_permits",
}


def _dsl_dimension(name: str, raw: Any, path: str) -> HardSignatureDimension:
    canonical_name = _DIMENSION_ALIASES.get(name, name)
    if raw is None or raw == "unknown" or raw == "incomplete":
        return HardSignatureDimension(
            canonical_name,
            DimensionState.UNKNOWN,
            blocker_id=path if raw is None else None,
        )
    if raw == "unresolved_model_semantics":
        return HardSignatureDimension(
            canonical_name,
            DimensionState.UNRESOLVED_MODEL_SEMANTICS,
            blocker_id="Q001.identity" if canonical_name == "identity_discriminator" else path,
        )
    if not isinstance(raw, str) or ":" not in raw:
        return HardSignatureDimension(
            canonical_name,
            DimensionState.KNOWN_VALUE,
            value=raw,
            evidence_refs=(f"SYNTH:{path}",),
        )
    kind, payload = raw.split(":", 1)
    if kind == "known_value":
        return HardSignatureDimension(
            canonical_name,
            DimensionState.KNOWN_VALUE,
            value=payload,
            evidence_refs=(f"SYNTH:{path}",),
        )
    if kind == "known_absence":
        if not payload:
            raise InputError(f"{path}: known_absence requires evidence")
        return HardSignatureDimension(
            canonical_name,
            DimensionState.KNOWN_ABSENCE,
            evidence_refs=tuple(filter(None, payload.split("/"))),
            rationale="positive synthetic evidence",
        )
    if kind == "not_applicable":
        if not payload:
            raise InputError(f"{path}: not_applicable requires rationale")
        return HardSignatureDimension(
            canonical_name,
            DimensionState.NOT_APPLICABLE,
            rationale=payload,
        )
    if kind == "source_conflict":
        refs = tuple(filter(None, payload.split("/")))
        return HardSignatureDimension(
            canonical_name,
            DimensionState.UNKNOWN,
            evidence_refs=refs,
            blocker_id=f"{path}.source_conflict",
            source_conflict=True,
        )
    raise InputError(f"{path}: unsupported fixture DSL value {raw!r}")


def _fixture_unit(label: str, raw: Mapping[str, Any]) -> FactualUnitReference:
    dimensions: dict[str, HardSignatureDimension] = {}
    tokens: dict[Profile, str] = {}
    incomplete: dict[Profile, str] = {}

    for key, profile in (("p1_signature", Profile.P1), ("p2_signature", Profile.P2)):
        value = raw.get(key)
        if isinstance(value, str) and value.startswith("complete:"):
            tokens[profile] = value.split(":", 1)[1]
        elif isinstance(value, str) and value.startswith("incomplete"):
            incomplete[profile] = value.partition(":")[2] or "unspecified"

    other = raw.get("other_p1_dimensions")
    if isinstance(other, str) and other.startswith("complete:"):
        tokens[Profile.P1] = other.split(":", 1)[1]

    nested = raw.get("p1_dimensions", {})
    if not isinstance(nested, Mapping):
        raise InputError(f"{label}.p1_dimensions must be an object")
    for name, value in nested.items():
        canonical = _DIMENSION_ALIASES.get(name, name)
        dimensions[canonical] = _dsl_dimension(canonical, value, f"{label}.{name}")

    reserved = {"p1_signature", "p2_signature", "p1_dimensions", "other_p1_dimensions"}
    for name, value in raw.items():
        if name in reserved:
            continue
        canonical = _DIMENSION_ALIASES.get(name, name)
        dimensions[canonical] = _dsl_dimension(canonical, value, f"{label}.{name}")

    return FactualUnitReference(
        id=label,
        dimensions=dimensions,
        complete_tokens=tokens,
        incomplete_reasons=incomplete,
    )


def _fixture_comparison(
    fixture_id: str,
    raw: Mapping[str, Any],
    *,
    units_raw: Mapping[str, Any] | None = None,
) -> ComparisonInput:
    units_doc = units_raw if units_raw is not None else raw.get("units", {})
    a = _fixture_unit("A", units_doc.get("A", {}))
    b = _fixture_unit("B", units_doc.get("B", {}))
    evidence_ids = tuple(raw.get("evidence", []))
    evidence = {
        identifier: EvidenceRecord(identifier, "verified") for identifier in evidence_ids
    }
    witness_items = list(raw.get("witnesses", []))
    if "witness" in raw:
        witness_items.append(raw["witness"])
    witnesses = tuple(
        TravellerWitness(
            id=str(item.get("id", f"W{index}")),
            scope=str(item.get("scope", "R007")),
            dimension=str(item.get("dimension", "visa_scope")),
            decision_a=item.get("a"),
            decision_b=item.get("b"),
            status=str(item.get("status", "verified")),
            evidence_refs=tuple(item.get("evidence_refs", [])),
            traveller_scope=str(item.get("traveller_scope", "civilian_short_stay")),
        )
        for index, item in enumerate(witness_items, 1)
    )
    derivations = tuple(
        RuleDerivation(
            rule=str(item["rule"]),
            requires=_evaluator_result(item["requires"]),
        )
        for item in raw.get("derivations", [])
    )
    a_jur = a.dimensions.get("final_admission_jurisdiction")
    b_jur = b.dimensions.get("final_admission_jurisdiction")
    jurisdiction_difference: bool | None = None
    if a_jur and b_jur and a_jur.complete and b_jur.complete:
        jurisdiction_difference = a_jur.semantic_value() != b_jur.semantic_value()

    data_blockers: list[DataBlocker] = []
    for unit in (a, b):
        for dimension in unit.dimensions.values():
            if dimension.blocker_id and dimension.state is not DimensionState.UNRESOLVED_MODEL_SEMANTICS:
                data_blockers.append(DataBlocker(dimension.blocker_id, dimension.evidence_refs))
    model_blockers: list[ModelBlocker] = []
    for unit in (a, b):
        for dimension in unit.dimensions.values():
            if dimension.state is DimensionState.UNRESOLVED_MODEL_SEMANTICS and dimension.blocker_id:
                model_blockers.append(
                    ModelBlocker(dimension.blocker_id, frozenset({Profile.P3}))
                )
    return ComparisonInput(
        id=fixture_id,
        a=a,
        b=b,
        witnesses=witnesses,
        evidence=evidence,
        derivations=derivations,
        data_blockers=tuple(data_blockers),
        model_blockers=tuple(model_blockers),
        jurisdiction_difference=jurisdiction_difference,
        jurisdiction_evidence_refs=evidence_ids,
    )


def load_fixture_variants(fixture: Mapping[str, Any]) -> tuple[ComparisonInput, ...]:
    fixture_id = str(fixture["id"])
    if "input" in fixture:
        return (_fixture_comparison(fixture_id, fixture["input"]),)
    shared = fixture.get("shared_facts", {"A": {}, "B": {}})
    variants: list[ComparisonInput] = []
    for variant in fixture.get("input_variants", []):
        raw = dict(variant)
        if "record_order" in raw:
            raw["evidence"] = raw["record_order"]
        variants.append(_fixture_comparison(fixture_id, raw, units_raw=shared))
    if not variants:
        raise InputError(f"{fixture_id}: fixture has no input")
    return tuple(variants)


def load_fixtures(q001_dir: str | Path = "experiments/q001") -> tuple[Mapping[str, Any], ...]:
    document = _read_json(Path(q001_dir) / "evaluator-fixtures.yaml")
    fixtures = document.get("fixtures")
    if not isinstance(fixtures, list):
        raise InputError("evaluator-fixtures.yaml has no fixtures array")
    return tuple(fixtures)
