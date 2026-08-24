"""Chained environments used by the CEK machine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .errors import InterpreterError


class UndefinedVariableError(InterpreterError):
    """Raised when a name cannot be found in an environment chain."""


@dataclass
class Environment:
    """A mutable lexical environment with an optional parent."""

    bindings: dict[str, Any] = field(default_factory=dict)
    parent: Environment | None = None

    def define(self, name: str, value: Any) -> None:
        """Bind a name in this environment."""
        self.bindings[name] = value

    def lookup(self, name: str) -> Any:
        """Look up a name through this environment and its parents."""
        if name in self.bindings:
            return self.bindings[name]
        if self.parent is not None:
            return self.parent.lookup(name)
        raise UndefinedVariableError(f"undefined variable: {name}")

    def extend(self) -> Environment:
        """Create an empty child environment."""
        return Environment(parent=self)

    def __repr__(self) -> str:
        return f"Environment(bindings={self.bindings!r}, parent={self.parent is not None})"

