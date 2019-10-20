"""*   -1 : BOMB
*   -2 : UnRevealed
*   -3 : SafeUnrevealed
*   0-8: Mine Count Revealed
"""
import numpy as np
import random
import copy

class Agent:
    def __init__(self,env,i):
        if i==0:
            self.dimension=env.dimension
            self.env = env
            self.agentBoard = np.array([-2]*(self.dimension*self.dimension))
            self.agentBoard = np.reshape(self.agentBoard,(self.dimension,self.dimension))
            self.probabilityMatrix = np.array([1.0]*(self.dimension*self.dimension), dtype= float)
            self.probabilityMatrix = np.reshape(self.probabilityMatrix, (self.dimension,self.dimension))
            # self.unRevealedMatrix = np.array([0]*(self.dimension*self.dimension)).reshape(self.dimension,self.dimension)
            # self.effectiveMinesCount = np.array([0]*(self.dimension*self.dimension)).reshape(self.dimension,self.dimension)
            # self.unRevealedCount = np.array([0]*(self.dimension*self.dimension)).reshape(self.dimension,self.dimension)
        else:
            self.dimension = len(env)
            self.agentBoard = copy.deepcopy(env)
            self.probabilityMatrix = np.array([1.0]*(self.dimension*self.dimension), dtype= float)
            self.probabilityMatrix = np.reshape(self.probabilityMatrix, (self.dimension,self.dimension))

    def getKnowledge(self,row,column):
        #Unrealved : returns list of coordinates
        #revealed = 8-len(unrevealed)  
        #count_revealed: revealed - revealed mines
        unrevealed = []
        revealed = 0
        revealed_mines = 0
        safe_unrevealed = 0
        safe_revealed = 0
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if(i == 0 and j == 0):
                    continue;
                elif 0<=row+i<self.dimension and 0<=column+j<self.dimension :
                    if self.agentBoard[row+i][column+j] == -1:
                        revealed_mines +=1
                    elif self.agentBoard[row+i][column+j] == -2:
                        unrevealed.append((row+i,column+j))
                    elif self.agentBoard[row+i][column+j] == -3:
                        safe_unrevealed +=1
                    elif self.agentBoard[row+i][column+j] >= 0:
                        safe_revealed += 1
        # revealed = 8-len(unrevealed)
        # safe_revealed = revealed - revealed_mines - safe_
        return (unrevealed, safe_revealed+safe_unrevealed, revealed_mines)

    def updateKnowledge(self,i,j,val, query):
        agentBoard[i][j]=val
        noOfIter = 0
        currSet1=set()
        currSet1.add((i,j))
        while(currSet1):
            x,y=currSet1.pop()
            updated_set = self.updateNeighbours(x, y)
            currSet1 = currSet1+updated_set
            while (updated_set):
                if query:
                    p, q = a.pop()
                    self.querySafeCells(p,q)

            noOfIter += 1
        return noOfIter

    def querySafeCells(self, row, column):
        if(self.agentBoard[row][column] == -3):
            self.agentBoard[i][j] = self.env.reveal(i,j)
          
    # def updateKnowledgeIter(self,query,prevSet):
    #     # count = 0
    #     while(prevSet):
    #         i,j=prevSet.pop()
    #         a=self.updateNeighbours(i,j)
    #
    #     return set1;

    def printMinesweeper(self):
        print("<<<<<<<<<<<<<<<start>>>>>>>>>>>>>>>>")
        for i in range(self.dimension):
            string = ""
            for j in range(self.dimension):
                if(self.agentBoard[i][j] == -2):
                    string += ("? ")
                elif(self.agentBoard[i][j] == -1):
                    string += ("* ")
                else:
                    string += str(self.agentBoard[i][j]) + " " 
            print(string+"\n")
        print("<<<<<<<<<<<<<<<<end>>>>>>>>>>>>>>>>>")

    def getUnknownCount(self):
        count = 0;
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.agentBoard[i][j] == -2:
                    count += 1;
        return count;

    def updateNeighbours(self, row, column):
        minesCount = self.agentBoard[row][column]
        if(minesCount < 0):
            return 0
        (unrevealedList,safeCount,revealedMines) = self.getKnowledge(row, column)
        effectiveMinesCount = minesCount - revealedMines
        # newInfo = 0;
        if(minesCount == revealedMines):
            for (r,c) in unrevealedList:
                # Safe to query these elements
                self.agentBoard[r][c] = -3;
                set1.add((r,c))
                # newInfo = 1
        if(8-minesCount == safeCount or effectiveMinesCount == len(unrevealedList)):
            for (r,c) in unrevealedList:
                self.agentBoard[r][c] = -1;
                set1.add((r, c))
                # newInfo = 1
        return set1

    def checkInconsistency(self):
        for i in range(self.dimension):
            for j in range(self.dimension):
                minesCount = self.agentBoard[i][j]
                if(minesCount < 0):
                    continue
                else:
                    (unrevealedList,safeCount,revealedMines) = self.getKnowledge(i, j)
                    if(revealedMines > minesCount):
                        return True
        return False

    def checkSat(self, row, column):
        isMine = self.checkSatVal(row, column, -3)
        if(isMine):
            # self.agentBoard[row][column] = -1
            return -1
        else:
            isNotMine = self.checkSatVal(row, column, -1)
            if(isNotMine):
                # self.agentBoard[row][column] = -3
                return -3
            else:
                return -2

    def checkSatVal(self, row, column, val):
        copyBoard = Agent(self.agentBoard, 1)
        copyBoard.agentBoard[row][column] = val
        copyBoard.updateKnowledge(False)
        return copyBoard.checkInconsistency()

    def updateProbability(self):
        for row in range(self.dimension):
            for col in range(self.dimension):
                self.probabilityMatrix[row][col] = 1
        for row in range(self.dimension):
            for col in range(self.dimension):
                if self.agentBoard[row][col]>=0:
                    minesCount = self.agentBoard[row][col]
                    unrevealedList, safe_revealed, revealed_mines = self.getKnowledge(row,col)
                    if(len(unrevealedList) == 0):
                        continue
                    effectiveMinesCount = minesCount - revealed_mines
                    probability = float(effectiveMinesCount)/float(len(unrevealedList))
                    for (i,j) in unrevealedList:
                        if(self.probabilityMatrix[i][j] == 1):
                            self.probabilityMatrix[i][j] = probability
                        else:
                            self.probabilityMatrix[i][j] = max(self.probabilityMatrix[i][j], probability)
                elif(self.agentBoard[row][col] == -1):
                    self.probabilityMatrix[row][col] = 2.0

    def getMinProbability(self, noOfMin):
        minProb = []
        self.updateProbability()
        (a,b) = np.where(self.probabilityMatrix < 1)
        for i in range(len(a)):
            minProb.append((self.probabilityMatrix[a[i]][b[i]],a[i],b[i]))
        minProb.sort()
        return minProb[:noOfMin]

    def getEffectiveMines(self,row,column):
        if(self.agentBoard[row][column] < 0):
            print("ERROR SHOULDN'T COME HERE")
            exit()
        revealed_mines = 0
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if(i == 0 and j == 0):
                    continue;
                elif 0<=row+i<self.dimension and 0<=column+j<self.dimension :
                    if self.agentBoard[row+i][column+j] == -1:
                        revealed_mines +=1
        return self.agentBoard[row][column] - revealed_mines
