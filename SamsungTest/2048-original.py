import sys
import copy

n = int(sys.stdin.readline())
maze = []
target = []
history = []
new_ones = []
for x in range(n):
    maze.append(sys.stdin.readline()[:-1].split(' '))
    maze[x] = list(map(int, maze[x]))


def left_zerobye(lst, n):
    for i in range(int(n)):
        try:
            zeros = lst[i].count(0)
            for j in range(zeros):
                lst[i].remove(0)
            for j in range(zeros):
                lst[i].append(0)
        except ValueError:
            break


def clockwise(lst):
    sedu = lst[:]
    result_1 = []
    for i in range(n):
        single = []
        for j in range(n - 1, -1, -1):
            single.append(sedu[j][i])
        result_1.append(single)
    return result_1


new_ones.append(maze[:])
history.append(maze[:])
# print(maze)
for plays in range(5):
    target = new_ones[:]
    new_ones = []
    for plate in target:
        # 3 rotations
        now_handle = copy.deepcopy(plate)
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
            if now_handle not in history:
                history.append(now_handle[:])
                new_ones.append(now_handle[:])
            now_handle = copy.deepcopy(plate)


# print(new_ones)
a = 2
for subarray in history:
    for subsubarray in subarray:
        for numbers in subsubarray:
            if a < numbers:
                a = numbers
print(a)

