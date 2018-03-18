import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('pad.jpg', 1)
print(img.shape)

# resize the shape of image (due to my laptop's situation)
img = cv2.resize(img, (564, 1000))
print("fixed shape =",img.shape)

# m = no. of sample, n = no. of features
m = 30
n = 3

# make a matrix to save input data in the form of (single row): [1, Blue, Green, Red]
color = np.zeros((m, n), dtype=float)

'''
count = 0
color_RGB = 2
for i in range(536, 536 + 94):
    for j in range(0, 94):
        color[0] += img[i, j]
        color[1] += img[i, j  +94]
        color[2] += img[i, j + 94 * 2]
        color[3] += img[i, j + 94 * 3]
        color[4] += img[i, j + 94 * 4]
        color[5] += img[i, j + 94 * 5]
        count += 1
        #print(color)
'''
# add X0 to the first column
color = np.c_[np.ones((m, 1)), color]

for _ in range(6):
    #print("everage blue color = {:.0f}".format(color[_]))
    print("everage blue color = ", np.ceil(color[_]))
# start to access the BGR information , in openCV, image is loaded in order: B>G>R (0>1>2)
for i in range(0, 5):
    for j in range(0, 6):
        color[i * 6 + j] = [1,
                            np.sum(img[(536 + 94 * i):(536 + 94 * i + 94), (94 * j):(94 * j + 94)][:, :, 0]),
                            np.sum(img[(536 + 94 * i):(536 + 94 * i + 94), (94 * j):(94 * j + 94)][:, :, 1]),
                            np.sum(img[(536 + 94 * i):(536 + 94 * i + 94), (94 * j):(94 * j + 94)][:, :, 2])]
        #print(i,"*",j," = ",np.sum(img[(536 + 94 * i):(536 + 94 * i + 94), (94 * j):(94 * j +94)][:,:,0]))
        print(np.ceil(color/(94 * 94)))

# change into matplolib's order: R>G>B, and display it
b,g,r = cv2.split(img)
img = cv2.merge((r,g,b))
plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.show()

#cv2.imshow('jpg', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
