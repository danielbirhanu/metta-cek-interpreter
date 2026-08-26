"""Chained environments used by the CEK machine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .errors import InterpreterError, InvalidAssignmentError


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

    def set_existing(self, name: str, value: Any) -> None:
        """Update the nearest existing binding in the environment chain."""
        if name in self.bindings:
            self.bindings[name] = value
            return
        if self.parent is not None:
            self.parent.set_existing(name, value)
            return
        raise InvalidAssignmentError(f"cannot set undefined variable: {name}")

    def __repr__(self) -> str:
        return f"Environment(bindings={self.bindings!r}, parent={self.parent is not None})"
