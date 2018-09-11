import re

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


# for prob4 : read into a 3-D list
# [ [ 'm1', [ [song1], [song2] ...] ]
#   [ 'm2', [ [song1], [song2] ...]
#   [ 'm3', [ [song1], [song2] ...] ]
def readfile_prob4():
    f = open('input4.txt', 'r')
    lst = list(f)
    single_prob = []
    overall_output = []
    for n in range(len(lst)):
        # first group: “string” , second group: [string]
        src = re.search(r'(“.+?”)(\[.+?\])', lst[n])
        m = src.group(1)[1:-1]
        music = src.group(2)[1:-1]
        music = music.split(', ')
        for i in range(len(music)):
            music[i] = music[i][1:-1].split(',')
        single_prob.append(m)
        single_prob.extend(music)
        overall_output.append(single_prob)
        single_prob = []
    return overall_output


def readfile_prob5():
    f = open('input5.txt', 'r')
    lst = list(f)
    single_prob = []
    overall_output = []
    for n in range(len(lst)):
        # [string]
        src = re.search(r'\[.+?\]', lst[n])
        term = src.group()[1:-1]
        term = term.split(',')
        for i in range(len(term)):
            term[i] = term[i][1:-1]
        single_prob.extend(term)
        overall_output.append(single_prob)
        single_prob = []
    return overall_output
