'''
This random model makes the random board of puzzle and dragon
'''

import numpy as np

ｂ = np.array([0,0,0,0,0,0])
while(1):
    a = np.random.rand(5, 6) * 6
    a = np.floor(a)
    a = a.astype(int)
    b[(a[1][1])] += 1
    Total = np.sum(b)
    print("0:{:.3f}".format(b[0]/Total),"1:{:.3f}".format(b[1]/Total),
          "2:{:.3f}".format(b[2]/Total),"3:{:.3f}".format(b[3]/Total),
          "4:{:.3f}".format(b[4]/Total),"5:{:.3f}".format(b[5]/Total))