"""Offline research-package integrity checks, never a legal/evaluator verdict."""

from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit


GATES = {"G-SCOPE", "G-CONTEXT", "G-HARD", "G-TIME", "G-EVIDENCE"}
REVIEW_STATES = {"supported_in_principle", "needs_evidence", "model_unresolved"}
SOURCE_ROLES = {"domestic_official_guidance", "domestic_legal_text", "foreign_travel_advisory"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def records_by_id(records: object, label: str) -> dict:
    require(isinstance(records, list) and bool(records), f"{label}: nonempty list required")
    result = {}
    for record in records:
        require(isinstance(record, dict), f"{label}: object required")
        key = record.get("id")
        require(isinstance(key, str) and bool(re.fullmatch(r"[a-z][a-z0-9-]*", key)), f"{label}: invalid ID")
        require(key not in result, f"{label}: duplicate ID {key}")
        result[key] = record
    return result


def local_file(root: Path, relative: str) -> Path:
    require(isinstance(relative, str) and bool(relative), "file path required")
    require(not Path(relative).is_absolute(), "absolute file path rejected")
    path = (root / relative).resolve()
    require(path.is_relative_to(root.resolve()), "file escapes package")
    require(path.is_file(), f"missing file: {relative}")
    return path


def validate_records(source_data: dict, research: dict, root: Path) -> dict:
    require(source_data.get("schema_version") == research.get("schema_version") == "source-pilot-v1", "wrong schema")
    retrieved = date.fromisoformat(source_data["retrieval_date"])
    require(date.fromisoformat(research["review_date"]) >= retrieved, "review predates retrieval")
    require(research.get("review_status") == "research_draft_not_independently_verified", "research cannot promote verification status")
    require(research.get("production_certificates") == [], "research cannot contain production certificates")
    require(bool(re.fullmatch(r"[a-f0-9]{64}", research.get("historical_factual_hash", ""))), "invalid baseline hash")
    sources = records_by_id(source_data["sources"], "sources")
    require(len(sources) <= 10, "pilot source-target budget exceeded")
    urls = set()
    for key, source in sources.items():
        url = source.get("url", "")
        parsed = urlsplit(url)
        require(parsed.scheme == "https" and bool(parsed.hostname), f"{key}: HTTPS source required")
        require(url not in urls, f"{key}: duplicate source target")
        urls.add(url)
        require(source.get("role") in SOURCE_ROLES, f"{key}: unknown source role")
        require(source.get("access") in {"read", "failed"}, f"{key}: unknown retrieval state")
        require(bool(source.get("publisher")) and bool(source.get("limitation")), f"{key}: publisher/limitations required")
        require("effective_from" in source and "source_date" in source, f"{key}: explicit dates required, null allowed")
        if source["source_date"] is not None:
            require(date.fromisoformat(source["source_date"]) <= retrieved, f"{key}: source date after retrieval")
            require(source.get("source_date_kind") not in {None, "unknown"}, f"{key}: date meaning required")
        else:
            require(source.get("source_date_kind") == "unknown", f"{key}: missing source date must remain unknown")
        if source["effective_from"] is not None:
            date.fromisoformat(source["effective_from"])
            require(bool(source.get("effective_date_basis")), f"{key}: legal effective date needs a basis")
        if source["access"] == "read":
            require(bool(source.get("locator")) and bool(source.get("excerpt")), f"{key}: read source needs locator and excerpt")
            require(len(source["excerpt"].split()) <= 25, f"{key}: excerpt too long")
        else:
            require(source.get("excerpt") is None and source.get("locator") is None, f"{key}: failed retrieval cannot provide read evidence")
    observations = records_by_id(research["observations"], "observations")
    for key, observation in observations.items():
        require(observation.get("kind") in {"source_supported", "research_inference"}, f"{key}: unsupported claim status")
        require(bool(observation.get("statement")), f"{key}: statement required")
        refs = observation.get("sources")
        require(isinstance(refs, list) and bool(refs), f"{key}: source references required")
        for ref in refs:
            require(ref in sources, f"{key}: unknown source {ref}")
            require(sources[ref]["access"] == "read", f"{key}: unread source cannot support observation")
    cases = records_by_id(research["cases"], "cases")
    dossiers = set()
    for key, case in cases.items():
        path = local_file(root, case["dossier"])
        require(path not in dossiers, "duplicate dossier")
        dossiers.add(path)
        require(case.get("core_submission") == "not_submitted", f"{key}: no automatic core promotion")
        require(case.get("research_outcome") in {"candidate_travel_discontinuity", "classification_unresolved"}, f"{key}: not a production verdict")
        require(isinstance(case.get("candidate_context"), dict) and bool(case["candidate_context"]), f"{key}: context required")
        refs = case.get("observations")
        require(isinstance(refs, list) and bool(refs), f"{key}: observations required")
        require(all(ref in observations for ref in refs), f"{key}: unknown observation")
        gates = case.get("gates", {})
        require(set(gates) == GATES and all(state in REVIEW_STATES for state in gates.values()), f"{key}: all five research gates required")
        gaps = case.get("gaps")
        require(isinstance(gaps, list) and bool(gaps), f"{key}: remaining gaps required")
        require(all(gap.get("kind") in {"evidence", "model"} and bool(gap.get("question")) for gap in gaps), f"{key}: typed actionable gaps required")
        if "model_unresolved" in gates.values():
            require(any(gap["kind"] == "model" for gap in gaps), f"{key}: model blocker must be explained")
    require(dossiers == set((root / "cases").glob("*.md")), "unregistered dossier")
    return {"status": "PASS", "scope": "Research integrity only; not legal verification or a Stage 1 verdict", "cases": len(cases), "observations": len(observations), "source_targets": len(sources), "sources_read": sum(s["access"] == "read" for s in sources.values()), "production_certificates": 0}


def verify_checksums(root: Path) -> None:
    listed = set()
    for line in (root / "checksums.sha256").read_text().splitlines():
        digest, name = line.split("  ", 1)
        require(name not in listed and name != "checksums.sha256", "duplicate or self-referential checksum")
        listed.add(name)
        path = local_file(root, name)
        require(hashlib.sha256(path.read_bytes()).hexdigest() == digest, f"checksum mismatch: {name}")
    expected = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and p.suffix in {".json", ".md", ".py"} and "__pycache__" not in p.parts}
    require(listed == expected, "checksum manifest does not cover exactly the package files")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        result = validate_records(json.loads((root / "sources.json").read_text()), json.loads((root / "observations.json").read_text()), root)
        verify_checksums(root)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
