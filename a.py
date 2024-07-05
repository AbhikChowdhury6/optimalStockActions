#part a

Xbar = 7
X0 = 3
N = 14
p = 0.25


Jtable = [[-1]*(N+1) for i in range(Xbar + 1)]

policyTable = [["   "]*(N+1) for i in range(Xbar + 1)]



#fill in the N column with the expected values

for priceIndex in range(len(Jtable)):
    if not(priceIndex > (X0 + N) or priceIndex < (X0 - N)):
        Jtable[priceIndex][N] = priceIndex

#for x in Jtable:
#z    print (x)

#fill in the rest of the table
#iterate through every column staring from n-1 to zero
for colIndex in range(N-1, -1, -1):
    #iterate through every row starting from Xbar going down
    for priceIndex in range(Xbar + 1):
        #check if this state is reachable based on N if not leave at -1 
        if priceIndex > (X0 + colIndex) or priceIndex < (X0 - colIndex):
            pass
        else: 
            #if j is at index 0 then calculate j diffrently
            if priceIndex == 0:
                Jtable[priceIndex][colIndex] = (Jtable[priceIndex][colIndex + 1] * (1-p)) + (Jtable[priceIndex + 1][colIndex + 1] * p)
            #else calculate the expected value from the i+1 column and row j+-1
            else:
                if priceIndex == Xbar:
                    Jtable[priceIndex][colIndex] = Xbar
                else:
                    #print(colIndex)
                    #print(priceIndex)
                    pnoChange = 1 - (2* p)
                    Jtable[priceIndex][colIndex] = (Jtable[priceIndex][colIndex + 1] * pnoChange) + (Jtable[priceIndex + 1][colIndex + 1] * p) + (Jtable[priceIndex - 1][colIndex + 1] * p)
    #print("column ", colIndex )
    
#for x in Jtable:
#    print (x)



#print the Jtable

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
for col in Jtable[Xbar]:
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
        if Jtable[Xbar - rowindex][col] >= 0:
            toPrint += " %.4f"%Jtable[Xbar - rowindex][col]
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




#fill in the policy table
for colIndex in range(N, -1, -1):
    #iterate through every row starting from Xbar going down
    for priceIndex in range(Xbar + 1):
        #check if this state is reachable based on N if not leave at -1 
        if Jtable[priceIndex][colIndex] == -1:
            pass
        else:
            if Jtable[priceIndex][colIndex] <= priceIndex:
                policyTable[priceIndex][colIndex] = "  S"
            else:
                policyTable[priceIndex][colIndex] = "  D"



#for x in policyTable:
#    print(x)


#print policyTable
toPrint = ""
#print Y label, Y ticks, Yline, top row of data
toPrint +=  Ylabel
toPrint +=  str(Yticks[0])
toPrint += " |"
for col in policyTable[Xbar]:
    toPrint += col
print(toPrint)

#for every row
for rowindex in range(1,Xbar+1):
    # print Y label spacer, Y line, that row of data
    toPrint = ""
    toPrint += " " * len(Ylabel)
    toPrint += str(Yticks[rowindex])
    toPrint += " |"
    for col in range(N+1):
        toPrint += policyTable[Xbar - rowindex][col]
    print(toPrint)
    

#print Xline
toPrint = " " * len(Ylabel)
toPrint += "  |"
toPrint += "_" * (3 * len(Xticks))
print(toPrint)

#print Xticks
toPrint = ""
toPrint += " " * len(Ylabel)
toPrint += "    "
for x in Xticks:
    toPrint += '{:3}'.format(str(x))
print(toPrint)

#print X label
toPrint = ""
toPrint += " " * len(Ylabel)
toPrint += "    "
toPrint += Xlabel
print(toPrint)







































