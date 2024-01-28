"""
MODULE DOCSTRING
This file is used to  give an idea about how to create a module
The module will:
- be named after the folder the file is in: mymath
- require an empty __init__.py file
   - you can add requirements to the init file by specifing what needs to be imported
- collect all the files in the folder
- be immediately available by all python files at the same level as the folder mymath
"""

def square(number):
    """
    This function returns the square of a given number
    """
    return number ** 2

def double(number):
    """
    This function returns twice the value of a given number
    """
    return number * 2

def add(a, b):
    """
    This function returns the sum of given numbers
    """
    return a + b