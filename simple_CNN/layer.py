import numpy as np
from datagen import DataGenerator
import platform


class FC:

    # nodes is the hidden nodes number
    def __init__(self, batch, feature_len, nodes, activation):
        self.activation = activation
        self.w = np.random.rand(nodes, feature_len) - 0.5
        self.b = np.zeros(nodes, dtype=float)
        self.z = np.empty((batch, nodes), dtype=float)
        self.a = np.empty((batch, nodes), dtype=float)
    
    def forward_prop(self, input):
        self.z = np.matmul(input, self.w.T) + self.b
        self.a = getattr(Activations(), self.activation)(self.z)

        return self.a

    def back_prop(self, label=False, w_nextlayer=None, delta_nextlayer=None, a_previouslayer=None):

        deri_a_wrt_z = getattr(Activations(), self.activation + '_derivative')(self.z)

        if label is False:
            # delta's first axis is also batch number, be familiar with matmul expression
            delta = np.squeeze(np.matmul(w_nextlayer.T, np.expand_dims(delta_nextlayer, axis=2)), axis=-1) * deri_a_wrt_z
        else:
            delta = Loss().CE_derivative(label, self.a) * deri_a_wrt_z
        
        # gradient_w = np.average(np.matmul(np.expand_dims(a_previouslayer, axis=2), np.expand_dims(delta, axis=1)), axis=0).T
        gradient_w = np.average(np.matmul(np.expand_dims(delta, axis=2), np.expand_dims(a_previouslayer, axis=1)), axis=0)
        gradient_b = np.average(delta, axis=0)
        self.w -= 0.1 * gradient_w
        self.b -= 0.1 * gradient_b

        return self.w, delta


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

    layer_1 = FC(batch, 256, 12, 'sigmoid')
    layer_2 = FC(batch, 12, 10, 'sigmoid')

    for i in range(1000000):

        x, y = data_generator.load_data()
        x = np.reshape(x, (batch, 16 * 16))

        layer1_a = layer_1.forward_prop(x)
        layer2_a = layer_2.forward_prop(layer1_a)

        layer2_w, layer2_delta = layer_2.back_prop(label=y, a_previouslayer=layer1_a)
        layer1_w, layer1_delta = layer_1.back_prop(w_nextlayer=layer2_w, delta_nextlayer=layer2_delta, a_previouslayer=x)

        if (i + 1) % 100 == 0:
            true_prediction = 0
            for (x, y) in zip(valid_x, valid_y):
                x = np.reshape(x, (1, 16 * 16))
                layer1_out = layer_1.forward_prop(x)
                layer2_out = layer_2.forward_prop(layer1_out)
                if np.argmax(y) == np.argmax(layer2_out):
                    true_prediction += 1
            print('ite:{}, acc={}'.format((i + 1), true_prediction / 162))
