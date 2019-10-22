import numpy as np
import random
import copy
import Environment
import Agent
import pickle
import minesweeper
import strategies

dimension = int(input("dimension: "))
bombs = int(input("bomb count: "))
env=Environment.Environment(dimension,bombs)
# agent=Agent.Agent(env,0)
# blasts = 0
# iterations = 0
# a.printMinesweeper();
# blasts = minesweeper.playMinesweeper(env, strategies.getRandomNextCell)
# print("getRandomNextCell score : "+str(float(bombs-blasts)/bombs))
# blasts = minesweeper.playMinesweeper(env, strategies.getMinProbCell)
# print("getMinProbCell score : "+str(float(bombs-blasts)/bombs))
blasts = minesweeper.playMinesweeperAI(env, strategies.getCheckSATCell)
print("getMinProbCell score : "+str(float(bombs-blasts)/bombs))