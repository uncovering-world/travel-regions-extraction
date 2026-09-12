from __future__ import annotations

import json
from dataclasses import replace

import pytest

from ctr_evaluator.evaluator import evaluate, may_merge
from ctr_evaluator.loaders import load_fixture_variants, load_fixtures
from ctr_evaluator.model import (
    DimensionState,
    EvaluatorResult,
    FactualUnitReference,
    HardSignatureDimension,
    Profile,
    SignatureEquality,
)


@pytest.fixture(scope="module")
def fixtures_by_id():
    return {item["id"]: item for item in load_fixtures()}


def _fixture(fixtures_by_id, fixture_id: str):
    return load_fixture_variants(fixtures_by_id[fixture_id])[0]


@pytest.mark.parametrize("profile", list(Profile))
def test_incomplete_signatures_never_merge(fixtures_by_id, profile: Profile) -> None:
    comparison = _fixture(fixtures_by_id, "F003-no-witness-incomplete-signature")
    assert may_merge(comparison.a, comparison.b, profile, comparison=comparison) is False
    assert evaluate(comparison, profile).result is not EvaluatorResult.MAY_MERGE


def test_missing_or_null_is_unknown_not_known_absence(fixtures_by_id) -> None:
    comparison = _fixture(fixtures_by_id, "F009-empty-is-not-known-absence")
    dimension = comparison.a.dimensions["relevant_hard_permits"]
    assert dimension.state is DimensionState.UNKNOWN


def test_known_absence_requires_positive_evidence() -> None:
    with pytest.raises(ValueError, match="positive evidence"):
        HardSignatureDimension("permit", DimensionState.KNOWN_ABSENCE)


def test_not_applicable_requires_rule_rationale() -> None:
    with pytest.raises(ValueError, match="rule rationale"):
        HardSignatureDimension("route", DimensionState.NOT_APPLICABLE)


@pytest.mark.parametrize(
    ("fixture_id", "expected"),
    [
        ("F011-local-overlay-rejected-witness", EvaluatorResult.SEPARATION_NOT_PROVEN),
        ("F012-out-of-scope-traveller-rejected", EvaluatorResult.SEPARATION_NOT_PROVEN),
        ("F013-provisional-witness-not-sufficient", EvaluatorResult.DATA_UNKNOWN),
    ],
)
def test_rejected_witnesses_cannot_split(fixtures_by_id, fixture_id, expected) -> None:
    output = evaluate(_fixture(fixtures_by_id, fixture_id), Profile.P1)
    assert output.result is expected
    assert output.witnesses == ()


def test_verified_jurisdiction_difference_splits_p2(fixtures_by_id) -> None:
    output = evaluate(_fixture(fixtures_by_id, "F001-jurisdiction-only-difference"), Profile.P2)
    assert output.result is EvaluatorResult.MUST_SEPARATE
    assert "R011" in output.applied_rules


def test_unverified_jurisdiction_assertion_cannot_split(fixtures_by_id) -> None:
    comparison = _fixture(fixtures_by_id, "F001-jurisdiction-only-difference")
    comparison = replace(comparison, jurisdiction_evidence_refs=())
    output = evaluate(comparison, Profile.P2)
    assert output.result is EvaluatorResult.DATA_UNKNOWN
    assert output.witnesses == ()


def test_p3_is_model_unresolved_when_identity_matters(fixtures_by_id) -> None:
    output = evaluate(_fixture(fixtures_by_id, "F005-identity-undefined"), Profile.P3)
    assert output.result is EvaluatorResult.MODEL_UNRESOLVED
    assert output.blocked_by_model == ("Q001.identity",)


def test_input_order_and_display_names_do_not_change_output(fixtures_by_id) -> None:
    variants = load_fixture_variants(fixtures_by_id["F014-order-and-name-invariance"])
    outputs = [evaluate(item, Profile.P2).to_dict() for item in variants]
    assert outputs[0] == outputs[1]


def test_swapping_endpoints_preserves_semantic_output(fixtures_by_id) -> None:
    variants = load_fixture_variants(fixtures_by_id["F015-swap-symmetry"])
    outputs = [evaluate(item, Profile.P1).to_dict() for item in variants]
    assert outputs[0] == outputs[1]


def test_source_conflict_and_rule_conflict_are_distinct(fixtures_by_id) -> None:
    source = evaluate(_fixture(fixtures_by_id, "F006-authoritative-source-conflict"), Profile.P1)
    rules = evaluate(_fixture(fixtures_by_id, "F007-rule-conflict"), Profile.P1)
    assert source.result is EvaluatorResult.DATA_UNKNOWN
    assert rules.result is EvaluatorResult.RULE_CONFLICT


def test_output_arrays_and_explanation_are_deterministic(fixtures_by_id) -> None:
    comparison = _fixture(fixtures_by_id, "F001-jurisdiction-only-difference")
    first = evaluate(comparison, Profile.P2).to_dict()
    reversed_comparison = replace(
        comparison,
        evidence=dict(reversed(list(comparison.evidence.items()))),
        jurisdiction_evidence_refs=tuple(reversed(comparison.jurisdiction_evidence_refs)),
    )
    second = evaluate(reversed_comparison, Profile.P2).to_dict()
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)
    for key in ("applied_rules", "witnesses", "blocked_by_data", "blocked_by_model", "evidence_refs"):
        assert first[key] == sorted(set(first[key]))


def test_signature_true_is_impossible_when_either_side_is_incomplete(fixtures_by_id) -> None:
    output = evaluate(_fixture(fixtures_by_id, "F003-no-witness-incomplete-signature"), Profile.P1)
    assert output.signature_equal is SignatureEquality.UNKNOWN
