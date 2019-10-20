# -*- coding: utf-8 -*-
"""MineSweeper.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Jzby29ZtnAf9dR2N_2ooZWRuPpnIecQE
"""

import numpy as np
import random
import copy
import Agent
import Environment

def playMineSweeper(env, getNextCell):
    agent = Agent.Agent(env,0)
    blasts = 0
    iterations = 0
    agent.printMinesweeper();
    while(agent.getUnknownCount() > 0):
        iterations += 1
        (x,y) = agent.getNextCell()
        result = agent.env.reveal(x,y)
        if(result == -1):
            print("Bomb blast")
            blasts += 1
        agent.agentBoard[x][y] = result
        agent.updateKnowledge(True)
        agent.printMinesweeper()
    return blasts

