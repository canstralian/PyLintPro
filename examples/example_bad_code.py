# examples/example_bad_code.py

# This file contains examples of Python code with various PEP 8 violations
# Use this with PyLintPro to see how it detects and suggests improvements

def bad_function( x,y ):
    result=x+y    # Missing spaces around operators
    return result

class my_class:
    def __init__(self):
        pass

# Long line that exceeds the recommended 79 character limit and should be split into multiple lines
def very_long_function_name_that_exceeds_the_line_limit(parameter_one, parameter_two, parameter_three):
    return parameter_one + parameter_two + parameter_three

# Missing blank lines
def function_one():
    return 1
def function_two():
    return 2

# Trailing whitespace and other issues
def function_with_issues():   
    x=1
    y=2   
    return x+y
    

# Import issues
import os,sys
from typing import *