import numpy

N, M = map(int, input().strip().split(' '))

arr = numpy.array([input().strip().split(' ') for _ in range(N)], int)
arr_sum = numpy.sum(arr, axis = 0)
print (numpy.prod(arr_sum))

'''
Here's the online solution (just combine the lines i wrote) 
print (numpy.prod(numpy.sum(numpy.array([input().strip().split(' ') for _ in range(N)], int), axis = 0)))
'''