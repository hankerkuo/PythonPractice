import numpy as np
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
            x = -y + (Half_Of_N -1) + Half_Of_N
            y = -t + (Half_Of_N -1)
        Index = Index >> 2
        i *= 2
    #print("node", count,"x:", x,"y:", y)
    x, y = map(int, (x, y))
    return x, y
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
def LastTwoDigit(D):
    return D & 3

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

def N_Order_Coordinate_to_Index(x, y, N):
    Index = 0
    while(N >= 2):
        Cur_corr_x = 2 ** (2 * np.log2(N) - 1)
        Cur_corr_y = 2 ** (2 * np.log2(N) - 2)
        if x < N / 2:
            if y < N / 2:
                Index = Index + Cur_corr_x * 0 + Cur_corr_y * 0
            elif y >= N / 2 and y <= N - 1:
                Index = Index + Cur_corr_x * 0 + Cur_corr_y * 1
                y = y - N / 2
        elif x >= N / 2 and x <= N-1:
            if y < N / 2:
                Index = Index + Cur_corr_x * 1 + Cur_corr_y * 0
                x = x - N / 2
            elif y >= N / 2 and y <= N - 1:
                Index = Index + Cur_corr_x * 1 + Cur_corr_y * 1
                x = x - N / 2
                y = y - N / 2
        N /= 2
    return int(Index)
def ColumnWise_Coordinate_to_Index(x, y, M, N):
    Index = 0
    if x % 2 == 0:                      #if the x coordinate is even, which means odd column
        Index = M * x + y
    elif x % 2 == 1:                    #if the x coordinate is odd, which means even column
        Index = M * x + (M - 1 - y)
    return int(Index)
def ColumnWise(Index, M, N):
    if Index > M * N - 1:
        print('WARNNING : Index is out of range, Index :', Index, 'Expected Maximum Index :', M * N -1)
    x = np.floor(Index / M)             #decide the x coordinate
    if x % 2 == 0:                      #if the x coordinate is even, which means odd column
        y = Index % M
    elif x % 2 == 1:                    #if the x coordinate is odd, which means even column
        y = M - (Index % M) - 1
    x, y = map(int, (x, y))
    return x, y

'''
Find_grid returns a list of coordinates (el.1 ~ el.8) in 9x9 adjacent range of target coordinate, for example,
el.6    el.7    el.8
el.4   Target   el.5
el.1    el.2    el.3
'''
def Find_grid(x, y, x_MAX, y_MAX, SideLength_Of_GridSize):
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
print(ColumnWise(ColumnWise_Coordinate_to_Index(0, 3, 5, 5), 5, 5))
'''
[[1.0, 1.0], [1.0, 2.0], [1.0, 3.0], [2.0, 1.0], [2.0, 2.0], [2.0, 3.0], [3.0, 1.0], [3.0, 2.0], [3.0, 3.0]]
'''