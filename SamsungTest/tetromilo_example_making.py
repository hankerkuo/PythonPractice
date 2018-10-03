import numpy as np

N = np.random.random_integers(4, 10)
M = np.random.random_integers(1, 10)
vals = np.random.random_integers(1, 100, (N, M))
vals = vals.tolist()

print(N, M)
for i in range(N):
    for j in range(M):
        print(vals[i][j], end=' ')
    print("")


# import <something>

def tetromino(mat):
    x_size = len(mat)
    y_size = len(mat[0])
    biggest = 0

    tetro1 = [[0, 0], [0, 1], [0, 2], [0, 3]]
    tetro1_rot90 = [[0, 0], [1, 0], [2, 0], [3, 0]]
    tetro2 = [[0, 0], [0, 1], [1, 0], [1, 1]]
    tetro3 = [[0, 0], [1, 0], [2, 0], [2, 1]]
    tetro3_rot90 = [[0, 0], [0, 1], [0, 2], [1, 0]]
    tetro3_rot180 = [[0, 0], [0, 1], [1, 1], [2, 1]]
    tetro3_rot270 = [[0, 2], [1, 0], [1, 1], [1, 2]]
    tetro3_sym = [[0, 1], [1, 1], [2, 0], [2, 1]]
    tetro3_sym_rot90 = [[0, 0], [1, 0], [1, 1], [1, 2]]
    tetro3_sym_rot180 = [[0, 0], [0, 1], [1, 0], [2, 0]]
    tetro3_sym_rot270 = [[0, 0], [0, 1], [0, 2], [1, 2]]
    tetro4 = [[0, 0], [1, 0], [1, 1], [2, 1]]
    tetro4_rot90 = [[0, 1], [0, 2], [1, 0], [1, 1]]
    tetro4_sym = [[0, 1], [1, 0], [1, 1], [2, 0]]
    tetro4_sym_rot90 = [[0, 0], [0, 1], [1, 1], [1, 2]]
    tetro5 = [[0, 0], [0, 1], [0, 2], [1, 1]]
    tetro5_rot90 = [[0, 1], [1, 0], [1, 1], [2, 1]]
    tetro5_rot180 = [[0, 1], [1, 0], [1, 1], [1, 2]]
    tetro5_rot270 = [[0, 0], [1, 0], [1, 1], [2, 0]]

    tetro_all = [tetro1, tetro1_rot90, tetro2, tetro3, tetro3_rot90,
                 tetro3_rot180, tetro3_rot270, tetro3_sym, tetro3_sym_rot90,
                 tetro3_sym_rot180, tetro3_sym_rot270, tetro4, tetro4_rot90,
                 tetro4_sym, tetro4_sym_rot90, tetro5, tetro5_rot90,
                 tetro5_rot180, tetro5_rot270]

    for tetro in tetro_all:
        for x in range(0, x_size):
            for y in range(0, y_size):
                try:
                    part_sum = mat[x + tetro[0][0]][y + tetro[0][1]] + mat[x + tetro[1][0]][y + tetro[1][1]] + \
                               mat[x + tetro[2][0]][y + tetro[2][1]] + mat[x + tetro[3][0]][y + tetro[3][1]]
                    biggest = part_sum if part_sum > biggest else biggest
                except IndexError:
                    continue

    return biggest


if __name__ == "__main__":
    # mat_size = [int(x) for x in input().split(' ')]
    mat_size = [N, M]

    mat = []
    for n in range(0, mat_size[0]):
        temp = vals[n]
        mat.append(temp)

    result = tetromino(mat)
    print("ans:", result)