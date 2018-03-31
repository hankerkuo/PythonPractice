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

print(Hilbert_Coordinate_to_Index(0, 5, 8))
print(Hilbert(Hilbert_Coordinate_to_Index(12, 12, 16), 16))