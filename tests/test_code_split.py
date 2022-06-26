import logging
import os
import sys
from pathlib import Path

import pytest
from fixtures.sample_data import code

from code_split import __version__
from code_split.code_split import main, run

__author__ = "Matthias Homann"
__copyright__ = "Matthias Homann"
__license__ = "GPL-3.0-or-later"


def test_main_version(capsys):
    """Basic test of main()"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    with pytest.raises(SystemExit) as pytest_exit:
        main(["--version"])
    captured = capsys.readouterr()
    assert __version__ in captured.out
    assert pytest_exit.type == SystemExit
    assert pytest_exit.value.code == 0


def test_run_version(capsys, monkeypatch):
    """CLI Tests of run()"""
    with pytest.raises(SystemExit) as pytest_exit:
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["code_split", "--version"])
            run()
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


def test_code_split_abs_path(tmp_path):
    """Test code_split with sample date using absolute path

    First the sample code is created in the folder "tmp_path/source/" from the sample_data.code
    and then the code_split is applies and the result compared with the sample_data snippets.

    Parameters
    ----------
    tmp_path : Path
        Temp path fixture
    """
    d = tmp_path / "source"
    d.mkdir()
    src = d / "test_code.py"
    src.write_text("".join(code.values()))
    assert src.read_text() == "".join(code.values())
    main(["-i", str(src), "-f", str(d)])
    for name, value in code.items():
        if not name.startswith("skip"):
            my_data = d / f"{name}.py"
            assert my_data.read_text() == value


def test_code_split_rel_path(tmp_path):
    """Test code_split with sample date using relative path

    First the sample code is created in the folder "tmp_path/source/" from the sample_data.code
    and then the code_split is applies and the result compared with the sample_data snippets.

    Parameters
    ----------
    tmp_path : Path
        Temp path fixture
    """
    # Change working directory to tmp_path
    os.chdir(tmp_path)
    assert str(tmp_path) == os.getcwd()
    d = tmp_path / "source"
    d.mkdir()
    src = d / "test_code.py"
    src.write_text("".join(code.values()))
    assert src.read_text() == "".join(code.values())
    main(["-i", "source/test_code.py", "-f", "source"])
    for name, value in code.items():
        if not name.startswith("skip"):
            my_data = d / f"{name}.py"
            assert my_data.read_text() == value


def test_code_split_no_path(tmp_path):
    """Test code_split with sample date without specifying the path

    First the sample code is created in the folder "tmp_path/source/" from the sample_data.code
    and then the code_split is applies and the result compared with the sample_data snippets.

    Parameters
    ----------
    tmp_path : Path
        Temp path fixture
    """
    # Change working directory to tmp_path/source
    d = tmp_path / "source"
    d.mkdir()
    os.chdir(tmp_path / "source")
    assert str(tmp_path / "source") == os.getcwd()
    src = d / "test_code.py"
    src.write_text("".join(code.values()))
    assert src.read_text() == "".join(code.values())
    main(["-i", "test_code.py"])
    for name, value in code.items():
        if not name.startswith("skip"):
            my_data = d / f"{name}.py"
            assert my_data.read_text() == value


def test_code_split_new_folder(tmp_path):
    """Test code_split with sample date using relative path

    First the sample code is created in the folder "tmp_path/source/" from the sample_data.code
    and then the code_split is applies and the result compared with the sample_data snippets.

    Parameters
    ----------
    tmp_path : Path
        Temp path fixture
    """
    # Change working directory to tmp_path/source
    d = tmp_path / "source"
    d.mkdir()
    os.chdir(tmp_path / "source")
    assert str(tmp_path / "source") == os.getcwd()
    src = d / "test_code.py"
    src.write_text("".join(code.values()))
    assert src.read_text() == "".join(code.values())
    main(["-i", "test_code.py", "-f", "new"])
    for name, value in code.items():
        if not name.startswith("skip"):
            my_data = d / "new" / f"{name}.py"
            assert my_data.read_text() == value


def test_code_split_file_not_found(caplog, tmp_path):
    """Test code_split with non-existing input file

    Parameters
    ----------
    caplog : fixture
    tmp_path : Path
        Temp path fixture
    """
    caplog.set_level(logging.ERROR)
    d = tmp_path / "source"
    d.mkdir()
    src = d / "test_code_not_found.py"
    main(["-i", str(src)])
    assert caplog.record_tuples == [
        (
            "code_split.code_split",
            logging.ERROR,
            f"Can't find input file {src}",
        )
    ]


def test_code_split_single_def(tmp_path):
    """Test code_split with sample date which has no main

    First the sample code is created in the folder "tmp_path/source/" from first function of sample_data.code
    and then the code_split is applies and the result compared with the sample_data snippets.

    Parameters
    ----------
    tmp_path : Path
        Temp path fixture
    """
    d = tmp_path / "source"
    d.mkdir()
    src = d / "test_code.py"
    result = ""
    for name, value in code.items():
        if value.startswith("def"):
            result = value
            src.write_text(value)
            break
    assert src.read_text() == result
    main(["-i", str(src), "-f", str(d)])
    for name, value in code.items():
        if name.startswith("def"):
            my_data = d / f"{name}.py"
            assert my_data.read_text() == value
            break
