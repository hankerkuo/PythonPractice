Total_List = [[]]
Score_List = []
Total_List.clear()
#print(Total_List)
for i in range(int(input())):
    List = []
    List.append(input())
    List.append(float(input()))
    Total_List.append(List)
    Score_List.append(Total_List[i][1])

#Sorted_List = sorted(Total_List,key = lambda x : x[1])
# first sort both the Total_List and Score_List
Total_List.sort(key = lambda x : x[1])
Score_List.sort()
NamesGonaShow = []
#print(Total_List)

for j in range(len(Score_List)-1):
    if Score_List[j]<Score_List[j+1]:
        #print(Total_List[j+1][0])
        NamesGonaShow.append(Total_List[j+1][0])
        for k in range(j+1,len(Score_List)-1):
            if Score_List[j+1] == Score_List[k+1]:          #There may be different numbers other than second small number
                #print (Total_List[k+1][0])
                NamesGonaShow.append(Total_List[k+1][0])
        break

NamesGonaShow.sort()
print('\n'.join(NamesGonaShow))



