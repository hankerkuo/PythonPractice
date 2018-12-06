import numpy as np

# a and b are numpy arrays representing each digit for two big number
a = np.random.randint(10, size=250)
b = np.random.randint(10, size=259)
print(a, b, sep='\n')
# reverse the array for calculating convenience
a = np.flip(a, 0)
b = np.flip(b, 0)

# let the two array be same length
length_diff = len(a) - len(b)
if length_diff:
    if length_diff > 0:
        for i in range(length_diff):
            b = np.append(b, 0)
    elif length_diff < 0:
        for i in range(-length_diff):
            a = np.append(a, 0)

# using basic math method, if single digit addition > 10, than the carry will be 1 and add to next digit
sum = []
carry = 0
for i, num_1 in enumerate(a):
    digit_sum = num_1 + b[i] + carry
    if digit_sum >= 10:
        sum.append(digit_sum - 10)
        carry = 1
    else:
        sum.append(digit_sum)
        carry = 0
if carry == 1:
    sum.append(1)

sum.reverse()
for ele in sum:
    print(ele, end='')
