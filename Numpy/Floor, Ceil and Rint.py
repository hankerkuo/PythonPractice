import numpy

A = numpy.array(input().strip().split(' '), float)

print (numpy.floor(A), numpy.ceil(A), numpy.rint(A), sep = '\n')