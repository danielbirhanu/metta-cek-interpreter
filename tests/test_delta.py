import pytest

from metta_cek.delta import delta
from metta_cek.errors import ArityError, DivisionByZeroError, TypeMismatchError


@pytest.mark.parametrize(
    ("operator", "arguments", "expected"),
    [
        ("+", [7, 3], 10), ("-", [7, 3], 4),
        ("*", [7, 3], 21), ("/", [7, 3], 2),
        ("%", [7, 3], 1), ("<", [3, 7], True),
        (">", [7, 3], True), ("<=", [3, 3], True),
        (">=", [3, 3], True), ("=", [3, 3], True),
        ("!=", [3, 4], True), ("and", [True, False], False),
        ("or", [True, False], True), ("not", [False], True),
    ],
)
def test_delta_primitives(operator, arguments, expected) -> None:
    assert delta(operator, arguments) == expected


def test_delta_rejects_wrong_arity() -> None:
    with pytest.raises(ArityError):
        delta("+", [1])


def test_delta_rejects_wrong_types() -> None:
    with pytest.raises(TypeMismatchError):
        delta("+", [True, 1])


@pytest.mark.parametrize("operator", ["/", "%"])
def test_delta_rejects_zero_divisor(operator) -> None:
    with pytest.raises(DivisionByZeroError):
        delta(operator, [5, 0])

