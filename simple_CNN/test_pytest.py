import platform
import numpy as np
import sys

sys.path.append('C:\github_projects\PythonPractice\simple_CNN')
sys.path.append('C:\GithubProject\PythonPractice\simple_CNN')

from layer import Conv2D, FC, Activations
from datagen import DataGenerator


# def change_smth(kernel):
#     kernel = np.expand_dims(kernel, 0)

conv = Conv2D(3, 2, 'same', 1, 'sigmoid')

if platform.system() == 'Windows':
    folder = 'C:/data/train_data'
    test_folder = 'C:/data/test_data'
elif platform.system() == 'Linux':
    folder = '/home/shaoheng/Documents/PythonPractice/handwritedigit'

data_generator = DataGenerator(
    folder, 10, (16, 16), class_num=10)

def test_CNN_2D_with_FC():
    fc_layer = FC(10, 'sigmoid')
    conv = Conv2D(filter_size=3, channels=2, padding='same', stride=1, activation='sigmoid')

    x, y = data_generator.load_data()
    x = np.expand_dims(x, -1)  # the data is 1-channel, add the channel to the last axis

    x = conv.forward_prop(x)
    x = np.reshape(x, (np.shape(x)[0], -1))
    x = fc_layer.forward_prop(x)

    w, delta = fc_layer.back_prop(label=y)
    w, delta = conv.back_prop(w_nextlayer=w, delta_nextlayer=delta, next_layer='FC')
    
    assert x.shape == (10, 10)

def test_put_zeros():
    matrix = np.arange(18).reshape((2, 3, 3))
    conv = Conv2D(filter_size=3, channels=2, padding='same', stride=2, activation='sigmoid')
    matrix = conv.put_zeros(matrix, 2, del_last_ele=True)
    print(matrix)
    assert matrix.shape == (2, 5, 5)


def test_CNN_2D_with_CNN_2D():
    fc_layer = FC(10, 'sigmoid')
    conv_1 = Conv2D(filter_size=3, channels=2, padding='same', stride=1, activation='sigmoid')
    conv_2 = Conv2D(filter_size=5, channels=4, padding='same', stride=2, activation='sigmoid')

    x, y = data_generator.load_data()
    x = np.expand_dims(x, -1)  # the data is 1-channel, add the channel to the last axis

    x = conv_1.forward_prop(x)
    x = conv_2.forward_prop(x)

    x = np.reshape(x, (np.shape(x)[0], -1))
    x = fc_layer.forward_prop(x)

    w, delta = fc_layer.back_prop(label=y)
    w, delta = conv_2.back_prop(w_nextlayer=w, delta_nextlayer=delta, next_layer='FC')
    w, delta = conv_1.back_prop(w_nextlayer=w, delta_nextlayer=delta, next_layer='Conv2D')
    
    assert x.shape == (10, 10)


def test_relu_activation():
    matrix = np.arange(9).reshape((3, 3)) - 5
    relu = Activations().relu
    relu_deri = Activations().relu_derivative
    matrix_after_relu = relu(matrix)
    print(matrix_after_relu)
    matrix_relu_deri = relu_deri(matrix)
    print(matrix_relu_deri)
    assert matrix_after_relu.shape == (3, 3)
    
if __name__ == '__main__':
    test_relu_activation()
