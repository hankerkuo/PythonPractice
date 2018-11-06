# source : https://stackoverflow.com/questions/35076223/how-to-randomly-shuffle-data-and-target-in-python
import numpy as np
from random import shuffle
train = np.array([[1, 0], [2, 1], [3, 0]])
target = np.array([0, 1, 0])

N = 3
ind_list = [i for i in range(N)]
shuffle(ind_list)

# use 1-d array to index!
train_new = train[ind_list, :]
target_new = target[ind_list]

print(train_new)
print(target_new)
