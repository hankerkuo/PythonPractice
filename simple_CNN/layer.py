import numpy as np
from datagen import DataGenerator
import platform


class FC:

    # nodes is the hidden nodes number
    def __init__(self, nodes, activation):
        self.activation = activation
        self.nodes = nodes
        self.initialized = False

    def forward_prop(self, input):
        if not self.initialized:
            self.w = np.random.rand(self.nodes, np.shape(input)[1]) - 0.5
            self.b = np.zeros(self.nodes, dtype=float)
            self.initialized = True
        self.z = np.matmul(input, self.w.T) + self.b
        self.a = getattr(Activations(), self.activation)(self.z)
        self.a_previous = input

        return self.a

    def back_prop(self, label=False, w_nextlayer=None, delta_nextlayer=None):

        deri_a_wrt_z = getattr(Activations(), self.activation + '_derivative')(self.z)

        if label is False:
            # delta's first axis is also batch number, be familiar with matmul expression
            delta = np.squeeze(np.matmul(w_nextlayer.T, np.expand_dims(delta_nextlayer, axis=2)), axis=-1) * deri_a_wrt_z
        else:
            delta = Loss().MSE_derivative(label, self.a) * deri_a_wrt_z
        
        gradient_w = np.average(np.matmul(np.expand_dims(delta, axis=2), np.expand_dims(self.a_previous, axis=1)), axis=0)
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
        assert activation in ['sigmoid'], 'acitvation method not defined!'

        self.filter_size = filter_size
        self.channels = channels
        self.padding = padding
        self.stride = stride
        self.activation = activation
        self.initialized = False
    
    # input receive 4-dimension data [channels, batch, height, width] 
    def forward_prop(self, input):
        # saves the input 
        if self.padding == 'same':
            input = self.same_padding(input, self.filter_size)
        self.a_previous = input

        if not self.initialized:
            self.batch = np.shape(input)[1]
            self.out_h_w = np.floor((np.array(np.shape(input)[2: 4]) - self.filter_size) / self.stride + 1).astype('int')
            self.w = np.random.rand(self.channels, self.filter_size, self.filter_size) - 0.5
            self.b = np.zeros(self.channels, dtype=float)
            self.z = np.empty((self.channels, self.batch, self.out_h_w[0], self.out_h_w[1]))
            self.initialized = True

        # each channel
        for i, w in enumerate(self.w):
            self.z[i] = self.conv_operation(input, w, stride=self.stride, padding=self.padding)
        
        self.a = getattr(Activations(), self.activation)(self.z)

        return self.a
    
    def back_prop(self, label=False, w_nextlayer=None, delta_nextlayer=None, next_layer=None):
        
        delta = np.empty((self.channels, self.batch, self.out_h_w[0], self.out_h_w[1]))
        gradient_w = np.zeros((self.channels, self.batch, self.filter_size, self.filter_size))

        # each channel
        for i, z in enumerate(self.z):
            deri_a_wrt_z = getattr(Activations(), self.activation + '_derivative')(z)

            if next_layer == 'FC':
                w_next = w_nextlayer[:, i * self.out_h_w[0] * self.out_h_w[1]: (i + 1) * self.out_h_w[0] * self.out_h_w[1]]
                delta[i] = np.reshape(np.matmul(w_next.T, np.expand_dims(delta_nextlayer, axis=2)), 
                                        (self.batch, self.out_h_w[0], self.out_h_w[1])) * deri_a_wrt_z

            delta_put_zeros = self.put_zeros(delta[i], self.stride)
            gradient_w[i] += self.conv_operation(self.a_previous, delta_put_zeros, 1, padding='valid', batch_filter=True)

            self.w[i] -= 0.1 * np.average(gradient_w[i], axis=0)
            self.b[i] -= 0.1 * np.average(delta[i])

        return self.w, delta

    '''
    conv operation , output the conv result for a single output channel
    conv operation revceives 4-dimension data [channels, batch, height, width]
    batch_filter means to calculate every batch of sample with different filter, now used for back prop calculating ∂C/∂W
    '''
    def conv_operation(self, input, filter, stride, padding, batch_filter=False):
        # only support for square filter
        filter_size = np.shape(filter)[-1]

        out_h_w = np.floor((np.array(np.shape(input)[2: 4]) - filter_size) / stride + 1).astype('int')
        output = np.zeros((np.shape(input)[1], out_h_w[0], out_h_w[1]))
        
        if padding == 'same':
            input = self.same_padding(input, filter_size)
        elif padding == 'valid':
            pass

        if not batch_filter:
            # every channel from input layer
            for ch in range(np.shape(input)[0]):
                # height
                for h in range(np.shape(output)[1]):
                    # width
                    for w in range(np.shape(output)[2]):
                        output[:, h, w] += np.sum(input[ch, :, h * stride: h * stride + filter_size, 
                                                               w * stride: w * stride + filter_size] * filter, axis=(1, 2))
        if batch_filter:
            assert np.shape(input)[1] == np.shape(filter)[0], 'input batch size and filter batch size not consistent!'
            for ch in range(np.shape(input)[0]):
                for h in range(np.shape(output)[1]):
                    for w in range(np.shape(output)[2]):
                        # use different filter at each batch
                        for b in range(np.shape(filter)[0]):
                            output[b, h, w] += np.sum(input[ch, b, h * stride: h * stride + filter_size, 
                                                                   w * stride: w * stride + filter_size] * filter[b])
        return output
    
    def same_padding(self, input, filter_size):
        if  filter_size % 2 != 0:
            pad_left = (filter_size - 1) // 2
            pad_right = (filter_size - 1) // 2
        else:
            pad_left = filter_size // 2
            pad_right = filter_size // 2 + 1
        return np.pad(input, ((0, 0), (0, 0), (pad_left, pad_right), (pad_left, pad_right)), mode='constant')
    
    # input is (batch, size_h, size_w)
    # used in multiplication between (forward part of BP, backward part of BP)
    # check my CNN derivation for details 
    def put_zeros(self, input, stride):
        if stride == 1:
            return input
        input_shape = np.shape(input)
        output = np.zeros((input_shape[0], input_shape[1] * stride, input_shape[2] * stride))
        for h in range(input_shape[1]):
            for w in range(input_shape[2]):
                np.put(output[:], [h * stride, w * stride], input[:, h, w])
        return output




class Activations:

    def __init__(self):
        pass
    
    def sigmoid(self, input):
        return 1. / (1. + np.exp(-input))
    
    def sigmoid_derivative(self, input):
        return self.sigmoid(input) * (1. - self.sigmoid(input))


class Loss:

    def __init__(self):
        pass
    
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

    batch = 20
    class_num = 10

    data_generator = DataGenerator(
        folder, batch, (16, 16), class_num=class_num)
    
    valid_data_gen = DataGenerator(
        test_folder, 162, (16, 16), class_num=class_num)
    valid_x, valid_y = valid_data_gen.load_data()

    conv_1 = Conv2D(filter_size=3, channels=2, padding='same', stride=2, activation='sigmoid')
    fc_1 = FC(nodes=10, activation='sigmoid')

    def forward(x):
        x = np.expand_dims(x, 0)
        x = conv_1.forward_prop(x)
        x = np.swapaxes(x, 0, 1) # swap channel and batch
        x = np.reshape(x, (np.shape(x)[0], -1)) # flatten for feeding into FC
        x = fc_1.forward_prop(x)

        return x

    for i in range(1000000):

        x, y = data_generator.load_data()

        # forward
        forward(x)

        # backward
        w, delta = fc_1.back_prop(label=y)
        w, delta = conv_1.back_prop(w_nextlayer=w, delta_nextlayer=delta, next_layer='FC')

        # validation
        if (i + 1) % 10 == 0:
            true_prediction = 0
            for (x, y) in zip(valid_x, valid_y):
                x = np.expand_dims(x, 0)
                x = forward(x)
                if np.argmax(y) == np.argmax(x):
                    true_prediction += 1
            print('ite:{}, acc={}'.format((i + 1), true_prediction / 162))
