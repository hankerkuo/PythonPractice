# change the sequence of two arrays
import numpy

arr = input().strip().split(' ')
a = numpy.array(arr,float)
b = numpy.array(arr,float)
for i in range(len(a)):
    b[i] = a[len(a)-1-i]
print(b)