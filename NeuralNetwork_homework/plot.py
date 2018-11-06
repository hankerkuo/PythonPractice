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

'''
result_file = 'WShared-Epochs_200 LRate_0.1 Filter_None Time_Wed Oct 17 204347 2018.npy'
a = np.load(result_file)

No_filter = np.load('Epochs_2000 LRate_0.01 Time_Wed Oct 17 154146 2018.npy')
No_filter = every_ten_epoch(No_filter)
sobel = np.load('Epochs_2000 LRate_0.01 Filter_sobel Time_Wed Oct 17 174544 2018.npy')
sobel = every_ten_epoch(sobel)
prewitt = np.load('Epochs_2000 LRate_0.01 Filter_prewitt Time_Wed Oct 17 174909 2018.npy')
prewitt = every_ten_epoch(prewitt)
laplacian = np.load('Epochs_2000 LRate_0.01 Filter_laplacian Time_Wed Oct 17 190855 2018.npy')
laplacian = every_ten_epoch(laplacian)
laplacian_gaussian = np.load('Epochs_2000 LRate_0.01 Filter_laplacian_of_guassian Time_Wed Oct 17 191001 2018.npy')
laplacian_gaussian = every_ten_epoch(laplacian_gaussian)
'''

new = np.load('Net4_WShared_Epochs_2000 LRate_0.01 Filter_None Time_Mon Nov  5 233129 2018.npy')
# new = every_ten_epoch(new)
'''
drawing part

df = pd.DataFrame({'epoch': np.concatenate((No_filter[0], No_filter[0], No_filter[0], No_filter[0], No_filter[0])),
        'train_accuracy': np.concatenate((No_filter[1], sobel[1], prewitt[1], laplacian[1], laplacian_gaussian[1])),
        'filters': np.concatenate(( np.array(['No_filter' for i in range(len(No_filter[0]))]),
                                    np.array(['sobel' for i in range(len(No_filter[0]))]),
                                    np.array(['prewitt' for i in range(len(No_filter[0]))]),
                                    np.array(['laplacian' for i in range(len(No_filter[0]))]),
                                    np.array(['laplacian_gaussian' for i in range(len(No_filter[0]))]) ))
                   })
sns.set()
sns.relplot(x="epoch", y="train_accuracy",
            facet_kws=dict(sharex=False), hue="filters",
            kind="line", legend="full", data=df);
plt.show()
'''

''' best accuracy finding '''
target = new
print('best testing accuracy:', np.max(target[2][0:2000]), 'its training accuracy:', target[1][np.argmax(target[2][0:2000])])
