from __future__ import annotations

import json
import shutil
from pathlib import Path

from ctr_evaluator.evaluator import evaluate
from ctr_evaluator.loaders import load_q001
from ctr_evaluator.model import EvaluatorResult, Profile
from ctr_evaluator.reporting import evaluate_profiles


def test_q001_adapter_loads_expected_snapshot() -> None:
    bundle = load_q001()
    assert bundle.spec_version == "0.1.1-draft"
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


def test_q001_incomplete_schema_produces_no_merge() -> None:
    bundle = load_q001()
    assert all(
        evaluate(comparison, profile).result is not EvaluatorResult.MAY_MERGE
        for comparison in bundle.comparisons
        for profile in Profile
    )


def test_q001_preserves_provisional_evidence() -> None:
    bundle = load_q001()
    comparison = next(item for item in bundle.comparisons if item.id == "C001")
    assert comparison.evidence["E01"].status == "provisional"
    output = evaluate(comparison, Profile.P1)
    assert output.result is EvaluatorResult.DATA_UNKNOWN
    assert "E01.status" in output.blocked_by_data


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
