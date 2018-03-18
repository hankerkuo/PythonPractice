import numpy as np
import cv2
import matplotlib.pyplot as plt
# Load an color image in grayscale


for _ in range(5):
    img_Color = cv2.imread('ParkBoYoung.png', 1)
    print("Image shape = ",img_Color.shape)
    #img_Color = cv2.line(img_Color, (0, 0), (727, 463), (255, 0, 0), 5)
    img_Color = cv2.rectangle(img_Color, (200, 0), (500, 350), (0, 255, 0), 3)
    img_Color = cv2.circle(img_Color, (447, 300), 63, (0, 0, 255), 50)
    img_Color = cv2.circle(img_Color, (447, 300), 63, (0, 0, 0), 50)
    cv2.imshow('BY', img_Color)
    cv2.waitKey(0)
    '''
    img_Black = cv2.imread('ParkBoYoung.png', 0)
    cv2.imshow('BY', img_Black)
    '''
    img_Color = cv2.imread('ParkBoYoung.png', 0)
    cv2.imshow('BY', img_Color)
    cv2.waitKey(0)

cv2.imwrite('Park_JPG.jpg', img_Color, [10])
cv2.destroyAllWindows()


