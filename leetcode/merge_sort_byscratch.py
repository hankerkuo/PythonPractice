import collections

class Sort:
    # L -> Left, R -> Right, C -> Combination
    def merge(self, L, R):
        L = collections.deque(L)
        R = collections.deque(R)
        C = []
        while(L and R):
            if L[0] <= R[0]:
                C.append(L.popleft())
            else:
                C.append(R.popleft())
        if(L):
            Rest = L
        elif(R):
            Rest = R
        while(Rest):
            C.append(Rest.popleft())
        return C

    # T -> Target
    def merge_sort(self, T):
        if len(T) == 1:
            return T
        mid = len(T) // 2
        L = self.merge_sort(T[0: mid])
        R = self.merge_sort(T[mid:])
        return self.merge(L, R)


x = [2, 4, 1, 6, 8, 5, 3, 7]
sort = Sort()
after_sort = sort.merge_sort(x)
print(after_sort)
