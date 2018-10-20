import numpy as np
from six.moves import cPickle as pickle
import time
import filters

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

# 1st layer initialization
CNN_layer1_map = np.ndarray(shape=(8, 8))
CNN_layer1_shared_weight = (np.random.rand(3, 3) - 0.5) * 2.5
CNN_layer1_bias = np.random.rand(8, 8)
CNN_layer1_stride = 2

# 2nd layer initialization
CNN_layer2_map = np.ndarray(shape=(4, 4))
CNN_layer2_shared_weight = (np.random.rand(5, 5) - 0.5) * 2.5
CNN_layer2_bias = np.random.rand(4, 4)
CNN_layer2_stride = 2

# FC layer initialization
FC_w = (np.random.rand(16, 10) - 0.5) * 2.5
FC_b = np.random.rand(1, 10)
FC_a = 0

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
                         for ele in layer1_input[in_ind_y - 1: in_ind_y + 2]]) * CNN_layer1_shared_weight
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
                         for ele in layer2_input[in_ind_y - 2: in_ind_y + 3]]) * CNN_layer2_shared_weight
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
    global FC_w, FC_b, CNN_layer1_shared_weight, CNN_layer1_bias, CNN_layer2_shared_weight, CNN_layer2_bias
    FC_input = CNN_layer2_map.reshape(1, -1)
    CNN2_a_flat = CNN_layer2_map.reshape(1, -1)
    CNN1_a_flat = CNN_layer1_map.reshape(1, -1)
    y = tr_lab[sample].reshape(1, 10)

    # L - 1 layer update, delta shape = (1, 10)
    delta = ((y - FC_a) * sig_deri(FC_a))
    deri_FC_w = np.dot(FC_input.T, delta)
    deri_bias = delta
    FC_w = FC_w + learning_rate * deri_FC_w
    FC_b = FC_b + learning_rate * deri_bias

    # L - 2 layer update, delta shape = (1, 16)
    # deri_CNN_layer2_weight shape = (16, 144) 144(=12*12) is the amount after padding (8, 8)
    layer2_input = np.pad(CNN_layer1_map, ((2, 2), (2, 2)), 'constant', constant_values=((0, 0), (0, 0)))
    delta = np.dot(delta, FC_w.T) * sig_deri(CNN2_a_flat)
    deri_CNN_layer2_weight = np.dot(delta.T, layer2_input.reshape(1, 144))
    deri_CNN_layer2_weight = np.reshape(deri_CNN_layer2_weight, (4, 4, 12, 12))
    for index_y in range(4):
        for index_x in range(4):
            in_ind_x = index_x * CNN_layer1_stride + 2
            in_ind_y = index_y * CNN_layer1_stride + 2
            # loop for the kernel
            for y in range(5):
                for x in range(5):
                    CNN_layer2_shared_weight[y][x] = CNN_layer2_shared_weight[y][x] + \
                        learning_rate * deri_CNN_layer2_weight[index_y][index_x][in_ind_y - 2 + y][in_ind_x - 2 + x]
            CNN_layer2_bias = CNN_layer2_bias + learning_rate * np.reshape(delta, (4, 4))

    # L - 3 layer update, delta shape = (1, 64)
    # deri_CNN_layer1_weight shape = (64, 18 * 18) 18 * 18 is the amount after padding (16, 16)
    layer1_input = np.pad(tr_dat[sample], ((1, 1), (1, 1)), 'constant', constant_values=((0, 0), (0, 0)))
    # first make a (16, 64) CNN weight reference, to make the previous delta shape(1, 16) to (1, 64)
    weight_reference = []
    for index_y in range(4):
        for index_x in range(4):
            in_ind_x = index_x * CNN_layer1_stride
            in_ind_y = index_y * CNN_layer1_stride
            single = np.zeros(shape=64)
            for y in range(-2, 3):
                for x in range(-2, 3):
                    if 0 <= (in_ind_y + y) <= 7 and 0 <= (in_ind_x + x) <= 7:
                        single[8 * (in_ind_y + y) + (in_ind_x + x)] = CNN_layer2_shared_weight[y + 2][x + 2]
            weight_reference.append(single)
    weight_reference = np.array(weight_reference)
    delta = np.dot(delta, weight_reference) * sig_deri(CNN1_a_flat)
    deri_CNN_layer1_weight = np.dot(delta.T, layer1_input.reshape(1, 18*18))
    deri_CNN_layer1_weight = np.reshape(deri_CNN_layer1_weight, (8, 8, 18, 18))
    for index_y in range(8):
        for index_x in range(8):
            in_ind_x = index_x * CNN_layer1_stride + 1
            in_ind_y = index_y * CNN_layer1_stride + 1
            # loop for each kernel
            for y in range(3):
                for x in range(3):
                    CNN_layer1_shared_weight[y][x] = CNN_layer1_shared_weight[y][x] + \
                        learning_rate * deri_CNN_layer1_weight[index_y][index_x][in_ind_y - 1 + y][in_ind_x - 1 + x]
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
    return accuracy

def train_accuracy():
    test_y = tr_lab
    test_count = 0
    for i in range(160):
        result = training(i, test=False)
        if np.argmax(test_y[i]) == np.argmax(result):
            test_count += 1
            accuracy = test_count / 160 * 100
    print('train accuracy:', accuracy)
    return accuracy

# hyper parameters
learning_rate = 0.01
epochs = 2000
filter_type = 'None'  # None, sobel, prewitt, laplacian, laplacian_of_guassian

if __name__ == "__main__":

    # use filter
    if filter_type != 'None':
        for num in range(len(tr_dat)):
            tr_dat[num] = getattr(filters, filter_type)(tr_dat[num])
        for num in range(len(te_dat)):
            te_dat[num] = getattr(filters, filter_type)(te_dat[num])

    # record -> 0: epoch 1: trainingaccuracy 2: testing accuracy
    record = np.ndarray(shape=(3, epochs))

    for epoch in range(epochs):
        for stochastic in range(320):
            samples = np.random.random_integers(0, 319)
            training(samples)
            back_prop(samples)
            # print(FC_w[0])
        print('epoch ', epoch, ':')
        record[0][epoch] = epoch + 1
        record[1][epoch] = train_accuracy()
        record[2][epoch] = test_accuracy()

    # np.savetxt('epochs {} {}.txt'.format(epochs, time.asctime().replace(':', '')), record, fmt='%2.3f')
    np.save('WShared-Epochs_{} LRate_{} Filter_{} Time_{}.npy'
            .format(epochs, learning_rate, filter_type, time.asctime().replace(':', '')), record)

