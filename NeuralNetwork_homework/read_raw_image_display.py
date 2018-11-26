import cv2
import gabor_filter
import matplotlib as plt
import numpy as np

# getGaborKernel -> cv2.getGaborKernel(ksize, sigma, theta, lambd, gamma[, psi[, ktype]])
class Gb_filter:
    def __init__(self, ksize, sigma, theta, lambd, gamma, threshold):
        self.ksize = ksize
        self.sigma = sigma
        self.theta = theta
        self.lambd = lambd
        self.gamma = gamma
        self.threshold = threshold
    def process_on_image(self, image):
        image = gabor_filter.gabor(image, self.ksize, self.sigma, self.theta, self.lambd, self.gamma, self.threshold)
        return image

Gb = Gb_filter(ksize=3, sigma=12, theta=0, lambd=np.pi, gamma=15, threshold=0)
display_size = 150
display_digit = '1'
# final = np.zeros((display_size, display_size))
for i in range(1, 49):
    if i % 12 == 1:
        single_row = cv2.imread('HandWriteDigit/'+display_digit+'_'+str(i)+'.png', 0) / 255
        single_row = Gb.process_on_image(single_row)
        single_row = cv2.resize(single_row, (display_size, display_size))
    else:
        image = cv2.imread('HandWriteDigit/'+display_digit+'_'+str(i)+'.png', 0) / 255
        image = Gb.process_on_image(image)
        image = cv2.resize(image, (display_size, display_size))
        single_row = np.concatenate((single_row, image), axis=1)
    if i % 12 == 0 and i != 0:
        if i == 12:
            final = single_row
        else:
            final = np.concatenate((final, single_row), axis=0)
# image = gabor_filter.gabor(image, 3, 12, 0, np.pi, 100, threshold=0)
# print(np.shape(final))
# final = cv2.resize(final, (1568, 32))
cv2.imshow('1', final)
cv2.waitKey(0)