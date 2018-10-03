import sys

n = int(sys.stdin.readline())
maze = []
for x in range(n):
    maze.append(sys.stdin.readline()[:-1].split(' '))
    maze[x] = list(map(int, maze[x]))
sum = 0
for i in range(n):
    for j in range(n):
        sum += maze[i][j]

# print("total", sum)
def left_zerobye(lst, n):
    for i in range(int(n)):
        lst[i] = [y for y in lst[i] if y != 0]
        for j in range(n - len(lst[i])):
            lst[i].append(0)


def clockwise(lst):
    sedu = lst[:]
    result_1 = []
    for i in range(n):
        single = []
        for j in range(n - 1, -1, -1):
            single.append(sedu[j][i])
        result_1.append(single)
    return result_1


# for ccc in range(50):
def games():
    history = []
    new_ones = []
    new_ones.append(maze[:])
    history.append(maze[:])
    # print(maze)
    for plays in range(5):
        target = new_ones[:]
        new_ones = []
        for plate in target:
            # now_handle = copy.deepcopy(plate)
            now_handle = plate[:]
            # 3 rotations
            for i in range(4):
                for rots in range(i):
                    now_handle = clockwise(now_handle[:])
                left_zerobye(now_handle, n)
                # main game moving part
                for m in range(n):
                    pt = 0
                    while now_handle[m][pt] != 0 and pt < n - 1:
                        if now_handle[m][pt] == now_handle[m][pt + 1]:
                            now_handle[m][pt] *= 2
                            now_handle[m][pt + 1:] = now_handle[m][pt + 2:]
                            now_handle[m].append(0)
                        pt += 1

                min = 2
                for subarray in now_handle:
                    for numbers in subarray:
                        if min < numbers:
                            min = numbers
                if min * 2 > sum:
                    print(min)
                    return
                if now_handle not in history:
                    history.append(now_handle[:])
                    new_ones.append(now_handle[:])
                now_handle = plate[:]


    # print(new_ones)
    a = 2
    for subarray in history:
        for subsubarray in subarray:
            for numbers in subsubarray:
                if a < numbers:
                    a = numbers
    print(a)


games()

