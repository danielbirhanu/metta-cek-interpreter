"""Interpreter-specific exceptions."""


class InterpreterError(Exception):
    """Base class for errors raised by the interpreter."""


class ParseError(InterpreterError):
    """Raised when source text cannot be parsed."""


class ArityError(InterpreterError):
    """Raised when an operation receives the wrong number of arguments."""


class TypeMismatchError(InterpreterError):
    """Raised when an operation receives invalid value types."""


class DivisionByZeroError(InterpreterError):
    """Raised when division or modulo uses zero as its divisor."""


class UndefinedFunctionError(InterpreterError):
    """Raised when an application operator is not callable."""


class FunctionArityError(InterpreterError):
    """Raised when a closure receives the wrong number of arguments."""


class InvalidAssignmentError(InterpreterError):
    """Raised when `set` targets an undefined name."""
