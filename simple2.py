import numpy as np
import cv2
from datetime import datetime

def LastTwoDigit(D):
    return D & 3
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
    return x, y
'''
Main function begins
'''
for i in range(50):
    startTime = datetime.now()
    N = 32
    img = np.zeros((900, 900, 3), np.uint8) + 255   #make an empty image, the part "+255" is to make it white (original one is black)
    Siz_Fix = int(900/N)                            #let the Hilbert curve fit the image size 900 * 900
    for j in range(N*N-1):
        print('node', j, 'x:', Hilbert(j, N)[0], 'y:', Hilbert(j, N)[1])
        Start_x, Start_y = map(lambda x : x * Siz_Fix, Hilbert(j, N))
        End_x, End_y = map(lambda x : x * Siz_Fix, Hilbert(j + 1, N))
        cv2.line(img, (Start_x, 900 - Start_y), (End_x, 900 - End_y), (0, 140, 255), 3)
    time = datetime.now() - startTime
    print(time)

