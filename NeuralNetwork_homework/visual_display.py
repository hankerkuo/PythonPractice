import numpy as np
import cv2
from six.moves import cPickle as pickle
import filters
import gabor_filter

with open('./train_data/data.pickle', 'rb') as f:
    tr_dat = pickle.load(f)
with open('./train_data/label.pickle', 'rb') as f:
    tr_lab = pickle.load(f)
with open('./test_data/data.pickle', 'rb') as f:
    te_dat = pickle.load(f)
with open('./test_data/label.pickle', 'rb') as f:
    te_lab = pickle.load(f)

display = 20
# image = filters.laplacian(tr_dat[display], threshhold=0)
image = gabor_filter.gabor(tr_dat[display], 3, 12, 0, np.pi, 100, threshhold=0.9) +\
        gabor_filter.gabor(tr_dat[display], 3, 12, 45, np.pi, 1, threshhold=0.9) +\
        gabor_filter.gabor(tr_dat[display], 3, 12, 90, np.pi, 1, threshhold=0.9)

original_img = cv2.resize(tr_dat[display], (200, 200))
image = cv2.resize(image, (200, 200))

parellel_img = np.concatenate((original_img, image), axis=1)
cv2.imshow('BY', parellel_img)
cv2.waitKey(0)

print(tr_dat[display])