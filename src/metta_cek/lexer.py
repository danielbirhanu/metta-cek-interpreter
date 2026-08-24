"""Tokenizer for MeTTa-like S-expression source."""

from __future__ import annotations

from dataclasses import dataclass

from .errors import ParseError


@dataclass(frozen=True)
class Token:
    """A token with its source location."""

    kind: str
    text: str
    line: int
    column: int


def tokenize(source: str) -> list[Token]:
    """Convert source text into tokens terminated by EOF."""
    tokens: list[Token] = []
    index = 0
    line = 1
    column = 1
    while index < len(source):
        character = source[index]
        if character.isspace():
            if character == "\n":
                line += 1
                column = 1
            else:
                column += 1
            index += 1
            continue
        start_line, start_column = line, column
        if character == "(":
            tokens.append(Token("LEFT_PAREN", character, line, column))
            index += 1
            column += 1
            continue
        if character == ")":
            tokens.append(Token("RIGHT_PAREN", character, line, column))
            index += 1
            column += 1
            continue
        if character.isdigit() or (
            character == "-"
            and index + 1 < len(source)
            and source[index + 1].isdigit()
        ):
            end = index + 1
            while end < len(source) and source[end].isdigit():
                end += 1
            tokens.append(Token("INTEGER", source[index:end], start_line, start_column))
            column += end - index
            index = end
            continue
        if character.isalpha() or character in "_+-*/%<>=!":
            end = index + 1
            while end < len(source) and (
                source[end].isalnum() or source[end] in "_+-*/%<>=!?"
            ):
                end += 1
            tokens.append(Token("SYMBOL", source[index:end], start_line, start_column))
            column += end - index
            index = end
            continue
        raise ParseError(
            f"unexpected character {character!r} at line {line}, column {column}"
        )
    tokens.append(Token("EOF", "", line, column))
    return tokens

