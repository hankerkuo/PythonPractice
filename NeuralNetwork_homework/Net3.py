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

# x is the weight of first CNN network
x = np.ndarray(shape=(8, 8, 3, 3))

x[1][1] = [[1, 2, 3],
           [1, 2, 3],
           [1, 2, 3]]

# 1st layer initialization
CNN_layer1_map = np.ndarray(shape=(8, 8))
CNN_layer1_weight = (np.random.rand(8, 8, 3, 3) - 0.5) * 2.5
CNN_layer1_bias = np.random.rand(8, 8)
CNN_layer1_stride = 2

# 2nd layer initialization
CNN_layer2_map = np.ndarray(shape=(4, 4))
CNN_layer2_weight = (np.random.rand(4, 4, 5, 5) - 0.5) * 2.5
CNN_layer2_bias = np.random.rand(4, 4)
CNN_layer2_stride = 2

# FC layer initialization
FC_w = (np.random.rand(16, 10) - 0.5) * 2.5
FC_b = np.random.rand(1, 10)
FC_a = 0

# learning details
learning_rate = 0.5

def training(sample, test=False):
    global CNN_layer1_map
    if test is True:
        layer1_input = np.pad(te_dat[sample], ((1, 1), (1, 1)), 'constant', constant_values=((0, 0), (0, 0)))
    else:
        # zero padding, constant_values default is zero
        layer1_input = np.pad(tr_dat[sample], ((1, 1), (1, 1)), 'constant', constant_values=((0, 0), (0, 0)))
    # first CNN layer, index from 1 starts
    for index_y in range(8):
        for index_x in range(8):
            in_ind_x = index_x * CNN_layer1_stride + 1
            in_ind_y = index_y * CNN_layer1_stride + 1
            output_mat = np.array([ele[in_ind_x - 1: in_ind_x + 2]
                         for ele in layer1_input[in_ind_y - 1: in_ind_y + 2]]) * CNN_layer1_weight[index_y][index_x]
            z = np.sum(output_mat) + CNN_layer1_bias[index_y][index_x]
            # with activation function
            CNN_layer1_map[index_y][index_x] = sigmoid(z)
            # print(output_mat, z, ' ', index_y, index_x, sep='')

    # zero padding
    layer2_input = np.pad(CNN_layer1_map, ((2, 2), (2, 2)), 'constant', constant_values=((0, 0), (0, 0)))
    # second CNN layer
    global CNN_layer2_map
    for index_y in range(4):
        for index_x in range(4):
            in_ind_x = index_x * CNN_layer2_stride + 2
            in_ind_y = index_y * CNN_layer2_stride + 2
            output_mat = np.array([ele[in_ind_x - 2: in_ind_x + 3]
                         for ele in layer2_input[in_ind_y - 2: in_ind_y + 3]]) * CNN_layer2_weight[index_y][index_x]
            z = np.sum(output_mat) + CNN_layer2_bias[index_y][index_x]
            # with activation function
            CNN_layer2_map[index_y][index_x] = sigmoid(z)
            # print(output_mat, z, ' ', index_y, index_x, sep='')

    # FC layer
    global FC_a
    FC_input = CNN_layer2_map.reshape(1, -1)
    FC_z = np.dot(FC_input, FC_w) + FC_b
    FC_a = sigmoid(FC_z)
    return FC_a

def back_prop(sample):
    global FC_w, FC_b, CNN_layer1_weight, CNN_layer1_bias, CNN_layer2_weight, CNN_layer2_bias
    FC_input = CNN_layer2_map.reshape(1, -1)
    CNN2_a_flat = CNN_layer2_map.reshape(1, -1)
    CNN1_a_flat = CNN_layer1_map.reshape(1, -1)
    y = tr_lab[sample].reshape(1, 10)

    # L - 1 layer update, delta shape = (1, 10)
    delta = ((y - FC_a) * sig_deri(FC_a))
    deri_FC_w = np.dot(FC_input.T, delta)
    deri_bias = (y - FC_a) * sig_deri(FC_a)
    FC_w = FC_w + learning_rate * deri_FC_w
    FC_b = FC_b + learning_rate * deri_bias

    # L - 2 layer update, delta shape = (1, 16)
    # deri_CNN_layer2_weight shape = (16, 144) 144(=12*12) is the amount after padding (8, 8)
    layer2_input = np.pad(CNN_layer1_map, ((2, 2), (2, 2)), 'constant', constant_values=((0, 0), (0, 0)))
    delta = np.dot(delta, FC_w.T) * sig_deri(CNN2_a_flat)
    deri_CNN_layer2_weight = np.dot(delta.T, layer2_input.reshape(1, 144))
    for index_y in range(4):
        for index_x in range(4):
            in_ind_x = index_x * CNN_layer1_stride + 2
            in_ind_y = index_y * CNN_layer1_stride + 2
            # loop for each kernel
            for y in range(5):
                for x in range(5):
                    CNN_layer2_weight[index_y][index_x][y][x] = CNN_layer2_weight[index_y][index_x][y][x] + \
                        learning_rate * (deri_CNN_layer2_weight[4 * index_y + index_x][12 * (in_ind_y - 2 + y) + (in_ind_x - 2 + x)])
            CNN_layer2_bias = CNN_layer2_bias + learning_rate * np.reshape(delta, (4, 4))

    # L - 3 layer update, delta shape = (1, 64)
    # deri_CNN_layer1_weight shape = (64, 18 * 18) 18 * 18 is the amount after padding (16, 16)
    layer1_input = np.pad(tr_dat[sample], ((1, 1), (1, 1)), 'constant', constant_values=((0, 0), (0, 0)))
    # first make a (16, 64) CNN weight reference
    weight_reference = []
    for index_y in range(4):
        for index_x in range(4):
            in_ind_x = index_x * CNN_layer1_stride
            in_ind_y = index_y * CNN_layer1_stride
            single = np.zeros(shape=64)
            for y in range(-2, 3):
                for x in range(-2, 3):
                    if 0 <= (in_ind_y + y) <= 7 and 0 <= (in_ind_x + x) <= 7:
                        single[8 * (in_ind_y + y) + (in_ind_x + x)] = CNN_layer2_weight[index_y][index_x][y + 2][x + 2]
            weight_reference.append(single)
    weight_reference = np.array(weight_reference)
    delta = np.dot(delta, weight_reference) * sig_deri(CNN1_a_flat)
    deri_CNN_layer1_weight = np.dot(delta.T, layer1_input.reshape(1, 18*18))
    for index_y in range(8):
        for index_x in range(8):
            in_ind_x = index_x * CNN_layer1_stride + 1
            in_ind_y = index_y * CNN_layer1_stride + 1
            # loop for each kernel
            for y in range(3):
                for x in range(3):
                    CNN_layer1_weight[index_y][index_x][y][x] = CNN_layer1_weight[index_y][index_x][y][x] + \
                        learning_rate * (deri_CNN_layer1_weight[8 * index_y + index_x][18 * (in_ind_y - 1 + y) + (in_ind_x - 1 + x)])
            CNN_layer1_bias = CNN_layer1_bias + learning_rate * np.reshape(delta, (8, 8))

def test_accuracy():
    test_y = te_lab
    test_count = 0
    for i in range(160):
        result = training(i, test=True)
        if np.argmax(test_y[i]) == np.argmax(result):
            test_count += 1
            accuracy = test_count / 160 * 100
    print('test accuracy:', accuracy)

def train_accuracy():
    test_y = tr_lab
    test_count = 0
    for i in range(160):
        result = training(i, test=False)
        if np.argmax(test_y[i]) == np.argmax(result):
            test_count += 1
            accuracy = test_count / 160 * 100
    print('train accuracy:', accuracy)

if __name__ == "__main__":
    for epoch in range(50):
        for samples in range(320):
            training(samples)
            back_prop(samples)
            # print(FC_w[0])
        train_accuracy()
        test_accuracy()


