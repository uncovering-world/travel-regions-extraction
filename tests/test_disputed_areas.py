import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "data" / "disputed-areas"
sys.path.insert(0, str(ROOT))
import build  # noqa: E402


def test_register_is_valid():
    assert build.validate(build.read("areas.csv"), build.read("facts.csv"), build.read("sources.csv")) == []


def test_generated_files_are_up_to_date():
    result = subprocess.run([sys.executable, str(ROOT / "build.py"), "--check"], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_validation_rejects_a_fact_without_a_source():
    facts = build.read("facts.csv")
    facts[0] = {**facts[0], "source_ids": ""}
    errors = build.validate(build.read("areas.csv"), facts, build.read("sources.csv"))
    assert any("source" in e for e in errors)


def test_validation_rejects_an_unknown_kind():
    facts = build.read("facts.csv")
    index = next(i for i, f in enumerate(facts) if f["field"] == "kind")
    facts[index] = {**facts[index], "value": "interesting"}
    assert build.validate(build.read("areas.csv"), facts, build.read("sources.csv"))
