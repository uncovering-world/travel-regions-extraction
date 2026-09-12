"""Canonical Travel Regions reference pairwise evaluator."""

from .evaluator import evaluate, may_merge, must_separate
from .model import DimensionState, EvaluatorResult, Profile
from .signatures import signature_complete, signatures_equal

__all__ = [
    "DimensionState",
    "EvaluatorResult",
    "Profile",
    "evaluate",
    "may_merge",
    "must_separate",
    "signature_complete",
    "signatures_equal",
]

__version__ = "0.1.0"
