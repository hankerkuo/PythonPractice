import numpy as np


w = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

a = np.ones((16, 5, 5))

# output_dim = 5
# w_flattern = np.repeat(w, output_dim, axis=0)

print(np.sum(a, axis=(0, 1)))