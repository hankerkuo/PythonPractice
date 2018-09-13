import re


def readtxt():
    f = list(open('glassbead_escape_2.txt', 'r'))
    f[-1] = f[-1] + '\n' if f[-1][-1] != '\n' else f[-1]
    f = [a[:-1] for a in f]
    return f

data = readtxt()
maze = data[1:]
move_dic = {'U': [-1, 0], 'D': [1, 0], 'R': [0, 1], 'L': [0, -1]}
# for m, row in enumerate(maze):
#     redball_position = re.search(r'R', row)
#     if redball_position:
#         print(m + 1, redball_position.start() + 1)

# find the positions of each item
for m, row in enumerate(maze):
    for n, column in enumerate(row):
        if column == 'R':
            redball_positon = [m, n]
        elif column == 'O':
            hole_position = [m, n]
        elif column == 'B':
            blueball_position = [m, n]

def possible_way(map, point):
    way = ''
    if map[point[0] - 1][point[1]] != '#':
        way += 'U'
    if map[point[0] + 1][point[1]] != '#':
        way += 'D'
    if map[point[0]][point[1] + 1] != '#':
        way += 'R'
    if map[point[0]][point[1] - 1] != '#':
        way += 'L'
    return way

# redball_positon = [2,5]

# for direc in possible_way(maze, redball_positon):
#     start_point = redball_positon
#     single_route.append(start_point)
#     now_point = redball_positon
#     next_point = [now_point[n] + i for n, i in enumerate(move_dic[direc])]
#     while maze[next_point[0]][next_point[1]] != '#':
#         # if find the hole
#         if next_point == hole_position:
#             break
#         now_point = next_point
#         next_point = [next_point[n] + i for n, i in enumerate(move_dic[direc])]
#     single_route.append(now_point)
#     all_route.append(single_route)
#     single_route = []
#
# target = all_route[:]
# for item in target:
#     redball_positon = item[-1]
#     for direc in possible_way(maze, redball_positon):
#         print(direc)
#         start_point = redball_positon
#         single_route.append(start_point)
#         now_point = redball_positon
#         next_point = [now_point[n] + i for n, i in enumerate(move_dic[direc])]
#         while maze[next_point[0]][next_point[1]] != '#':
#             # if find the hole
#             if next_point == hole_position:
#                 break
#             now_point = next_point
#             next_point = [next_point[n] + i for n, i in enumerate(move_dic[direc])]
#         single_route.append(now_point)
#         all_route.append(single_route)
#         single_route = []

all_route = [[redball_positon]]

def find_route(redball_positon):
    single_route = []
    all_route = [[redball_positon]]
    for i in range(10):
        target = all_route[:]
        all_route = []
        for item in target:
            redball_positon = item[-1]
            for direc in possible_way(maze, redball_positon):
                print(direc)
                start_point = redball_positon
                single_route.append(start_point)
                now_point = redball_positon
                next_point = [now_point[n] + i for n, i in enumerate(move_dic[direc])]
                while maze[next_point[0]][next_point[1]] != '#':
                    # if find the hole
                    if next_point == hole_position:
                        print('found path:', i + 1)
                        return
                        break
                    now_point = next_point
                    next_point = [next_point[n] + i for n, i in enumerate(move_dic[direc])]
                single_route.append(item)
                single_route.append(now_point)
                all_route.append(single_route)
                single_route = []

find_route(redball_positon)
print(all_route)
