import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "data" / "entry-rules"
sys.path.insert(0, str(ROOT))
import discover  # noqa: E402


def test_generated_files_are_up_to_date():
    result = subprocess.run([sys.executable, str(ROOT / "discover.py"), "--check"], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_an_ignored_candidate_needs_a_reason():
    candidate = {"key": "Ruritania / Strelsau", "country": "Ruritania", "iso_codes": "", "place": "Strelsau",
                 "place_title": "Strelsau", "wikidata": "Q1", "section": "", "passage": "a passage", "passages": 1,
                 "source_url": "https://en.wikipedia.org/w/index.php?title=x&oldid=1"}
    pins = {"articles": [], "navbox": {"title": "t", "oldid": 1, "read": "2026-10-03"}, "unread": []}
    _, _, broken = discover.report([candidate], [{"key": candidate["key"], "census_ids": "ignore", "reason": ""}],
                                   [], pins, [])
    assert broken == ["Ruritania / Strelsau: ignored without a reason"]


def test_a_mapping_to_an_unknown_census_row_is_reported():
    candidate = {"key": "Ruritania / Strelsau", "country": "Ruritania", "iso_codes": "", "place": "Strelsau",
                 "place_title": "Strelsau", "wikidata": "Q1", "section": "", "passage": "a passage", "passages": 1,
                 "source_url": "https://en.wikipedia.org/w/index.php?title=x&oldid=1"}
    pins = {"articles": [], "navbox": {"title": "t", "oldid": 1, "read": "2026-10-03"}, "unread": []}
    _, _, broken = discover.report([candidate], [{"key": candidate["key"], "census_ids": "no-such-row", "reason": ""}],
                                   [], pins, [])
    assert broken == ["Ruritania / Strelsau: unknown census id no-such-row"]
