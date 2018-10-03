import numpy as np
from six.moves import cPickle as pickle

with open('./train_data/data.pickle', 'rb') as f:
    tr_dat = pickle.load(f)
with open('./train_data/label.pickle', 'rb') as f:
    tr_lab = pickle.load(f)
with open('./test_data/data.pickle', 'rb') as f:
    te_dat = pickle.load(f)
with open('./test_data/label.pickle', 'rb') as f:
    te_lab = pickle.load(f)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sig_deri(x):
    return x * (1 - x)


''' data set initialization'''
tr_dat = tr_dat.reshape(-1, 16 * 16)
te_dat = te_dat.reshape(-1, 16 * 16)
x = tr_dat
y = tr_lab
test_x = te_dat
test_y = te_lab
deri_weights = 0
deri_bias = 0
''' 1st layer initialization'''
w = (np.random.rand(16 * 16, 10) - 0.5) * 2.5
b = np.random.rand(1, 10)


for epoch in range(500):
    w = w + 0.01 * deri_weights
    b = b + 0.01 * deri_bias
    z = np.matmul(x, w) + b
    a = sigmoid(z)
    mse = 0.5 * np.sum((a - y) ** 2)
    deri_weights = np.dot(x.T, ((y - a) * sig_deri(a)))
    deri_bias = (y - a) * sig_deri(a)
    # print(mse)

    test_z = np.matmul(test_x, w)
    test_a = sigmoid(test_z)
    test_count = 0
    train_count = 0
    for i in range(160):
        if np.argmax(test_y[i]) == np.argmax(test_a[i]):
            test_count += 1
    print("%d epoch test accuracy" % epoch, test_count / 160 * 100)

    for i in range(320):
        if np.argmax(y[i]) == np.argmax(a[i]):
            train_count += 1
    print("%d epoch train accuracy" % epoch, train_count / 320 * 100)



