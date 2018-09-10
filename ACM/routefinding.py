def file_reading():
    f = open('routefinding.txt', 'r')
    spot, road = f.readline()[:-1].split(' ')
    rd_list = []
    for i in range(int(road)):
        rd_list.append(f.readline()[:-1].split(' '))
    start, end = f.readline().split(' ')
    return start, end, rd_list


def finding_road(start, end, road_list, total_length=0, walking_method=[]):
    destiny = end
    current_road = walking_method[:]
    for road in road_list:
        if road[1] == destiny:
            length = total_length + int(road[2])
            print('from', road[1], 'to', road[0], 'length:', road[2], 'total length:', length)
            if road[0] == start:
                walking_method.append(end)
                walking_method.append(start)
                print('one road found,', walking_method, 'length:', length)
                walking_method = current_road[:]
                continue
            else:
                walking_method.append(destiny)
                end = road[0]
                finding_road(start, end, road_list, length, walking_method)
                walking_method = current_road[:]



def finding_road_ver2(start, end, road_list, total_length=0, walking_method=''):
    destiny = end
    current_road = walking_method
    for road in road_list:
        if road[1] == destiny:
            length = total_length + int(road[2])
            # print('from', road[1], 'to', road[0], 'length:', road[2], 'total length:', length)
            if road[0] == start:
                walking_method += '>-' + end
                walking_method += '>-' + start
                # This is extended slice syntax. It works by doing [begin:end:step]
                walking_method = walking_method[::-1][:-2]
                print('route found,', walking_method, 'length:', length)
                walking_method = current_road
                continue
            else:
                walking_method += '>-' + destiny
                end = road[0]
                finding_road_ver2(start, end, road_list, length, walking_method)
                walking_method = current_road


# from a to b
a, b, rd_list = file_reading()
finding_road_ver2(a, b, rd_list)
