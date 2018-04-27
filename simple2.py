import numpy as np

p = np.array([[0, 1, -1], [0, 1, 1], [1, 0, 0]])
a = np.array([[1, 2, 0], [2, 1, 7], [5, 0, -3]])
p_inverse = np.linalg.inv(p)

print(np.linalg.eig(a))
print(np.dot(np.dot(p_inverse, a), p))