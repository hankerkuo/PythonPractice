import numpy as np


w = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

a = np.ones((16, 5, 5))
b = np.arange(16 * 5 * 5)
b = np.reshape(b, (16, 5, 5))
c = a * b


# output_dim = 5
# w_flattern = np.repeat(w, output_dim, axis=0)

print(np.shape(c))
# print(np.rot90(b, k=2, axes=(1, 2)))