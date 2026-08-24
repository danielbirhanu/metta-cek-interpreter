"""Abstract syntax tree nodes for the scoped MeTTa-like language."""

from __future__ import annotations

from dataclasses import dataclass


class Expression:
    """Base class for all expressions."""


@dataclass(frozen=True)
class Literal(Expression):
    """An integer or boolean literal."""

    value: int | bool


@dataclass(frozen=True)
class Variable(Expression):
    """A name resolved through the CEK environment."""

    name: str


@dataclass(frozen=True)
class Application(Expression):
    """A prefix application, including the operator expression."""

    operator: Expression
    arguments: tuple[Expression, ...]


@dataclass(frozen=True)
class IfExpression(Expression):
    """Conditional expression."""

    condition: Expression
    then_branch: Expression
    else_branch: Expression


@dataclass(frozen=True)
class DefineExpression(Expression):
    """Variable definition."""

    name: str
    value: Expression


@dataclass(frozen=True)
class FunctionDefinition(Expression):
    """Named function definition."""

    name: str
    parameters: tuple[str, ...]
    body: Expression


@dataclass(frozen=True)
class SetExpression(Expression):
    """Mutation of an existing binding."""

    name: str
    value: Expression


@dataclass(frozen=True)
class WhileExpression(Expression):
    """Condition-controlled loop."""

    condition: Expression
    body: Expression


@dataclass(frozen=True)
class Program:
    """A source file's ordered top-level expressions."""

    expressions: tuple[Expression, ...]

