"""Command-line entry point for the interpreter."""

from __future__ import annotations

import argparse
import sys
from contextlib import nullcontext
from pathlib import Path

from .config import SOURCE_EXTENSION
from .errors import InterpreterError
from .logger import TransitionLogger, run_with_trace
from .machine import CEKMachine
from .parser import parse


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="danielInterpreter",
        description="Run a deliberately scoped MeTTa-like CEK program.",
    )
    parser.add_argument(
        "--run",
        metavar="FILE",
        help=f"run a {SOURCE_EXTENSION} source file",
    )
    parser.add_argument(
        "--trace",
        action="store_true",
        help="print CEK transition tracing to the terminal",
    )
    parser.add_argument(
        "--trace-file",
        metavar="FILE",
        help="write CEK transition tracing to a file",
    )
    return parser


def main() -> int:
    """Parse command-line arguments and report setup status."""
    parser = build_parser()
    arguments = parser.parse_args()
    if not arguments.run:
        parser.print_help()
        return 0
    try:
        result = run_file(
            Path(arguments.run),
            trace=arguments.trace,
            trace_file=Path(arguments.trace_file) if arguments.trace_file else None,
        )
    except (InterpreterError, OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"Result: {format_result(result)}")
    return 0


def run_file(
    path: Path,
    *,
    trace: bool = False,
    trace_file: Path | None = None,
) -> object:
    """Parse and execute one source file."""
    if path.suffix != SOURCE_EXTENSION:
        raise ValueError(
            f"source files must use the {SOURCE_EXTENSION} extension"
        )
    source = path.read_text(encoding="utf-8")
    machine = CEKMachine()
    state = machine.initial_state(parse(source))
    if trace_file is not None:
        stream_context = trace_file.open("w", encoding="utf-8")
    elif trace:
        stream_context = nullcontext(sys.stdout)
    else:
        stream_context = nullcontext(None)
    with stream_context as stream:
        if stream is not None:
            state = run_with_trace(machine, state, TransitionLogger(stream))
        else:
            while not machine.is_final(state):
                state = machine.step(state)
    return state.control


def format_result(value: object) -> str:
    """Format a runtime value using source-language spelling."""
    if value is True:
        return "true"
    if value is False:
        return "false"
    return str(value)
