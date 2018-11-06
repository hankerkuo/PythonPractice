import numpy as np

a = np.array([3, 2, 1, 3, 5])
b = np.array([3, 2, 3, 3, 5])

# convenient to calculate the accuracy
print(np.mean(a == b))