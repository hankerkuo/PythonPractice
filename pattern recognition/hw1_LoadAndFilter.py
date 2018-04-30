from six.moves import cPickle as pickle
from scipy import ndimage
import matplotlib.pyplot as plt
import numpy as np
import hw1_shuffleAndLabel as sf

# extract data and label set from pickle file
with open('./test_data/data_raw.pickle', 'rb') as f:
    a = pickle.load(f)
with open('./test_data/label_raw.pickle', 'rb') as f:
    b = pickle.load(f)
# extract data and label set from pickle file

# a = np.reshape(a, (-1, 16, 16, 1))
a_after_sobel = np.ndarray(shape=(np.shape(a)), dtype=np.float32)
a_after_prewitt = np.ndarray(shape=(np.shape(a)), dtype=np.float32)
a_after_laplacian = np.ndarray(shape=(np.shape(a)), dtype=np.float32)
a_after_gaussian_laplace = np.ndarray(shape=(np.shape(a)), dtype=np.float32)
for _ in range(160):
    a_after_sobel[_, :, :] = ndimage.sobel(a[_, :, :], 0)
    a_after_prewitt[_, :, :] = ndimage.prewitt(a[_, :, :], 0)
    a_after_laplacian[_, :, :] = ndimage.laplace(a[_, :, :])
    a_after_gaussian_laplace[_, :, :] = ndimage.gaussian_laplace(a[_, :, :], sigma=1)

print(a[2])
print(a_after_prewitt[2])
plt.imshow(a_after_gaussian_laplace[2], cmap='gray')
plt.show()