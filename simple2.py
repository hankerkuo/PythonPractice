import numpy as np

a = np.array([[1, 2],
              [3, 4],
              [5, 6]])

index = [2, 0, 1]
index2 = [1, 0]
b = a[[2, 0, 1], 1]
c = a[[2, 0, 1], 0]
b = np.expand_dims(b, axis=1)
c = np.expand_dims(c, axis=1)
d = np.concatenate((b, c), axis=1)
e = np.concatenate((np.expand_dims(a[[2, 0, 1], 1], axis=1), np.expand_dims(a[[2, 0, 1], 0], axis=1)), axis=1)
print(a.shape[1:])