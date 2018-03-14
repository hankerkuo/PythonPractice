s = input()
L = ""

for i in range(len(s)):
    if s[i].islower():
        #print(s[i].upper(), end='')
        L = L + s[i].upper()
    else:
        #print(s[i].lower(), end='')
        L = L + s[i].lower()

print(L)


def swap_case(s):
    L = ""

    for i in range(len(s)):
        if s[i].islower():
            # print(s[i].upper(), end='')
            L = L + s[i].upper()
        else:
            # print(s[i].lower(), end='')
            L = L + s[i].lower()

    return L




