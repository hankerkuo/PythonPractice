import numpy as np
from sklearn.metrics import confusion_matrix

target = np.load('Net5_ConfusionMatrix_WShared_Epochs_1000 LRate_0.01 Filter_None Time_Wed Nov 21 040347 2018.npy')
epoch = 500
cf_matrix = confusion_matrix(target[epoch][0], target[epoch][1])

print(cf_matrix)


