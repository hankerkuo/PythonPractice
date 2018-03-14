import numpy

#raw_Data = input().strip().split('')
arr = numpy.array(input().strip().split(' '),int)  #Here to assign the type of Data; integer is important, because the output format will also change due to the data type changing
print(numpy.reshape(arr,(3,3)))
