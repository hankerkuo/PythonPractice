import readtxt

pb = readtxt.readfile_prob5()

for single in pb:
    type_time = 0
    for ele in single:
        for i in range(len(ele)):
            count = 0
            for elem in single:
                try:
                    if ele[i] == elem[i]:
                        count += 1
                except IndexError:
                    continue
            if count == 1:
                type_time += i+1
                break
            if i == len(ele) - 1:
                type_time += len(ele)
    print(type_time, 'for', single)