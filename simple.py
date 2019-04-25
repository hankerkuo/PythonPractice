import numpy as np
import cv2

pic = cv2.imread('01.jpg')
a = np.array([1, 2])
pic_region = pic[0:100, 100:200]
pic_1 = cv2.imwrite('pic_1.jpg', pic_region)
print(pic_region.shape)