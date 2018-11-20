import numpy as np
from sklearn.metrics import confusion_matrix

target = np.load('')
epoch = 8
cf_matrix = confusion_matrix(target[epoch][0], target[epoch][1])

print(cf_matrix)


