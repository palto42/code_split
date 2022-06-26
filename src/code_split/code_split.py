"""
Split Python code files per class and function
"""

import argparse
import logging
import re
import sys
from pathlib import Path
from typing import List

from attr import s

from code_split import __version__

__author__ = "Matthias Homann"
__copyright__ = "Matthias Homann"
__license__ = "GPL-3.0-or-later"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from code_split.code_split import split_code`,
# when using this Python module as a library.


def split_code(src_code: str, folder: str) -> None:
    """Reads the source code file and writes a new output file
    per contained top level class and function.

    The functions accepts relative and absolute paths for the scr_code and folder.

    Parameters
    ----------
    src_code : str
        Name of the source code which will be used as input
    folder : str
        Output folder for the new files
    """
    src_path = Path(src_code)
    if not src_path.is_absolute():
        src_path = Path.cwd().joinpath(src_path)
        _logger.debug("Appended CWD to input file path")
    if folder:
        output = Path(folder)
        if not output.is_absolute():
            output = Path.cwd().joinpath(output)
    else:
        output = Path.cwd()

    if not output.is_dir():
        _logger.info("Create output folder %s", output)
        output.mkdir()
    out_file = None
    cache = ""
    blank_lines = ""
    pre_comment = ""
    try:
        with src_path.open(encoding="utf-8") as file:
            for line in file.readlines():
                if line.startswith("@"):
                    cache += line
                if line.startswith("def") or line.startswith("class"):
                    out_file_name = re.findall(r"^\w+\s+(\w+).*", line)[0] + ".py"
                    _logger.info("NEW output file: %s", out_file_name)
                    if out_file:
                        out_file.close()
                    out_file = output.joinpath(out_file_name).open("w", encoding="utf-8")
                    out_file.write(pre_comment)
                    pre_comment = ""
                    out_file.write(cache)
                    cache = ""
                    blank_lines = ""
                elif not line.startswith(" ") and len(line.strip()) and out_file:
                    # Class of function ended, either comments or main code
                    out_file.close()
                    out_file = None

                if not line.strip():
                    # cache blank lines
                    blank_lines += line
                    # ignore comments before functions is separated by a blank line
                    pre_comment = ""
                elif out_file:
                    if blank_lines:
                        out_file.write(blank_lines)
                        blank_lines = ""
                    _logger.debug("> %s", line.strip())
                    out_file.write(line)
                elif line.startswith("#"):
                    pre_comment += line
        if out_file:
            out_file.close()
    except FileNotFoundError:
        _logger.error("Can't find input file %s", src_code)


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args: List[str]) -> argparse.Namespace:
    """Parse command line parameters

    Parameters
    ----------
    args : List[str]
        command line parameters as list of strings
        (for example  ``["--help"]``).

    Returns
    -------
    argparse.Namespace
        command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Python code split tool")
    parser.add_argument(
        "--version",
        action="version",
        version="code_split {ver}".format(ver=__version__),
    )
    parser.add_argument("-i", "--input", required=True, type=str, help="Python code file to be split")
    parser.add_argument("-f", "--folder", type=str, help="Destination folder for the split code")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel: int) -> None:
    """Setup basic logging

    Parameters
    ----------
    loglevel : int
        minimum loglevel for emitting messages
    """
    log_format = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout, format=log_format, datefmt="%Y-%m-%d %H:%M:%S")


def main(args: List[str]) -> None:
    """Wrapper allowing :func:`split_code` to be called with string arguments in a CLI fashion

    Parameters
    ----------
    args : List[str])
        command line parameters as list of strings
        (for example  ``["-i", "my_source_code.py", "-f", "/path/to/output]``).
    """
    settings = parse_args(args=args)
    setup_logging(settings.loglevel)
    _logger.info(f"Split code file '{settings.input}' into folder '{settings.folder}'")
    split_code(settings.input, settings.folder)
    _logger.info("Script ends here")


def run() -> None:
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function is used as entry point for the console script by setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m code_split.code_split -i my_source_code.py
    #
    run()
