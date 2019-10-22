import numpy as np
import random
import copy
import Agent
import Environment
import strategies

def iteration(agent,x,y):
    '''
    reveals the cell value at coordinates (x,y) and prints the Agent game board
    '''
    if(agent.agentBoard[x][y] != -2):
        print("SHOULDN'T COME HERE ERROR!!");
    # agent.agentBoard[x][y] = agent.env.reveal(x,y)
    agent.updateKnowledge(x,y,agent.env.reveal(x,y),True)
    agent.printMinesweeper()

def playMinesweeper(env, getNextCell):
    '''
    env : Environment Object that stores the information of the enivronment or the board.
    getNextCell : The stratergy used by the agent to decide the next move.
    returns the number of times the agent clicked on a mine cell.
    '''
    agent = Agent.Agent(env,0)      # Create an object of Agent class
    blasts = 0
    noOfIter = 0
    agent.printMinesweeper()
    while(agent.getUnknownCount() > 0):     #Game still not completed
        noOfIter += 1
        (x,y) = getNextCell(agent)
        print("Revealed: "+str(x)+" "+str(y))
        result = agent.env.reveal(x,y)
        if(result == -1):
            print("Bomb blast")
            blasts += 1
        # agent.agentBoard[x][y] = result
        agent.updateKnowledge(x,y,result,True)
        # agent.printMinesweeper()
    agent.printMinesweeper()
    return blasts

def playMinesweeperAI(env, getNextCell):
    '''
    env : Environment Object that stores the information of the enivronment or the board.
    getNextCell : The stratergy used by the agent to decide the next move.
    returns the number of times the agent clicked on a mine cell.
    '''
    agent = Agent.Agent(env,0)      # Create an object of Agent class
    blasts = 0
    noOfIter = 0
    agent.printMinesweeper()
    (x,y) = strategies.getFirstRandomNextCell(agent)    #Agent uniformly chooses any random cell to play the first move.
    iteration(agent,x,y)
    while(agent.getUnknownCount() > 0):     #Game still not completed
        noOfIter += 1
        (res,x,y) = getNextCell(agent)
        resultString = "Revealed: "+str(x)+" "+str(y)+" "
        if(res == -2 or res == -3):
            result = agent.env.reveal(x,y)  #reveals information about the cell.
            if(result == -1):
                resultString += "Bomb blast"
                blasts += 1
            elif(res == -3):
                resultString += "Found safe cell"
        else:
            resultString += "Found Bomb"
            result = -1
        # agent.agentBoard[x][y] = result
        print(resultString)
        agent.updateKnowledge(x,y,result,True)  # The agent updates its knowledge based on the information it recieved from its move.
        agent.printMinesweeper()
    agent.printMinesweeper()
    return blasts

