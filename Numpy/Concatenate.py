import numpy

N, M, P = map(int,input().strip().split(' '))

matrix_A = numpy.array([input().strip().split(' ') for _ in range(N)],int)
matrix_B = numpy.array([input().strip().split(' ') for _ in range(M)],int)

print(numpy.concatenate((matrix_A, matrix_B), axis = 0))