
from copy import deepcopy
from multiprocessing import Pipe, Process

from ggAgent import Agent
from ggGame import FTTT
from random import random
import time

def mergeDicts(d1, d2):
    mdict = deepcopy(d1)

    for k in d2.keys():
        if(k in mdict):
            mdict[k][0] += d2[k][0]
            mdict[k][1] += d2[k][1]
        else:
            mdict[k] = d2[k]
    
    return mdict

if __name__ == '__main__':
    start_time = time.time()

    player1 = Agent("Best", e_thresh=0.5)
    player2 = Agent("Ever")
    game = FTTT([player1, player2])

    i = 0
    while(time.gmtime(time.time() - start_time).tm_hour < 12):
        i += 1
        if(i % 1000 == 0):
            print(f"{time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))}: Finished {i} runs...")
        game.startGame()

    print(f"You got {i} games worth of training!")
    print(f"player1 wins: {player1.num_wins}")
    print(f"player2 wins: {player2.num_wins}")
    player1.save()
    player2.save()

    #print(f"It took {time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))} seconds to run.")


#if __name__ == '__main__':
#    start_time = time.time()
#
#    all_trainers = []
#
#    for i in range(1000):
#        parent_conn, child_conn = Pipe()
#        p1 = Agent(hash(i + random()), e_thresh=random())
#        p2 = Agent(hash(i + random()), e_thresh=random())
#        game = FTTT([p1, p2])
#        LTM = {}
#        p = Process(target=game.runGames, args=(child_conn, 1000))
#
#        all_trainers.append([p, LTM, parent_conn])
#    
#    for p in all_trainers:
#        p[0].start()
#        p[1] = p[2].recv()
#    
#    d = {}
#    for p in all_trainers:
#        d = mergeDicts(d, p[1])
#    
#    derek = Agent("Best")
#    derek.LTM = d
#    derek.save()
#
#    print(f"It took {time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))} seconds to run.")