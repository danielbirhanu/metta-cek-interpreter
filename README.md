# Daniel CEK Interpreter

This project implements a deliberately scoped MeTTa-like language rather than the full MeTTa language. Its purpose is to demonstrate how a CEK abstract machine makes evaluation state explicit and inspectable.

## CEK in one sentence

Every machine state is `State(Control, Environment, Continuation)`:

- `Control (C)`: what is being evaluated now;
- `Environment (E)`: what names mean;
- `Continuation (K)`: what remains to be done afterward.

```text
source → lexer → parser → AST → CEK states → final value
```

## Language

The syntax is parenthesized, prefix/S-expression syntax:

```lisp
(+ 1 2)
(define x 10)
(if (< x 20) (* x 2) 0)
(define (double x) (* x 2))
(double 5)
(while (< x 10) (set x (+ x 1)))
```

The implementation supports integer and boolean literals, variables, applications, `if`, `define`, named functions, `set`, `begin`, and `while`.

Primitives are `+`, `-`, `*`, `/`, `%`, `<`, `>`, `<=`, `>=`, `=`, `!=`, `and`, `or`, and `not`. Arithmetic is integer-based; division uses floor division.

## CEK design

`step(state)` performs exactly one transition. The driver repeats it until a value with `KRet` is reached. Important continuation frames are:

- `KRet`: completed computation;
- `KApp`: completed application values, saved environment, pending expressions, and rest continuation;
- `KIf`: condition result and the two branches;
- `KDefine` and `KSet`: pending environment updates;
- `KSequence`: remaining top-level or `begin` expressions;
- `KWhileCondition` and `KWhileBody`: explicit loop control.

Applications evaluate operator and arguments left-to-right. Primitive calls invoke the centralized `delta(operator, arguments)` only after all values are ready. `if` evaluates only the selected branch.

## Scope

Functions are closures containing parameters, body, and definition environment. Calls create a child of that definition environment, so the language uses lexical scoping. The saved environment in `KApp` is for resuming application evaluation and is not itself a dynamic-scoping rule.

## While and mutation

`set` updates the nearest existing binding. A `while` condition is evaluated; a true condition evaluates the body and then re-enters the condition through `KWhileBody`; a false condition returns `false`. No hidden Python loop evaluates the language loop in one step.

## Running the interpreter

The configured command is `danielInterpreter` and source files use `.daniel`.

```bash
uv sync
uv run danielInterpreter --run examples/01_arithmetic.daniel
uv run danielInterpreter --run examples/05_while_complex.daniel
```

Enable a terminal trace:

```bash
uv run danielInterpreter --run examples/05_while_complex.daniel --trace
```

Write the trace to a file:

```bash
uv run danielInterpreter --run examples/05_while_complex.daniel --trace-file trace.log
```

The extension is configured in `src/metta_cek/config.py`:

```python
SOURCE_EXTENSION = ".daniel"
```

## Examples

| File | Demonstrates | Result |
| --- | --- | ---: |
| `01_arithmetic.daniel` | primitive addition | `3` |
| `02_variables.daniel` | definitions and lookup | `30` |
| `03_conditional.daniel` | comparison and `if` | `20` |
| `04_function_scope.daniel` | closure and lexical scope | `15` |
| `05_while_complex.daniel` | mutation, `begin`, and while | `15` |

## Tests and quality checks

```bash
uv run pytest
uv run python -m compileall src tests
```

The tests cover lexing, parsing, delta, CEK transitions, functions, lexical scope, while, logging, CLI behavior, and all examples.

## Error handling

The interpreter reports custom errors including `ParseError`, undefined-variable errors, arity errors, type errors, division-by-zero errors, invalid assignment errors, and invalid machine states.

## Known limitations

- This is not full MeTTa compatibility.
- Values are currently integers, booleans, primitives, and closures.
- Function definitions currently have one body expression; `begin` provides explicit sequencing.
- There are no strings, lists, pattern matching, atoms, modules, or macros.
- `/` is integer floor division.