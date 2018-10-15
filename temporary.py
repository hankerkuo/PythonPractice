import numpy as np
l = 10
def abc():
    global l
    l += 1
a = np.array([[1,2,3], [4,5,6]])
a = np.reshape(a, (1, 6))
a = np.reshape(a, (2, 3))
abc()
print(l)