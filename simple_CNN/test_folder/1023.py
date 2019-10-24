from random import shuffle
import numpy as np
a = (10,)
b = np.array([[1, 2, 0, 0],[4, 3, 2, 1]])
c = np.array([[1, 2, 0, 0],[4, 3, 2, 1]])

b_c = np.array([[1, 1, 1],[-1, -1, -1],[-1, -1, -1],[1, 1, 1]])


def relu_prime(z):
    return (z > 0) * np.ones(z.shape)

print (b * c)