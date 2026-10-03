import io
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent / "data" / "disputed-areas"
sys.path.insert(0, str(ROOT))
import build  # noqa: E402
import import_facts  # noqa: E402
import verify_quotes  # noqa: E402

MANUAL = {"area_id": "bir-tawil", "field": "inhabited", "value": "no", "source_ids": "NE",
          "quote": "a passage long enough to be found", "read_date": "2026-10-03", "evidence": "secondary", "origin": "manual"}
MACHINE = {"area_id": "bir-tawil", "field": "ne_name", "value": "Bir Tawil", "source_ids": "NE",
           "quote": "", "read_date": "2026-10-03", "evidence": "machine", "origin": "machine"}
# the same fact as MANUAL, the way a file for import_facts.py gives it
ROW = {"area_id": "bir-tawil", "field": "inhabited", "value": "no", "evidence": "secondary",
       "source_url": "https://en.wikipedia.org/w/index.php?title=Bir_Tawil&oldid=1", "quote": "a passage long enough to be found"}


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


def page_as_read(markup, tmp_path, monkeypatch):
    """The text verify_quotes keeps of a Wikipedia revision whose HTML is `markup`."""
    monkeypatch.setattr(verify_quotes, "CACHE", tmp_path)
    monkeypatch.setattr(verify_quotes.time, "sleep", lambda seconds: None)
    monkeypatch.setattr(verify_quotes.urllib.request, "urlopen",
                        lambda request, timeout: io.BytesIO(json.dumps({"parse": {"text": markup}}).encode()))
    return verify_quotes.page_text("https://en.wikipedia.org/w/index.php?title=Kafia_Kingi&oldid=1377801384")


def test_a_passage_running_across_a_citation_marker_is_found(tmp_path, monkeypatch):
    # Wikipedia's markup of a footnote; with the tags turned into spaces it reads "[ 1 ]"
    text = page_as_read('<th>Estimate (2010)<sup class="reference"><a href="#cite_note-1"><span class="cite-bracket">&#91;</span>1'
                        '<span class="cite-bracket">&#93;</span></a></sup></th><td>16,000</td>', tmp_path, monkeypatch)
    assert verify_quotes.squash("Estimate (2010) 16,000") in verify_quotes.squash(text)


def test_a_passage_running_across_a_citation_needed_tag_is_found(tmp_path, monkeypatch):
    text = page_as_read('<p>100 sub-tribes live in the state,<sup class="noprint Inline-Template">&#91;<i>'
                        '<a href="/wiki/Wikipedia:Citation_needed"><span title="This claim needs references.">citation needed</span></a>'
                        '</i>&#93;</sup> including Nocte</p>', tmp_path, monkeypatch)
    assert verify_quotes.squash("100 sub-tribes live in the state, including Nocte") in verify_quotes.squash(text)


def test_other_bracketed_text_stays_in_the_passage():
    assert verify_quotes.squash("Order 1958 [India] , [ c ] and [ note 1 ]") == "order 1958 [india] , [ c ] and [ note 1 ]"


def imported(*rows, facts=(), sources=()):
    """What import_facts makes of these rows: the facts, the sources and the rows it left out."""
    return import_facts.merge([(f"rows.csv line {n}", row) for n, row in enumerate(rows, 2)], build.read("areas.csv"),
                              list(facts), list(sources), date(2026, 10, 3))


def test_an_imported_row_becomes_a_manual_fact_with_its_source():
    facts, sources, left_out = imported(ROW)
    assert facts == [{**MANUAL, "source_ids": "S0001"}] and left_out == []
    assert sources == [{"source_id": "S0001", "url": ROW["source_url"], "access": "manual", "note": ""}]
    assert build.validate(build.read("areas.csv"), facts, sources) == []


def test_importing_never_replaces_an_existing_fact():
    facts, sources, left_out = imported({**ROW, "value": "yes"}, facts=[MANUAL])
    assert facts == [MANUAL] and sources == []
    assert len(left_out) == 1 and "rows.csv line 2: bir-tawil/inhabited" in left_out[0] and "already has 'no'" in left_out[0]


def test_two_rows_for_one_area_and_field_are_both_left_out():
    facts, sources, left_out = imported(ROW, {**ROW, "value": "yes"})
    assert facts == [] and sources == [] and len(left_out) == 2


def test_rows_that_break_the_rules_of_the_register_are_left_out():
    for change in ({"area_id": "atlantis"}, {"field": "colour"}, {"field": "wd_label"}, {"field": "kind", "value": "interesting"},
                   {"value": ""}, {"evidence": "memory"}, {"evidence": "machine"}, {"quote": "too short"}, {"quote": None},
                   {"source_url": "from memory"}, {"source_url": "https://en.wikipedia.org/wiki/Bir_Tawil"}):
        facts, sources, left_out = imported({**ROW, **change})
        assert (facts, sources, len(left_out)) == ([], [], 1), change


def test_a_known_source_keeps_its_id_and_new_ones_are_numbered_after_it():
    known = {"source_id": "S0007", "url": ROW["source_url"], "access": "manual", "note": ""}
    facts, sources, _ = imported(ROW, {**ROW, "field": "origin", "value": "1902", "source_url": "https://example.org/b"},
                                 {**ROW, "field": "parties", "value": "nobody", "source_url": "https://example.org/a"}, sources=[known])
    assert [(f["field"], f["source_ids"]) for f in facts] == [("parties", "S0008"), ("origin", "S0009"), ("inhabited", "S0007")]
    assert [(s["source_id"], s["url"]) for s in sources] == [("S0007", ROW["source_url"]), ("S0008", "https://example.org/a"),
                                                             ("S0009", "https://example.org/b")]


def test_imported_facts_stand_before_the_machine_facts_of_their_area():
    abyei = {**MACHINE, "area_id": "abyei"}
    facts, _, _ = imported(ROW, {**ROW, "area_id": "abyei"}, facts=[abyei, MACHINE])
    assert [(f["area_id"], f["origin"]) for f in facts] == [("abyei", "manual"), ("abyei", "machine"),
                                                            ("bir-tawil", "manual"), ("bir-tawil", "machine")]


def test_the_importer_adds_to_the_files_and_lists_what_it_left_out(tmp_path, monkeypatch, capsys):
    machine = "bir-tawil,ne_note,\"Claimed by no one, see \"\"terra nullius\"\"\",NE,,2026-10-03,machine,machine\n"
    (tmp_path / "areas.csv").write_text("area_id,name,wikidata_id,natural_earth_id\nbir-tawil,Bir Tawil,,\n")
    (tmp_path / "facts.csv").write_text(",".join(import_facts.FACT_COLUMNS) + "\n" + machine)
    (tmp_path / "sources.csv").write_text("source_id,url,access,note\nNE,https://example.org/ne,machine,\"Natural Earth, pinned\"\n")
    (tmp_path / "rows.csv").write_text(",".join(import_facts.COLUMNS) + "\n"
                                       + f"bir-tawil,inhabited,no,{ROW['source_url']},{ROW['quote']},secondary\n"
                                       + f"bir-tawil,kind,interesting,{ROW['source_url']},{ROW['quote']},secondary\n")
    monkeypatch.setattr(build, "ROOT", tmp_path)
    monkeypatch.setattr(import_facts, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["import_facts.py", "--date", "2026-10-03", str(tmp_path / "rows.csv")])
    assert import_facts.main() == 1
    assert "rows.csv line 3: bir-tawil/kind: value 'interesting' not allowed" in capsys.readouterr().err
    after = (tmp_path / "facts.csv").read_text(), (tmp_path / "sources.csv").read_text()
    assert after[0] == (",".join(import_facts.FACT_COLUMNS) + "\n"
                        + f"bir-tawil,inhabited,no,S0001,{ROW['quote']},2026-10-03,secondary,manual\n" + machine)
    assert after[1].endswith(f"\"Natural Earth, pinned\"\nS0001,{ROW['source_url']},manual,\n")
    assert import_facts.main() == 1  # a second run finds both rows unusable and changes nothing
    assert "bir-tawil/inhabited: the register already has 'no'" in capsys.readouterr().err
    assert after == ((tmp_path / "facts.csv").read_text(), (tmp_path / "sources.csv").read_text())


def test_a_file_with_other_columns_is_refused(tmp_path, monkeypatch):
    (tmp_path / "census.csv").write_text("id,name,parties,kind\nbir-tawil,Bir Tawil,none,unclaimed\n")
    monkeypatch.setattr(build, "ROOT", tmp_path)
    monkeypatch.setattr(import_facts, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["import_facts.py", "--date", "2026-10-03", str(tmp_path / "census.csv")])
    with pytest.raises(SystemExit):
        import_facts.main()
    assert sorted(p.name for p in tmp_path.iterdir()) == ["census.csv"]
