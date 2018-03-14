'''
The dot tool returns the dot product of two arrays.
The cross tool returns the cross product of two arrays.
'''
import numpy

N = int(input().strip())
A = numpy.array([input().strip().split(' ') for _ in range(N)], int)
B = numpy.array([input().strip().split(' ') for _ in range(N)], int)

print(numpy.dot(A, B))

'''
This is the DIY multiplication of matrices

A_B_Product = numpy.empty(shape = (N, N), dtype = int)
for i in range(N):
    for j in range(N):
        A_B_Product[i][j] = numpy.dot(A[i], numpy.array([B[k][j] for k in range(N)]))
print (A_B_Product)
'''
