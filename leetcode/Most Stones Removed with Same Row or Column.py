import collections

class Solution:
    def removeStones(self, stones):
        graph = collections.defaultdict(list)

        for i, stone in enumerate(stones):
            for j in range(i):
                if stone[0] == stones[j][0] or stone[1] == stones[j][1]:
                    graph[i].append(j)
                    graph[j].append(i)

        seen_map = [False] * len(stones)
        count = 0
        for i, stone in enumerate(stones):
            if not seen_map[i]:
                seen_map[i] = True
                visiting_list = []
                visiting_list.append(i)
                while (len(visiting_list) > 0):
                    v = visiting_list.pop()
                    for nei in graph[v]:
                        if not seen_map[nei]:
                            seen_map[nei] = True
                            count += 1
                            visiting_list.append(nei)

        return count

        """
        :type stones: List[List[int]]
        :rtype: int
        """

a = collections.defaultdict(list)
a[123].append(1)
a[456].append(1)
del a[456]
print(a)