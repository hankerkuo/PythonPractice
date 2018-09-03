dic = []
# initialize the dictionary
for i in range(65, 91):
    dic.append(chr(i))


def compression(input_list):
    current_pt = 0
    output_list = []
    while current_pt < len(input_list):
        end_pt = current_pt + 1
        while input_list[current_pt:end_pt] in dic and end_pt < len(input_list) + 1:
                end_pt += 1
        if end_pt < len(input_list) + 1:
            dic.append(input_list[current_pt:end_pt])
        output_index = dic.index(input_list[current_pt:end_pt - 1])
        output_list.append(output_index + 1)
        current_pt = end_pt - 1
    return output_list


print(compression('ABABABABABABABAB'))
print(dic)

