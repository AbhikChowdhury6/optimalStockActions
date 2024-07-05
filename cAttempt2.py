import math
import random


#make a class that has the simParams
class simParams:
    def __init__(self,Xbar,Xn,n,N,p,beta,numtraj):
        self.Xbar = Xbar
        self.Xn = Xn
        self.n = n
        self.N = N
        self.p = p
        self.beta = beta
        self.numtraj = numtraj


def calcJtildeTable(trajectories, simParams):
    JtildeTable = [[0]*(simParams.N+1) for i in range(simParams.Xbar + 1)]

    for timeStep in range(simParams.N+1):
        #print("timestep", timeStep)
        for stockPrice in range(simParams.Xbar+1):
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
    
    return JtildeTable



def printJtable(Jtable, simParams):
    Ylabel = "stock price "
    Xlabel = "time"

    Yticks = range(simParams.Xbar, -1, -1)
    Xticks = range(simParams.N + 1)

    toPrint = ""
    #print Y label, Y ticks, Yline, top row of data
    toPrint +=  Ylabel
    toPrint +=  str(Yticks[0])
    toPrint += " |"
    for col in Jtable[simParams.Xbar]:
        if col > 0:
            toPrint += " %.4f"%col
        else:
            toPrint += "       "
    print(toPrint)

    #for every row
    for rowindex in range(1,simParams.Xbar+1):
        # print Y label spacer, Y line, that row of data
        toPrint = ""
        toPrint += " " * len(Ylabel)
        toPrint += str(Yticks[rowindex])
        toPrint += " |"
        for col in range(simParams.N+1):
            if Jtable[simParams.Xbar - rowindex][col] >= 0:
                toPrint += " %.4f"%Jtable[simParams.Xbar - rowindex][col]
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


    


#TODO update this to say if it was ever the end of a trajecotry it was sell
def printPolicyTable(Jtable, simParams):
    policyTable = [["   "]*(simParams.N+1) for i in range(simParams.Xbar + 1)]

    for colIndex in range(simParams.N, -1, -1):
        #iterate through every row starting from Xbar going down
        for priceIndex in range(simParams.Xbar + 1):
            #check if this state is reachable based on N if not leave at -1 
            if Jtable[priceIndex][colIndex] == -1 or priceIndex > priceToSell:
                pass
            else:
                if Jtable[priceIndex][colIndex] == priceIndex or colIndex == N:
                    policyTable[priceIndex][colIndex] = "  S"
                else:
                    policyTable[priceIndex][colIndex] = "  D"

    #print policyTable
    toPrint = ""
    #print Y label, Y ticks, Yline, top row of data
    toPrint +=  Ylabel
    toPrint +=  str(Yticks[0])
    toPrint += " |"
    for col in policyTable[simParams.Xbar]:
        toPrint += col
    print(toPrint)

    #for every row
    for rowindex in range(1,simParams.Xbar+1):
        # print Y label spacer, Y line, that row of data
        toPrint = ""
        toPrint += " " * len(Ylabel)
        toPrint += str(Yticks[rowindex])
        toPrint += " |"
        for col in range(N+1):
            toPrint += policyTable[simParams.Xbar - rowindex][col]
        print(toPrint)
        

    #print Xline
    toPrint = " " * len(Ylabel)
    toPrint += "  |"
    toPrint += "_" * (3 * len(Xticks))
    print(toPrint)

    #print Xticks
    toPrint = ""
    toPrint += " " * len(Ylabel)
    toPrint += "     "
    for x in Xticks:
        toPrint += '{:3}'.format(str(x))
    print(toPrint)

    #print X label
    toPrint = ""
    toPrint += " " * len(Ylabel)
    toPrint += "    "
    toPrint += Xlabel
    print(toPrint)



def runBetaSim(simParams):
    priceToSell = int(math.floor(simParams.Xn*simParams.beta))

    trajectories = []
    for _ in range(simParams.numtraj):
        trajectoryToAppend = []
        trajectoryToAppend.append(simParams.Xn)
        #check if we sell
        if simParams.Xn >= priceToSell:
            sold = True
        else:
            sold = False
        for timeStep in range(simParams.n, simParams.N+1):
            if not sold:
                r = random.randint(0,100)
                #generate the next state
                nextState = trajectoryToAppend[timeStep-1]
                if r > 100 - (simParams.p * 100) and trajectoryToAppend[timeStep-1] != simParams.Xbar:
                    nextState = trajectoryToAppend[timeStep-1] + 1
                if r < simParams.p * 100 and trajectoryToAppend[timeStep-1] != 0:
                    nextState = trajectoryToAppend[timeStep-1] - 1
                #append it
                trajectoryToAppend.append(nextState)
                #see if we sell
                if nextState >= priceToSell:
                    sold = True
        trajectories.append(trajectoryToAppend)
    
    return trajectories


#take in simParams and return the cost estemate
def betaSimExpectation(simParams):
    trajectories = runBetaSim(simParams)

    #calculate the expected value for Xn and return
    #sum all of the last elements of the trajectories and divide by the count
    return sum(x[len(x)] for t in trajectories)/ len(trajectories)



#make a one step lookahead cost estemator 
#take in simParams and return the cost estemate with one step lookahead
def oneStepLookaheadExpectation(simParams):
    simParams.n += 1
    if simParams.Xn == 0:
        sameComponent = (1-simParams.p) * betaSimExpectation(simParams)
        
        simParams.Xn += 1
        increaseComponent = (1-simParams.p) * betaSimExpectation(simParams)
        return sameComponent + increaseComponent

    else:
        if simParams.Xn == simParams.Xbar:
            sameComponent = (1-simParams.p) * betaSimExpectation(simParams)
            
            simParams.Xn -= 1
            decreseComponent = (1-simParams.p) * betaSimExpectation(simParams)
            return sameComponent + decreseComponent

        else:
            sameComponent = (1-(2*simParams.p)) * betaSimExpectation(simParams)

            simParams.Xn += 1
            increaseComponent = (1-simParams.p) * betaSimExpectation(simParams)

            simParams.Xn -= 2
            decreseComponent = (1-simParams.p) * betaSimExpectation(simParams)

            return sameComponent + increaseComponent + decreseComponent



def runOneStepLookaheadSim(simParams):
    #the sale condition for the one step lookahead is 
    #if the estemated vlaue for this state is less then the current vlaue
    trajectories = []
    for _ in range(simParams.numtraj):
        trajectoryToAppend = []
        trajectoryToAppend.append(simParams.Xn)

        #check if we sell
        if simParams.Xn >= oneStepLookaheadExpectation(simParams):
            sold = True
        else:
            sold = False

        for timeStep in range(simParams.n, simParams.N+1):
            if not sold:
                r = random.randint(100)
                #generate the next state
                nextState = trajectoryToAppend[timeStep-1]
                if r > 100 - (simParams.p * 100) and trajectoryToAppend[timeStep-1] != simParams.Xbar:
                    nextState = trajectoryToAppend[timeStep-1] + 1
                if r < simParams.p * 100 and trajectoryToAppend[timeStep-1] != 0:
                    nextState = trajectoryToAppend[timeStep-1] - 1
                #append it
                trajectoryToAppend.append(nextState)
                
                #see if we sell
                trajParams = simParams
                trajParams.Xn = nextState
                trajParams.n = timeStep
                if nextState >= oneStepLookaheadExpectation(simParams):
                    sold = True
        trajectories.append(trajectoryToAppend)
    
    return trajectories



def main():
    Xbar = 7
    Xn = 3
    n = 0
    N = 14
    p = 0.25
    beta = 1.4
    numtraj = 20

    params = simParams(Xbar,Xn,n,N,p,beta,numtraj)

    #run a one step lookahead simulation
    OSLATrajectories = runOneStepLookaheadSim(params)

    #calculate the Jtable
    JTildetable = calcJtildeTable(OSLATrajectories, params)

    #print the Jtable
    printJtable(JTildetable, params)

    #print the policy table
    printPolicyTable(JTildetable, params)






if __name__ == "__main__":
    main()




