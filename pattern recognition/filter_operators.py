import numpy as np
from scipy import ndimage
import cv2


def Relu_threshold(input, threshold=3):
    for height in range(np.shape(input)[0]):
        for width in range(np.shape(input)[1]):
            if input[height, width] <= threshold:
                input[height, width] = 0
    output = input
    return output


def sobel_operator(input, threshold=3):
    input_y = np.ndarray(shape=(np.shape(input)[1:]), dtype=np.float32)
    input_x = np.ndarray(shape=(np.shape(input)[1:]), dtype=np.float32)
    output = np.ndarray(shape=(np.shape(input)), dtype=np.float32)
    for _ in range(len(input)):
        input_y[:, :] = ndimage.sobel(input[_, :, :], 0)
        input_x[:, :] = ndimage.sobel(input[_, :, :], 1)
        output[_, :, :] = np.sqrt(np.square(input_x[:, :]) + np.square(input_y[:, :]))
        output[_, :, :] = Relu_threshold(output[_, :, :], threshold=threshold)
    return output


def prewitt_operator(input, threshold=3):
    input_y = np.ndarray(shape=(np.shape(input)[1:]), dtype=np.float32)
    input_x = np.ndarray(shape=(np.shape(input)[1:]), dtype=np.float32)
    output = np.ndarray(shape=(np.shape(input)), dtype=np.float32)
    for _ in range(len(input)):
        input_y[:, :] = ndimage.prewitt(input[_, :, :], 0)
        input_x[:, :] = ndimage.prewitt(input[_, :, :], 1)
        output[_, :, :] = np.sqrt(np.square(input_x[:, :]) + np.square(input_y[:, :]))
        output[_, :, :] = Relu_threshold(output[_, :, :], threshold=threshold)
    return output


def laplacian_operator(input):
    output = np.ndarray(shape=(np.shape(input)), dtype=np.float32)
    for _ in range(len(input)):
        output[_, :, :] = ndimage.laplace(input[_, :, :])
    return output


def gaussian_laplace_operator(input):
    output = np.ndarray(shape=(np.shape(input)), dtype=np.float32)
    for _ in range(len(input)):
        output[_, :, :] = ndimage.gaussian_laplace(input[_, :, :], sigma=1)
    return output


