import cv2
import gabor_filter
import matplotlib as plt
import numpy as np

# getGaborKernel -> cv2.getGaborKernel(ksize, sigma, theta, lambd, gamma[, psi[, ktype]])

Gb = gabor_filter.Gb_filter(ksize=3, sigma=12, theta=0, lambd=np.pi, gamma=15, threshold=0)
Gb_2 = gabor_filter.Gb_filter(ksize=3, sigma=12, theta=45, lambd=np.pi, gamma=15, threshold=0)
display_size = 150
display_digit = '2'
# final = np.zeros((display_size, display_size))
for display_digit in range(10):
    display_digit = str(display_digit)
    for i in range(1, 49):
        if i % 12 == 1:
            single_row = cv2.imread('HandWriteDigit/'+display_digit+'_'+str(i)+'.png', 0) / 255
            # single_row = Gb.process_on_image(single_row)
            single_row = gabor_filter.double_Gabor(single_row, Gb, Gb_2)
            single_row = cv2.resize(single_row, (display_size, display_size))
        else:
            image = cv2.imread('HandWriteDigit/'+display_digit+'_'+str(i)+'.png', 0) / 255
            # image = Gb.process_on_image(image)
            image = gabor_filter.double_Gabor(image, Gb, Gb_2)
            image = cv2.resize(image, (display_size, display_size))
            single_row = np.concatenate((single_row, image), axis=1)
        if i % 12 == 0 and i != 0:
            if i == 12:
                final = single_row
            else:
                final = np.concatenate((final, single_row), axis=0)

    final = final * 255
    cv2.imwrite('double_gabor_{}.jpg'.format(display_digit), final)
# cv2.imshow('digit_amount48', final)
# cv2.waitKey(0)