import numpy

N, M = map(int, input().strip().split(' '))
A = numpy.array([input().strip().split(' ') for _ in range(N)], int)
B = numpy.array([input().strip().split(' ') for _ in range(N)], int)

print(A + B, A - B, A * B, A//B, A % B, A ** B, sep='\n')