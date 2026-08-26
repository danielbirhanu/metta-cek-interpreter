from pathlib import Path

from metta_cek.cli import run_file

EXAMPLES = Path(__file__).parents[1] / "examples"


def test_progressive_examples() -> None:
    expected = {
        "01_arithmetic.daniel": 3,
        "02_variables.daniel": 30,
        "03_conditional.daniel": 20,
        "04_function_scope.daniel": 15,
        "05_while_complex.daniel": 15,
    }
    for filename, result in expected.items():
        assert run_file(EXAMPLES / filename) == result

