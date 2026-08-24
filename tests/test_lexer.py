from metta_cek.lexer import tokenize


def test_tokenize_tracks_locations_and_literals() -> None:
    tokens = tokenize("(+ 12 true)\n")
    assert [token.kind for token in tokens] == [
        "LEFT_PAREN",
        "SYMBOL",
        "INTEGER",
        "SYMBOL",
        "RIGHT_PAREN",
        "EOF",
    ]
    assert tokens[2].text == "12"
    assert tokens[2].line == 1
    assert tokens[-1].line == 2
