"""Deterministic Q001 result artifacts and run summary."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

from . import __version__
from .evaluator import evaluate
from .fixtures import FixtureReport
from .model import DatasetBundle, EvaluatorOutput, Profile
from .signatures import PROFILE_DEFINITIONS


FROZEN_FILENAMES = (
    "evidence.json",
    "sources.json",
    "source-index.md",
    "route-matrix.json",
    "comparisons.yaml",
)


def frozen_input_hashes(q001_dir: str | Path) -> tuple[str, dict[str, str]]:
    root = Path(q001_dir)
    paths = sorted((root / "facts").glob("*.json")) + [root / name for name in FROZEN_FILENAMES]
    per_file: dict[str, str] = {}
    aggregate = hashlib.sha256()
    for path in paths:
        relative = path.relative_to(root).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        per_file[relative] = digest
        aggregate.update(relative.encode("utf-8"))
        aggregate.update(b"\0")
        aggregate.update(bytes.fromhex(digest))
    return aggregate.hexdigest(), per_file


def evaluate_profiles(
    bundle: DatasetBundle, profiles: Iterable[Profile]
) -> tuple[EvaluatorOutput, ...]:
    selected = tuple(sorted(set(profiles), key=lambda item: item.value))
    return tuple(
        evaluate(comparison, profile)
        for comparison in sorted(bundle.comparisons, key=lambda item: item.id)
        for profile in selected
    )


def build_artifact(
    bundle: DatasetBundle, profiles: Iterable[Profile]
) -> tuple[dict[str, object], tuple[EvaluatorOutput, ...]]:
    selected = tuple(sorted(set(profiles), key=lambda item: item.value))
    outputs = evaluate_profiles(bundle, selected)
    counts: dict[str, dict[str, int]] = {}
    for profile in selected:
        profile_counts = Counter(
            output.result.value for output in outputs if output.profile is profile
        )
        counts[profile.value] = {
            result: profile_counts.get(result, 0)
            for result in (
                "must_separate",
                "may_merge",
                "separation_not_proven",
                "model_unresolved",
                "data_unknown",
                "rule_conflict",
            )
        }
    aggregate_hash, per_file = frozen_input_hashes(bundle.q001_dir)
    artifact: dict[str, object] = {
        "evaluator_version": __version__,
        "spec_version": bundle.spec_version,
        "dataset_snapshot": bundle.dataset_snapshot,
        "profiles": {
            profile.value: PROFILE_DEFINITIONS[profile] for profile in selected
        },
        "frozen_factual_inputs_hash": {
            "algorithm": "sha256",
            "value": aggregate_hash,
            "files": per_file,
        },
        "summary": counts,
        "results": [output.to_dict() for output in outputs],
    }
    return artifact, outputs


def _representative_results(contract_path: Path) -> dict[tuple[str, str], str]:
    text = contract_path.read_text(encoding="utf-8")
    section = text.split("## 8. Representative Q001 classifications", 1)[1]
    section = section.split("## 9.", 1)[0]
    current: str | None = None
    expected: dict[tuple[str, str], str] = {}
    for line in section.splitlines():
        comparison_match = re.match(r"\s{2}(C\d{3}):", line)
        if comparison_match:
            current = comparison_match.group(1)
            continue
        profile_match = re.match(r"\s{4}(P[123]): \{result: ([a-z_]+)", line)
        if current and profile_match:
            expected[(current, profile_match.group(1))] = profile_match.group(2)
    return expected


def render_run_summary(
    bundle: DatasetBundle,
    outputs: tuple[EvaluatorOutput, ...],
    fixture_report: FixtureReport,
) -> str:
    by_profile: dict[Profile, list[EvaluatorOutput]] = defaultdict(list)
    for output in outputs:
        by_profile[output.profile].append(output)

    lines = [
        "# Q001 evaluator run summary",
        "",
        f"- Evaluator version: `{__version__}`",
        f"- Spec version: `{bundle.spec_version}`",
        f"- Dataset snapshot: `{bundle.dataset_snapshot}`",
        f"- Fixtures: {fixture_report.fixture_count}/{fixture_report.fixture_count} passed",
        "",
        "## Result counts",
        "",
        "| Profile | must_separate | may_merge | separation_not_proven | model_unresolved | data_unknown | rule_conflict |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for profile in Profile:
        counts = Counter(item.result.value for item in by_profile[profile])
        lines.append(
            f"| {profile.value} | {counts['must_separate']} | {counts['may_merge']} | "
            f"{counts['separation_not_proven']} | {counts['model_unresolved']} | "
            f"{counts['data_unknown']} | {counts['rule_conflict']} |"
        )

    lines.extend(["", "## Certificates and blockers", ""])
    for profile in Profile:
        split_ids = sorted(
            item.comparison_id
            for item in by_profile[profile]
            if item.result.value == "must_separate"
        )
        data_ids = sorted(
            item.comparison_id for item in by_profile[profile] if item.blocked_by_data
        )
        model_ids = sorted(
            item.comparison_id for item in by_profile[profile] if item.blocked_by_model
        )
        lines.extend(
            [
                f"- {profile.value} sufficient split certificates: {', '.join(split_ids) or 'none'}",
                f"- {profile.value} blocked by data: {', '.join(data_ids) or 'none'}",
                f"- {profile.value} blocked by model: {', '.join(model_ids) or 'none'}",
            ]
        )
    may_merge = sorted(
        f"{item.comparison_id}/{item.profile.value}"
        for item in outputs
        if item.result.value == "may_merge"
    )
    lines.extend(
        [
            f"- `may_merge` produced: {'yes — ' + ', '.join(may_merge) if may_merge else 'no'}",
            "",
            "## Representative classification comparison",
            "",
        ]
    )
    expected = _representative_results(Path(bundle.q001_dir) / "evaluator-contract.md")
    actual = {(item.comparison_id, item.profile.value): item.result.value for item in outputs}
    mismatches = [
        (comparison, profile, expected_result, actual.get((comparison, profile), "missing"))
        for (comparison, profile), expected_result in sorted(expected.items())
        if actual.get((comparison, profile)) != expected_result
    ]
    if mismatches:
        for comparison, profile, expected_result, actual_result in mismatches:
            lines.append(
                f"- {comparison}/{profile}: contract representative `{expected_result}`; evaluator `{actual_result}`."
            )
    else:
        lines.append("No result-level mismatches were found.")
    lines.extend(
        [
            "",
            "The evaluator emits pairwise outcomes only. This artifact contains no canonical region assignments.",
            "",
        ]
    )
    return "\n".join(lines)


def write_result_artifacts(
    bundle: DatasetBundle,
    artifact: dict[str, object],
    outputs: tuple[EvaluatorOutput, ...],
    fixture_report: FixtureReport,
) -> tuple[Path, Path]:
    results_dir = Path(bundle.q001_dir) / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    json_path = results_dir / "evaluator-results.json"
    summary_path = results_dir / "run-summary.md"
    json_path.write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    summary_path.write_text(
        render_run_summary(bundle, outputs, fixture_report), encoding="utf-8"
    )
    return json_path, summary_path
