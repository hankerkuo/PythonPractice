import numpy as np
import cv2

def gabor_fn(sigma, theta, Lambda, psi, gamma):
    sigma_x = sigma
    sigma_y = float(sigma) / gamma

    # Bounding box
    nstds = 3  # Number of standard deviation sigma
    xmax = max(abs(nstds * sigma_x * np.cos(theta)), abs(nstds * sigma_y * np.sin(theta)))
    xmax = np.ceil(max(1, xmax))
    ymax = max(abs(nstds * sigma_x * np.sin(theta)), abs(nstds * sigma_y * np.cos(theta)))
    ymax = np.ceil(max(1, ymax))
    xmin = -xmax
    ymin = -ymax
    (y, x) = np.meshgrid(np.arange(ymin, ymax + 1), np.arange(xmin, xmax + 1))

    # Rotation
    x_theta = x * np.cos(theta) + y * np.sin(theta)
    y_theta = -x * np.sin(theta) + y * np.cos(theta)

    gb = np.exp(-.5 * (x_theta ** 2 / sigma_x ** 2 + y_theta ** 2 / sigma_y ** 2)) * np.cos(2 * np.pi / Lambda * x_theta + psi)
    return gb

def gabor(lst, ksize, sigma, theta, lambd, gamma, threshhold=0):
    # getGaborKernel -> cv2.getGaborKernel(ksize, sigma, theta, lambd, gamma[, psi[, ktype]])
    kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma)
    result = np.ndarray(shape=(np.shape(lst)[0], np.shape(lst)[1]))
    pad_size = (ksize - 1) // 2
    lst = np.pad(lst, ((pad_size, pad_size), (pad_size, pad_size)), 'constant', constant_values=((0, 0), (0, 0)))
    for y in range(np.shape(result)[0]):
        for x in range(np.shape(result)[1]):
            result[y][x] = np.sum([ele[x:x + ksize] for ele in lst[y:y + ksize]] * kernel)
            if result[y][x] < threshhold:
                result[y][x] = 0
    return result

a = cv2.getGaussianKernel(5, -1)
# getGaborKernel -> cv2.getGaborKernel(ksize, sigma, theta, lambd, gamma[, psi[, ktype]])
b = cv2.getGaborKernel((5, 5), 12, 90, np.pi, 1)
np.set_printoptions(precision=3, suppress=True)
print(b)