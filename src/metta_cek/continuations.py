"""Continuation frames for explicit CEK transitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class Continuation:
    """Base continuation type."""


@dataclass(frozen=True)
class KRet(Continuation):
    """The final continuation."""


@dataclass(frozen=True)
class KApp(Continuation):
    """Application progress: completed values and pending expressions."""

    done: tuple[Any, ...]
    saved_environment: Any
    todo: tuple[Any, ...]
    rest: Continuation


@dataclass(frozen=True)
class KIf(Continuation):
    """Conditional branches waiting for a condition value."""

    saved_environment: Any
    then_branch: Any
    else_branch: Any
    rest: Continuation


@dataclass(frozen=True)
class KDefine(Continuation):
    """A definition waiting for its value."""

    name: str
    saved_environment: Any
    rest: Continuation


@dataclass(frozen=True)
class KSequence(Continuation):
    """Top-level forms waiting to be evaluated."""

    saved_environment: Any
    todo: tuple[Any, ...]
    rest: Continuation

