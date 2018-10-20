import numpy as np

a = np.array([
    [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]],

    [[3, 2, 3],
     [4, 5, 6],
     [7, 8, 9]],
])

b = np.array([[1], [2], [3]])
print(np.dot(a, b))
print(np.transpose(a, axes=(0,2,1)))