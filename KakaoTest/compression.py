import readtxt


def compression(input_list):
    # initialize the dictionary
    dic = []
    for i in range(65, 91):
        dic.append(chr(i))
    # start to find compression output and add dictionary library
    current_pt = 0
    output_list = []
    while current_pt < len(input_list):
        end_pt = current_pt
        while input_list[current_pt:end_pt + 1] in dic and end_pt < len(input_list):
                end_pt += 1
        if end_pt < len(input_list):
            dic.append(input_list[current_pt:end_pt + 1])
        output_index = dic.index(input_list[current_pt:end_pt])
        output_list.append(output_index + 1)
        current_pt = end_pt
    return output_list, dic

prob2_input = readtxt.readfile_prob2()
for i in range(len(prob2_input)):
    print('input:', prob2_input[i])
    print('output:', compression(prob2_input[i])[0])
    print('dictionary:', compression(prob2_input[i])[1], '\n')

