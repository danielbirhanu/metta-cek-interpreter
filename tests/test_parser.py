from metta_cek.ast import (
    Application,
    DefineExpression,
    FunctionDefinition,
    IfExpression,
    Literal,
    Program,
    SetExpression,
    Variable,
    WhileExpression,
)
from metta_cek.parser import parse


def test_parse_basic_expressions() -> None:
    program = parse("(+ 1 x)")
    assert program == Program(
        (Application(Variable("+"), (Literal(1), Variable("x"))),)
    )


def test_parse_special_forms() -> None:
    program = parse(
        "(define x 10) "
        "(if true x 0) "
        "(set x 2) "
        "(while (< x 3) (set x (+ x 1)))"
    )
    assert isinstance(program.expressions[0], DefineExpression)
    assert isinstance(program.expressions[1], IfExpression)
    assert isinstance(program.expressions[2], SetExpression)
    assert isinstance(program.expressions[3], WhileExpression)


def test_parse_function_definition() -> None:
    program = parse("(define (double x) (* x 2))")
    assert program == Program(
        (
            FunctionDefinition(
                "double",
                ("x",),
                Application(Variable("*"), (Variable("x"), Literal(2))),
            ),
        )
    )
