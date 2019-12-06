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
    matrix = conv.put_zeros(matrix, 2, del_last_ele=True)
    assert matrix.shape == (2, 5, 5)


def test_CNN_2D_with_CNN_2D():
    fc_layer = FC(10, 'sigmoid')
    conv_1 = Conv2D(filter_size=3, channels=2, padding='same', stride=1, activation='sigmoid')
    conv_2 = Conv2D(filter_size=3, channels=2, padding='same', stride=1, activation='sigmoid')

    x, y = data_generator.load_data()
    x = np.expand_dims(x, 0)  # the data is 1-channel, add the channel to the first axis

    x = conv_1.forward_prop(x)
    x = conv_2.forward_prop(x)
    x = np.swapaxes(x, 0, 1) # swap channel and batch
    x = np.reshape(x, (np.shape(x)[0], -1))
    x = fc_layer.forward_prop(x)

    w, delta = fc_layer.back_prop(label=y)
    w, delta = conv_2.back_prop(w_nextlayer=w, delta_nextlayer=delta, next_layer='FC')
    w, delta = conv_1.back_prop(w_nextlayer=w, delta_nextlayer=delta, next_layer='Conv2D')
    
    assert x.shape == (20, 10)
