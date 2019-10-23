import Agent
import random
import numpy as np
import pdb
# Random cell to be chosen and revealed
def getFirstRandomNextCell(agent):
	x = int(random.uniform(0,agent.dimension))
	y = int(random.uniform(0,agent.dimension))
	agent.env.reveal(x,y,True);
	return (x,y)
# Choose Random cell which is set as -2(Value unknown)
def getRandomNextCell(agent):
    x = int(random.uniform(0,agent.dimension))
    y = int(random.uniform(0,agent.dimension))
    while(agent.agentBoard[x][y] != -2):
        x = int(random.uniform(0,agent.dimension))
        y = int(random.uniform(0,agent.dimension))
    return (x,y)

def getUnrevealedCell(agent):
	for i in range(agent.dimension):
		for j in range(agent.dimension):
			if(agent.agentBoard[i][j] == -2):
				return (i,j)
	return (-1,-1)

# Takes minimum probability list and Chooses the cell with minimum value in UnrevealedCountList
# UnrevealedCountList contains count of unrevealed cell,safe cells and revealed mines
# One of the strategy for forward propagation
def getMinProbCell(agent):
	minProbList = agent.getMinProbability(10)
	if(len(minProbList) == 0):
		return getUnrevealedCell(agent)
	unrevealedCountList = list(len(agent.getKnowledge(i,j)[0]) for (p,i,j) in minProbList)
	unrevealedCountList.sort()
	return minProbList[0][1:]
# One of the strategy for forward propagation
# Gives cell with minimum Effective Mines
def getMinEffectiveMines(agent):
    minEffectiveMines = []
    (xList,yList) = np.where(agent.agentBoard >= 1)
    for i in range(len(xList)):
        minEffectiveMines.append((agent.getEffectiveMines(xList[i],yList[i]),xList[i],yList[i]))
    (minEffMineCount,x,y) = minEffectiveMines.sort()[0]
    return (x,y)

# This strategy selects 5 least probability cells and 5 max probability cells and checks satisfyability for them
# and returns if found any inconsistency if not found any inconsistency then return minimum probability cell
def getCheckSATCell(agent):
	minProbList = agent.getMinProbabilityAll()
	candidates = list(set(minProbList[:5]).union(set(minProbList[-5:])))
	candidates.sort()
	for (p,rx,ry) in candidates:
		result = agent.checkSat(rx,ry)
		if(result == -2):
			continue
		else:
			print("AI got a clue"+str((result,rx,ry)))
			return (result,rx,ry)
	if(len(minProbList) != 0):
		(p,rx,ry) = minProbList[0]
	else:
		(rx, ry) = getUnrevealedCell(agent)
		if(rx == -1):
			print("ERROR SHOULDN'T COME HERE!!")
	return (-2,rx,ry)
