"""Canonical Travel Regions reference pairwise evaluator."""

from .evaluator import evaluate, hard_compatible, must_separate
from .model import DataBlockerKind, DimensionState, EvaluatorResult, Profile
from .signatures import signature_complete, signatures_equal

__all__ = [
    "DimensionState",
    "DataBlockerKind",
    "EvaluatorResult",
    "Profile",
    "evaluate",
    "hard_compatible",
    "must_separate",
    "signature_complete",
    "signatures_equal",
]

__version__ = "0.2.0"
