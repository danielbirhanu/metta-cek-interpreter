from pathlib import Path

import pytest

from metta_cek.cli import format_result, run_file


def test_run_file_executes_daniel_source(tmp_path: Path) -> None:
    source = tmp_path / "arithmetic.daniel"
    source.write_text("(+ 4 5)", encoding="utf-8")
    assert run_file(source) == 9


def test_run_file_rejects_wrong_extension(tmp_path: Path) -> None:
    source = tmp_path / "arithmetic.txt"
    source.write_text("(+ 4 5)", encoding="utf-8")
    with pytest.raises(ValueError, match=".daniel"):
        run_file(source)


def test_trace_file_contains_final_state(tmp_path: Path) -> None:
    source = tmp_path / "arithmetic.daniel"
    trace = tmp_path / "trace.log"
    source.write_text("(+ 4 5)", encoding="utf-8")
    assert run_file(source, trace_file=trace) == 9
    assert "FINAL STATE" in trace.read_text(encoding="utf-8")


def test_format_result_uses_language_booleans() -> None:
    assert format_result(True) == "true"
    assert format_result(False) == "false"
