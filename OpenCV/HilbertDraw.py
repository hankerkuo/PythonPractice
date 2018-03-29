import numpy as np
import cv2
# Reference : https://marcin-chwedczuk.github.io/iterative-algorithm-for-drawing-hilbert-curve

#estimate the last 2 digit's binary and with 011 (3)
def LastTwoDigit(D):
    return D & 3

def X_Coordinate(x):
    if x & 2 == 0:
        return 0
    elif x & 2 == 2:
        return 1

def y_Coordinate(y):
    if y & 2 == 0:
        return y & 1
    elif y & 2 == 2:
        return y ^ 3

def Hilbert(Index, N):
    count = Index
    x = X_Coordinate(LastTwoDigit(Index))
    y = y_Coordinate(LastTwoDigit(Index))
    Index = Index >> 2
    i = 4
    while(i <= N):
        Half_Of_N = i / 2
        Case = LastTwoDigit(Index)
        if Case == 0:
            t = x
            x = y
            y = t
        elif Case == 1:
            y = y + Half_Of_N
        elif Case == 2:
            x = x + Half_Of_N
            y = y + Half_Of_N
        elif Case == 3:
            t = x
            x = -y + (Half_Of_N -1) + Half_Of_N
            y = -t + (Half_Of_N -1)
        Index = Index >> 2
        i *= 2
    print("no.", count,"x:", x,"y:", y)
    x = int(x)
    y = int(y)
    return x,y

'''
Main function begins
'''
N = 64
img = np.zeros((900, 900, 3), np.uint8)
for i in range(N*N-1):
    cv2.line(img,(Hilbert(i,N)[0]*int(900/N),Hilbert(i,N)[1]*int(900/N)),
             (Hilbert(i+1,N)[0]*int(900/N),Hilbert(i+1,N)[1]*int(900/N)),(255,0,0),2)
    cv2.imshow('Hilbert', img)
    cv2.waitKey(1)
cv2.waitKey(0)


