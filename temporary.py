class test:
    def __init__(self):
        print('test class')
    def __str__(self):
        return 'this is str'
    def __repr__(self):
        return 'this is repr'

if __name__ == '__main__':
    for i, level in enumerate(range(2, 6)):
        print(i, level)
