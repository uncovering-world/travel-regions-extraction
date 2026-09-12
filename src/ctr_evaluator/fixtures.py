"""Executable subset-oracle validation for the 15 contract fixtures."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .evaluator import evaluate
from .loaders import InputError, load_fixture_variants, load_fixtures
from .model import Profile


@dataclass(frozen=True)
class FixtureFailure:
    fixture_id: str
    profile: str
    message: str


@dataclass(frozen=True)
class FixtureReport:
    fixture_count: int
    assertion_count: int
    failures: tuple[FixtureFailure, ...]

    @property
    def passed(self) -> bool:
        return not self.failures


def _assert_subset(expected: Any, actual: Any, path: str = "result") -> None:
    if isinstance(expected, Mapping):
        if not isinstance(actual, Mapping):
            raise AssertionError(f"{path}: expected object, got {type(actual).__name__}")
        for key, value in expected.items():
            if key == "all_variants_equal":
                continue
            if key not in actual:
                raise AssertionError(f"{path}.{key}: missing")
            _assert_subset(value, actual[key], f"{path}.{key}")
        return
    if isinstance(expected, list):
        if expected != actual:
            raise AssertionError(f"{path}: expected {expected!r}, got {actual!r}")
        return
    if expected != actual:
        raise AssertionError(f"{path}: expected {expected!r}, got {actual!r}")


def validate_fixtures(q001_dir: str | Path = "experiments/q001") -> FixtureReport:
    fixtures = load_fixtures(q001_dir)
    failures: list[FixtureFailure] = []
    assertion_count = 0
    for fixture in fixtures:
        fixture_id = str(fixture["id"])
        try:
            variants = load_fixture_variants(fixture)
        except (InputError, ValueError) as exc:
            failures.append(FixtureFailure(fixture_id, "input", str(exc)))
            continue
        for profile_name, expected in fixture["expected"].items():
            profile = Profile(profile_name)
            outputs = [evaluate(variant, profile).to_dict() for variant in variants]
            try:
                for output in outputs:
                    _assert_subset(expected, output)
                    assertion_count += 1
                if expected.get("all_variants_equal") is True:
                    semantic = [
                        {
                            key: value
                            for key, value in output.items()
                            if key not in {"comparison_id"}
                        }
                        for output in outputs
                    ]
                    if any(item != semantic[0] for item in semantic[1:]):
                        raise AssertionError("input variants do not have equal semantic output")
                    assertion_count += 1
            except AssertionError as exc:
                failures.append(FixtureFailure(fixture_id, profile_name, str(exc)))
    return FixtureReport(len(fixtures), assertion_count, tuple(failures))
