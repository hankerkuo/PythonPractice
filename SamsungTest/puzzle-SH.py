import sys
row, col = map(int, sys.stdin.readline().split())
board = []
for _ in range(row):
    line = list(sys.stdin.readline())
    board.append(line)

direction = ((0,1),(1,0),(0,-1),(-1,0))

# total_position = []
r_position = [0, 0]
b_position = [0, 0]
g_position = [0, 0]

for n in range(row):
    for m in range(col):
        if board[n][m] == 'B':
            b_position = [n, m]
        elif board[n][m] == 'R':
            r_position = [n, m]
        elif board[n][m] == 'O':
            g_position = [n, m]


def move_board(que):
    result = 9999
    while len(que) != 0 :
        now_position = que[0]
        move_count = now_position[1]
        que.pop(0)

        for i in range(4):
            now_r_x = now_position[0][0][0]; now_r_y = now_position[0][0][1]
            now_b_x = now_position[0][1][0]; now_b_y = now_position[0][1][1]
            cr = 0; cb = 0

            #이동
            while (board[now_r_x + direction[i][0]][now_r_y + direction[i][1]] !="#" and
                    board[now_r_x][now_r_y] != "O"):
                now_r_x += direction[i][0]
                now_r_y += direction[i][1]
                cr += 1

            while(board[now_b_x + direction[i][0]][now_b_y + direction[i][1]] != "#" and
                  board[now_b_x][now_b_y] != "O"):
                now_b_x += direction[i][0]
                now_b_y += direction[i][1]
                cb +=1

            #겹치면 가까운거 이동

            if now_r_x == now_b_x and now_r_y == now_b_y:
                if board[now_r_x][now_r_y] == "O":
                    continue
                if cr > cb:
                    now_r_x -= direction[i][0]
                    now_r_y -= direction[i][1]
                else:
                    now_b_x -= direction[i][0]
                    now_b_y -= direction[i][1]

            # 만약 b가 O에 도착 끝
            if board[now_b_x][now_b_y] == "O":
                continue

            # r 이 O면 현재 에서 +1
            if board[now_r_x][now_r_y] == "O":
                # if move_count + 1 < result:
                #     result = move_count +1
                # return result
                return (move_count + 1)

            # 체크
            new_position = [[now_r_x, now_r_y], [now_b_x, now_b_y]]
            if new_position in total_position:
                continue
            # 이동 횟수남아 있으면 추가

            if move_count < 9:
                total_position.append(new_position)
                temp = []
                temp.append(new_position)
                temp.append(move_count + 1)
                que.append(temp)

    return -1

if __name__ == "__main__":
    for i in range(1000):
        total_position = []
        temp = []
        queue = []
        temp.append(r_position)
        temp.append(b_position)
        total_position.append(temp)

        queue.append([[r_position, b_position], 0])
        result = move_board(queue)

        print(result)