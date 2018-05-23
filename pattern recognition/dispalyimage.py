import numpy as np
import cv2
from six.moves import cPickle as pickle
from filter_operators import *

with open('./train_data/data.pickle', 'rb') as f:
    tr_dat = pickle.load(f)
with open('./train_data/label.pickle', 'rb') as f:
    tr_lab = pickle.load(f)
with open('./test_data/data.pickle', 'rb') as f:
    te_dat = pickle.load(f)
with open('./test_data/label.pickle', 'rb') as f:
    te_lab = pickle.load(f)


image = laplacian_operator(tr_dat)
image = cv2.resize(image[121], (100, 100))

cv2.imshow('random', image)
cv2.waitKey(0)