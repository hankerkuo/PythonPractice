s = "Toronto is the largest City in Canada"
t = "Python courses in Toronto by Bodenseo"
# s = "".join(["".join(x) for x in zip(s,t)])
s = ["".join(x) for x in zip(s, t)]
print(s)
