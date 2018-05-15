import numpy as np

input = np.array([[0, 0],
                  [0, 1],
                  [1, 0],
                  [1, 1]])


def layer1(x1, x2):
    output1 = -0.5 + x1 + x2
    output2 = 1.5 - x1 - x2
    if output1 >= 0:
        output1 = 1
    else:
        output1 = -1
    if output2 >= 0:
        output2 = 1
    else:
        output2 = -1
    return output1, output2


def output_layer(x1, x2):
    return x1 + x2 - 1


for i in range(4):
    # print(layer1(input[i][0], input[i][1]))
    print(output_layer(*layer1(input[i][0], input[i][1])))