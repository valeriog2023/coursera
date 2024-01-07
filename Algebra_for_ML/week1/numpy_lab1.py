import numpy as np

one_dimensional_arr = np.array([10, 12, 13, 11])
print(one_dimensional_arr)

# Create an array with 3 integers, starting from the default integer 0.
b = np.arange(3)
print(b)

# Create an array that starts from the integer 1, ends at 20, incremented by 3.
c = np.arange(1, 20, 3)
print(c)

# if you wanted to create an array with five evenly spaced values in the interval from 0 to 100? 
# First paremeter is the starting number, in this case 0, 
# the final number 100 and the number of elements in the array, in this case, 5. 
# you can also specify the data type of the resulting values (see second example)
lin_spaced_arr = np.linspace(0, 100, 5)
print(lin_spaced_arr)
#
# using arange andlinspace with data type = int. float or char
lin_spaced_arr_int = np.linspace(0, 100, 5, dtype=int)
c_int = np.arange(1, 20, 3, dtype=int)
b_float = np.arange(3, dtype=float)
print(lin_spaced_arr_int)
print(c_int)
print(b_float)

char_arr = np.array(['Welcome to Math for ML!'])
print(char_arr)       # this prints ['Welcome to Math for ML!']
print(char_arr.dtype) # Prints the data type of the array which is <U23
#Note <U23 means that:
# type is U: unicode
# lenght is 23
# architecture is little endian: <
# see https://numpy.org/doc/stable/user/basics.types.html
#
#
############################################ 
#  numpy special ways to create arrays
#
# Return a new array of shape 3, filled with ones. 
ones_arr = np.ones(3)
print(ones_arr)  # [1. 1. 1.]

# Return a new array of shape 3, filled with zeroes.
zeros_arr = np.zeros(3)
print(zeros_arr) # [0. 0. 0.]

# Return a new array of shape 3, without initializing entries.
empt_arr = np.empty(3)
print(empt_arr) # [values are random because the vector is not initialized it depends on the previous content of the memory location]
 
# Return a new array of shape 3 with random numbers between 0 and 1.
rand_arr = np.random.rand(3)
print(rand_arr)   # random values, e.g. [0.00561904 0.64135794 0.804284  ]
#
#
#
############################################ 
#  MULTI DIMENSIONAL ARRAYS
#
# Create a 2 dimensional array (2-D)
two_dim_arr = np.array([[1,2,3], [4,5,6]])
print(two_dim_arr)
# [[1 2 3]
# [4 5 6]]
#
# you can also reshape an existing vecotr
# 1-D array 
one_dim_arr = np.array([1, 2, 3, 4, 5, 6])
#
# Multidimensional array using reshape()
multi_dim_arr = np.reshape(
                one_dim_arr,  # the array to be reshaped
                (2,3)         # dimensions of the new array
               )
# Print the new 2-D array with two rows and three columns
print(multi_dim_arr)
# [[1 2 3]
#  [4 5 6]]

# Dimension of the 2-D array multi_dim_arr
multi_dim_arr.ndim  #  this returns 2

# Shape of the 2-D array multi_dim_arr
# Returns shape of 2 rows and 3 columns
multi_dim_arr.shape  # this returns the tuple (2, 3)

# Size of the array multi_dim_arr
# Returns total number of elements
multi_dim_arr.size # this returns 6

#
#
############################################ 
#  MATH OPERATIONS for arrays
#
arr_1 = np.array([2, 4, 6])
arr_2 = np.array([1, 3, 5])

# Adding two 1-D arrays
addition = arr_1 + arr_2
print(addition)
# this reutrns [ 3  7 11]

# Subtracting two 1-D arrays
subtraction = arr_1 - arr_2
print(subtraction)
# this returns [ 1  1 1]

# Multiplying two 1-D arrays elementwise
multiplication = arr_1 * arr_2
print(multiplication)
# this returns [ 2  12 30]

# Multiply all elements by a scalar (also called broadcasting)
vector = np.array([1, 2])
vector * 1.6
# this gives as result the array array([1.6, 3.2])

#
#
############################################ 
#  INDEX AND SLICING
#
# indexing is the same as normal lists..
# Indexing on a 2-D array
two_dim = np.array(([1, 2, 3],
          [4, 5, 6], 
          [7, 8, 9]))

# Select element number 8 from the 2-D array using indices i, j.
print(two_dim[2][1])

## SLICING
# for one dimension it works like for a list
# for more dimensions we have
# Slice the two_dim array to get the first two rows
sliced_arr_1 = two_dim[0:2]
sliced_arr_1
# returns array([[1, 2, 3],
#                [4, 5, 6]])
# Similarily, slice the two_dim array to get the last two rows
sliced_two_dim_rows = two_dim[1:3]
print(sliced_two_dim_rows)
# returns array([[4, 5, 6],
#                [7, 8, 9]])
#
sliced_two_dim_cols = two_dim[:,1]  # this is one dimension array
print(sliced_two_dim_cols)
sliced_two_dim_cols = two_dim[:,1:] # this returns 2 dimension
print(sliced_two_dim_cols)
sliced_two_dim_cols = two_dim[:,:1] # this returns 2 dimension
print(sliced_two_dim_cols)
# first result
# [2 5 8]
# second result
# [[2 3]
#  [5 6]
#  [8 9]]
# third result
# [[1]
#  [4]
#  [7]]]
#
##################################
# - Stacking
#################################
# Stacking is a feature of NumPy that leads to increased customization of arrays. 
# It means to join two or more arrays, either horizontally or vertically, 
# meaning that it is done along a new axis.
#
# np.vstack() - stacks vertically
# np.hstack() - stacks horizontally
# np.hsplit() - splits an array into several smaller arrays
a1 = np.array([[1,1], 
               [2,2]])
a2 = np.array([[3,3],
              [4,4]])
#
# examples
# Stack the arrays vertically
vert_stack = np.vstack((a1, a2))
print(vert_stack)
# returns 
# [[1 1]
#  [2 2]
#  [3 3]
#  [4 4]]

# Stack the arrays horizontally
horz_stack = np.hstack((a1, a2))
print(horz_stack)
# returns
# [[1 1 3 3]
#  [2 2 4 4]]