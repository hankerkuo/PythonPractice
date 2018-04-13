import numpy as np

scores = np.array([1, 2, 3])

def test(*x):
    return x


sequence = test(scores)
print(sequence)
for i in sequence:
    print(i)
