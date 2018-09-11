import readtxt

pb = readtxt.readfile_prob5()
for single in pb:
    type_time = 0
    for ele in single:
        lst = single[:]
        for i in range(len(ele)):
            n = 0
            while len(lst) > 1 and n < len(lst):
                try:
                    if ele[i] != lst[n][i]:
                        lst.remove(lst[n])
                        continue
                except IndexError:
                    lst.remove(lst[n])
                    continue
                n += 1
            if len(lst) == 1 or i == len(ele) - 1:
                type_time += i+1
                break
    print(type_time, 'for', single)


