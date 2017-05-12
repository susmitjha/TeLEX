import random
import numpy as np

# intruders set to 0 y02 = 0
y = [0 for i in range(0,8)]
timey = [0 for i in range(0,8)]

#y00 = 0 .. 0
#y01 = 0 .. 1
#y02 = 0 .. 2
#y10 = 0 .. 3
#y12 = 0 .. 4
#y20 = 0 .. 5
#y21 = 0 .. 6
#y22 = 0 .. 7

numintruders  = 0 # max 2 allowed at anytime

agent1x = 0
agent1y = 0

agent2x = 10
agent2y = 10

def locy(i):
    if i >= 0 and i <= 2:
        return 0
    elif i >= 3 and i <= 4:
        return 5
    elif i >= 5 and i <= 7:
        return 10
    else:
        return -1

def locx(i):
    if i == 0 or i == 3 or i == 5:
        return 0
    elif i == 1 or i == 6:
        return 5
    elif i == 2 or i == 4 or i == 7:
        return 10
    else:
        return -1

def getClosest(agentx, agenty, y):
    d = 100000
    choice = -1
    for j in range(0,8):
        if y[j] == 1:
            d1 = (agentx - locx(j)) * (agentx - locx(j)) + (agenty - locy(j)) * (agenty - locy(j)) 
            if d1 < d:
                d = d1
                choice = j
    #assert(choice!=-1)
    return choice,d






for i in range(1,1000):
    # originate intruders
    #print(numintruders)
    intrud = random.randint(0,8)
    if (numintruders < 2):
        if (intrud != 8):
            y[intrud] = 1
            numintruders = numintruders + 1
    assert(sum(y) <= 2)

    # update intruder clocks
    for j in range(0,8):
        if (y[j] == 1):
            timey[j] += 1

    # update agent locations
    dest1,d1 = getClosest(agent1x, agent1y, y)
    dest2,d2 = getClosest(agent2x, agent2y, y)

    # if single destination and they both pick it, award it to closer one
    if dest1 == dest2:
        if d1 > d2:
            dest1 = -1
        else:
            dest2 = -1

    if dest1 != -1:
        if d1 == 0:
            y[dest1] = 0
            timey[dest1] = 0
        else:
            if (i %2 == 0):
                if (locx(dest1) > agent1x):
                    agent1x = agent1x + 1
                elif (locx(dest1) <  agent1x):
                    agent1x = agent1x - 1
            else:
                if (locy(dest1) > agent1y):
                    agent1y = agent1y + 1
                elif (locy(dest1) < agent1y):
                    agent1y = agent1y - 1
        
    if dest2 != -1:
        if d2 == 0:
            y[dest2] = 0
            timey[dest2] = 0
        else:
            if (i %2 == 0):
                if (locx(dest2) > agent2x):
                    agent2x = agent2x + 1
                elif (locx(dest2) < agent2x):
                    agent2x = agent2x - 1
            else:
                if (locy(dest2) > agent2y):
                    agent2y = agent2y + 1
                elif (locy(dest2) < agent2y):
                    agent2y = agent2y - 1
        
    if(locx(dest1) == agent1x and locy(dest1) == agent1y):
        y[dest1] = 0
        timey[dest1] = 0
        numintruders = numintruders -1 


    if(locx(dest2) == agent2x and locy(dest2) == agent2y):
        y[dest2] = 0
        timey[dest2] = 0
        numintruders = numintruders -1 

    #print(dest1, locx(dest1), locy(dest1))
    #print(dest2, locx(dest2), locy(dest2))


    # dump all 
    print(i, agent1x, agent1y, agent2x, agent2y, y[0], y[1], y[2], y[3], y[4], y[5], y[6], y[7], timey[0], timey[1], timey[2], timey[3], timey[4], timey[5], timey[6], timey[7])


