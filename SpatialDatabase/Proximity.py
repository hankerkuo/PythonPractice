import numpy as np
import cv2
import matplotlib.pyplot as plt

def LastTwoDigit(D):
    return D & 3
def X_Coordinate_N_Order(x):
    if x & 2 == 0:      #x binary and 10 == 00
        return 0
    elif x & 2 == 2:    #x binary and 10 == 10
        return 1
def y_Coordinate_N_Order(y):
    return y & 1        #x binary and 01
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
def Hilbert(Index, N):
    count = Index
    x = X_Coordinate_Hilbert(LastTwoDigit(Index))
    y = y_Coordinate_Hilbert(LastTwoDigit(Index))
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
    #print("node", count,"x:", x,"y:", y)
    x, y = map(int, (x, y))
    return x, y
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

N = 2
while (N <= 2**10):
    LSS_ColumnWise = 0
    LSS_Hilbert = 0
    LSS_N_Order = 0
    for j in range(N * N - 1):
        LSS_ColumnWise = LSS_ColumnWise + (ColumnWise(j, N, N)[0] - ColumnWise(j + 1, N, N)[0])**2 + (ColumnWise(j, N, N)[1] - ColumnWise(j + 1, N, N)[1])**2
        LSS_Hilbert = LSS_Hilbert + (Hilbert(j, N)[0] - Hilbert(j + 1, N)[0])**2 + (Hilbert(j, N)[1] - Hilbert(j + 1, N)[1])**2
        LSS_N_Order = LSS_N_Order + (N_Order(j, N)[0] - N_Order(j + 1, N)[0])**2 + (N_Order(j, N)[1] - N_Order(j + 1, N)[1])**2
    print('The LLS in ColunmWise :',LSS_ColumnWise,
          'The LLS in Hilbert :', LSS_Hilbert,
          'The LLS in N_Order :', LSS_N_Order, sep = '\n')
    plt.plot(N, LSS_ColumnWise, 'rv')
    plt.plot(N, LSS_Hilbert, 'b*')
    plt.plot(N, LSS_N_Order, 'y*')
    N *= 2
plt.show()
