import platform
import numpy as np
import sys

sys.path.append('C:\github_projects\PythonPractice\simple_CNN')

from layer import Conv2D, FC
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
    folder, 20, (16, 16), class_num=10)

x, y = data_generator.load_data()
x = np.expand_dims(x, 0)  # the data is 1-channel, add the channel to the first axis
x = np.repeat(x, 7, axis=0)

kernel = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])


def test_for_x():
    assert x.shape == (7, 20, 16, 16)

def test_CNN_forwardprop():
    assert conv.forward_prop(x).shape == (2, 20, 16, 16)

def test_CNN_2D_with_FC():
    fc_layer = FC(10, 'sigmoid')
    conv = Conv2D(filter_size=3, channels=2, padding='same', stride=1, activation='sigmoid')

    x, y = data_generator.load_data()
    x = np.expand_dims(x, 0)  # the data is 1-channel, add the channel to the first axis

    x = conv.forward_prop(x)
    x = np.swapaxes(x, 0, 1) # swap channel and batch
    x = np.reshape(x, (np.shape(x)[0], -1))
    x = fc_layer.forward_prop(x)

    w, delta = fc_layer.back_prop(label=y)
    w, delta = conv.back_prop(w_nextlayer=w, delta_nextlayer=delta, next_layer='FC')
    

    assert x.shape == (20, 10)

def test_put_zeros():
    matrix = np.arange(18).reshape((2, 3, 3))
    conv = Conv2D(filter_size=3, channels=2, padding='same', stride=2, activation='sigmoid')
    matrix = conv.put_zeros(matrix, 2)
    assert matrix.shape == (2, 6, 6)
