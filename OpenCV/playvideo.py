import numpy as np
import cv2 as cv
cap = cv.VideoCapture('C:/OneDrive/文件/NRLab/Visual Computing/이교수님/presentation3(final project)/movie/Harry.Potter.and.the.Half-Blood.Prince.2009.Bluray.1080p.DTS-HD.x264-Grym.mkv')
while(cap.isOpened()):
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('frame', gray)
    if cv.waitKey(0) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()