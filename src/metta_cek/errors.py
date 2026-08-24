"""Interpreter-specific exceptions."""


class InterpreterError(Exception):
    """Base class for errors raised by the interpreter."""


class ParseError(InterpreterError):
    """Raised when source text cannot be parsed."""

