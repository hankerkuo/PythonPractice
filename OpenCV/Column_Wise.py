import numpy as np
import cv2
'''
ColumnWise function gives the corresponding coordinate of Index. M, N refer to the size of a M * N rectangle
'''
def ColumnWise(Index, M, N):
    if Index > M * N - 1:
        print('WARNNING : Index is out of range, Index :', Index, 'Expected Maximum Index :', M * N -1)
    x = np.floor(Index / M)
    if x % 2 == 0:
        y = Index % M
    elif x % 2 == 1:
        y = M - (Index % M) - 1
    x, y = map(int, (x, y))
    return x, y
'''
Main function begins, Beware of M can not be 1 here, which will make the curve a straight line
'''
M = 2
N = 30
if M == 1:
    print('ERROR : M cannot be 1')
elif M != 1:
    img = np.zeros((900, 900, 3), np.uint8) + 255   #make an empty image, the part "+255" is to make it white (original one is black)
    Siz_Fix_M = int(900/(M-1))                      #let the ColumnWise curve fit the image size 900 * 900, M for y-axis and N for x-axis
    Siz_Fix_N = int(900/N)
    for j in range(N * M - 1):
        Start_x, Start_y = ColumnWise(j, M, N)
        End_x, End_y = ColumnWise(j + 1, M, N)
        '''
        Start to fit the image scale.
        Result is equivalent with:
        Start_x = Start_x * Siz_Fix_N
        Start_y = Start_y * Siz_Fix_M
        End_x = End_x * Siz_Fix_N
        End_y = End_y * Siz_Fix_M
        '''
        Start_x, End_x = map(lambda x: x * Siz_Fix_N, (Start_x, End_x))
        Start_y, End_y = map(lambda x: x * Siz_Fix_M, (Start_y, End_y))
        '''
        Start to draw line
        '''
        cv2.line(img, (Start_x, Start_y), (End_x, End_y), (0, 140, 255), 3)
        cv2.imshow('N_Order', img)
        cv2.waitKey(1)
    cv2.waitKey(0)