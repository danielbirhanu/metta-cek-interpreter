import pytest

from metta_cek.errors import FunctionArityError
from metta_cek.machine import CEKMachine
from metta_cek.parser import parse


def evaluate(source: str):
    machine = CEKMachine()
    state = machine.initial_state(parse(source))
    while not machine.is_final(state):
        state = machine.step(state)
    return state.control


def test_function_call_uses_parameters() -> None:
    assert evaluate("(define (double x) (* x 2)) (double 5)") == 10


def test_nested_function_call() -> None:
    source = (
        "(define (double x) (* x 2)) "
        "(define (quadruple x) (double (double x))) "
        "(quadruple 3)"
    )
    assert evaluate(source) == 12


def test_lexical_scope_uses_definition_environment() -> None:
    source = "(define x 10) (define (read) x) (define x 20) (read)"
    assert evaluate(source) == 20


def test_function_arity_is_checked() -> None:
    with pytest.raises(FunctionArityError):
        evaluate("(define (double x) (* x 2)) (double 1 2)")

