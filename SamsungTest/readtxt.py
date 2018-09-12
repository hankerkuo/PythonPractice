import re


def readfile_glassbead_escape():
    f = open('glassbead_escape_1.txt', 'r')
    lst = list(f)
    # if the end is not \n then add \n, for the convenience
    lst[-1] = lst[-1] + '\n' if lst[-1][-1] != '\n' else lst[-1]
    # delete all the \n in each element
    lst = [a[:-1] for a in lst]
    row, column = map(int, lst[0].split(' '))
    maze = lst[1:]
    return row, column, maze


print(readfile_glassbead_escape())