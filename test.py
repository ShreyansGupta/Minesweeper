import numpy as np
import random
import copy
import Environment
import Agent

bombs = 10;
env=Environment.Environment(5,bombs)
a=Agent.Agent(env,0)
blasts = 0
iterations = 0
a.printMinesweeper();