Student_Score = []

for i in range(int(input())):
    list_tem = tuple(input().split(' '))
    dict = {'Name':list_tem[0],'Maths':float(list_tem[1]),'Physics':float(list_tem[2]),'Chemisry':float(list_tem[3])}
    Student_Score.append(dict)

FindingName = input()

for i in range(len(Student_Score)):
    if FindingName == Student_Score[i]['Name']:
        #use format output to 2 digits
        print("%.2f"% ((Student_Score[i]['Maths']+Student_Score[i]['Physics']+Student_Score[i]['Chemisry'])/3))


