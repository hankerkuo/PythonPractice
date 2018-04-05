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
    '''
    Old version, if use this code, i should begin with value 4
    x = X_Coordinate_N_Order(LastTwoDigit(Index))
    y = y_Coordinate_N_Order(LastTwoDigit(Index))
    Index = Index >> 2
    '''
    x, y = (0, 0)
    i = 2
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
N_Order_Coordinate_to_Index function gives the corresponding Index of coordinate, N is the size of N_Order curve
'''
def N_Order_Coordinate_to_Index(x, y, N):
    Index = 0
    while(N >= 2):
        Half_N = N / 2
        Cur_corr_x = 2 ** (2 * np.log2(N) - 1)
        Cur_corr_y = 2 ** (2 * np.log2(N) - 2)
        if x < Half_N:
            if y < Half_N:
                Index = Index + Cur_corr_x * 0 + Cur_corr_y * 0
            elif y >= Half_N and y <= N - 1:
                Index = Index + Cur_corr_x * 0 + Cur_corr_y * 1
                y = y - Half_N
        elif x >= Half_N and x <= N - 1:
            if y < Half_N:
                Index = Index + Cur_corr_x * 1 + Cur_corr_y * 0
                x = x - Half_N
            elif y >= Half_N and y <= N - 1:
                Index = Index + Cur_corr_x * 1 + Cur_corr_y * 1
                x = x - Half_N
                y = y - Half_N
        N /= 2
    return int(Index)
'''
Main function begins
'''
N = 32
img = np.zeros((900, 900, 3), np.uint8) + 255   #make an empty image, the part "+255" is to make it white (original one is black)
Siz_Fix = int(900/N)                            #let the N_Order curve fit the image size 900 * 900
for j in range(N * N - 1):
    print('node', j, 'x:', N_Order(j, N)[0], 'y:', N_Order(j, N)[1])
    Start_x, Start_y = map(lambda x : x * Siz_Fix, N_Order(j, N))
    End_x, End_y = map(lambda x : x * Siz_Fix, N_Order(j + 1, N))
    cv2.line(img, (Start_x, 900 - Start_y), (End_x, 900 - End_y), (0, 140, 255), 2)
    cv2.imshow('N_Order', img)
    cv2.waitKey(1)
cv2.waitKey(0)