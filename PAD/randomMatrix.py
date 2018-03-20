'''
This random model makes the random board, Random_Board, of puzzle and dragon (a 5 * 6 matrix)
Numbers 0~5 represent the 6 kind of beads in PAD
'''

import numpy as np

#ｂ = np.array([0,0,0,0,0,0])

for i in range(1000):
    #np.random.rand yields random numbers in the range [0, 1)
    Random_Board = np.random.rand(5, 6) * 6
    Random_Board = np.floor(Random_Board)
    Random_Board = Random_Board.astype(int)
    if i == 0:
        Sum_of_Board = Random_Board
    else:
        Sum_of_Board = np.r_[Sum_of_Board, Random_Board]
    '''
    stunned a long time for this if and else statement! 
    In the first iteration fo this loop, when i = 0, declare Sum_of_Board 
    as a np.array to restore all of the random board which have been made
    After first loop, push each Random_Board into Sum_of_Board
    '''
    print("The",i+1, "th random board has been added")
    '''
    b[(Random_Board[1][1])] += 1
    Total = np.sum(b)
    print("0:{:.3f}".format(b[0] / Total), "1:{:.3f}".format(b[1] / Total),
          "2:{:.3f}".format(b[2] / Total), "3:{:.3f}".format(b[3] / Total),
          "4:{:.3f}".format(b[4] / Total), "5:{:.3f}".format(b[5] / Total))
    '''
np.savetxt('Random_1', Sum_of_Board, fmt="%1.0f")
#save the random arrays into an txt file