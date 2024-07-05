import math
import random

#part c
Xbar = 7
X0 = 3
N = 14
p = 0.25

beta = 1.44
#one step lookahead
priceToSell = int(math.floor(X0*beta))







trajectoryCount = 20
#make a trajectory list of 20
trajectories = []
for _ in range(trajectoryCount):
    trajectoryToAppend = []
    trajectoryToAppend.append(X0)
    sold = False
    for timeStep in range(1, N+1):
        if not sold:
            r = random.randint(1,4)
            #calculate the next state
            nextState = trajectoryToAppend[timeStep-1]
            if r == 3 and trajectoryToAppend[timeStep-1] != Xbar:
                nextState = trajectoryToAppend[timeStep-1] + 1
            if r == 4 and trajectoryToAppend[timeStep-1] != 0:
                nextState = trajectoryToAppend[timeStep-1] - 1
            #append it
            trajectoryToAppend.append(nextState)
            #see if we sell
            if nextState >= priceToSell:
                sold = True


    trajectories.append(trajectoryToAppend)

#for t in trajectories:
#    print(t)

JtildeTable = [[0]*(N+1) for i in range(Xbar + 1)]

#fill in the JtildeTable with the values learned from the trajectories
#initialize to 0
#fill in every column starting from the beginning


for timeStep in range(0,N+1,1):
    #print("timestep", timeStep)
    for stockPrice in range(Xbar+1):
        totalReward = 0
        count = 0
        for t in trajectories:
            if len(t) > timeStep:
                if t[timeStep] == stockPrice:
                    #print(stockPrice)
                    #print(t)
                    #print(t[timeStep])
                    #print(timeStep)
                    count += 1
                    totalReward += t[len(t)-1]
        if count > 0:
            #print(stockPrice, timeStep, count)
            JtildeTable[stockPrice][timeStep] = totalReward/count

#for x in JtildeTable:
#    print(x)


#we append trajectories to the list
#the trajectories are of the form [state1, state2, ... , whateverEndState]
#the total reward is the endstate vlaue
#the policy is that they sold at the endstate value and the endstate time position

#print table
Ylabel = "stock price "
Xlabel = "time"

Yticks = range(Xbar, -1, -1)
Xticks = range(N + 1)


toPrint = ""
#print Y label, Y ticks, Yline, top row of data
toPrint +=  Ylabel
toPrint +=  str(Yticks[0])
toPrint += " |"
for col in JtildeTable[Xbar]:
    if col > 0:
        toPrint += " %.4f"%col
    else:
        toPrint += "       "
print(toPrint)

#for every row
for rowindex in range(1,Xbar+1):
    # print Y label spacer, Y line, that row of data
    toPrint = ""
    toPrint += " " * len(Ylabel)
    toPrint += str(Yticks[rowindex])
    toPrint += " |"
    for col in range(N+1):
        if JtildeTable[Xbar - rowindex][col] >= 0:
            toPrint += " %.4f"%JtildeTable[Xbar - rowindex][col]
        else:
            toPrint += "       "
    print(toPrint)
    
#print Xline
toPrint = " " * len(Ylabel)
toPrint += "  |"
toPrint += "_" * (7 * len(Xticks))
print(toPrint)

#print Xticks
toPrint = ""
toPrint += " " * len(Ylabel)
toPrint += "    "
for x in Xticks:
    toPrint += '{:7}'.format(str(x))
print(toPrint)

#print X label
toPrint = ""
toPrint += " " * len(Ylabel)
toPrint += "    "
toPrint += Xlabel
print(toPrint)

