import numpy as np
import random
import copy
import Environment
import Agent
import pickle
import minesweeper
import strategies
import time

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
startTime = time.time()
blasts = minesweeper.playMinesweeperAI(env, strategies.getCheckSATCell)
endTime = time.time()
print("Total time : "+str(endTime-startTime))
print("getCheckSATCell score : "+str(float(bombs-blasts)/bombs))