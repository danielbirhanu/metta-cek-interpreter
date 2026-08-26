import pytest

from metta_cek.errors import InvalidAssignmentError
from metta_cek.machine import CEKMachine
from metta_cek.parser import parse


def run(source: str):
    machine = CEKMachine()
    state = machine.initial_state(parse(source))
    transitions = 0
    while not machine.is_final(state):
        state = machine.step(state)
        transitions += 1
    return state.control, transitions


def test_set_and_while_update_a_counter() -> None:
    source = "(define x 0) (while (< x 3) (set x (+ x 1))) x"
    result, transitions = run(source)
    assert result == 3
    assert transitions > 20


def test_while_supports_multiple_body_expressions() -> None:
    source = (
        "(define i 1) (define total 0) "
        "(while (<= i 3) (begin (set total (+ total i)) (set i (+ i 1)))) "
        "total"
    )
    assert run(source)[0] == 6


def test_while_false_at_start_returns_false() -> None:
    assert run("(define x 4) (while (< x 3) (set x 9))")[0] is False


def test_set_undefined_name_fails() -> None:
    with pytest.raises(InvalidAssignmentError):
        run("(set missing 1)")
