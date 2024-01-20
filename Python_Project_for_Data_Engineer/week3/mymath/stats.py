"""
MODULE DOCSTRING
This file is used to  give an idea about how to create a module
The module will:
- be named after the folder the file is in: mymath
- require an empty __init__.py file
import    
- collect all the files in the folder
- be immediately available by all python files at the same level as the folder mymath
"""

def mean(numbers):
    """
    This function returns the mean of the given list of numbers
    """
    return sum(numbers)/len(numbers)

def median(numbers):
    """
    This function returns median of the given list of numbers
    """
    numbers.sort()
   
    if len(numbers) % 2 == 0:
       median1 = numbers[len(numbers) // 2]
       median2 = numbers[len(numbers) // 2 - 1]
       mymedian = (median1 + median2) / 2
    else:
       mymedian = numbers[len(numbers) // 2]
    return mymedian