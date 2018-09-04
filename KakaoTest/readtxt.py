def readfile_prob1():
    f = open('input1.txt', 'r')
    lst = []
    for i in f.readlines():
        i = i[:-1]
        lst.append(i.split())
    return lst


def readfile_prob2():
    f = open('input2.txt', 'r')
    lst = []
    for i in f.readlines():
        lst.append(i[:-1])
    return lst


def readfile_prob3():
    f = open('input3.txt', 'r')
    lst = []
    for i in f.readlines():
        i = i[:-1]
        lst.append(i.split(', '))
    return lst

