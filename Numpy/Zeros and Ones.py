import numpy

#N, M, R = map(int, input().strip().split(' '))
'''
in order to measure the length of N, use map and list function
'''
N = list(map(int, input().strip().split(' ')))
'''
if len(N) == 1:
    print(numpy.zeros((N[0]), dtype=int), numpy.ones((N[0]), dtype=int), sep='\n')
elif len(N) == 2:
    print(numpy.zeros((N[0], N[1]), dtype=int), numpy.ones((N[0], N[1]), dtype=int), sep='\n')
else:
    print(numpy.zeros((N[0], N[1], N[2]), dtype=int), numpy.ones((N[0], N[1], N[2]), dtype=int), sep='\n')
'''
print(numpy.zeros((N), dtype=int), numpy.ones((N), dtype=int), sep='\n')