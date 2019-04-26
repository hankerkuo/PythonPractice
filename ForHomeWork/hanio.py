

def hanio(n, start, mid, end):
    if n == 1:
        print("plate", n, "from", start, "move to", end)
    elif n >= 2:
        hanio(n-1, start, end, mid)
        print("plate", n, "from", start, "move to", end)
        hanio(n-1, mid, start, end)


hanio(5, 'A', 'B', 'C')