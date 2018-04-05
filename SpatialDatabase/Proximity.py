import numpy as np
import cv2
import matplotlib.pyplot as plt
from datetime import datetime
'''
estimate the last 2 digit's "binary AND" with 3(Binary: 11)
'''
def LastTwoDigit(D):
    return D & 3
'''
N_Order function gives the corresponding coordinate of Index , N is the size of N_Order curve
'''
def N_Order(Index, N):
    x, y = (0, 0        )
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
    x, y = map(int, (x, y))
    return np.array([x, y])
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
Hilbert function gives the corresponding coordinate of Index , N is the size of Hilbert curve
'''
def Hilbert(Index, N):
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
            x = -y + (Half_Of_N -1) + Half_Of_N
            y = -t + (Half_Of_N -1)
        Index = Index >> 2
        i *= 2
    x, y = map(int, (x, y))
    return np.array([x, y])
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
    return np.array([x, y])
'''
ColumnWise_Coordinate_to_Index function gives the corresponding Index of coordinate, M, N refer to the size of a M * N rectangle
'''
def ColumnWise_Coordinate_to_Index(x, y, M, N):
    Index = 0
    if x % 2 == 0:                      # if the x coordinate is even, which means odd column
        Index = M * x + y
    elif x % 2 == 1:                    # if the x coordinate is odd, which means even column
        Index = M * x + (M - 1 - y)
    return int(Index)
'''
Find_grid returns a list of coordinates (el.1 ~ el.n*n) in n(SideLength_Of_GridSize)*n adjacent range of target coordinate, for example,
el    ...   -->    ...  el.n*n
el    ...  Target  ...  el.n*2
el.1  ...   -->    ...  el.n
AND THE　SideLength_Of_GridSize　MUST BE ODD NUMBER
'''
def Find_grid(x, y, x_MAX, y_MAX, SideLength_Of_GridSize):
    if SideLength_Of_GridSize % 2 == 0:
        print('WARNING : Side length must be odd number, Find_grid function ends')
        return 0
    Half_SOG = SideLength_Of_GridSize / 2
    el = np.array([x, y]) - np.array([np.floor(Half_SOG), np.floor(Half_SOG)])
    Result_Corr = []
    for Corr_y in range(0, SideLength_Of_GridSize):
        for Corr_x in range(0, SideLength_Of_GridSize):
            curr = el + np.array([Corr_x, Corr_y])
            curr_x = curr[0]
            curr_y = curr[1]
            if x_MAX >= curr_x >= 0 and y_MAX >= curr_y >= 0:
                Result_Corr.append(list(curr))
    return Result_Corr
'''
First part - Determine the 2D data distance LLS in the order of 1D data index 
'''
N = 2
while (N <= 2**0):                          #The power part means the loop times we want to iterate, '0' means there's no loop
    startTime = datetime.now()
    LSS_ColumnWise = 0
    LSS_Hilbert = 0
    LSS_N_Order = 0
    for j in range(N * N - 1):
        LSS_ColumnWise += (np.sum((ColumnWise(j, N, N) - ColumnWise(j + 1, N, N)) ** 2)) ** 0.5
        LSS_Hilbert += (np.sum((Hilbert(j, N) - Hilbert(j + 1, N)) ** 2)) ** 0.5
        LSS_N_Order += (np.sum((N_Order(j, N) - N_Order(j + 1, N)) ** 2)) ** 0.5
    print('The number', '%2i' % np.log2(N),'average distance in ColunmWise :', '%-10.2f' % (LSS_ColumnWise / (N * N - 1)),
          'Hilbert :', '%-10.2f' % (LSS_Hilbert / (N * N - 1)),
          'N_Order :', '%-10.2f' % (LSS_N_Order / (N * N - 1)))
    plt.plot(N, LSS_ColumnWise / (N * N - 1), 'rs')
    plt.plot(N, LSS_Hilbert / (N * N - 1), 'b*')
    plt.plot(N, LSS_N_Order / (N * N - 1), 'gx')
    N *= 2
    print(datetime.now() - startTime)
plt.show()
'''
Second part - Determine the 1D data distance in the adjacent n*n square of 2D data
'''
N = 2                                                                       # cuver starts at N*N situation
while (N <= 2**6):                                                          # The power part means the loop times we want to iterate, '0' means there's no loop
    LSS_ColumnWise = 0
    LSS_Hilbert = 0
    LSS_N_Order = 0
    for y in range(N):                                                      # The 1st and 2nd layer of loop go through all the points in the curver
        for x in range(N):
            Adja_Corr = Find_grid(x, y, N - 1, N - 1, 3)
            Amount = len(Adja_Corr)
            Index_ColumnWise = ColumnWise_Coordinate_to_Index(x, y, N, N)
            Index_Hilbert = Hilbert_Coordinate_to_Index(x, y, N)
            Index_N_Order = N_Order_Coordinate_to_Index(x, y, N)
            for i in range(Amount):                                         # The 3rd layer of loop is to find all of the adjacent points of the target point
                Corr_x = Adja_Corr[i][0]
                Corr_y = Adja_Corr[i][1]
                C_Adja_Corr_Index = ColumnWise_Coordinate_to_Index(Corr_x, Corr_y, N, N)
                H_Adja_Corr_Index = Hilbert_Coordinate_to_Index(Corr_x, Corr_y, N)
                N_Adja_Corr_Index = N_Order_Coordinate_to_Index(Corr_x, Corr_y, N)
                LSS_ColumnWise += abs(Index_ColumnWise - C_Adja_Corr_Index)
                LSS_Hilbert += abs(Index_Hilbert - H_Adja_Corr_Index)
                LSS_N_Order += abs(Index_N_Order - N_Adja_Corr_Index)
    print('The number', '%2i' % np.log2(N), 'average distance in ColunmWise :', '%-10i' % (LSS_ColumnWise / (N * N)),
          'Hilbert :', '%-10i' % (LSS_Hilbert / (N * N)),
          'N_Order :', '%-10i' % (LSS_N_Order / (N * N)))
    plt.plot(N, LSS_ColumnWise / (N * N), 'rs')
    plt.plot(N, LSS_Hilbert / (N * N), 'b*')
    plt.plot(N, LSS_N_Order / (N * N), 'gx')
    N *= 2
plt.show()





