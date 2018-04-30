"""
To know more or get code samples, please visit my website:
https://morvanzhou.github.io/tutorials/
Or search: 莫烦Python
Thank you for supporting!
"""

# 6 - CNN example

import numpy as np
np.random.seed(1337)  # for reproducibility
from keras.models import Sequential
from keras.layers import Dense, Activation, Convolution2D, MaxPooling2D, Flatten
from keras.optimizers import Adam
from six.moves import cPickle as pickle
import tensorflow as tf

with open('./train_data/data.pickle', 'rb') as f:
    tr_dat = pickle.load(f)
with open('./train_data/label.pickle', 'rb') as f:
    tr_lab = pickle.load(f)
with open('./test_data/data.pickle', 'rb') as f:
    te_dat = pickle.load(f)
with open('./test_data/label.pickle', 'rb') as f:
    te_lab = pickle.load(f)

# data pre-processing
tr_dat = tr_dat.reshape(-1, 1, 16, 16)
te_dat = te_dat.reshape(-1, 1, 16, 16)

# Another way to build your CNN
model = Sequential()

# Conv layer 1 output shape (32, 16, 16)
model.add(Convolution2D(
    batch_input_shape=(None, 1, 16, 16),
    filters=32,
    kernel_size=5,
    strides=1,
    padding='same',     # Padding method
    data_format='channels_first',
))
model.add(Activation('relu'))

# Pooling layer 1 (max pooling) output shape (32, 8, 8)
model.add(MaxPooling2D(
    pool_size=2,
    strides=2,
    padding='same',    # Padding method
    data_format='channels_first',
))

# Conv layer 2 output shape (64, 8, 8)
model.add(Convolution2D(64, 5, strides=1, padding='same', data_format='channels_first'))
model.add(Activation('relu'))

# Pooling layer 2 (max pooling) output shape (64, 4, 4)
model.add(MaxPooling2D(2, 2, 'same', data_format='channels_first'))

# # Fully connected layer 1 input shape (64 * 4 * 4) = (), output shape (1024)
# model.add(Flatten())
# model.add(Dense(1024))
# model.add(Activation('relu'))

# Fully connected layer 2 to shape (10) for 10 classes
model.add(Flatten())
model.add(Dense(10))
model.add(Activation('softmax'))

# Another way to define your optimizer
adam = Adam(lr=1e-4)

# We add metrics to get more results you want to see
model.compile(optimizer=adam,
              loss='categorical_crossentropy',
              metrics=['accuracy'])

print('Training ------------')
# Another way to train the model
model.fit(tr_dat, tr_lab, epochs=200, batch_size=36)

print('\nTesting ------------')
# Evaluate the model with the metrics we defined earlier
loss, accuracy = model.evaluate(te_dat, te_lab)

print('\ntest loss: ', loss)
print('\ntest accuracy: ', accuracy)

