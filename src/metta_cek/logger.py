"""Readable logging for CEK state transitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TextIO

from .machine import State


@dataclass
class TransitionLogger:
    """Write numbered CEK transitions to a stream."""

    stream: TextIO
    step_number: int = 0

    def log(self, current: State, next_state: State, rule: str) -> None:
        """Write one transition and advance the step counter."""
        self.stream.write("=" * 60 + "\n")
        self.stream.write(f"STEP {self.step_number}\n")
        self.stream.write("=" * 60 + "\n")
        self.stream.write("CONTROL:\n")
        self.stream.write(f"    {current.control!r}\n\n")
        self.stream.write("ENVIRONMENT:\n")
        self.stream.write(f"    {current.environment!r}\n\n")
        self.stream.write("CONTINUATION:\n")
        self.stream.write(f"    {current.continuation!r}\n\n")
        self.stream.write(f"TRANSITION: {rule}\n\n")
        self.stream.write("NEXT STATE:\n")
        self.stream.write(f"    CONTROL: {next_state.control!r}\n")
        self.stream.write(f"    ENVIRONMENT: {next_state.environment!r}\n")
        self.stream.write(f"    CONTINUATION: {next_state.continuation!r}\n")
        self.stream.flush()
        self.step_number += 1

    def log_final(self, state: State) -> None:
        """Write the final state after all transitions."""
        self.stream.write("=" * 60 + "\n")
        self.stream.write(f"FINAL STATE {self.step_number}\n")
        self.stream.write("=" * 60 + "\n")
        self.stream.write(f"CONTROL: {state.control!r}\n")
        self.stream.write(f"ENVIRONMENT: {state.environment!r}\n")
        self.stream.write(f"CONTINUATION: {state.continuation!r}\n")
        self.stream.flush()


def run_with_trace(machine, state: State, logger: TransitionLogger) -> State:
    """Drive a machine to completion while logging every transition."""
    while not machine.is_final(state):
        next_state = machine.step(state)
        logger.log(state, next_state, transition_name(state, next_state))
        state = next_state
    logger.log_final(state)
    return state


def transition_name(current: State, next_state: State) -> str:
    """Return a compact rule name inferred from state shapes."""
    control_name = type(current.control).__name__
    continuation_name = type(current.continuation).__name__
    if control_name == "Application":
        return "APPLICATION_START"
    if control_name == "IfExpression":
        return "IF_START"
    if control_name == "WhileExpression":
        return "WHILE_START"
    if control_name == "SetExpression":
        return "SET_START"
    if control_name == "DefineExpression":
        return "DEFINE_START"
    if continuation_name == "KApp":
        return "APPLICATION_PROGRESS"
    if continuation_name == "KIf":
        return "IF_BRANCH_SELECT"
    if continuation_name == "KWhileCondition":
        return "WHILE_CONDITION"
    if continuation_name == "KWhileBody":
        return "WHILE_BODY_COMPLETE"
    if continuation_name == "KSet":
        return "SET_COMPLETE"
    if continuation_name == "KDefine":
        return "DEFINE_COMPLETE"
    if control_name == "Variable":
        return "VARIABLE_LOOKUP"
    return "VALUE_RETURN"

