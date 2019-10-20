import numpy as np
import random
import copy
import Environment
import Agent
import pickle
import minesweeper
import strategies

def iteration(a,x,y):
	a.agentBoard[x][y] = a.env.reveal(x,y)
	a.updateKnowledge(True)
	a.printMinesweeper()

dimension = int(input("dimension: "))
bombs = int(input("bomb count: "))
env=Environment.Environment(dimension,bombs)
agent=Agent.Agent(env,0)
# blasts = 0
# iterations = 0
# a.printMinesweeper();
# blasts = minesweeper.playMinesweeper(env, strategies.getRandomNextCell)
# print("getRandomNextCell score : "+str(float(bombs-blasts)/bombs))
# blasts = minesweeper.playMinesweeper(env, strategies.getMinProbCell)
# print("getRandomNextCell score : "+str(float(bombs-blasts)/bombs))