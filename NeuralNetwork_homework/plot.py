import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def every_ten_epoch(lst, epochs):
    result = []
    for i in range(3):
        row = [lst[i][j] for j in range(0, epochs, 10)]
        result.append(row)
    return np.array(result)

No_filter = np.load('Net5_WShared_Epochs_1000 LRate_0.01 Filter_None Time_Wed Nov 21 040347 2018.npy')
# No_filter = every_ten_epoch(No_filter, 1000)
Gabor = np.load('Net5_WShared_Epochs_1000 LRate_0.01 Filter_gabor Time_Mon Nov 26 234349 2018.npy')
# Gabor = every_ten_epoch(Gabor, 1000)
double_Gabor = np.load('Net5_WShared_Epochs_1000 LRate_0.01 Filter_double_gabor Time_Wed Nov 28 011046 2018.npy')
# double_Gabor = every_ten_epoch(double_Gabor, 1000)


'''drawing part for net 5, with only Gabor filter
df = pd.DataFrame({'epoch': np.concatenate((No_filter[0], No_filter[0], No_filter[0])),
        'train_accuracy': np.concatenate((No_filter[1], Gabor[1], double_Gabor[1])),
        'filters': np.concatenate(( np.array(['No_filter' for i in range(len(No_filter[0]))]),
                                    np.array(['Gabor_1' for i in range(len(No_filter[0]))]),
                                    np.array(['Gabor_2' for i in range(len(No_filter[0]))]) ))

                   })
sns.set()
sns.relplot(x="epoch", y="train_accuracy",
            facet_kws=dict(sharex=False), hue="filters",
            kind="line", legend="full", data=df);
plt.show()
'''

''' best accuracy finding '''

# new = every_ten_epoch(new)

target = No_filter
print('best testing accuracy:', np.max(target[2][0:1000]), 'its training accuracy:', target[1][np.argmax(target[2][0:1000])])
