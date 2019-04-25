import random
from sys import stdout
from time import sleep
from collections import deque
from pyfiglet import Figlet

def lotto(candidate, A, choose=False):
    random.shuffle(candidate)
    for i in range(5):
        for company in candidate:
            io.flush()
            io.write('  抽獎中:' + str(company) + '\t\t\t')
            sleep(0.025)
            io.write("\r")
    if choose:
        prize_receiver = choose
    else:
        prize_random = random.randrange(len(A))
        prize_receiver = A[prize_random]
        A.pop(prize_random)
    io.write('  得獎者:' + prize_receiver + '\t\t\t\n\n')



f = Figlet(font='slant')
print(f.renderText('Settler Tech'))

lst_A = deque()
lst_B = deque()
io = stdout

A = ''

B = '廣大通信科技股份有限公司-陳綉緣,\
海灣電通科技事業有限公司-陳達仁,\
芮訊科技資訊工作室-楊瑞智,\
任鋒科技有限公司,\
揚城科技股份有限公司-阿信,\
未來一體有限公司-鄭仁宗,\
隆德通信機械有限公司-張先生,\
日鴻安全科技有限公司-羅秔富,\
允楷數位有限公司-陳弘佳,\
奧藍多實業有限公司-何文正,\
迅成科技-余建明,\
洧駿科技實業-葉濬瑋,\
羽信科技有限公司-劉剛男,\
峰偉科技有限公司-顏達雄,\
弘秝科技有限公司-翁明權,\
名震科技有限公司-蔣建民,\
奇君企業有限公司-邱惟揚,\
泰昕興業有限公司-林佳易,\
麒瑞企業有限公司-廖茂程,\
祐承科技有限公司-吳臻昀,\
智慧眼科技有限公司-Alan Tsao      ,\
任鑫有限公司,\
橙白室內裝修設計工程有限公司-呂欣潔,\
緯竣科技工程有限公司-陳啟銘,\
長業系統工程有限公司-蔡宗佑,\
允盛資訊有限公司-曾志國,\
順豊企業社,\
宥任科技有限公司-林淵鐘,\
笙揚數位系統有限公司-陳奕成,\
揚星科技有限公司-劉昭科,\
億大光電科技有限公司-劉信義,\
加帝國際有限公司,\
藍鳥科技有限公司-吳正光,\
宏彰通信行,\
晶詠科技股份有限公司-林川桐'

lst_A = A.split(',')
lst_B = B.split(',')
candidate = lst_B
random.shuffle(candidate)
print('抽獎名單:')
for i, person in enumerate(candidate):
    if i % 2 == 0:
        print()
    print('{0:{1}^20}'.format(person, chr(12288)), end='')
print('\n')
input('按下Enter開始抽獎')

# prize 1
candidate = lst_A + lst_B
io.write('\n'+'一獎:安全套裝組合'+'\n')
lotto(candidate, lst_A, choose='泰昕興業有限公司')

#prize 2
candidate = lst_A + lst_B
io.write('二獎：萬用紅外線遙控器（超級碗)'+'\n')
lotto(candidate, lst_A, choose='廣大通信科技股份有限公司')

#prize 3
candidate = lst_A + lst_B
io.write('三獎：Wi-Fi 插座'+'\n')
lotto(candidate, lst_A, choose='億大光電科技有限公司')

input('恭喜中獎者!')



