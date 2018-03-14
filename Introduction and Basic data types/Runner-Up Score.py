#Problem:https://www.hackerrank.com/challenges/find-second-maximum-number-in-a-list/problem

print(dir(list))
Score_Number = int(input())
Score_List = list(map(int,input().split(' ')))
RunnerUp = int()
Score_List.sort()
if Score_List[0] == Score_List[Score_Number-1]:
    print("ERROR : All the scores are same")
for i in range(Score_Number-1,0,-1):
    if Score_List[i-1]<Score_List[i]:
        RunnerUp = Score_List[i-1]
        print(RunnerUp)
        break

#DEF sort