"""Runtime value representations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Primitive:
    """A built-in operator awaiting dispatch through delta."""

    name: str


@dataclass(frozen=True)
class Closure:
    """A function body and its definition environment."""

    parameters: tuple[str, ...]
    body: Any
    definition_environment: Any

