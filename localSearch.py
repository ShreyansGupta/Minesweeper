import numpy as np
import random
import copy
import Agent
import Environment

bombs = 10;
env=Environment.Environment(5,bombs)
a=Agent.Agent(env,0)
blasts = 0
iterations = 0
a.printMinesweeper();
x = int(random.uniform(0,a.dimension))
y = int(random.uniform(0,a.dimension))
# while(a.agentBoard[x][y] != -2):
#   x = int(random.uniform(0,a.dimension)
#   y = int(random.uniform(0,a.dimension))
# print (str(x)+"**"+str(y))
while(a.getUnknownCount() > 0):
    iterations += 1
    # (x,y) = a.getMinProbability()
    x = int(input())
    y = int(input())
    result = a.env.reveal(x,y)
    if(result == -1):
        print("Bomb blast")
        blasts += 1
    a.agentBoard[x][y] = result
    a.updateKnowledge(True)
    a.printMinesweeper()
print("score : "+str(float(10-blasts)/10))

