import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "data" / "disputed-areas"
sys.path.insert(0, str(ROOT))
import build  # noqa: E402

MANUAL = {"area_id": "bir-tawil", "field": "inhabited", "value": "no", "source_ids": "NE",
          "quote": "a passage long enough to be found", "read_date": "2026-10-03", "evidence": "secondary", "origin": "manual"}


def errors_with(fact):
    return build.validate(build.read("areas.csv"), [fact], build.read("sources.csv"))


def test_register_is_valid():
    assert build.validate(build.read("areas.csv"), build.read("facts.csv"), build.read("sources.csv")) == []


def test_generated_files_are_up_to_date():
    result = subprocess.run([sys.executable, str(ROOT / "build.py"), "--check"], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_a_well_formed_manual_fact_is_accepted():
    assert errors_with(MANUAL) == []


def test_a_fact_without_a_source_is_rejected():
    assert any("source" in e for e in errors_with({**MANUAL, "source_ids": ""}))


def test_a_manual_fact_without_a_quoted_passage_is_rejected():
    assert any("passage" in e for e in errors_with({**MANUAL, "quote": ""}))


def test_memory_is_not_an_evidence_level():
    assert any("evidence" in e for e in errors_with({**MANUAL, "evidence": "memory"}))


def test_an_unknown_kind_is_rejected():
    assert errors_with({**MANUAL, "field": "kind", "value": "interesting"})
