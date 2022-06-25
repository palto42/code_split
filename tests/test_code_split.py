import pytest

from code_split import __version__
from code_split.code_split import main

__author__ = "Matthias Homann"
__copyright__ = "Matthias Homann"
__license__ = "GPL-3.0-or-later"


def test_main_version(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    with pytest.raises(SystemExit) as pytest_exit:
        main(["--version"])
    captured = capsys.readouterr()
    assert __version__ in captured.out
    assert pytest_exit.type == SystemExit
    assert pytest_exit.value.code == 0


def test_main_input_missing(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    with pytest.raises(SystemExit) as pytest_exit:
        main([])
    captured = capsys.readouterr()
    assert "required: -i/--input" in captured.err
    assert pytest_exit.type == SystemExit
    assert pytest_exit.value.code == 2
