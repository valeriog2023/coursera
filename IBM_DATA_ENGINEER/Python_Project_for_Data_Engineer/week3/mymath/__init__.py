"""
MODULE DOCSTRING
This file is used to  give an idea about how to create a module
The module will:
- be named after the folder the file is in: mymath
- require an empty __init__.py file
   - you can add requirements to the init file by specifing what needs to be imported
- collect all the files in the folder
- be immediately available by all python files at the same level as the folder mymath

You can verify the package by opening a python terminal at the level of the folder and 
trying to import the module, e.g.

(base) vale6811@tc2:~/Desktop/Coursera/Python_Project_for_Data_Engineer/week3$ python
Python 3.8.3 (default, Jul  2 2020, 16:21:59) 
[GCC 7.3.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import mymath
>>> mymath.basic.add(3,4)
7
>>> mymath.stats.mean([3,4,5])
4.0
"""
from . import basic
from . import stats