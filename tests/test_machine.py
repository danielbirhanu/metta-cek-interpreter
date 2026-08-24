from metta_cek.ast import Literal, Program, Variable
from metta_cek.continuations import KRet
from metta_cek.environment import Environment
from metta_cek.machine import CEKMachine, State
from metta_cek.parser import parse


def test_literal_reaches_final_state_one_transition() -> None:
    machine = CEKMachine()
    state = machine.initial_state(Program((Literal(7),)))
    next_state = machine.step(state)
    assert next_state.control == 7
    assert machine.is_final(next_state)


def test_variable_lookup_is_explicit() -> None:
    machine = CEKMachine()
    environment = Environment({"x": 42})
    state = State(Variable("x"), environment, KRet())
    next_state = machine.step(state)
    assert next_state.control == 42
    assert next_state.environment is environment


def test_final_state_cannot_step() -> None:
    machine = CEKMachine()
    state = State(3, Environment(), KRet())
    try:
        machine.step(state)
    except Exception as error:
        assert "final" in str(error)
    else:
        raise AssertionError("expected final-state error")


def test_primitive_application_uses_cek_application_steps() -> None:
    machine = CEKMachine()
    state = machine.initial_state(parse("(+ 2 (* 3 4))"))
    steps = 0
    while not machine.is_final(state):
        state = machine.step(state)
        steps += 1
    assert state.control == 14
    assert steps > 5

