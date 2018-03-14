'''
The mean tool computes the arithmetic mean along the specified axis.
The var tool computes the arithmetic variance along the specified axis.
The std tool computes the arithmetic standard deviation along the specified axis.
'''
import numpy

N, M = map(int, input().strip().split(' '))
arr = numpy.array([input().strip().split(' ') for _ in range(N)], int)
print(numpy.mean(arr, axis = 1), numpy.var(arr, axis = 0), numpy.std(arr), sep = '\n')

