import numpy as np
import cv2

# Load an color image in grayscale


for _ in range(5):
    img_Color = cv2.imread('ParkBoYoung.png', 1)
    cv2.imshow('BY', img_Color)
    cv2.waitKey(50)
    '''
    img_Black = cv2.imread('ParkBoYoung.png', 0)
    cv2.imshow('BY', img_Black)
    '''
    img_Color = cv2.imread('ParkBoYoung.png', 1)
    cv2.imshow('BY', img_Color)
    cv2.waitKey(50)

cv2.imwrite('Park_JPG.jpg', img_Color, [10])
cv2.destroyAllWindows()


