import numpy as np
import cv2

img = np.zeros((1024,512,3), np.uint8)
for i in range(5):
    cv2.line(img,(10+10*i,10),(20+10*i,10),(255,0,0),2)
    cv2.line(img,(20+10*i,10),(20+10*i,20),(255,0,0),2)
    cv2.line(img,(20+10*i,20),(10+10*i,20),(255,0,0),2)
cv2.imshow('BY', img)
cv2.waitKey(0)