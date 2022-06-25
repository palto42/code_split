"""
Split Python code files for class and function
"""

import argparse
import logging
import os
import re
import sys

from attr import s

from code_split import __version__

__author__ = "Matthias Homann"
__copyright__ = "Matthias Homann"
__license__ = "GPL-3.0-or-later"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from code_split.skeleton import fib`,
# when using this Python module as a library.


def split_code(src_code: str, folder: str) -> None:
    if not src_code.startswith("/"):
        src_code = os.path.join(os.getcwd(), src_code)
        _logger.debug("Appended CWD to input file path")
    if not folder:
        folder = os.getcwd()
    elif not folder.startswith("/"):
        folder = os.path.join(os.getcwd(), folder)
    if not os.path.isdir(folder):
        _logger.info("Create output folder %s", folder)
        os.makedirs(folder)
    file_header = ""
    out_file = None
    try:
        with open(src_code, "r", encoding="utf-8") as file:
            for line in file.readlines():

                if line.startswith("def") or line.startswith("class"):
                    out_file_name = re.findall(r"^\w+\s+(\w+).*", line)[0] + ".py"
                    _logger.info("NEW output file: %s", out_file_name)
                    if out_file:
                        out_file.close()
                    out_file = open(os.path.join(folder, out_file_name), "w", encoding="utf-8")
                elif not line.startswith(" ") and len(line.strip()) and out_file:
                    # Class of function ended, either comments or main code
                    out_file.close()
                    out_file = None
                if out_file:
                    _logger.debug("> %s", line.strip())
                    out_file.write(line)
        if out_file:
            out_file.close()
    except FileNotFoundError:
        _logger.error("Can't find input file %s", src_code)


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Python code split tool")
    parser.add_argument(
        "--version",
        action="version",
        version="code_split {ver}".format(ver=__version__),
    )
    parser.add_argument("-i", "--input", required=True, type=str, help="Python code file to be split")
    parser.add_argument("-f", "--folder", type=str, help="Destination folder for the splitted code")
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


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.info(f"Split code file '{args.input}' into folder '{args.folder}'")
    split_code(args.input, args.folder)
    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
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
    #     python -m code_split.skeleton 42
    #
    run()
