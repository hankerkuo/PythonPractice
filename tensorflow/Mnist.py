import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
# number 1 to 10 data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

image_0 = mnist.train.images[1]
image_0 = np.resize(image_0, (28, 28))
plt.imshow(image_0, cmap='Greys_r')
plt.show()