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

def hyper_tan(x):
    return 1.7159 * np.tanh(2 / 3 * x)

def ht_deri(x):
    return 1.7159 * (2 / 3) * (1 - np.tanh(x) ** 2)


epochs = 1

achieve_goal = False
while achieve_goal is False:
    ''' data set initialization'''
    tr_dat = tr_dat.reshape(-1, 16 * 16)
    te_dat = te_dat.reshape(-1, 16 * 16)
    x = tr_dat
    y = tr_lab
    test_x = te_dat
    test_y = te_lab
    start = 0
    ''' 1st layer initialization'''
    w_1 = (np.random.rand(16 * 16, 12) - 0.5) * 2.5
    b_1 = np.random.rand(1, 12)
    deri_w_1 = 0
    deri_b_1 = 0
    ''' 2nd layer initialization'''
    w_2 = (np.random.rand(12, 10) - 0.5) * 2.5
    b_2 = np.random.rand(1, 10)
    deri_w_2 = 0
    deri_b_2 = 0
    for epoch in range(epochs):
        # x = x[start: start + BATCH]
        # start += BATCH
        # 1st layer
        w_1 = w_1 + 0.01 * deri_w_1
        b_1 = b_1 + 0.01 * deri_b_1
        z_1 = np.matmul(x, w_1) + b_1
        a_1 = sigmoid(z_1)
        # 2nd layer
        w_2 = w_2 + 0.01 * deri_w_2
        b_2 = b_2 + 0.01 * deri_b_2
        z_2 = np.matmul(a_1, w_2) + b_2
        a_2 = sigmoid(z_2)
        # calculate the derivatives using back-propagation
        deri_w_2 = np.dot(a_1.T, ((y - a_2) * sig_deri(a_2)))
        deri_b_2 = np.sum((y - a_2) * sig_deri(a_2), axis=0)
        deri_w_1 = np.dot(x.T, (np.dot((y - a_2) * sig_deri(a_2), w_2.T) * sig_deri(a_1)))
        deri_b_1 = np.sum(np.dot((y - a_2) * sig_deri(a_2), w_2.T) * sig_deri(a_1), axis=0)

        test_z_1 = np.matmul(test_x, w_1) + b_1
        test_a_1 = sigmoid(test_z_1)
        test_z_2 = np.matmul(test_a_1, w_2) + b_2
        test_a_2 = sigmoid(test_z_2)

        test_count = 0
        train_count = 0

        # for i in range(160):
        #     if np.argmax(test_y[i]) == np.argmax(test_a_2[i]):
        #         test_count += 1
        #         accuracy = test_count / 160 * 100
        #         if accuracy >= 65:
        #             1
        #             # achieve_goal = True
        # print("%d epoch test accuracy" % epoch, accuracy)
        #
        # for i in range(320):
        #     if np.argmax(y[i]) == np.argmax(a_2[i]):
        #         train_count += 1
        #         accuracy = train_count / 320 * 100
        # print("%d epoch train accuracy" % epoch, accuracy)


    test_count = 0
    for i in range(160):
        if np.argmax(test_y[i]) == np.argmax(test_a_2[i]):
            test_count += 1
            accuracy = test_count / 160 * 100
    mse = 0.5 * np.sum((a_2 - y) ** 2) / 320
    print("Final test accuracy:", accuracy, "average loss:", mse)

# mse = 0.5 * np.sum((a_2 - y) ** 2) / 320
# print("Final test accuracy:", accuracy, "average loss:", mse)



