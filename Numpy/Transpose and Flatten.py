import numpy
N,M = map(int,input().split(' '))
a = numpy.empty(shape=(N,M),dtype=int)         #use numpy.empty to decide a big enough to store the data
for i in range(0,N):
    a[i] = list(map(int,input().split(' ')))   #use this loop to add single row of a

print(numpy.transpose(a),a.flatten(),sep="\n")

