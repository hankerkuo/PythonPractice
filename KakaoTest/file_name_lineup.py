list = ['F-5 Freedom Fighter', 'B-50 Superfortress', 'A-10 Thunderbolt II', 'F-14 Tomcat']
list_2 = ['img12.png', 'img10.png', 'img02.png', 'img1.png', 'IMG01.GIF', 'img2.JPG']

# separate the list into head part and number part
def file_name_renew(lst):
    list_separated = []
    list_final = []
    for index, elements in enumerate(lst):
        head_part = False
        number_part_start_pt = 0
        tail_part_start_pt = 0
        for i, j in enumerate(elements):
            if ord(j) >= 48 and ord(j) <= 57:
                if head_part is False:
                    number_part_start_pt = i
                    head_part = True
            if (ord(j) < 48 or ord(j) > 57) and head_part is True:
                tail_part_start_pt = i
                break
        list_separated.append(lst[index][0:number_part_start_pt])
        list_separated.append(lst[index][number_part_start_pt:tail_part_start_pt])
        list_separated.append(lst[index][tail_part_start_pt:])
        list_final.append(list_separated)
        list_separated = []
    list_final.sort(key=lambda x: int(x[1]))
    list_final.sort(key=lambda x: str.upper(x[0]))
    for i in range(len(list_final)):
        list_final[i] = list_final[i][0] + str(list_final[i][1]) + list_final[i][2]
    return list_final

print(file_name_renew(list))