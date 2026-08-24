"""Smoke tests for the initial project setup."""

from metta_cek import __version__
from metta_cek.config import SOURCE_EXTENSION


def test_package_metadata_is_available() -> None:
    """The package exposes a version and configurable source extension."""
    assert __version__ == "0.1.0"
    assert SOURCE_EXTENSION.startswith(".")

