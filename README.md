# code_split

Split Python code files per class and function.

## Description

This script will split a Python code file into separate files per main class or function.
The new files will be named as per the class or function it contains.
The newly created files will contain class/function decorators as well as comments directly before the class or function (without empty lines).

Intermediate comments and the main code will be ignored.

## Usage

The tool requires at least the source code file name, optionally an output path can be specified.
The source file name and the output folder can be relative to the current working directory or with absolute path.

```text
usage: code_split [-h] [--version] -i INPUT [-f FOLDER] [-v] [-vv]

Python code split tool

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -i INPUT, --input INPUT
                        Python code file to be split
  -f FOLDER, --folder FOLDER
                        Destination folder for the split code
  -v, --verbose         set loglevel to INFO
  -vv, --very-verbose   set loglevel to DEBUG
```

### Example

Below shows the source files and the new files created from it by the command `code_split -i source_code.py`:

`source_code.py`

```python
"""Source header and imports will be ignored"""
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
# This is the first exported class
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

## Run as docker image

### Build image

Note: docker tags must not contain the `+` char, that's why it is replaced by `-`in blow command.

```sh
# from project base path
VERSION=$(python -m setuptools_scm) docker build --build-arg VERSION="$VERSION" --rm --pull -f Dockerfile -t "codesplit:latest" -t "codesplit:${VERSION//[+]/-}" .
```

The latest docker image can also be crated with `tox -e docker`.

After building the image, it is exported as `tar` file to the `./dist` folder.

Install the image from `tar` with the command `gunzip -c <file.tar.gz> | docker load`

### Execute script

`podman` runs rootless as the current user.

```sh
podman run --rm  -v $(pwd)/tmp:/src code_split:latest code_split -i /src/sample_code.py -f /src/split
```

### podman rootless

If `podman` is executed with `sudo -u my_user`, the user account must be configured with `loginctl enable-linger my_user` configured.
For more information about this command see [Configure Systemd to Enable User Processes to Continue to Run After Logout](https://docs.oracle.com/en/operating-systems/oracle-linux/8/obe-systemd-linger/)

At least for the build process the `subuid`and `subgid` must be configured for the user,
see [podman > set subuid and subgid](https://wiki.archlinux.org/title/Podman#Set_subuid_and_subgid).

#### Docker

Note: The `-u` option is used in order to run the script inside docker as current user instead of the default docker user.

```sh
docker run --rm -u $(id -u ${USER}):$(id -g ${USER}) -v $(pwd)/tmp:/src codesplit:latest code_split -i /src/sample_code.py -f /src/split
```

---

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.2.2. For details and usage
information on PyScaffold see <https://pyscaffold.org/>.
