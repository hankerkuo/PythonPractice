import numpy as np

# a = np.load('C:/OneDrive/文件/NRLab/2018가을학기/신경회로망 특론/4st과제/results/'
#         'Net5_ConfusionMatrix_WShared_Epochs_1000 LRate_0.01 Filter_None Time_Wed Nov 21 040347 2018.npy')


a = np.array([[1,2], [3,4]])
b = np.array([[5,6], [7,8]])
c = np.concatenate((a, b), axis=1)
print(c)
