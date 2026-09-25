from copy import deepcopy
import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1] / "experiments/source-pilot"
spec = importlib.util.spec_from_file_location("source_pilot_validator", ROOT / "validate.py")
pilot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pilot)


@pytest.fixture
def data():
    return (json.loads((ROOT / "sources.json").read_text()), json.loads((ROOT / "observations.json").read_text()))


def test_package_valid_and_deterministic(data):
    first = pilot.validate_records(*data, ROOT)
    assert first == pilot.validate_records(*deepcopy(data), ROOT)
    assert first["cases"] == 3
    assert first["sources_read"] == 8
    assert first["production_certificates"] == 0


def test_failed_retrieval_cannot_support_claim(data):
    data[1]["observations"][0]["sources"] = ["fr-order-unavailable"]
    with pytest.raises(ValueError, match="unread source"):
        pilot.validate_records(*data, ROOT)


@pytest.mark.parametrize("change", ["verification", "certificate", "submission", "verdict", "gate"])
def test_research_is_not_silently_promoted(data, change):
    research = data[1]
    if change == "verification":
        research["review_status"] = "verified"
    elif change == "certificate":
        research["production_certificates"] = [{"status": "verified"}]
    elif change == "submission":
        research["cases"][0]["core_submission"] = "submitted"
    elif change == "verdict":
        research["cases"][0]["research_outcome"] = "hard_compatible"
    else:
        research["cases"][0]["gates"]["G-EVIDENCE"] = "proven_true"
    with pytest.raises(ValueError):
        pilot.validate_records(*data, ROOT)


def test_unknown_nationality_and_effective_dates_are_allowed(data):
    assert data[1]["cases"][1]["candidate_context"]["nationality"] is None
    assert all(s["effective_from"] is None for s in data[0]["sources"])
    assert pilot.validate_records(*data, ROOT)["status"] == "PASS"


def test_effective_date_cannot_be_inferred_from_retrieval(data):
    data[0]["sources"][0]["effective_from"] = data[0]["retrieval_date"]
    with pytest.raises(ValueError, match="needs a basis"):
        pilot.validate_records(*data, ROOT)


@pytest.mark.parametrize("reference", ["missing-source", "duplicate-source", "missing-observation", "missing-dossier", "escaped-dossier"])
def test_broken_references_rejected(data, reference):
    if reference == "missing-source":
        data[1]["observations"][0]["sources"] = ["absent"]
    elif reference == "duplicate-source":
        data[0]["sources"].append(deepcopy(data[0]["sources"][0]))
    elif reference == "missing-observation":
        data[1]["cases"][0]["observations"] = ["absent"]
    elif reference == "missing-dossier":
        data[1]["cases"][0]["dossier"] = "cases/missing.md"
    else:
        data[1]["cases"][0]["dossier"] = "../q001/README.md"
    with pytest.raises(ValueError):
        pilot.validate_records(*data, ROOT)


def test_historical_factual_hash_unchanged(data):
    from ctr_evaluator.reporting import frozen_input_hashes
    actual, _ = frozen_input_hashes(ROOT.parent / "q001")
    assert actual == data[1]["historical_factual_hash"]
