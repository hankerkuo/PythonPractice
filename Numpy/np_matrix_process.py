import numpy as np
lst = []
a = np.array([
    [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]],

    [[3, 2, 3],
     [4, 5, 6],
     [7, 8, 9]],
])

b = np.array([
             [[1, 0, 1],
              [0, 1, 0],
              [1, 0, 1]],

             [[1, 1, 1],
              [1, 1, 1],
              [1, 1, 1]],

             [[0, 1, 0],
              [1, 0, 1],
              [0, 1, 0]]
             ])

c = np.array([[1, 0, 1],
              [0, 1, 0],
              [1, 0, 1]])
# c = a *b
print(np.dot(a, c))
# print(np.sum(c, axis=(1, 2)))
# print(np.transpose(a, axes=(0,2,1)))