"""
To know more or get code samples, please visit my website:
https://morvanzhou.github.io/tutorials/
Or search: 莫烦Python
Thank you for supporting!
"""

# please note, all tutorial code are running under python3.5.
# If you use the version like python2.7, please modify the code accordingly

# 5 - Classifier example

import numpy as np
np.random.seed(1337)  # for reproducibility
# from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import RMSprop
from six.moves import cPickle as pickle

with open('./train_data/data.pickle', 'rb') as f:
    tr_dat = pickle.load(f)
with open('./train_data/label.pickle', 'rb') as f:
    tr_lab = pickle.load(f)
with open('./test_data/data.pickle', 'rb') as f:
    te_dat = pickle.load(f)
with open('./test_data/label.pickle', 'rb') as f:
    te_lab = pickle.load(f)

# data pre-processing
tr_dat = tr_dat.reshape(tr_dat.shape[0], -1)
te_dat = te_dat.reshape(te_dat.shape[0], -1)

# Another way to build your neural net
model = Sequential([
    Dense(32, input_dim=16*16),
    Activation('relu'),
    Dense(10),
    Activation('softmax'),
])

# Another way to define your optimizer
rmsprop = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)

# We add metrics to get more results you want to see
model.compile(optimizer=rmsprop,
              loss='categorical_crossentropy',
              metrics=['accuracy'])

print('Training ------------')
# Another way to train the model
model.fit(tr_dat, tr_lab, epochs=100, batch_size=32)

print('\nTesting ------------')
# Evaluate the model with the metrics we defined earlier
loss, accuracy = model.evaluate(te_dat, te_lab)

print('test loss: ', loss)
print('test accuracy: ', accuracy)

