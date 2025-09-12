# examples/example_good_code.py

"""
This file demonstrates well-formatted Python code that follows PEP 8 standards.
Use this with PyLintPro to see clean code analysis.
"""

from typing import List, Optional


def calculate_sum(x: int, y: int) -> int:
    """Calculate the sum of two integers."""
    result = x + y
    return result


class MyClass:
    """A well-formatted example class."""
    
    def __init__(self, name: str) -> None:
        """Initialize the class with a name."""
        self.name = name
    
    def get_name(self) -> str:
        """Return the name."""
        return self.name


def process_list(items: List[str]) -> Optional[str]:
    """
    Process a list of items and return the first one if available.
    
    Args:
        items: List of string items to process
        
    Returns:
        First item if list is not empty, None otherwise
    """
    if not items:
        return None
    
    return items[0]


def main() -> None:
    """Main function demonstrating good code structure."""
    calculator_result = calculate_sum(10, 20)
    print(f"Result: {calculator_result}")
    
    my_instance = MyClass("Example")
    print(f"Name: {my_instance.get_name()}")
    
    sample_list = ["apple", "banana", "cherry"]
    first_item = process_list(sample_list)
    print(f"First item: {first_item}")


if __name__ == "__main__":
    main()