# This are notes for the Coursera course: Algebra for Machine Learning

https://www.coursera.org/learn/machine-learning-linear-algebra/

## Week 1 - Basic linear algebra intro and Numpy Lab
## Week 2 - Basic Linear algebra operations with matrices (in numpy as well)
## Week 3 - Matrices
Neural networks work with matrices
E.g. <P>
Let's create a table for some emails and count how many times the words lottery
and win show up in the email

| Spam Mail?  | Lottery #   | Win#     | Score  | 
| ----------- | ----------- | -------- | ------ |
| Yes         | 1           |  1       |    2   |
| Yes         | 2           |  1       |    3   |
| No          | 0           |  0       |    0   |
| Yes         | 0           |  2       |    2   |
| No          | 0           |  1       |    1   |
| No          | 1           |  0       |    1   |
| Yes         | 2           |  2       |    4   |
| Yes         | 2           |  0       |    2   |
| Yes         | 1           |  2       |    3   |

Let's also give a value to each world and count what value does each email gets
e.g.
Lottery 1, win 1 - Threshold = 1.5
classifyies eveything (in the table) correctly

This above is an example of natural language processing
also known as simple calssifier and neural network with one layer
if you graph the points above in 2 dimensions (one for lottery and one for win)
you get a scatter plot where you can draw a line that separates the space
perfectly:
``` 1*win + 1*Lottery > 1.5 (for spam)
where the two 1 are the coefficient for the score and 1.5 is the threshold

We can also consider the datset as a matrix of values and the model as a vector (transposed) then apply the check with the threshold
| 1  1 |                           | 2 |
| 2  1 |                           | 3 |  
| 0  0 |                           | 0 |  
| 0  2 |    (vector for the model) | 2 | 
| 0  1 |    X     | 1 |        =   | 1 |  > 1.5 ?
| 1  0 |          | 1 |            | 1 |
| 2  2 |                           | 4 |
| 2  0 |                           | 2 |
| 1  2 |                           | 3 |

Note  that I can also include the threshold (called the bias) in the equation
1*win + 1*Lottery > 1.5 == 1*win + 1*Lottery - 1.5 > 0 and rewrit the matrices
| 1  1  1 |                              | 0.5  |
| 2  1  1 |                              | 1.5  |  
| 0  0  1 |                              | -1.5 |  
| 0  2  1 |    (vector for the model)    | 0.5  | 
| 0  1  1 |    X     | 1    |        =   | -0.5 | 
| 1  0  1 |          | 1    |            | -0.5 | 
| 2  2  1 |          | -1.5 |            | 2.5  |
| 2  0  1 |       (and bias)             | 0.5  |
| 1  2  1 |                              | 1.5  |

```   
Note that you can also model logical operator as neural networks (single perceptron)
See Lab
<P>

| AND |  X | Y  |
|-----|----|----|   
| No  |  0 | 0  |
| No  |  1 | 0  |
| No  |  0 | 1  |
| Yes |  1 | 1  |

Model vector = (1,1) and threshold 1.5