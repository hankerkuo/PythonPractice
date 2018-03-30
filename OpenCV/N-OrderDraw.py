import numpy as np
import cv2
# Reference : https://marcin-chwedczuk.github.io/iterative-algorithm-for-drawing-hilbert-curve

#estimate the last 2 digit's "binary AND" with 3(Binary: 11)
def LastTwoDigit(D):
    return D & 3
'''
my basic 2X2 unit 
01 11
00 10   input : 00, output : 11
'''
def X_Coordinate_N_Order(x):
    if x & 2 == 0:      #x binary and 10 == 00
        return 0
    elif x & 2 == 2:    #x binary and 10 == 10
        return 1

def y_Coordinate_N_Order(y):
    return y & 1        #x binary and 01
'''
N_Order function gives the corresponding coordinate of Index , N is the size of N_Order curve
'''
def N_Order(Index, N):
    count = Index
    x = X_Coordinate_N_Order(LastTwoDigit(Index))
    y = y_Coordinate_N_Order(LastTwoDigit(Index))
    Index = Index >> 2
    i = 4
    while(i <= N):
        Half_Of_N = i / 2
        Case = LastTwoDigit(Index)
        if Case == 0:
            1
        elif Case == 1:
            y = y + Half_Of_N
        elif Case == 2:
            x = x + Half_Of_N
        elif Case == 3:
            x = x + Half_Of_N
            y = y + Half_Of_N
        Index = Index >> 2
        i *= 2
    #print("node", count,"x:", x,"y:", y)
    x, y = map(int, (x, y))
    return x, y

'''
Main function begins
'''
N = 64
img = np.zeros((900, 900, 3), np.uint8) + 255   #make an empty image, the part "+255" is to make it white (original one is black)
Siz_Fix = int(900/N)                            #let the N_Order curve fit the image size 900 * 900
for j in range(N * N - 1):
    print('node', j, 'x:', N_Order(j, N)[0], 'y:', N_Order(j, N)[1])
    Start_x, Start_y = map(lambda x : x * Siz_Fix, N_Order(j, N))
    End_x, End_y = map(lambda x : x * Siz_Fix, N_Order(j + 1, N))
    cv2.line(img, (Start_x, Start_y), (End_x, End_y), (0, 140, 255), 2)
    cv2.imshow('N_Order', img)
    cv2.waitKey(1)
cv2.waitKey(0)