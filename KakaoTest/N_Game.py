import readtxt

# the function for transferring decimal system number to different system number
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


# if the carry system is larger than 10, substitute 10~15 with A to F (using ASCII)
def A_to_F(lst):
    for n, i in enumerate(lst):
        if i >= 10:
            lst[n] = chr(i+55)
    return lst


# main function, the demand of the question
def n_carry_game(n, t, m, p):
    all_array = []
    result_array = ''
    add = 0
    while len(all_array) < t * m:
        all_array.extend(decimal_to_n(add, n))
        add += 1
    # print(all_array)
    for i in range(t):
        next_num = all_array[p - 1]
        result_array = result_array + str(next_num)
        p = p + m
    return result_array

prob1_input = readtxt.readfile_prob1()
for i in range(len(prob1_input)):
    wish_list = n_carry_game(*list(map(int, prob1_input[i])))
    print('input:', prob1_input[i])
    print('output:', wish_list, '\n')


