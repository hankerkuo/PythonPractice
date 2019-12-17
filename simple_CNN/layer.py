import numpy as np
import platform

from collections import deque

from datagen import DataGenerator



class FC:

    # nodes is the hidden nodes number
    def __init__(self, nodes, activation):
        self.activation = activation
        self.nodes = nodes
        self.initialized = False

    def forward_prop(self, input):
        if not self.initialized:
            self.w = np.random.rand(self.nodes, np.shape(input)[1]) - 0.5
            self.b = np.random.rand(self.nodes)
            self.initialized = True
        self.z = np.matmul(input, self.w.T) + self.b
        self.a = getattr(Activations(), self.activation)(self.z)
        self.a_previous = input

        return self.a

    def back_prop(self, label=False, w_nextlayer=None, delta_nextlayer=None):

        deri_a_wrt_z = getattr(Activations(), self.activation + '_derivative')(self.z)

        if label is False:
            # delta's first axis is also batch number, be familiar with matmul expression
            delta = np.squeeze(np.matmul(w_nextlayer.T, 
                    np.expand_dims(delta_nextlayer, axis=2)), axis=-1) * deri_a_wrt_z
        else:
            delta = Loss().MSE_derivative(label, self.a) * deri_a_wrt_z
        
        gradient_w = np.average(np.matmul(np.expand_dims(delta, axis=2), 
                        np.expand_dims(self.a_previous, axis=1)), axis=0)
        gradient_b = np.average(delta, axis=0)
        self.w -= 0.1 * gradient_w
        self.b -= 0.1 * gradient_b

        return self.w, delta


class Conv1D:

    # 1D conv, filter size is a integer
    def __init__(self, filter_size, channels, padding, stride, activation):
        assert padding in ['same'], 'Padding method not defined!'
        assert activation in ['sigmoid'], 'acitvation method not defined!'

        self.filter_size = filter_size
        self.channels = channels
        self.padding = padding
        self.stride = stride
        self.activation = activation
        self.initialized = False
    
    def forward_prop(self, input):
        if not self.initialized:
            self.batch = np.shape(input)[0]
            self.input_dim = np.shape(input)[1]
            self.output_dim = np.ceil(np.shape(input)[1] / self.stride).astype('int')
            self.w = np.random.rand(self.channels, self.filter_size) - 0.5
            self.b = np.zeros(self.channels, dtype=float)
            self.z = np.empty((self.channels, self.batch, self.output_dim))
            self.initialized = True

        if self.padding == 'same':
            input = self.same_padding(input)

        self.a_previous = input
        
        # each channel
        for i, w in enumerate(self.w):
            # each output node
            for k in range(self.output_dim):
                self.z[i, :, k] = np.dot(input[:, k * self.stride: k * self.stride + self.filter_size], w) + self.b[i]
        self.a = getattr(Activations(), self.activation)(self.z)

        # flatten the output
        self.a = np.swapaxes(self.a, 0, 1)
        self.a = np.reshape(self.a, (self.batch, -1))

        return self.a
    
    def back_prop(self, label=False, w_nextlayer=None, delta_nextlayer=None, next_layer=None):
        
        delta = np.empty((self.channels, self.batch, self.output_dim))
        gradient_w = np.zeros((self.channels, self.batch, self.filter_size))

        # each channel
        for i, z in enumerate(self.z):
            deri_a_wrt_z = getattr(Activations(), self.activation + '_derivative')(z)

            if next_layer == 'FC':
                w_next = w_nextlayer[:, i * self.output_dim: (i + 1) * self.output_dim]
                delta[i, :, :] = np.squeeze(np.matmul(w_next.T, np.expand_dims(delta_nextlayer, axis=2)), axis=-1) * deri_a_wrt_z
            elif next_layer == 'Conv1D':
                filter_sz_next = np.shape(w_nextlayer)[1]
                w_next = np.rot90(w_nextlayer)
                delta_next = np.swapaxes(delta_nextlayer, 0, 1)
                delta_next = np.pad(delta_next, ((0, 0), (0, 0), (filter_sz_next - 1, filter_sz_next - 1)), mode='constant')
                w_by_delta = np.matmul(w_next, delta_next)
                for k in range(self.output_dim):
                    # average is used for averaging the error of every channel in the next layer
                    delta[i, :, k] = np.average(np.diagonal (w_by_delta[:, :, k : k + filter_sz_next], axis1=1, axis2=2), axis=1)
                delta[i] = delta[i] * deri_a_wrt_z

            # each output node
            for k in range(self.output_dim):
                gradient_w[i] += np.multiply(np.expand_dims(delta[i, :, k], axis=1), 
                                            self.a_previous[:, k * self.stride: k * self.stride + self.filter_size])
            self.w[i] -= 1 * np.average(gradient_w[i], axis=0)
            self.b[i] -= 1 * np.average(delta[i])

        return self.w, delta

    def same_padding(self, input):
        if self.filter_size % 2 != 0:
            pad_left = (self.filter_size - 1) // 2
            pad_right = (self.filter_size - 1) // 2
            return np.pad(input, ((0, 0), (pad_left, pad_right)), mode='constant')
        else:
            pad_left = self.filter_size // 2
            pad_right = self.filter_size // 2 + 1
            return np.pad(input, ((0, 0), (pad_left, pad_right)), mode='constant')             
            

class Conv2D:

    # 2D conv, filter size is also an integer (receive square filter)
    def __init__(self, filter_size, channels, padding, stride, activation):
        assert padding in ['same'], 'Padding method not defined!'
        assert activation in ['sigmoid', 'relu'], 'acitvation method not defined!'

        self.filter_size = filter_size
        self.channels = channels
        self.padding = padding
        self.stride = stride
        self.activation = activation
        self.initialized = False
    
    # input receive 4-dimension data [batch, height, width, channels] 
    def forward_prop(self, input):
        # saves the input 
        if self.padding == 'same':
            self.a_previous = self.same_padding(input, self.filter_size)
        elif self.padding == 'valid':
            self.a_previous = input

        self.batch = np.shape(self.a_previous)[0]
        self.out_h_w = np.floor((np.array(np.shape(self.a_previous)[1: 3]) - self.filter_size) 
                        / self.stride + 1).astype('int')
        self.z = np.empty((self.batch, self.out_h_w[0], self.out_h_w[1], self.channels))

        if not self.initialized:
            self.w = (np.random.rand(self.channels, 
                        self.filter_size, self.filter_size, np.shape(self.a_previous)[3]) - 0.5)
            self.b = np.random.rand(self.channels)
            self.initialized = True

        # each channel
        for i, w in enumerate(self.w):
            self.z[:, :, :, i] = self.conv_operation(input, w, stride=self.stride, padding=self.padding)
        
        self.a = getattr(Activations(), self.activation)(self.z)

        return self.a
    
    def back_prop(self, label=False, w_nextlayer=None, delta_nextlayer=None, next_layer=None):
        
        delta = np.empty((self.batch, self.out_h_w[0], self.out_h_w[1], self.channels))
        gradient_w = np.zeros((self.batch, self.channels, 
                        self.filter_size, self.filter_size, np.shape(self.a_previous)[3]))

        delta_return = np.empty((self.batch, 
                        self.out_h_w[0] * self.stride, self.out_h_w[1] * self.stride, self.channels))

        # each channel
        for i in range(self.channels):
            deri_a_wrt_z = getattr(Activations(), self.activation + '_derivative')(self.z[..., i])

            if type(next_layer) == FC:
                w_next = w_nextlayer[:, i * self.out_h_w[0] * self.out_h_w[1]: 
                            (i + 1) * self.out_h_w[0] * self.out_h_w[1]]
                delta[..., i] = np.reshape(np.matmul(w_next.T, np.expand_dims(delta_nextlayer, axis=2)), 
                                              (self.batch, self.out_h_w[0], self.out_h_w[1])) * deri_a_wrt_z

            elif type(next_layer) == Conv2D:
                w_delta = np.zeros((self.batch, self.out_h_w[0], self.out_h_w[1]))
                w_delta = self.conv_operation(delta_nextlayer, np.rot90(w_nextlayer[..., i], 
                            k=2, axes=(1, 2)), 1, 'same', mode='channel')
                delta[..., i] = w_delta * deri_a_wrt_z

            delta_put_zeros = self.put_zeros(delta[..., i], self.stride, del_last_ele=False)
            delta_return[..., i] = delta_put_zeros

            gradient_w[:, i] += self.conv_operation(self.a_previous, delta_put_zeros, 1, 
                                padding='valid', mode='batch_filter')

            self.w[i] -= 0.01 * np.average(gradient_w[:, i], axis=0)
            self.b[i] -= 0.01 * np.average(delta[..., i])

        return self.w, np.array(delta_return)

    '''
    conv operation , output the conv result for a single output channel
    conv operation revceives 4-dimension data [batch, height, width, channels]
    filter -> [size, size, channels]
    batch_filter -> [batch, size, size, channels]
    output -> [batch, outsize_x, outsize_y]
    batch_filter means to calculate every batch of sample with different filter, now used for back prop calculating ∂C/∂W
    '''
    def conv_operation(self, input, filter, stride, padding, mode='normal'):
        assert mode in ['normal', 'batch_filter', 'channel'], 'mode not supported!'

        # only support for square filter
        filter_size = np.shape(filter)[1]

        if padding == 'same':
            input = self.same_padding(input, filter_size)
        elif padding == 'valid':
            pass

        out_h_w = np.floor((np.array(np.shape(input)[1: 3]) - filter_size) / stride + 1).astype('int')
        
        if mode in ['normal', 'channel']:
            output = np.zeros((np.shape(input)[0], out_h_w[0], out_h_w[1]))
            # height
            for h in range(out_h_w[0]):
                # width
                for w in range(out_h_w[1]):
                    if mode in ['normal']:
                        output[:, h, w] = np.sum(input[:, h * stride: h * stride + filter_size, 
                                                        w * stride: w * stride + filter_size, :] * filter, axis=(1, 2, 3))
                    elif mode in ['channel']:
                        for ch in range(np.shape(input)[3]):
                            output[:, h, w] += np.sum(input[:, h * stride: h * stride + filter_size, 
                                                          w * stride: w * stride + filter_size, ch] * filter[ch], axis=(1, 2))

        if mode == 'batch_filter':
            output = np.zeros((np.shape(input)[0], out_h_w[0], out_h_w[1], np.shape(input)[3]))
            for ch in range(np.shape(input)[3]):
                for h in range(out_h_w[0]):
                    for w in range(out_h_w[1]):
                        # use different filter at each batch
                        for b in range(np.shape(filter)[0]):
                            assert np.shape(input)[0] == np.shape(filter)[0], \
                            'input batch size and filter batch size not consistent!'
                            output[b, h, w, ch] = np.sum(input[b, h * stride: h * stride + filter_size, 
                                                                  w * stride: w * stride + filter_size, ch] * filter[b])
        return output
    
    def same_padding(self, input, filter_size):
        if  filter_size % 2 != 0:
            pad_left = (filter_size - 1) // 2
            pad_right = (filter_size - 1) // 2
        else:
            pad_left = filter_size // 2
            pad_right = filter_size // 2 + 1
        return np.pad(input, ((0, 0), (pad_left, pad_right), (pad_left, pad_right), (0, 0)), mode='constant')
    
    # input is (batch, size_h, size_w)
    # used in multiplication between (forward part of BP, backward part of BP)
    # check my CNN derivation for details 
    def put_zeros(self, input, stride, del_last_ele=False):
        if stride == 1:
            return input
        input_shape = np.shape(input)
        output = np.zeros((input_shape[0], input_shape[1] * stride, input_shape[2] * stride))
        
        for ch, h_w in enumerate(input):
            for h in range(input_shape[1]):
                for w in range(input_shape[2]):
                    output[ch, h * stride, w * stride] = h_w[h, w]

        if del_last_ele:
            return output[:, :-1, :-1]
        else:
            return output


class Activations:

    def __init__(self):
        pass
    
    def sigmoid(self, input):
        return 1. / (1. + np.exp(-input))
    
    def sigmoid_derivative(self, input):
        return self.sigmoid(input) * (1. - self.sigmoid(input))
    
    def relu(self, input):
        return np.where(input > 0, input, 0)
    
    def relu_derivative(self, input):
        output = np.where(self.relu(input) == 0, 0, 1)
        output = np.where(input == 0, 0.5, output)
        return output


class Loss:

    def __init__(self):
        pass
    
    def MSE(self, y, x):
        return (1 / 2) * (y - x) ** 2

    def MSE_derivative(self, y, x):
        return -1 * (y - x)
    
    def CE_derivative(self, y, x, eps=10e-10):
        return -1 * (x - y) / ((x - 1) * x + eps)


if __name__ == '__main__':

    if platform.system() == 'Windows':
        folder = 'C:/data/train_data'
        test_folder = 'C:/data/test_data'
    elif platform.system() == 'Linux':
        folder = '/home/shaoheng/Documents/PythonPractice/handwritedigit'

    batch = 10
    class_num = 10

    data_generator = DataGenerator(
        folder, batch, (16, 16), class_num=class_num)
    
    valid_data_gen = DataGenerator(
        test_folder, 160, (16, 16), class_num=class_num)
    valid_x, valid_y = valid_data_gen.load_data()

    train_data_gen = DataGenerator(
        folder, 320, (16, 16), class_num=class_num)
    train_full_x, train_full_y = train_data_gen.load_data()

    conv_1 = Conv2D(filter_size=3, channels=2, padding='same', stride=2, activation='relu')
    conv_2 = Conv2D(filter_size=3, channels=2, padding='same', stride=2, activation='relu')
    conv_3 = Conv2D(filter_size=3, channels=6, padding='same', stride=2, activation='relu')
    fc_1 = FC(nodes=10, activation='sigmoid')
    fc_2 = FC(nodes=12, activation='sigmoid')
    fc_3 = FC(nodes=20, activation='sigmoid')

    model = []
    model.append(conv_1)
    model.append(conv_2)
    model.append(conv_3)
    model.append(fc_1)

    def forward(x):
        for deep, now_layer in enumerate(model):
            if type(now_layer) == Conv2D and deep == 0:
                x = np.expand_dims(x, -1) 
            elif type(now_layer) == FC:
                x = np.reshape(x, (np.shape(x)[0], -1)) # flatten for feeding into FC
            x = now_layer.forward_prop(x)
        return x
    
    def backward(y):
        for deep, now_layer in enumerate(model[::-1]):
            if deep == 0:
                w, delta = now_layer.back_prop(label=y)
            else:
                if type(now_layer) == FC:
                    w, delta = now_layer.back_prop(w_nextlayer=w, delta_nextlayer=delta)
                elif type(now_layer) == Conv2D:
                    w, delta = now_layer.back_prop(w_nextlayer=w, delta_nextlayer=delta, next_layer=model[len(model) - deep])

    def batch_argmax(input):
        argmax = np.argmax(input, axis=1)
        output = np.zeros(np.shape(input))
        for b in range(np.shape(input)[0]):
            output[b, argmax[b]] = 1
        return output

    for i in range(1000000):

        x, y = data_generator.load_data()

        # forward
        forward(x)

        # backward
        backward(y)

        # overfitting and loss checking part
        if (i + 1) % 10 == 0: 
            prediction = forward(train_full_x)
            loss = np.sum(Loss().MSE(train_full_y, prediction))
            prediction = batch_argmax(prediction)
            acc = np.sum(prediction * train_full_y) / np.shape(prediction)[0]
            print('ite:{}, train_acc={}, loss={}'.format((i + 1), acc, loss)) 

        # validation
        if (i + 1) % 10 == 0:
            prediction = forward(valid_x)
            prediction = batch_argmax(prediction)
            acc = np.sum(prediction * valid_y) / np.shape(prediction)[0]
            print('ite:{}, valid_acc={} \n'.format((i + 1), acc)) 
            # print(fc_1.a)


