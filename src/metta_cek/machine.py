"""The explicit small-step CEK machine core."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .ast import (
    Application, DefineExpression, Expression, FunctionDefinition,
    IfExpression, Literal, Program, Variable,
)
from .continuations import KApp, KDefine, KIf, KRet, KSequence, Continuation
from .environment import Environment
from .errors import InterpreterError
from .values import Closure, Primitive


@dataclass(frozen=True)
class State:
    """A CEK snapshot: Control, Environment, and Continuation."""

    control: Any
    environment: Environment
    continuation: Continuation


class InvalidStateError(InterpreterError):
    """Raised when no CEK transition applies to a state."""


class CEKMachine:
    """Small-step evaluator for the current CEK core."""

    def initial_state(self, program: Program) -> State:
        """Create the initial state for a parsed program."""
        environment = Environment()
        expressions = program.expressions
        if not expressions:
            return State(None, environment, KRet())
        return State(
            expressions[0],
            environment,
            KSequence(environment, expressions[1:], KRet()),
        )

    def is_final(self, state: State) -> bool:
        """Return whether a state contains a final value and `KRet`."""
        return isinstance(state.continuation, KRet) and self._is_value(state.control)

    def step(self, state: State) -> State:
        """Perform exactly one CEK transition."""
        control, environment, continuation = (
            state.control,
            state.environment,
            state.continuation,
        )
        if self.is_final(state):
            raise InvalidStateError("cannot step a final CEK state")
        if isinstance(control, Literal):
            return self._continue(control.value, environment, continuation)
        if isinstance(control, Variable):
            return self._continue(environment.lookup(control.name), environment, continuation)
        if isinstance(control, Application):
            return State(
                control.operator,
                environment,
                KApp((), environment, control.arguments, continuation),
            )
        if isinstance(control, IfExpression):
            return State(
                control.condition,
                environment,
                KIf(environment, control.then_branch, control.else_branch, continuation),
            )
        if isinstance(control, DefineExpression):
            return State(
                control.value,
                environment,
                KDefine(control.name, environment, continuation),
            )
        if isinstance(control, FunctionDefinition):
            closure = Closure(control.parameters, control.body, environment)
            return self._continue(closure, environment, continuation)
        if self._is_value(control):
            return self._continue(control, environment, continuation)
        raise InvalidStateError(f"unsupported control: {control!r}")

    def _continue(self, value: Any, environment: Environment, continuation: Continuation) -> State:
        if isinstance(continuation, KRet):
            return State(value, environment, continuation)
        if isinstance(continuation, KSequence):
            if not continuation.todo:
                return State(value, environment, continuation.rest)
            next_expression = continuation.todo[0]
            return State(
                next_expression,
                continuation.saved_environment,
                KSequence(continuation.saved_environment, continuation.todo[1:], continuation.rest),
            )
        if isinstance(continuation, KIf):
            if not isinstance(value, bool):
                raise InterpreterError("if condition must evaluate to a boolean")
            branch = continuation.then_branch if value else continuation.else_branch
            return State(branch, continuation.saved_environment, continuation.rest)
        if isinstance(continuation, KDefine):
            continuation.saved_environment.define(continuation.name, value)
            return State(value, continuation.saved_environment, continuation.rest)
        if isinstance(continuation, KApp):
            done = continuation.done + (value,)
            if continuation.todo:
                return State(
                    continuation.todo[0],
                    continuation.saved_environment,
                    KApp(done, continuation.saved_environment, continuation.todo[1:], continuation.rest),
                )
            return self._apply(done, continuation.saved_environment, continuation.rest)
        raise InvalidStateError(f"unsupported continuation: {continuation!r}")

    def _apply(self, values: tuple[Any, ...], environment: Environment, rest: Continuation) -> State:
        operator, *arguments = values
        if isinstance(operator, Primitive):
            raise InterpreterError("primitive dispatch is implemented in Step 4")
        if isinstance(operator, Closure):
            if len(arguments) != len(operator.parameters):
                raise InterpreterError("function arity validation is implemented in Step 5")
            call_environment = operator.definition_environment.extend()
            for name, value in zip(operator.parameters, arguments):
                call_environment.define(name, value)
            return State(operator.body, call_environment, rest)
        raise InterpreterError(f"cannot apply value: {operator!r}")

    @staticmethod
    def _is_value(value: Any) -> bool:
        return isinstance(value, (int, bool, Primitive, Closure)) or value is None

