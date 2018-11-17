import numpy as np
import cv2
from six.moves import cPickle as pickle
import filters

with open('./train_data/data.pickle', 'rb') as f:
    tr_dat = pickle.load(f)
with open('./train_data/label.pickle', 'rb') as f:
    tr_lab = pickle.load(f)
with open('./test_data/data.pickle', 'rb') as f:
    te_dat = pickle.load(f)
with open('./test_data/label.pickle', 'rb') as f:
    te_lab = pickle.load(f)

display = 12
tr_dat[display] = filters.laplacian(tr_dat[display], threshhold=0)
image = tr_dat[display]
image = cv2.resize(tr_dat[display], (200, 200))
cv2.imshow('BY', image)
cv2.waitKey(0)

print(tr_dat[display])