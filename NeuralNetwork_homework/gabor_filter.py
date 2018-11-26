import numpy as np
import cv2


def gabor(lst, ksize, sigma, theta, lambd, gamma, threshold=0):
    # getGaborKernel -> cv2.getGaborKernel(ksize, sigma, theta, lambd, gamma[, psi[, ktype]])
    kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma)
    result = np.ndarray(shape=(np.shape(lst)[0], np.shape(lst)[1]))
    pad_size = (ksize - 1) // 2
    lst = np.pad(lst, ((pad_size, pad_size), (pad_size, pad_size)), 'constant', constant_values=((0, 0), (0, 0)))
    for y in range(np.shape(result)[0]):
        for x in range(np.shape(result)[1]):
            result[y][x] = np.sum([ele[x:x + ksize] for ele in lst[y:y + ksize]] * kernel)
            if result[y][x] < threshold:
                result[y][x] = 0
    return result


'''
b = cv2.getGaborKernel((5, 5), 12, 90, np.pi, 1)
np.set_printoptions(precision=3, suppress=True)
print(b)
'''