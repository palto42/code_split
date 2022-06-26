"""Sample data to construct the source code"""
import os
from typing import Dict

import pytest

code = {
    "skip_header": """\"\"\"This is a sample code to they `code_split`\"\"\"

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

""",
    "MyData": """# First trying a dataclass
@dataclass
class MyData:
    \"\"\"Sample dataclass\"\"\"

    name: str
    age: int

    def birthday(self):
        self.age += 1
""",
    "skip_blank_1": "\n\n",
    "SampleClass": """# Now with a random class
class SampleClass:
    \"\"\"Sample class\"\"\"

    def __init__(self, value: str) -> None:
        self.value = value

    def output(self) -> str:
        \"\"\"Output sample data

        Returns
        -------
        str
            Formatted data
        \"\"\"
        return f"Value is: {self.value}"
""",
    "skip_blank_2": "\n\n",
    "skip_comment_1": """# Interim comments
# will be ignored
""",
    "skip_blank_3": "\n\n",
    "my_function": """def my_function(data: MyData) -> str:
    dummy = SampleClass(data.name)
    # Sample comment
    return f"{dummy.output()}, age: {data.age}"
""",
    "skip_blank_4": "\n\n",
    "second_function": """def second_function(data: MyData) -> None:
    \"\"\"Print the data

    Parameters
    ----------
    data : MyData
        Dummy data
    \"\"\"
    print(">>", data)

    # Comments in function

    # Can have blank lines
""",
    "skip_blank_5": "\n\n",
    "skip_main": """# Main code starts here
print("This is the main code")
test_data = MyData(name="Joe", age=42)
print(my_function(test_data))
second_function(test_data)

# End of code
""",
}


@pytest.fixture
def get_code_file():
    return "".join(code)


def update_sample(snippets: Dict[str, str]) -> None:
    sample_code = os.path.join(os.path.dirname(__file__), "sample_code.py")
    with open(sample_code, "w", encoding="utf-8") as file:
        file.write("".join(snippets.values()))


# MAIN
update_sample(code)
print("Updated sample code file:")
print("----------------------------------------")
print("".join(code.values()))
print("----------------------------------------")
