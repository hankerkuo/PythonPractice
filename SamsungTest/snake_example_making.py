import numpy as np

board = np.random.random_integers(2, 10)
apple = np.random.random_integers(0, board * board)
turn = np.random.random_integers(1, 10)

def random_D_L():
    a = np.random.random_integers(0, 1)
    if a == 0:
        return 'L'
    else:
        return 'D'

lst =[]
lst_2 = []
R_D = []
vals = np.random.random_integers(1, board, (1000, 2))
vals = vals.tolist()
for item in vals:
    if item not in lst:
        lst.append(item)
# apple_position
vals_2 = np.random.random_integers(1, 50, (30))
vals_2 = vals_2.tolist()
for i in range(turn):
    R_D.append(random_D_L())
for item in vals_2:
    if item not in lst_2:
        lst_2.append(item)
lst_2.sort()


print(board)
print(apple)
for i in range(apple):
    print(lst[i][0], lst[i][1])
print(turn)
for i in range(turn):
    print(lst_2[i], R_D[i])


import sys

sys.setrecursionlimit(100000000)

# def input():
#     return sys.stdin.readline()[:-1]


N = board
K = apple
apple = []
for i in range(K):
    x, y = lst[i][0], lst[i][1]
    apple.append((x-1, y-1))

L = turn
change = []
for i in range(L):
    x, y = lst_2[i], R_D[i]
    change.append((int(x), y))

# arr = [뱀 존재 여부, 사과 존재 여부]
arr = []
for i in range(N):
    arr.append([[False, False] for x in range(N)])
arr[0][0][0] = True

for i in range(K):
    x = apple[i][0]
    y = apple[i][1]
    arr[x][y][1] = True

# move = [동, 남, 서, 북]
direction = [(0, 1), (1, 0), (0, -1), (-1, 0)]
move = 0
cnt = 0
result = 0
x, y = 0, 0
trace = [(0, 0)]
pointer = 0
while True:
    if cnt < L:
        if result == change[cnt][0]:
            while True:
                if change[cnt][1] == 'D':
                    move = (move+1) % 4
                else:
                    move = (move-1) % 4
                cnt += 1
                if cnt == L or change[cnt][0] != result:
                    break
    x += direction[move][0]
    y += direction[move][1]
    result += 1
    if (x < 0 or x >= N) or (y < 0 or y >= N) or arr[x][y][0]:
        print('ans:', result)
        exit()
    arr[x][y][0] = True
    trace.append((x, y))
    if not arr[x][y][1]:
        delx = trace[pointer][0]
        dely = trace[pointer][1]
        arr[delx][dely][0] = False
        pointer += 1
    else:
        arr[x][y][1] = False