import numpy as np
import cv2
# Reference : https://marcin-chwedczuk.github.io/iterative-algorithm-for-drawing-hilbert-curve

#estimate the last 2 digit's "binary AND" with 3(Binary: 11)
def LastTwoDigit(D):
    return D & 3
'''
my basic 2X2 unit 
01 10
00 11   input : 00, output : 11
'''
def X_Coordinate_Hilbert(x):
    if x & 2 == 0:      #x binary and 10 == 00
        return 0
    elif x & 2 == 2:    #x binary and 10 == 10
        return 1

def y_Coordinate_Hilbert(y):
    if y & 2 == 0:      #y binary and 10 == 00
        return y & 1    #y binary and 01
    elif y & 2 == 2:    #y binary and 10 == 10
        return y ^ 3    #y binary XOR 11
'''
Hilbert function gives the corresponding coordinate of Index , N is the size of Hilbert curve
'''
def Hilbert(Index, N):
    count = Index
    '''
    Old version, if use this code, i should begin with value 4
    x = X_Coordinate_Hilbert(LastTwoDigit(Index))
    y = y_Coordinate_Hilbert(LastTwoDigit(Index))
    Index = Index >> 2
    '''
    x, y = (0, 0)
    i = 2
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
            x = -y + (Half_Of_N - 1) + Half_Of_N
            y = -t + (Half_Of_N - 1)
        Index = Index >> 2
        i *= 2
    #print("node", count,"x:", x,"y:", y)
    x, y = map(int, (x, y))
    return y, x
'''
Hilbert_Coordinate_to_Index function gives the corresponding Index of coordinate, N is the size of Hilbert curve
'''
def Hilbert_Coordinate_to_Index(x, y, N):
    Index = 0
    while(N >= 2):
        Half_Of_N = N / 2
        Cur_corr_x = 2 ** (2 * np.log2(N) - 1)
        Cur_corr_y = 2 ** (2 * np.log2(N) - 2)
        if x < Half_Of_N:
            if y < Half_Of_N:
                Index = Index + Cur_corr_x * 0 + Cur_corr_y * 0
                t = x
                x = y
                y = t
                N /= 2
                continue
            elif y >= Half_Of_N and y <= N - 1:
                Index = Index + Cur_corr_x * 0 + Cur_corr_y * 1
                y = y - Half_Of_N
                N /= 2
                continue
        elif x >= Half_Of_N and x <= N-1:
            if y >= Half_Of_N and y <= N - 1:
                Index = Index + Cur_corr_x * 1 + Cur_corr_y * 0
                x = x - Half_Of_N
                y = y - Half_Of_N
                N /= 2
                continue
            elif y < Half_Of_N:
                Index = Index + Cur_corr_x * 1 + Cur_corr_y * 1
                t = y
                y = -x + (Half_Of_N - 1) + Half_Of_N
                x = -t + (Half_Of_N - 1)
                N /= 2
                continue
    return int(Index)

'''
Main function begins
'''
N = 32
img = np.zeros((900, 900, 3), np.uint8) + 255   #make an empty image, the part "+255" is to make it white (original one is black)
Siz_Fix = int(900/N)                            #let the Hilbert curve fit the image size 900 * 900
for j in range(N*N-1):
    print('node', j, 'x:', Hilbert(j, N)[0], 'y:', Hilbert(j, N)[1])
    Start_x, Start_y = map(lambda x : x * Siz_Fix, Hilbert(j, N))
    End_x, End_y = map(lambda x : x * Siz_Fix, Hilbert(j + 1, N))
    cv2.line(img, (Start_x, 900 - Start_y), (End_x, 900 - End_y), (0, 140, 255), 3)
    cv2.imshow('Hilbert', img)
    cv2.waitKey(1)
cv2.waitKey(0)


