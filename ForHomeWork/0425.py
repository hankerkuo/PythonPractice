def permutation(string, temp=''):
    print ('abc')
    if len(string) == 0:
        print(temp)
    for i in range(len(string)):
        temp += string[i]
        permutation(string[0:i] + string[i + 1:], temp)
        temp = temp[:-1]

def perm(string):
    for s in string:
        print(s)
permutation('xyz')

