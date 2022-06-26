# code_split

Split Python code files per class and function.

## Description

This script will split a Python code file into separate files per main class or function.
The new files will be named as per the class or function it contains.
The newly created files will contain class/function decorators as well as comments directly before the class or function (without empty lines).

Intermediate comments and the main code will be ignored.

### Example

Source code:

```python
"""Source header and imports will be ignoerd"""
import logging
from dataclasses import dataclass

logging.getLogger(__name__)

# This is the first exported class
@dataclass
class MyData:
    """Sample dataclass"""

    name: str
    age: int

    def birthday(self):
        self.age += 1


# Intermediate comments
# will be ignored

def my_function(data: MyData) -> str:
    dummy = SampleClass(data.name)
    # Sample comment
    return f"{dummy.output()}, age: {data.age}"

# Main code starts here
print("End of the example source code.")

```

The resulting files will be:

`MyData.py`

```python
# First trying a dataclass
@dataclass
class MyData:
    """Sample dataclass"""

    name: str
    age: int

    def birthday(self):
        self.age += 1

```

`my_function.py`

```python
def my_function(data: MyData) -> str:
    dummy = SampleClass(data.name)
    # Sample comment
    return f"{dummy.output()}, age: {data.age}"

```

## Usage

The tool requires at least the source code file name, optionally an output path can be specified.
The source file name and the output folder can be relative to the current working directory or with absolute path.

```txt
usage: code_split [-h] [--version] -i INPUT [-f FOLDER] [-v] [-vv]

Python code split tool

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -i INPUT, --input INPUT
                        Python code file to be split
  -f FOLDER, --folder FOLDER
                        Destination folder for the splitted code
  -v, --verbose         set loglevel to INFO
  -vv, --very-verbose   set loglevel to DEBUG
```

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.2.2. For details and usage
information on PyScaffold see https://pyscaffold.org/.
