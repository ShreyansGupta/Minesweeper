import Agent
import random
import numpy as np
import pdb

def getFirstRandomNextCell(agent):
	x = int(random.uniform(0,agent.dimension))
	y = int(random.uniform(0,agent.dimension))
	agent.env.reveal(x,y,True);
	return (x,y)

def getRandomNextCell(agent):
    x = int(random.uniform(0,agent.dimension))
    y = int(random.uniform(0,agent.dimension))
    while(agent.agentBoard[x][y] != -2):
        x = int(random.uniform(0,agent.dimension))
        y = int(random.uniform(0,agent.dimension))
    return (x,y)

def getMinProbCell(agent):
	noOfMin = 10
	minProbList = agent.getMinProbability(noOfMin)
	unrevealedCountList = list(len(agent.getKnowledge(i,j)[0]) for (p,i,j) in minProbList)
	return minProbList[unrevealedCountList.index(min(unrevealedCountList))][1:]

def getMinEffectiveMines(agent):
    minEffectiveMines = []
    (xList,yList) = np.where(agent.agentBoard >= 1)
    for i in range(len(xList)):
        minEffectiveMines.append((agent.getEffectiveMines(xList[i],yList[i]),xList[i],yList[i]))
    (minEffMineCount,x,y) = minEffectiveMines.sort()[0]
    return (x,y)

def getCheckSATCell(agent):
	# minEffectiveMines = []
	# (xList,yList) = np.where(agent.agentBoard >= 1)
	# for i in range(len(xList)):
	#     minEffectiveMines.append((agent.getEffectiveMines(xList[i],yList[i]),xList[i],yList[i]))
	# minEffectiveMines.sort()
	minProbList = agent.getMinProbabilityAll()
	# bombs = [(x,y) for (p,x,y) in minProbList if p == 1]
	# safes = [(x,y) for (p,x,y) in minProbList if p == 0]
	candidates = list(set(minProbList[:5]).union(set(minProbList[-5:])))
	for (p,x,y) in candidates:
		unrevealedList, safe, revealedMines = agent.getKnowledge(x,y)
		# print(unrevealedList)
		for (rx,ry) in unrevealedList:
			result = agent.checkSat(rx,ry)
			if(result == -2):
				continue
			else:
				print("AI got a clue"+str((result,rx,ry)))
				return (result,rx,ry)
	(p,rx,ry) = minProbList[0]
	return (-2,rx,ry)

def getSomething(agent):
	noOfCheckSATCandidates = 10
	minProbList = agent.getMinProbability(noOfCheckSATCandidates)
	unrevealedCountList = list((len(agent.getKnowledge(i,j)),i,j) for (p,i,j) in minProbList).sort()
