"""Typed domain model for the pairwise evaluator."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping


class Profile(str, Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class DimensionState(str, Enum):
    KNOWN_VALUE = "known_value"
    KNOWN_ABSENCE = "known_absence"
    UNKNOWN = "unknown"
    NOT_APPLICABLE = "not_applicable"
    UNRESOLVED_MODEL_SEMANTICS = "unresolved_model_semantics"


class EvaluatorResult(str, Enum):
    MUST_SEPARATE = "must_separate"
    HARD_COMPATIBLE = "hard_compatible"
    SEPARATION_NOT_PROVEN = "separation_not_proven"
    MODEL_UNRESOLVED = "model_unresolved"
    DATA_UNKNOWN = "data_unknown"
    RULE_CONFLICT = "rule_conflict"


class SignatureEquality(str, Enum):
    TRUE = "true"
    FALSE = "false"
    UNKNOWN = "unknown"


class DataBlockerKind(str, Enum):
    MISSING_FACT = "missing_fact"
    SOURCE_CONFLICT = "source_conflict"
    VERIFICATION_STATUS = "verification_status"


@dataclass(frozen=True, order=True)
class DataBlocker:
    id: str
    evidence_refs: tuple[str, ...] = ()
    profiles: frozenset[Profile] = field(default_factory=lambda: frozenset(Profile))
    kind: DataBlockerKind = DataBlockerKind.MISSING_FACT


@dataclass(frozen=True, order=True)
class ModelBlocker:
    id: str
    profiles: frozenset[Profile] = field(default_factory=lambda: frozenset(Profile))


@dataclass(frozen=True)
class HardSignatureDimension:
    name: str
    state: DimensionState
    value: Any = None
    evidence_refs: tuple[str, ...] = ()
    rationale: str | None = None
    blocker_id: str | None = None
    source_conflict: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "evidence_refs", tuple(sorted(set(self.evidence_refs))))
        if self.state is DimensionState.KNOWN_VALUE and (
            self.value is None or self.value == "unknown"
        ):
            raise ValueError(f"{self.name}: known_value requires a concrete value")
        if self.state is DimensionState.KNOWN_ABSENCE and not self.evidence_refs:
            raise ValueError(f"{self.name}: known_absence requires positive evidence")
        if self.state is DimensionState.NOT_APPLICABLE and not self.rationale:
            raise ValueError(f"{self.name}: not_applicable requires a rule rationale")

    @property
    def complete(self) -> bool:
        return self.state in {
            DimensionState.KNOWN_VALUE,
            DimensionState.KNOWN_ABSENCE,
            DimensionState.NOT_APPLICABLE,
        } and not self.source_conflict

    def semantic_value(self) -> tuple[str, Any]:
        if self.state is DimensionState.NOT_APPLICABLE:
            return (self.state.value, self.rationale)
        if self.state is DimensionState.KNOWN_ABSENCE:
            return (self.state.value, None)
        return (self.state.value, self.value)


@dataclass(frozen=True)
class FactualUnitReference:
    id: str
    dimensions: Mapping[str, HardSignatureDimension] = field(default_factory=dict)
    complete_tokens: Mapping[Profile, str] = field(default_factory=dict)
    incomplete_reasons: Mapping[Profile, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "dimensions", MappingProxyType(dict(self.dimensions)))
        object.__setattr__(self, "complete_tokens", MappingProxyType(dict(self.complete_tokens)))
        object.__setattr__(self, "incomplete_reasons", MappingProxyType(dict(self.incomplete_reasons)))


@dataclass(frozen=True)
class EvidenceRecord:
    id: str
    status: str
    source_refs: tuple[str, ...] = ()
    observed_as_of: str | None = None


@dataclass(frozen=True)
class TravellerWitness:
    id: str
    scope: str
    dimension: str
    decision_a: Any
    decision_b: Any
    status: str
    evidence_refs: tuple[str, ...] = ()
    traveller_scope: str = "civilian_short_stay"

    def __post_init__(self) -> None:
        object.__setattr__(self, "evidence_refs", tuple(sorted(set(self.evidence_refs))))


@dataclass(frozen=True, order=True)
class RuleDerivation:
    rule: str
    requires: EvaluatorResult
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class SignatureAssessment:
    complete: bool
    semantic_value: tuple[Any, ...] | None
    evidence_refs: tuple[str, ...] = ()
    data_blockers: tuple[DataBlocker, ...] = ()
    model_blockers: tuple[ModelBlocker, ...] = ()


@dataclass(frozen=True)
class ComparisonInput:
    id: str
    a: FactualUnitReference
    b: FactualUnitReference
    witnesses: tuple[TravellerWitness, ...] = ()
    evidence: Mapping[str, EvidenceRecord] = field(default_factory=dict)
    derivations: tuple[RuleDerivation, ...] = ()
    data_blockers: tuple[DataBlocker, ...] = ()
    model_blockers: tuple[ModelBlocker, ...] = ()
    jurisdiction_difference: bool | None = None
    jurisdiction_evidence_refs: tuple[str, ...] = ()
    disputed_identity_relevant: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "evidence", MappingProxyType(dict(self.evidence)))
        object.__setattr__(
            self, "jurisdiction_evidence_refs", tuple(sorted(set(self.jurisdiction_evidence_refs)))
        )


@dataclass(frozen=True)
class EvaluatorOutput:
    comparison_id: str
    profile: Profile
    result: EvaluatorResult
    applied_rules: tuple[str, ...]
    witnesses: tuple[str, ...]
    signature_a_complete: bool
    signature_b_complete: bool
    signature_equal: SignatureEquality
    blocked_by_data: tuple[str, ...]
    blocked_by_model: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        equal: bool | str
        if self.signature_equal is SignatureEquality.TRUE:
            equal = True
        elif self.signature_equal is SignatureEquality.FALSE:
            equal = False
        else:
            equal = "unknown"
        return {
            "comparison_id": self.comparison_id,
            "profile": self.profile.value,
            "result": self.result.value,
            "applied_rules": list(self.applied_rules),
            "witnesses": list(self.witnesses),
            "signature": {
                "a_complete": self.signature_a_complete,
                "b_complete": self.signature_b_complete,
                "equal": equal,
            },
            "blocked_by_data": list(self.blocked_by_data),
            "blocked_by_model": list(self.blocked_by_model),
            "evidence_refs": list(self.evidence_refs),
            "explanation": self.explanation,
        }


@dataclass(frozen=True)
class DatasetBundle:
    spec_version: str
    dataset_snapshot: str
    q001_dir: str
    comparisons: tuple[ComparisonInput, ...]
