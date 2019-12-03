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
                ch_sz_next = np.shape(w_nextlayer)[0]
                filter_sz_next = np.shape(w_nextlayer)[1]
                w_next = np.rot90(w_nextlayer)
                delta_next = np.swapaxes(delta_nextlayer, 0, 1)
                delta_next = np.pad(delta_next, ((0, 0), (0, 0), (filter_sz_next - 1, filter_sz_next - 1)), mode='constant')
                w_by_delta = np.matmul(w_next, delta_next)
                for k in range(self.output_dim):
                    delta[i, :, k] = np.sum(np.diagonal (w_by_delta[:, :, k : k + filter_sz_next], axis1=1, axis2=2), axis=1)
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

    batch = 10
    class_num = 10

    data_generator = DataGenerator(
        folder, batch, (16, 16), class_num=class_num)
    
    valid_data_gen = DataGenerator(
        test_folder, 162, (16, 16), class_num=class_num)
    valid_x, valid_y = valid_data_gen.load_data()

    conv_1 = Conv1D(5, 2, 'same', 2, 'sigmoid')
    conv_2 = Conv1D(5, 4, 'same', 2, 'sigmoid')
    # fc_1 = FC(nodes=12, activation='sigmoid')
    fc_2 = FC(nodes=10, activation='sigmoid')

    for i in range(1000000):

        x, y = data_generator.load_data()
        x = np.reshape(x, (batch, 16 * 16))

        # forward
        x = conv_1.forward_prop(x)
        x = conv_2.forward_prop(x)
        # x = fc_1.forward_prop(x)
        x = fc_2.forward_prop(x)

        # backward
        w, delta = fc_2.back_prop(label=y)
        # w, delta = fc_1.back_prop(w_nextlayer=w, delta_nextlayer=delta)
        w, delta = conv_2.back_prop(w_nextlayer=w, delta_nextlayer=delta, next_layer='FC')
        conv_1.back_prop(w_nextlayer=w, delta_nextlayer=delta, next_layer='Conv1D')

        # validation
        if (i + 1) % 10 == 0:
            true_prediction = 0
            for (x, y) in zip(valid_x, valid_y):
                x = np.reshape(x, (1, 16 * 16))
                x = conv_1.forward_prop(x)
                x = conv_2.forward_prop(x)
                # x = fc_1.forward_prop(x)
                x = fc_2.forward_prop(x)
                if np.argmax(y) == np.argmax(x):
                    true_prediction += 1
            print('ite:{}, acc={}'.format((i + 1), true_prediction / 162))
