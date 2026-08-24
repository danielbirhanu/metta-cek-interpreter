"""Command-line entry point for the interpreter."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="danielInterpreter",
        description="Run a deliberately scoped MeTTa-like CEK program.",
    )
    parser.add_argument(
        "--run",
        metavar="FILE",
        help="source file to run (execution is added in a later step)",
    )
    parser.add_argument(
        "--trace",
        action="store_true",
        help="enable CEK transition tracing (added in a later step)",
    )
    return parser


def main() -> int:
    """Parse command-line arguments and report setup status."""
    parser = build_parser()
    arguments = parser.parse_args()
    if arguments.run is None:
        parser.print_help()
        return 0
    parser.error("program execution is implemented in a later step")
    return 2
