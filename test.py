import numpy as np
import random
import copy
import Environment
import Agent
import pickle
import minesweeper

bombs = 10
env=Environment.Environment(5,bombs)


def iteration(a,x,y):
	a.agentBoard[x][y] = a.env.reveal(x,y)
	a.updateKnowledge(True)
	a.printMinesweeper()

bombs = 10;
env=Environment.Environment(5,bombs)
a=Agent.Agent(env,0)
blasts = 0
iterations = 0
a.printMinesweeper();