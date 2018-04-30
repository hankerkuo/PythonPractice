# These are all the modules we'll be using later. Make sure you can import them
# before proceeding further.
from __future__ import print_function
import imageio
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import tarfile
from IPython.display import display, Image
from sklearn.linear_model import LogisticRegression
from six.moves.urllib.request import urlretrieve
from six.moves import cPickle as pickle
with open('./notMNIST_large/A.pickle', 'rb') as f:
    a = pickle.load(f)
print(a[0])
plt.imshow(a[2], cmap='gray', interpolation='bicubic')
plt.show()