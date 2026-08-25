from io import StringIO

from metta_cek.logger import TransitionLogger, run_with_trace
from metta_cek.machine import CEKMachine
from metta_cek.parser import parse


def test_logger_records_transitions_and_final_state() -> None:
    stream = StringIO()
    logger = TransitionLogger(stream)
    final = run_with_trace(
        CEKMachine(),
        CEKMachine().initial_state(parse("(+ 1 2)")),
        logger,
    )
    output = stream.getvalue()
    assert final.control == 3
    assert "STEP 0" in output
    assert "APPLICATION_START" in output
    assert "FINAL STATE" in output
    assert logger.step_number > 0

