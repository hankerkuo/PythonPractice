import readtxt
input = readtxt.readfile_prob4_1()


# separate the sharp note
def sharp_note_sep(lst):
    real_list = []
    for n, i in enumerate(lst):
        if i == '#':
            real_list[-1] = lst[n-1:n+1]
        else:
            real_list.append(i)
    return real_list


def song_match(target):
    # all samples
    for i in range(len(target)):
        m = target[i][0]
        musicinfos = target[i][1:]
        m_list = sharp_note_sep(m)
        candidate = []
        # all song candidates in one sample
        for n in range(len(musicinfos)):
            time = ((int(musicinfos[n][1][0:2]) * 60 + int(musicinfos[n][1][3:5])) -
                    (int(musicinfos[n][0][0:2]) * 60 + int(musicinfos[n][0][3:5])))
            musicinfos[n].append(time)
            if len(m_list) > time:
                continue
            song = sharp_note_sep(musicinfos[n][3])
            for t in range(time - len(m_list)):
                for x in range(len(m_list)):
                    if song[(t + x) % len(song)] != m_list[x]:
                        break
                    elif x == len(m_list) - 1:
                        candidate.append(musicinfos[n])
                # if matched, means the for loop has gone through completely, then break
                else:
                    break
        candidate.sort(key=lambda s: -s[4])
        if len(candidate) == 0:
            print('No.', i+1, '>NO MATCHED SONGS<')
        else:
            print('No.', i+1, candidate[0][2])


song_match(input)

