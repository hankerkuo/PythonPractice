'''
This is the code trying to shift from numpy to cupy originally
But the matrix operation seems not big enough
As a result, compared to numpy, cupy is much slower instead
'''
# THIS IMPLEMENTATION WILL INCLUDE CONFUSION MATRIX
import cupy as cp
from six.moves import cPickle as pickle
import time
import filters
import gabor_filter_cupy

memory_pool = cp.cuda.MemoryPool()
cp.cuda.set_allocator(memory_pool.malloc)
pinned_memory_pool = cp.cuda.PinnedMemoryPool()
cp.cuda.set_pinned_memory_allocator(pinned_memory_pool.malloc)

with open('./train_data/data.pickle', 'rb') as f:
    tr_dat = pickle.load(f)
    tr_dat = cp.asarray(tr_dat)
with open('./train_data/label.pickle', 'rb') as f:
    tr_lab = pickle.load(f)
    tr_lab = cp.asarray(tr_lab)
with open('./test_data/data.pickle', 'rb') as f:
    te_dat = pickle.load(f)
    te_dat = cp.asarray(te_dat)
with open('./test_data/label.pickle', 'rb') as f:
    te_lab = pickle.load(f)
    te_lab = cp.asarray(te_lab)

def sigmoid(x):
    return 1 / (1 + cp.exp(-x))

def sig_deri(x):
    return x * (1 - x)


# 1st layer initialization
layer1_ch = 2
CNN_layer1_map = cp.ndarray(shape=(layer1_ch, 8, 8))
CNN_layer1_weight = (cp.random.rand(layer1_ch, 3, 3) - 0.5) * 2.5
CNN_layer1_bias = cp.random.rand(layer1_ch, 8, 8)
CNN_layer1_stride = 2

# 2nd layer initialization
layer2_ch = 4
CNN_layer2_map = cp.ndarray(shape=(layer2_ch, 4, 4))
CNN_layer2_weight = (cp.random.rand(layer2_ch, 5, 5) - 0.5) * 2.5
CNN_layer2_bias = cp.random.rand(layer2_ch, 4, 4)
CNN_layer2_stride = 2

# FC layer initialization
FC_w = (cp.random.rand(16, 10) - 0.5) * 2.5
FC_b = cp.random.rand(1, 10)
FC_a = 0

def training(sample, test=False):
    global CNN_layer1_map
    if test is True:
        layer1_input = cp.pad(te_dat[sample], ((1, 1), (1, 1)), 'constant', constant_values=((0, 0), (0, 0)))
    else:
        # zero padding, constant_values default is zero
        layer1_input = cp.pad(tr_dat[sample], ((1, 1), (1, 1)), 'constant', constant_values=((0, 0), (0, 0)))

    # first CNN layer, index from 1 starts
    for index_y in range(8):
        for index_x in range(8):
            in_x = index_x * CNN_layer1_stride + 1
            in_y = index_y * CNN_layer1_stride + 1
            # for both channels
            output_mat = cp.stack([ele[in_x - 1: in_x + 2] for ele in layer1_input[in_y - 1: in_y + 2]]) *\
                cp.stack([single_w for single_w in CNN_layer1_weight])
            z = cp.sum(output_mat, axis=(1, 2)) + cp.stack([single_b[index_y][index_x] for single_b in CNN_layer1_bias])
            # with activation function
            for ch in range(layer1_ch):
                CNN_layer1_map[ch][index_y][index_x] = sigmoid(z[ch])
            # print(output_mat, z, ' ', index_y, index_x, sep='')

    # zero padding, now layer2_input has two channels
    layer2_input = cp.pad(CNN_layer1_map, ((0, 0), (2, 2), (2, 2)), 'constant')

    # second CNN layer
    global CNN_layer2_map
    for index_y in range(4):
        for index_x in range(4):
            in_x = index_x * CNN_layer2_stride + 2
            in_y = index_y * CNN_layer2_stride + 2
            output_mat = cp.stack([ cp.stack([ cp.stack([ele[in_x - 2: in_x + 3] for ele in layer2_input[l1_ch][in_y - 2: in_y + 3]])
                                    for l1_ch in range(layer1_ch) ])
                                    * CNN_layer2_weight[l2_ch] for l2_ch in range(layer2_ch)])
            z = cp.sum(output_mat, axis=(1, 2, 3)) + cp.stack([single_b[index_y][index_x] for single_b in CNN_layer2_bias])
            # with activation function
            for ch in range(layer2_ch):
                CNN_layer2_map[ch][index_y][index_x] = sigmoid(z[ch])
            # print(output_mat, z, ' ', index_y, index_x, sep='')

    # FC layer
    global FC_a
    FC_input = CNN_layer2_map.reshape(4, -1)
    FC_z = cp.sum(cp.dot(FC_input, FC_w), axis=0) + FC_b
    FC_a = sigmoid(FC_z)
    return FC_a

def back_prop(sample):
    global FC_w, FC_b, CNN_layer1_weight, CNN_layer1_bias, CNN_layer2_weight, CNN_layer2_bias
    FC_input = cp.reshape(cp.sum(CNN_layer2_map, axis=0), (1, 16))
    CNN2_a_flat = CNN_layer2_map.reshape(4, -1)
    # CNN_a has two channel, first axis represents the channel
    CNN1_a_flat = cp.reshape(CNN_layer1_map, (2, -1))
    y = tr_lab[sample].reshape(1, 10)

    # L - 1 layer update, delta shape = (1, 10)
    delta = ((y - FC_a) * sig_deri(FC_a))
    deri_FC_w = cp.dot(FC_input.T, delta)
    deri_bias = delta
    FC_w = FC_w + learning_rate * deri_FC_w
    FC_b = FC_b + learning_rate * deri_bias

    # L - 2 layer update, delta shape = (4, 16)
    # deri_CNN_layer2_weight shape = (4, 16, 144) 144(=12*12) is the amount after padding (8, 8)
    layer2_input = cp.pad(cp.sum(CNN_layer1_map, axis=0), ((2, 2), (2, 2)), 'constant')
    delta = cp.dot(delta, FC_w.T) * sig_deri(CNN2_a_flat)
    delta = cp.reshape(delta, (4, 1, 16))
    deri_CNN_layer2_weight = cp.dot(cp.transpose(delta, axes=(0, 2, 1)), layer2_input.reshape(1, 12 * 12))
    deri_CNN_layer2_weight = cp.reshape(deri_CNN_layer2_weight, (4, 4, 4, 12, 12))
    for index_y in range(4):
        for index_x in range(4):
            in_ind_x = index_x * CNN_layer1_stride + 2
            in_ind_y = index_y * CNN_layer1_stride + 2
            # loop for each kernel
            for y in range(5):
                for x in range(5):
                    # loop for each channel
                    for ch in range(layer2_ch):
                        CNN_layer2_weight[ch][y][x] = CNN_layer2_weight[ch][y][x] + \
                            learning_rate * deri_CNN_layer2_weight[ch][index_y][index_x][in_ind_y - 2 + y][in_ind_x - 2 + x]
            for ch in range(layer2_ch):
                CNN_layer2_bias[ch] = CNN_layer2_bias[ch] + learning_rate * cp.reshape(delta[ch], (4, 4))

    # L - 3 layer update, delta shape = (2, 64)
    # deri_CNN_layer1_weight shape = (64, 18 * 18) 18 * 18 is the amount after padding (16, 16)
    layer1_input = cp.pad(tr_dat[sample], ((1, 1), (1, 1)), 'constant', constant_values=((0, 0), (0, 0)))

    # update the weight for each channel, eg, there're 4 channels in 2nd layer ->
    # 1st layer weight should be updated for 4 times
    layer_2_delta = delta
    for ch in range(layer2_ch):
        # print(CNN_layer1_weight[0])
        # first make a (16, 64) CNN weight reference
        weight_reference = []
        for index_y in range(4):
            for index_x in range(4):
                in_ind_x = index_x * CNN_layer1_stride
                in_ind_y = index_y * CNN_layer1_stride
                single = cp.zeros(shape=64)
                for y in range(-2, 3):
                    for x in range(-2, 3):
                        if 0 <= (in_ind_y + y) <= 7 and 0 <= (in_ind_x + x) <= 7:
                            single[8 * (in_ind_y + y) + (in_ind_x + x)] = CNN_layer2_weight[ch][y + 2][x + 2]
                weight_reference.append(single)
        weight_reference = cp.stack(weight_reference)

        # delta for two channels, delta matrix's first axis refers to the channel
        ''' elegant method'''
        delta = sig_deri(CNN1_a_flat) * cp.dot(layer_2_delta[ch], weight_reference)  # after this operation delta shape -> (2, 64)
        delta = cp.reshape(delta, (2, 1, 64))
        '''search the method for using cp.transpose'''
        deri_CNN_layer1_weight = cp.dot(cp.transpose(delta, axes=(0, 2, 1)), layer1_input.reshape(1, 18*18))
        deri_CNN_layer1_weight = cp.reshape(deri_CNN_layer1_weight, (2, 8, 8, 18, 18))

        # loop for each node in the feature map
        for index_y in range(8):
            for index_x in range(8):
                in_ind_x = index_x * CNN_layer1_stride + 1
                in_ind_y = index_y * CNN_layer1_stride + 1
                # loop for each kernel
                for y in range(3):
                    for x in range(3):
                        # loop for each channel's weight
                        for channels in range(layer1_ch):
                            CNN_layer1_weight[channels][y][x] = CNN_layer1_weight[channels][y][x] + \
                            learning_rate * deri_CNN_layer1_weight[channels][index_y][index_x][in_ind_y - 1 + y][in_ind_x - 1 + x]
                # loop for each channel's bias
                for channels in range(layer1_ch):
                    CNN_layer1_bias[channels] = CNN_layer1_bias[channels] + learning_rate * cp.reshape(delta[channels], (8, 8))


def validation_accuracy(gd_truth_n_prediction):
    global epoch
    test_y = te_lab
    test_count = 0
    for i in range(160):
        result = training(i, test=True)
        gd_truth_n_prediction[epoch][0][i] = cp.argmax(test_y[i])
        gd_truth_n_prediction[epoch][1][i] = cp.argmax(result)
        if cp.argmax(test_y[i]) == cp.argmax(result):
            test_count += 1
            accuracy = test_count / 160 * 100
    print('test accuracy:', accuracy)
    return accuracy

def train_accuracy():
    test_y = tr_lab
    test_count = 0
    for i in range(160):
        result = training(i, test=False)
        if cp.argmax(test_y[i]) == cp.argmax(result):
            test_count += 1
            accuracy = test_count / 160 * 100
    print('train accuracy:', accuracy)
    return accuracy

# hyper parameters
learning_rate = 0.01
epochs = 1000
filter_type = 'None'  # None, sobel, prewitt, laplacian, laplacian_of_guassian, gabor

if __name__ == "__main__":

    # use filter
    if filter_type != 'None':
        if filter_type == 'gabor':
            for num in range(len(tr_dat)):
                tr_dat[num] = gabor_filter_cupy.gabor(tr_dat[num], 3, 12, 0, cp.pi, 15, threshold=0)
            for num in range(len(te_dat)):
                te_dat[num] = gabor_filter_cupy.gabor(te_dat[num], 3, 12, 0, cp.pi, 15, threshold=0)
        else:
            for num in range(len(tr_dat)):
                tr_dat[num] = getattr(filters, filter_type)(tr_dat[num])
            for num in range(len(te_dat)):
                te_dat[num] = getattr(filters, filter_type)(te_dat[num])

    # record -> first axis -> [0]: epoch [1]: trainingaccuracy [2]: testing accuracy
    record = cp.ndarray(shape=(3, epochs))
    # ground_truth_plus_prediction -> 3d array -> axis0: epochs,
    # axis1: [0]:truth & [1]:prediction, axis2: each testing data
    ground_truth_plus_prediction = cp.ndarray(shape=(epochs, 2, 160))

    for epoch in range(epochs):
        for stochastic in range(320):
            samples = cp.random.random_integers(0, 319)
            training(samples)
            back_prop(samples)
        # if epoch % 10 == 0:
        print('epoch ', epoch, ':')
        record[0][epoch] = epoch + 1
        record[1][epoch] = train_accuracy()
        record[2][epoch] = validation_accuracy(ground_truth_plus_prediction)

    # cp.savetxt('epochs {} {}.txt'.format(epochs, time.asctime().replace(':', '')), record, fmt='%2.3f')
    cp.save('Net5_WShared_Epochs_{} LRate_{} Filter_{} Time_{}.cpy'
            .format(epochs, learning_rate, filter_type, time.asctime().replace(':', '')), record)
    cp.save('Net5_ConfusionMatrix_WShared_Epochs_{} LRate_{} Filter_{} Time_{}.cpy'
            .format(epochs, learning_rate, filter_type, time.asctime().replace(':', '')), ground_truth_plus_prediction)

