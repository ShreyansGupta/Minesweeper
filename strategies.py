import Agent
import random

def getRandomNextCell(agent):
    x = int(random.uniform(0,agent.dimension))
    y = int(random.uniform(0,agent.dimension))
    while(agent.agentBoard[x][y] != -2):
        x = int(random.uniform(0,agent.dimension))
        y = int(random.uniform(0,agent.dimension))
    return (x,y)

def getMinProbCell(agent):
	minProbList = agent.getMinProbability()
	unrevealedCountList = list(len(agent.getKnowledge(i,j)[0]) for (i,j) in minProbList)
	return minProbList[unrevealedCountList.index(min(unrevealedCountList))]