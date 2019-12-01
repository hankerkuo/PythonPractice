import numpy as np
from datagen import DataGenerator
import platform

class FC:

    # nodes is the hidden nodes number
    def __init__(self, batch, feature_len, nodes, activation):
        self.batch = batch
        self.feature_len = feature_len
        self.activation = activation
        self.w = np.random.rand(nodes, self.feature_len) - 0.5
        self.b = np.zeros(nodes, dtype=float)
        self.z = np.empty((self.batch, nodes), dtype=float)
        self.a = np.empty((self.batch, nodes), dtype=float)
    
    def forward_prop(self, input):
        self.z = np.dot(input, self.w.T) + self.b
        self.a = getattr(Activations(), self.activation)(self.z)

        return self.a

    def back_prop(self, label=False, w_nextlayer=None, delta_nextlayer=None, a_previouslayer=None):
        if label is False:
            delta = np.dot(w_nextlayer.T, delta_nextlayer) * getattr(Activations(), self.activation + '_derivative')(self.z)
        else:
            delta = Loss().MSE_derivative(label, self.a) * getattr(Activations(), self.activation + '_derivative')(self.z)
        
        delta = np.average(delta, axis=0)
        gradient_w = np.average(np.dot(np.expand_dims(a_previouslayer, axis=2), np.expand_dims(delta, axis=0)), axis=0).T
        gradient_b = delta
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


if __name__ == '__main__':
    # x = np.random.rand(16, 15)
    # fc_layer1 = FC(x, 10, 'sigmoid')

    # for i in range(10):
    #     layer1_a = fc_layer1.forward_prop()

    #     layer2_w = np.random.rand(20, 10)
    #     layer2_delta = np.random.rand(20)

    #     layer1_w, layer1_delta = fc_layer1.back_prop(layer2_w, layer2_delta, x)

    #     print(layer1_w)
    if platform.system() == 'Windows':
        folder = 'C:/data/train_data'
    elif platform.system() == 'Linux':
        folder = '/home/shaoheng/Documents/PythonPractice/handwritedigit'

    batch = 10
    class_num = 10

    data_generator = DataGenerator(
        folder, batch, (16, 16), class_num=class_num)

    layer_1 = FC(batch, 256, 12, 'sigmoid')
    layer_2 = FC(batch, 12, 10, 'sigmoid')

    for i in range(1000000):

        x, y = data_generator.load_data()
        x = np.reshape(x, (batch, 16 * 16))

        layer1_a = layer_1.forward_prop(x)
        layer2_a = layer_2.forward_prop(layer1_a)

        layer2_w, layer2_delta = layer_2.back_prop(label=y, a_previouslayer=layer1_a)
        layer1_w, layer1_delta = layer_1.back_prop(w_nextlayer=layer2_w, delta_nextlayer=layer2_delta, a_previouslayer=x)

        if i % 100 == 0:
            true_prediction = 0
            for i in range(batch):
                if np.argmax(y[i]) == np.argmax(layer2_a[i]):
                    true_prediction += 1
            print(true_prediction / batch)
        
