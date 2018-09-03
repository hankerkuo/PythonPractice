# the function to for transfer decimal system number to different system number
# 'sys' means the carry system category, e.g. binary system, sys = 2
def decimal_to_n(deci_num, sys):
    final = []
    while deci_num > sys - 1:
        remainder = deci_num % sys
        quotient = int(deci_num / sys)
        final.append(remainder)
        deci_num = quotient
    final.append(deci_num)
    final.reverse()
    if sys > 10:
        final = A_to_F(final)
    return final


# if the carry system is larger than 10, substitute 10~15 with A to F
def A_to_F(list):
    for n, i in enumerate(list):
        if i == 10:
            list[n] = 'A'
        if i == 11:
            list[n] = 'B'
        if i == 12:
            list[n] = 'C'
        if i == 13:
            list[n] = 'D'
        if i == 14:
            list[n] = 'E'
        if i == 15:
            list[n] = 'F'
    return list


# main function, the demand of the question
def n_carry_game(n, t, m, p):
    all_array = []
    result_array = []
    add = 0
    while len(all_array) < 10 ** 5:
        all_array.extend(decimal_to_n(add, n))
        add += 1
    # print(all_array)
    for i in range(t):
        next_num = all_array[p - 1]
        result_array.append(next_num)
        p = p + m
    return result_array

wish_list = n_carry_game(16, 16, 2, 2)
for i in range(len(wish_list)):
    print(wish_list[i], end='')


