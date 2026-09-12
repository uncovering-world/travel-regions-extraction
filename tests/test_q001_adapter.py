from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from ctr_evaluator.evaluator import evaluate
from ctr_evaluator.loaders import load_q001
from ctr_evaluator.model import DataBlockerKind, EvaluatorResult, Profile
from ctr_evaluator.reporting import (
    build_artifact,
    evaluate_profiles,
    representative_mismatches,
)


def test_q001_adapter_loads_expected_snapshot() -> None:
    bundle = load_q001()
    assert bundle.spec_version == "0.2.0-draft"
    assert bundle.dataset_snapshot == "2026-09-11"
    assert len(bundle.comparisons) == 49
    assert len(evaluate_profiles(bundle, Profile)) == 147


def test_q001_verified_witnesses_are_the_only_p1_splits() -> None:
    bundle = load_q001()
    split_ids = {
        comparison.id
        for comparison in bundle.comparisons
        if evaluate(comparison, Profile.P1).result is EvaluatorResult.MUST_SEPARATE
    }
    assert split_ids == {"C007", "C029", "C030", "C042"}


def test_q001_incomplete_schema_produces_no_hard_compatible() -> None:
    bundle = load_q001()
    assert all(
        evaluate(comparison, profile).result is not EvaluatorResult.HARD_COMPATIBLE
        for comparison in bundle.comparisons
        for profile in Profile
    )


def test_generated_artifact_uses_canonical_outcome_terminology() -> None:
    artifact, _ = build_artifact(load_q001(), Profile)
    serialized = json.dumps(artifact)
    assert '"hard_compatible"' in serialized
    assert '"may_merge"' not in serialized


def test_q001_preserves_provisional_evidence() -> None:
    bundle = load_q001()
    comparison = next(item for item in bundle.comparisons if item.id == "C001")
    assert comparison.evidence["E01"].status == "provisional"
    output = evaluate(comparison, Profile.P1)
    assert output.result is EvaluatorResult.DATA_UNKNOWN
    assert "E01.status" in output.blocked_by_data


def test_typed_comparison_blockers_drive_data_unknown() -> None:
    bundle = load_q001()
    expected = {
        "C032": ("east_admission_rules", "east_civilian_access"),
        "C040": ("admission_rules", "civilian_access", "current_control_geometry"),
    }
    for comparison_id, blocker_ids in expected.items():
        comparison = next(item for item in bundle.comparisons if item.id == comparison_id)
        output = evaluate(comparison, Profile.P1)
        assert output.result is EvaluatorResult.DATA_UNKNOWN
        assert output.blocked_by_data == blocker_ids
        applicable = {
            blocker.id: blocker.kind
            for blocker in comparison.data_blockers
            if Profile.P1 in blocker.profiles
        }
        assert applicable == {
            blocker_id: DataBlockerKind.MISSING_FACT for blocker_id in blocker_ids
        }


def test_prose_only_blocker_does_not_change_terminal_semantics() -> None:
    bundle = load_q001()
    comparison = next(item for item in bundle.comparisons if item.id == "C031")
    assert comparison.data_blockers
    assert all(Profile.P1 not in blocker.profiles for blocker in comparison.data_blockers)
    assert evaluate(comparison, Profile.P1).result is EvaluatorResult.SEPARATION_NOT_PROVEN


def test_representative_contract_and_evaluator_agree() -> None:
    bundle = load_q001()
    outputs = evaluate_profiles(bundle, Profile)
    assert representative_mismatches(bundle, outputs) == ()


def test_q001_validator_checks_typed_representative_blockers() -> None:
    completed = subprocess.run(
        [sys.executable, "experiments/q001/validate.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr


def test_replacing_all_display_names_does_not_change_semantics(tmp_path: Path) -> None:
    source = Path("experiments/q001")
    copied = tmp_path / "q001"
    shutil.copytree(source, copied)
    for index, path in enumerate(sorted((copied / "facts").glob("*.json")), 1):
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["name"] = f"Display label {index}"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    before = [item.to_dict() for item in evaluate_profiles(load_q001(source), Profile)]
    after = [item.to_dict() for item in evaluate_profiles(load_q001(copied), Profile)]
    assert before == after
