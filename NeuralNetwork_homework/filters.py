'''
implementation of filters for 2D array (lst)
'''

import numpy as np

def sobel(lst, threshhold=0):
    sobel_x = np.array([[-1,  0,  1],
                        [-2,  0,  2],
                        [-1,  0,  1]])
    sobel_y = np.array([[ 1,  2,  1],
                        [ 0,  0,  0],
                        [-1, -2, -1]])
    result = np.ndarray(shape=(np.shape(lst)[0], np.shape(lst)[1]))
    lst = np.pad(lst, ((1, 1), (1, 1)), 'constant', constant_values=((0, 0), (0, 0)))
    for y in range(np.shape(result)[0]):
        for x in range(np.shape(result)[1]):
            result[y][x] = np.sqrt(np.power(np.sum([ele[x:x + 3] for ele in lst[y:y + 3]] * sobel_x), 2) +
                                   np.power(np.sum([ele[x:x + 3] for ele in lst[y:y + 3]] * sobel_y), 2))
            if result[y][x] < threshhold:
                result[y][x] = 0
    return result

def prewitt(lst, threshhold=0):
    prewitt_x = np.array([[-1,  0,  1],
                          [-1,  0,  1],
                          [-1,  0,  1]])
    prewitt_y = np.array([[ 1,  1,  1],
                          [ 0,  0,  0],
                          [-1, -1, -1]])
    result = np.ndarray(shape=(np.shape(lst)[0], np.shape(lst)[1]))
    lst = np.pad(lst, ((1, 1), (1, 1)), 'constant', constant_values=((0, 0), (0, 0)))
    for y in range(np.shape(result)[0]):
        for x in range(np.shape(result)[1]):
            result[y][x] = np.sqrt(np.power(np.sum([ele[x:x + 3] for ele in lst[y:y + 3]] * prewitt_x), 2) +
                                   np.power(np.sum([ele[x:x + 3] for ele in lst[y:y + 3]] * prewitt_y), 2))
            if result[y][x] < threshhold:
                result[y][x] = 0
    return result

def laplacian(lst, threshhold=0):
    laplacian = np.array([[ 0,  1,  0],
                          [ 1, -4,  1],
                          [ 0,  1,  0]])
    result = np.ndarray(shape=(np.shape(lst)[0], np.shape(lst)[1]))
    lst = np.pad(lst, ((1, 1), (1, 1)), 'constant', constant_values=((0, 0), (0, 0)))
    for y in range(np.shape(result)[0]):
        for x in range(np.shape(result)[1]):
            result[y][x] = np.sum([ele[x:x + 3] for ele in lst[y:y + 3]] * laplacian)
            if result[y][x] < threshhold:
                result[y][x] = 0
    return result

def laplacian_of_guassian(lst, threshhold=0):
    laplacian = np.array([[ 0,  0, -1,  0,  0],
                          [ 0, -1, -2, -1,  0],
                          [-1, -2, 16, -2, -1],
                          [ 0, -1, -2, -1,  0],
                          [ 0,  0, -1,  0,  0]])
    result = np.ndarray(shape=(np.shape(lst)[0], np.shape(lst)[1]))
    lst = np.pad(lst, ((2, 2), (2, 2)), 'constant', constant_values=((0, 0), (0, 0)))
    for y in range(np.shape(result)[0]):
        for x in range(np.shape(result)[1]):
            result[y][x] = np.sum([ele[x:x + 5] for ele in lst[y:y + 5]] * laplacian)
            if result[y][x] < threshhold:
                result[y][x] = 0
    return result

