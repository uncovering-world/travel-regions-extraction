from copy import deepcopy
import json
from pathlib import Path

import pytest

from ctr_evaluator.cli import main
from ctr_evaluator.core import GATES, HARD_DIMENSIONS, evaluate_core
from ctr_evaluator.loaders import InputError, load_q001
from ctr_evaluator.model import Profile
from ctr_evaluator.reporting import build_artifact


@pytest.fixture
def bundle():
    return json.loads(Path("experiments/q001/stage1-core-example.json").read_text())


def equal_signatures(bundle):
    """Stipulate a full symbolic policy coverage proof, not sampled travellers."""
    bundle["certificates"] = []
    bundle["evidence"]["SYNTH-PROOF"]["contexts"] = ["all"]
    signature = {
        "coverage": {"state": "proven_true", "evidence_refs": ["SYNTH-PROOF"]},
        "dimensions": {
            dimension: {"state": "known_value", "value": {"policy_function": "identical-for-all-S"}, "evidence_refs": ["SYNTH-PROOF"]}
            for dimension in HARD_DIMENSIONS
        },
    }
    bundle["signatures"] = {"a": deepcopy(signature), "b": deepcopy(signature)}
    return bundle


def test_verified_cr_w_certificate_is_sufficient(bundle):
    result = evaluate_core(bundle)
    assert result["result"] == "must_separate"
    assert result["applied_rules"] == ["CR-W", "R044"]
    assert result["signature"]["equal"] == "unknown"
    assert result["profile"] == "S1-core-v1"
    assert result["spec_version"] == "0.3.0-draft"


@pytest.mark.parametrize("frequency", [0, 1, 1000000])
def test_class_frequency_never_filters_valid_witness(bundle, frequency):
    bundle["metadata"]["observed_class_frequency"] = frequency
    assert evaluate_core(bundle)["result"] == "must_separate"


@pytest.mark.parametrize("status", ["provisional", "conflicted", "unknown", "supported"])
def test_nonverified_evidence_is_insufficient(bundle, status):
    bundle["evidence"]["SYNTH-PROOF"]["status"] = status
    result = evaluate_core(bundle)
    assert result["result"] == "data_unknown"
    assert result["witnesses"] == []
    assert "SYNTH-PROOF.status" in result["blocked_by_data"]


def test_provisional_certificate_is_insufficient_even_with_verified_sources(bundle):
    bundle["certificates"][0]["status"] = "provisional"
    assert evaluate_core(bundle)["result"] == "data_unknown"


@pytest.mark.parametrize("dimension", ["site_access", "trekking_activity", "airport_queue", "final_admission_jurisdiction", "identity_discriminator"])
def test_noncore_dimensions_cannot_split(bundle, dimension):
    bundle["certificates"][0]["dimension"] = dimension
    assert evaluate_core(bundle)["result"] == "separation_not_proven"


def test_local_overlay_rejected_even_if_dimension_label_looks_hard(bundle):
    bundle["certificates"][0]["gates"]["G-HARD"]["state"] = "proven_false"
    bundle["metadata"]["overlay_geometry"] = "whole_province"
    assert evaluate_core(bundle)["result"] == "separation_not_proven"


@pytest.mark.parametrize("label", ["disputed", "claim_exists", "recognition_differs", "controller_differs", "military_control_differs", "dependency", "autonomous", "overseas", "island", "different_admission_jurisdiction"])
def test_labels_and_jurisdiction_neither_split_nor_block_complete_core_equality(bundle, label):
    equal_signatures(bundle)
    bundle["metadata"][label] = True
    result = evaluate_core(bundle)
    assert result["result"] == "hard_compatible"
    assert result["blocked_by_model"] == result["blocked_by_data"] == []
    assert "final_admission_jurisdiction" not in HARD_DIMENSIONS


@pytest.mark.parametrize("gate", GATES)
def test_each_missing_gate_prevents_certification(bundle, gate):
    del bundle["certificates"][0]["gates"][gate]
    result = evaluate_core(bundle)
    assert result["result"] == "data_unknown"
    assert f"W1.{gate}" in result["blocked_by_data"]


def test_undefined_permit_classification_is_model_unknown(bundle):
    bundle["certificates"][0]["gates"]["G-HARD"]["state"] = "model_unresolved"
    assert evaluate_core(bundle)["result"] == "model_unresolved"


def test_missing_source_never_counts_as_verified(bundle):
    bundle["evidence"] = {}
    assert evaluate_core(bundle)["result"] == "data_unknown"


def test_different_sources_can_collectively_prove_both_sides(bundle):
    source = bundle["evidence"].pop("SYNTH-PROOF")
    bundle["evidence"] = {
        "PROOF-A": {**source, "scopes": ["scope-a"]},
        "PROOF-B": {**source, "scopes": ["scope-b"]},
    }
    cert = bundle["certificates"][0]
    for gate in cert["gates"].values():
        gate["evidence_refs"] = ["PROOF-A", "PROOF-B"]
    cert["decision_a"]["evidence_refs"] = ["PROOF-A"]
    cert["decision_b"]["evidence_refs"] = ["PROOF-B"]
    assert evaluate_core(bundle)["result"] == "must_separate"


@pytest.mark.parametrize("side", ["decision_a", "decision_b"])
def test_both_decisions_must_be_proved(bundle, side):
    del bundle["certificates"][0][side]
    assert evaluate_core(bundle)["result"] == "data_unknown"


def test_unknown_literal_cannot_be_compared_as_decision_value(bundle):
    bundle["certificates"][0]["decision_a"]["value"] = "unknown"
    assert evaluate_core(bundle)["result"] == "data_unknown"


@pytest.mark.parametrize("kind", ["incident", "emergency", "event", "named_individual"])
def test_event_and_named_individual_rule_is_not_standing_core(bundle, kind):
    bundle["certificates"][0]["rule_kind"] = kind
    assert evaluate_core(bundle)["result"] == "separation_not_proven"


@pytest.mark.parametrize("purpose", ["work", "settlement", "military_mission", "diplomatic_mission"])
def test_out_of_scope_purposes(bundle, purpose):
    bundle["certificates"][0]["context"]["purpose"] = purpose
    assert evaluate_core(bundle)["result"] == "separation_not_proven"


@pytest.mark.parametrize("field,value", [("as_of", "2026-09-13"), ("traveller_scope", "another-scope"), ("scope_b", "other-scope")])
def test_certificate_must_match_bundle_scope_and_time(bundle, field, value):
    bundle["certificates"][0][field] = value
    assert evaluate_core(bundle)["result"] == "data_unknown"


@pytest.mark.parametrize("field,value", [("valid_to", "2026-09-12"), ("valid_from", "2026-09-13"), ("scopes", ["scope-a"]), ("contexts", ["other-class"]), ("source_competence", "")])
def test_evidence_must_apply_to_both_scopes_context_and_time(bundle, field, value):
    bundle["evidence"]["SYNTH-PROOF"][field] = value
    assert evaluate_core(bundle)["result"] == "data_unknown"


def test_no_certificate_is_not_compatibility(bundle):
    bundle["certificates"] = []
    assert evaluate_core(bundle)["result"] == "separation_not_proven"


def test_full_equality_needs_coverage_proof_not_matching_values(bundle):
    equal_signatures(bundle)
    del bundle["signatures"]["a"]["coverage"]
    assert evaluate_core(bundle)["result"] == "data_unknown"


def test_incomplete_accepted_dimension_blocks_compatibility(bundle):
    equal_signatures(bundle)
    del bundle["signatures"]["a"]["dimensions"][HARD_DIMENSIONS[-1]]
    assert evaluate_core(bundle)["result"] == "data_unknown"


def test_missing_jurisdiction_and_identity_are_not_core_blockers(bundle):
    equal_signatures(bundle)
    bundle["signatures"]["a"]["dimensions"]["identity_discriminator"] = {"state": "unresolved_model_semantics"}
    bundle["signatures"]["a"]["dimensions"]["final_admission_jurisdiction"] = {"state": "unknown"}
    assert evaluate_core(bundle)["result"] == "hard_compatible"


def test_positive_certificate_survives_unrelated_unknown(bundle):
    bundle["signatures"] = {"a": {"dimensions": {}}}
    assert evaluate_core(bundle)["result"] == "must_separate"


def test_equal_signature_and_positive_witness_requires_conflict_resolution(bundle):
    certificate = deepcopy(bundle["certificates"])
    equal_signatures(bundle)
    bundle["certificates"] = certificate
    result = evaluate_core(bundle)
    assert result["result"] == "data_unknown"
    assert "certificate_signature.source_conflict" in result["blocked_by_data"]


def test_consistent_relabeling_order_and_swap_are_invariant(bundle):
    before = evaluate_core(bundle)
    renamed = json.loads(json.dumps(bundle).replace("scope-a", "opaque-x").replace("scope-b", "opaque-y"))
    renamed["metadata"].update({"display_names": ["Germany", "France"], "stage2_destination_identity": ["island", "mainland"]})
    cert = renamed["certificates"][0]
    cert["decision_a"], cert["decision_b"] = cert["decision_b"], cert["decision_a"]
    renamed["scopes"]["a"], renamed["scopes"]["b"] = renamed["scopes"]["b"], renamed["scopes"]["a"]
    cert["scope_a"], cert["scope_b"] = cert["scope_b"], cert["scope_a"]
    cert["gates"] = dict(reversed(list(cert["gates"].items())))
    assert evaluate_core(renamed) == before


def test_stage2_metadata_has_no_effect_on_compatibility(bundle):
    equal_signatures(bundle)
    before = evaluate_core(bundle)
    bundle["metadata"]["stage2"] = {"must_split_destination": True, "regions": ["X", "Y"]}
    assert evaluate_core(bundle) == before


def test_core_output_deterministic_and_does_not_touch_historical_results(bundle):
    path = Path("experiments/q001/results/evaluator-results.json")
    before = path.read_bytes()
    assert json.dumps(evaluate_core(bundle), sort_keys=True) == json.dumps(evaluate_core(deepcopy(bundle)), sort_keys=True)
    artifact, _ = build_artifact(load_q001(), tuple(Profile))
    assert artifact == json.loads(before)
    assert path.read_bytes() == before


def test_historical_input_cannot_be_relabelled_as_core(bundle):
    bundle["profile"] = "P1"
    with pytest.raises(InputError, match="separate gate audit"):
        evaluate_core(bundle)


def test_cli_core_and_historical_fixture_paths_are_separate(capsys):
    assert main(["evaluate-core", "--input", "experiments/q001/stage1-core-example.json"]) == 0
    assert json.loads(capsys.readouterr().out)["profile"] == "S1-core-v1"
    assert main(["validate-fixtures"]) == 0
    assert json.loads(capsys.readouterr().out)["fixture_count"] == 15
