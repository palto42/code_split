"""This is a sample code to they `code_split`"""

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# First trying a dataclass
@dataclass
class MyData:
    """Sample dataclass"""

    name: str
    age: int

    def birthday(self):
        self.age += 1


# Now with a random class
class SampleClass:
    """Sample class"""

    def __init__(self, value: str) -> None:
        self.value = value

    def output(self) -> str:
        """Output sample data

        Returns
        -------
        str
            Formatted data
        """
        return f"Value is: {self.value}"


# Interim comments
# will be ignored


def my_function(data: MyData) -> str:
    dummy = SampleClass(data.name)
    # Sample comment
    return f"{dummy.output()}, age: {data.age}"


def second_function(
    data: MyData
) -> None:
    """Print the data

    Parameters
    ----------
    data : MyData
        Dummy data
    """
    print(">>", data)

    # Comments in function

    # Can have blank lines


# Main code starts here
print("This is the main code")
test_data = MyData(name="Joe", age=42)
print(my_function(test_data))
second_function(test_data)

# End of code
