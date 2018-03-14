import numpy

N, M = map(int, input().strip().split(' '))

arr = numpy.array([input().strip().split(' ') for _ in range(N)], int)
arr_min = numpy.min(arr, axis = 1)
print (numpy.max(arr_min))