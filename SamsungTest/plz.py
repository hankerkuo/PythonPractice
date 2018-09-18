import sys
a, b = sys.stdin.readline().split(' ')
maze = []
for i in range(int(a)):
    maze.append(sys.stdin.readline())

move_dic = {'U': [-1, 0], 'D': [1, 0], 'R': [0, 1], 'L': [0, -1]}
# ver2 - first element: 0 is y axis 1 is x axis, second element: +1 or -1
move_dic_ver2 = {'U': (0, -1), 'D': (0, +1), 'R': (1, +1), 'L': (1, -1)}

# find the positions of each item
for m, row in enumerate(maze):
    for n, column in enumerate(row):
        if column == 'R':
            redball_positon = [m, n]
        elif column == 'O':
            hole_position = [m, n]
        elif column == 'B':
            blueball_position = [m, n]


def to_next(point, dicrection):
    next = point[:]
    next[move_dic_ver2[dicrection][0]] = next[move_dic_ver2[dicrection][0]] + move_dic_ver2[dicrection][1]
    return next


def find_route_combine(red_po, blue_po):
    route = [[red_po, blue_po]]
    for play_times in range(10):
        target = route[:]
        route = []
        for item in target:
            red_po = item[-2]
            blue_po = item[-1]

            # speed up part
            break_loop = False
            for k in range(len(item) - 2):
                if item[k] == red_po and item[k + 1] == blue_po:
                    break_loop = True
            if break_loop is True:
                continue

            for direc in 'UDRL':
                red_now = red_po
                blue_now = blue_po
                red_wall = False
                blue_wall = False
                red_ball_in = False
                blue_ball_in = False

                while red_wall is False or blue_wall is False:
                    # if find the hole
                    if red_now == hole_position:
                        total_time = play_times + 1
                        red_ball_in = True
                    if blue_now == hole_position:
                        blue_ball_in = True
                        # print(route[-1])

                    if red_wall is False:
                        inner_red = red_now[:]
                        red_next = to_next(red_now, direc)
                        if maze[red_next[0]][red_next[1]] != '#':
                            red_now = red_next
                        elif maze[red_next[0]][red_next[1]] == '#':
                            red_wall = True

                    if blue_wall is False:
                        inner_blue = blue_now[:]
                        blue_next = to_next(blue_now, direc)
                        if maze[blue_next[0]][blue_next[1]] != '#':
                            blue_now = blue_next
                        elif maze[blue_next[0]][blue_next[1]] == '#':
                            blue_wall = True

                    if red_ball_in is False:
                        if red_now == blue_now:
                            if red_now == inner_red:
                                blue_now = inner_blue
                            if blue_now == inner_blue:
                                red_now = inner_red
                            break

                if red_ball_in and not blue_ball_in:
                    return total_time
                elif blue_ball_in:
                    continue
                else:
                    single_route = item[:]
                    single_route.append(red_now)
                    single_route.append(blue_now)
                    route.append(single_route)
    return -1


print(find_route_combine(redball_positon, blueball_position))