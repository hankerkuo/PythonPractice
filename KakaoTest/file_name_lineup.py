list = ['F-5 Freedom Fighter', 'B-50 Superfortress', 'A-10 Thunderbolt II', 'F-14 Tomcat']
list_2 = ['img12.png', 'img10.png', 'img02.png', 'img1.png', 'IMG01.GIF', 'img2.JPG']
import readtxt

# separate the list into head part and number part
def file_name_renew(lst):
    for index, elements in enumerate(lst):
        found_number = False
        for i, j in enumerate(elements):
            if found_number is False and 48 <= ord(j) <= 57:
                number_pt = i
                found_number = True
            elif found_number is True and (ord(j) < 48 or ord(j) > 57):
                tail_pt = i
                break
        lst[index] = [lst[index][0:number_pt], lst[index][number_pt:tail_pt], lst[index][tail_pt:]]
    lst.sort(key=lambda x: int(x[1]))
    lst.sort(key=lambda x: str.upper(x[0]))
    for i in range(len(lst)):
        lst[i] = lst[i][0] + lst[i][1] + lst[i][2]
    return lst

prob3_input = readtxt.readfile_prob3()
for i in range(len(prob3_input)):
    print('input:', prob3_input[i])
    print('output:', file_name_renew(prob3_input[i]), '\n')
