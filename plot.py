import matplotlib.pyplot as plt
import numpy as np
import random
import copy
import Environment
import Agent
import pickle
import minesweeper
import strategies
import time

dimension = 30
mineDensity = [0.1,0.2,0.3,0.4,0.5,0.6]
avgScore1 = []
avgScore2 = []
avgScore3 = []
avgScore4=[]
for mineDen in mineDensity:
	score1 = score2 = score3 = score4= 0
	bombs = int(mineDen*dimension*dimension)
	for i in range(10):
		env=Environment.Environment(dimension,bombs)
		# blasts1 = minesweeper.playMinesweeper(env, strategies.getRandomNextCell)
		# blasts2 = minesweeper.playMinesweeper(env, strategies.getMinProbCell)
		blasts3 = minesweeper.playMinesweeperAI(env, strategies.getCheckSATCell)
		blasts4 = minesweeper.playMinesweeperAIBonus(env, strategies.getCheckSATCell)

		# score1 += (float(bombs-blasts1)/bombs)
		# score2 += (float(bombs-blasts2)/bombs)
		score3 += (float(bombs-blasts3)/bombs)
		score4 += (float(bombs-blasts4)/bombs)

	# avgScore1.append(score1/10)
	# avgScore2.append(score2/10)
	avgScore3.append(score3/10)
	avgScore4.append(score4/10)

# print(avgScore1)
# print(avgScore2)
print(avgScore3)
print(avgScore4)


fig = plt.figure()
# plt.plot(mineDensity, avgScore1)
# plt.plot(mineDensity, avgScore2)
plt.plot(mineDensity, avgScore3,label="Original Algorithm Result")
plt.plot(mineDensity, avgScore4, label="Bonus Algorithm Result")
plt.xlabel('Mine Density')
plt.ylabel('Average Score')
plt.title('avgScore vs mineDensity')
plt.show()

