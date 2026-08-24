"""Parser from tokens to the explicit language AST."""

from __future__ import annotations

from .ast import (
    Application, DefineExpression, Expression, FunctionDefinition,
    IfExpression, Literal, Program, SetExpression, Variable, WhileExpression,
)
from .errors import ParseError
from .lexer import Token, tokenize


class Parser:
    """Recursive-descent parser for parenthesized expressions."""

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.position = 0

    def parse_program(self) -> Program:
        expressions: list[Expression] = []
        while not self._check("EOF"):
            expressions.append(self._parse_expression())
        return Program(tuple(expressions))

    def _parse_expression(self) -> Expression:
        token = self._advance()
        if token.kind == "INTEGER":
            return Literal(int(token.text))
        if token.kind == "SYMBOL":
            if token.text in {"true", "false"}:
                return Literal(token.text == "true")
            return Variable(token.text)
        if token.kind == "LEFT_PAREN":
            return self._parse_list(token)
        if token.kind == "RIGHT_PAREN":
            self._error(token, "unexpected ')'")
        self._error(token, "expected an expression")
        raise AssertionError("unreachable")

    def _parse_list(self, opening: Token) -> Expression:
        if self._check("RIGHT_PAREN"):
            self._error(self._peek(), "empty application is not allowed")
        head = self._parse_expression()
        items: list[Expression] = []
        while not self._check("RIGHT_PAREN"):
            if self._check("EOF"):
                self._error(opening, "missing ')' to close expression")
            items.append(self._parse_expression())
        self._advance()
        if not isinstance(head, Variable):
            return Application(head, tuple(items))
        return self._special_form(head.name, items, opening)

    def _special_form(
        self,
        name: str,
        items: list[Expression],
        token: Token,
    ) -> Expression:
        if name == "if":
            self._require_arity(name, items, 3, token)
            return IfExpression(*items)
        if name == "while":
            self._require_arity(name, items, 2, token)
            return WhileExpression(items[0], items[1])
        if name == "set":
            self._require_arity(name, items, 2, token)
            target = self._require_name(items[0], name, token)
            return SetExpression(target, items[1])
        if name == "define":
            self._require_arity_at_least(name, items, 2, token)
            target = items[0]
            if isinstance(target, Variable):
                self._require_arity(name, items, 2, token)
                return DefineExpression(target.name, items[1])
            if isinstance(target, Application) and isinstance(target.operator, Variable):
                parameters = tuple(
                    self._require_name(argument, name, token)
                    for argument in target.arguments
                )
                body = self._single_body(items[1:], name, token)
                return FunctionDefinition(target.operator.name, parameters, body)
            self._error(token, "define target must be a name or function signature")
        return Application(Variable(name), tuple(items))

    def _single_body(
        self,
        items: list[Expression],
        name: str,
        token: Token,
    ) -> Expression:
        self._require_arity(name, items, 1, token)
        return items[0]

    @staticmethod
    def _require_name(
        expression: Expression,
        form: str,
        token: Token,
    ) -> str:
        if not isinstance(expression, Variable):
            raise ParseError(
                f"{form} requires a symbol at "
                f"line {token.line}, column {token.column}"
            )
        return expression.name

    @staticmethod
    def _require_arity(
        name: str,
        items: list[Expression],
        expected: int,
        token: Token,
    ) -> None:
        if len(items) != expected:
            raise ParseError(
                f"{name} expects {expected} argument(s) at "
                f"line {token.line}, column {token.column}"
            )

    @staticmethod
    def _require_arity_at_least(
        name: str,
        items: list[Expression],
        expected: int,
        token: Token,
    ) -> None:
        if len(items) < expected:
            raise ParseError(
                f"{name} expects at least {expected} argument(s) at "
                f"line {token.line}, column {token.column}"
            )

    def _advance(self) -> Token:
        token = self._peek()
        self.position += 1
        return token

    def _peek(self) -> Token:
        return self.tokens[self.position]

    def _check(self, kind: str) -> bool:
        return self._peek().kind == kind

    @staticmethod
    def _error(token: Token, message: str) -> None:
        raise ParseError(f"{message} at line {token.line}, column {token.column}")


def parse(source: str) -> Program:
    """Tokenize and parse a complete source program."""
    return Parser(tokenize(source)).parse_program()
