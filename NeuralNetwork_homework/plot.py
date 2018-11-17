import numpy as np
import pandas as pd
# import seaborn as sns
import matplotlib.pyplot as plt

def every_ten_epoch(lst):
    result = []
    for i in range(3):
        row = [lst[i][j] for j in range(0, 2000, 10)]
        result.append(row)
    return np.array(result)

'''files loading'''
# result_file = 'WShared-Epochs_200 LRate_0.1 Filter_None Time_Wed Oct 17 204347 2018.npy'
# a = np.load(result_file)

No_filter = np.load('Net4_WShared_Epochs_2000 LRate_0.01 Filter_None Time_Tue Nov  6 170722 2018.npy')
# No_filter = every_ten_epoch(No_filter)
sobel = np.load('Net4_WShared_Epochs_2000 LRate_0.01 Filter_sobel Time_Sun Nov  4 233718 2018.npy')
# sobel = every_ten_epoch(sobel)
prewitt = np.load('Net4_WShared_Epochs_2000 LRate_0.01 Filter_prewitt Time_Mon Nov  5 040017 2018.npy')
# prewitt = every_ten_epoch(prewitt)
laplacian = np.load('Net4_WShared_Epochs_2000 LRate_0.01 Filter_laplacian Time_Mon Nov  5 040052 2018.npy')
# laplacian = every_ten_epoch(laplacian)
laplacian_gaussian = np.load('Net4_WShared_Epochs_2000 LRate_0.01 Filter_laplacian_of_guassian Time_Mon Nov  5 233107 2018.npy')
# laplacian_gaussian = every_ten_epoch(laplacian_gaussian)

print(np.shape(No_filter))

'''
drawing part, index 1 -> train accuracy, index 2 -> test accuracy 

df = pd.DataFrame({'epoch': np.concatenate((No_filter[0], No_filter[0], No_filter[0], No_filter[0], No_filter[0])),
        'test_accuracy': np.concatenate((No_filter[2], sobel[2], prewitt[2], laplacian[2], laplacian_gaussian[2])),
        'filters': np.concatenate(( np.array(['No_filter' for i in range(len(No_filter[0]))]),
                                    np.array(['sobel' for i in range(len(No_filter[0]))]),
                                    np.array(['prewitt' for i in range(len(No_filter[0]))]),
                                    np.array(['laplacian' for i in range(len(No_filter[0]))]),
                                    np.array(['laplacian_gaussian' for i in range(len(No_filter[0]))]) ))
                   })
sns.set()
sns.relplot(x="epoch", y="test_accuracy",
            facet_kws=dict(sharex=False), hue="filters",
            kind="line", legend="full", data=df);
plt.show()
'''

''' best accuracy finding '''
new = np.load('Net4_WShared_Epochs_2000 LRate_0.01 Filter_None Time_Mon Nov  5 233129 2018.npy')
# new = every_ten_epoch(new)

target = laplacian_gaussian
print('best testing accuracy:', np.max(target[2][0:2000]), 'its training accuracy:', target[1][np.argmax(target[2][0:2000])])
