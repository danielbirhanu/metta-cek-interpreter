"""Centralized semantics for primitive operators."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .errors import ArityError, DivisionByZeroError, TypeMismatchError

PRIMITIVE_NAMES = frozenset(
    {
        "+", "-", "*", "/", "%", "<", ">", "<=", ">=",
        "=", "!=", "and", "or", "not",
    }
)


def delta(operator: str, arguments: list[Any] | tuple[Any, ...]) -> Any:
    """Apply one primitive operator to already-evaluated arguments."""
    if operator not in PRIMITIVE_NAMES:
        raise ValueError(f"unknown primitive operator: {operator}")
    values = list(arguments)
    if operator == "not":
        _require_arity(operator, values, 1)
        _require_booleans(operator, values)
        return not values[0]
    if operator in {"and", "or"}:
        _require_arity(operator, values, 2)
        _require_booleans(operator, values)
        if operator == "and":
            return values[0] and values[1]
        return values[0] or values[1]
    _require_arity(operator, values, 2)
    if operator in {"=", "!="}:
        _require_comparable(operator, values)
        return values[0] == values[1] if operator == "=" else values[0] != values[1]
    _require_integers(operator, values)
    left, right = values
    operations: dict[str, Callable[[int, int], Any]] = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a // b,
        "%": lambda a, b: a % b,
        "<": lambda a, b: a < b,
        ">": lambda a, b: a > b,
        "<=": lambda a, b: a <= b,
        ">=": lambda a, b: a >= b,
    }
    if operator in {"/", "%"} and right == 0:
        raise DivisionByZeroError(f"{operator} cannot use zero as divisor")
    return operations[operator](left, right)


def _require_arity(operator: str, values: list[Any], expected: int) -> None:
    if len(values) != expected:
        raise ArityError(f"{operator} expects {expected} argument(s), got {len(values)}")


def _require_integers(operator: str, values: list[Any]) -> None:
    valid = all(
        isinstance(value, int) and not isinstance(value, bool)
        for value in values
    )
    if not valid:
        raise TypeMismatchError(f"{operator} expects integer arguments")


def _require_booleans(operator: str, values: list[Any]) -> None:
    if not all(isinstance(value, bool) for value in values):
        raise TypeMismatchError(f"{operator} expects boolean arguments")


def _require_comparable(operator: str, values: list[Any]) -> None:
    same_type = type(values[0]) is type(values[1])
    primitive_type = isinstance(values[0], (int, bool))
    if not same_type or not primitive_type:
        raise TypeMismatchError(
            f"{operator} expects two values of the same primitive type"
        )
