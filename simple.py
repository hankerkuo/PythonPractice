a = int(input())

for i in range((a - 1) // 2):
    print(' ' * ((a - 1) // 2 - i), end='')
    print('*' * (2 * i + 1), sep='', end='\n')

print('*' * a, sep='', end='\n')

for i in range((a - 1) // 2):
    print(' ' * (i + 1), end='')
    print('*' * (2 * ((a - 1) // 2 - i) - 1), sep='', end='\n')

