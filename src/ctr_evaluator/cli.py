"""Command-line interface for the reference evaluator."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .fixtures import validate_fixtures
from .core import evaluate_core
from .loaders import InputError, load_q001
from .model import Profile
from .reporting import build_artifact, write_result_artifacts


def _json_dump(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False))


def _profiles(value: str) -> tuple[Profile, ...]:
    try:
        parsed = tuple(Profile(item.strip()) for item in value.split(",") if item.strip())
    except ValueError as exc:
        raise argparse.ArgumentTypeError("profiles must be a comma-separated subset of P1,P2,P3") from exc
    if not parsed:
        raise argparse.ArgumentTypeError("at least one profile is required")
    return tuple(sorted(set(parsed), key=lambda item: item.value))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m ctr_evaluator")
    parser.add_argument(
        "--q001-dir",
        default="experiments/q001",
        help="Q001 package directory (default: experiments/q001)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate-fixtures", help="validate all synthetic contract fixtures")

    core_parser = subparsers.add_parser("evaluate-core", help="evaluate an explicit S1-core-v1 CR-W proof bundle; never reinterpret historical Q001 inputs")
    core_parser.add_argument("--input", required=True, type=Path, help="versioned JSON proof bundle")

    evaluate_parser = subparsers.add_parser("evaluate", help="evaluate one Q001 comparison")
    evaluate_parser.add_argument("--comparison", required=True)
    evaluate_parser.add_argument("--profile", required=True, choices=[item.value for item in Profile])

    all_parser = subparsers.add_parser("evaluate-all", help="evaluate every Q001 comparison")
    selection = all_parser.add_mutually_exclusive_group()
    selection.add_argument("--profile", choices=[item.value for item in Profile])
    selection.add_argument("--profiles", type=_profiles)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "evaluate-core":
            _json_dump(evaluate_core(json.loads(args.input.read_text(encoding="utf-8"))))
            return 0
        if args.command == "validate-fixtures":
            report = validate_fixtures(args.q001_dir)
            payload = {
                "status": "PASS" if report.passed else "FAIL",
                "fixtures_passed": report.fixture_count - len({item.fixture_id for item in report.failures}),
                "fixture_count": report.fixture_count,
                "assertions_checked": report.assertion_count,
                "failures": [
                    {
                        "fixture_id": item.fixture_id,
                        "profile": item.profile,
                        "message": item.message,
                    }
                    for item in report.failures
                ],
            }
            _json_dump(payload)
            return 0 if report.passed else 1

        bundle = load_q001(args.q001_dir)
        if args.command == "evaluate":
            matches = [item for item in bundle.comparisons if item.id == args.comparison]
            if not matches:
                raise InputError(f"unknown comparison id: {args.comparison}")
            from .evaluator import evaluate

            _json_dump(evaluate(matches[0], Profile(args.profile)).to_dict())
            return 0

        selected = (
            (Profile(args.profile),)
            if args.profile
            else args.profiles or tuple(Profile)
        )
        artifact, outputs = build_artifact(bundle, selected)
        if set(selected) == set(Profile):
            fixture_report = validate_fixtures(args.q001_dir)
            if not fixture_report.passed:
                raise InputError("fixture validation failed; result artifacts were not written")
            write_result_artifacts(bundle, artifact, outputs, fixture_report)
        _json_dump(artifact)
        return 0
    except (InputError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
