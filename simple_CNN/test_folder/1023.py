from random import shuffle
import numpy as np
a = np.array([10,20])
a_prime = np.array([10,20,10,20,30])
b = np.array([
    [[1, 2, 0, 0],[4, 3, 2, 1]],
    [[1, 2, 0, 0],[4, 3, 2, 1]]
              ]) # (2, 2, 4)
c = np.array([[1, 2, 0, 0],[4, 3, 2, 1]])

b_c = np.array([[1], [1], [2], [2]]) # (4, 1)

def change(x):
    x = np.resize(x, (1, 2*2*4))
    return x

def relu_prime(z):
    return (z > 0) * np.ones(z.shape)


change(b)
print (b.shape)