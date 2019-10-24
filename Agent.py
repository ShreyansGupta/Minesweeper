"""*   -1 : BOMB
*   -2 : UnRevealed
*   -3 : SafeUnrevealed
*   0-8: Mine Count Revealed
"""
import numpy as np
import random
import copy
import pdb
# Class for Agent Board and actions it can perform
# Agent Board is the matrix on which Agent will play
# Probability Matrix maintains the probability of mine at each cell
class Agent:
    def __init__(self,env,i, improve= False):
        if i == 0:
            self.dimension=env.dimension
            self.env = env
            self.agentBoard = np.array([-2]*(self.dimension*self.dimension))
            self.agentBoard = np.reshape(self.agentBoard,(self.dimension,self.dimension))
            self.probabilityMatrix = np.array([1.0]*(self.dimension*self.dimension), dtype= float)
            self.probabilityMatrix = np.reshape(self.probabilityMatrix, (self.dimension,self.dimension))
            self.improvement = improve
            # Now we know count of total mines
            if(self.improvement):
                self.totalMines = env.no_of_mines
                self.effectiveTotalMines = env.no_of_mines

        elif i == 1:
            # This is for creating copy of agent board to check satisfiablity of assumption we take
            # Probability Matrix for copy board to choose minimum probability neighbor to proceed
            self.dimension = len(env.agentBoard)
            self.agentBoard = copy.deepcopy(env.agentBoard)
            self.probabilityMatrix = np.array([1.0]*(self.dimension*self.dimension), dtype= float)
            self.probabilityMatrix = np.reshape(self.probabilityMatrix, (self.dimension,self.dimension))
            self.improvement = env.improvement
            if(self.improvement):
                self.totalMines = env.env.no_of_mines
                self.effectiveTotalMines = env.env.no_of_mines

    # This method returns unrevealed neighbors of a cell,total safe neighbors and revealed mines
    def getKnowledge(self,row,column):
        #Unrealved : returns list of coordinates
        #revealed = 8-len(unrevealed)  
        #count_revealed: revealed - revealed mines
        unrevealed = []
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

    # We get list of neighbours we can query( because safe) or those for which we know they have mine
    # After updating those cells we will update our knowledge in nearby neighbors
    # Returns all the changed elements
    # If query is false then we are just expanding our knowledge base and checking satisfiablity
    # with assumption so cells those which are marked as safe (-3) shouldn't be queried.

    def updateKnowledge(self,i,j,val, query):
        self.agentBoard[i][j]=val
        if(self.improvement and val == -1):
            self.effectiveTotalMines -= 1
        noOfIter = 0
        currSet1=set()
        changedElements = set()
        currSet1.add((i,j))
        changedElements.add((i,j))
        while(currSet1):
            x,y=currSet1.pop()
            updated_set = self.updateNeighbours(x, y)
            # pdb.set_trace()
            currSet1 = currSet1.union(updated_set)
            changedElements = changedElements.union(updated_set)
            while (updated_set):
                p, q = updated_set.pop()
                if query:
                    self.querySafeCells(p,q)
            noOfIter += 1
        return changedElements

    # After identifying safe cell we will query it to reveal the count of mines around it
    def querySafeCells(self, row, column):
        if(self.agentBoard[row][column] == -3):
            self.agentBoard[row][column] = self.env.reveal(row,column)
          
    # Method to Print the Agent Board( Minesweeper)
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

    # Returns number of cells whose information is not known
    def getUnknownCount(self):
        count = 0;
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.agentBoard[i][j] == -2:
                    count += 1;
        return count;
    # This method returns list of updated neighbors
    def updateNeighbours(self, row, column):
        updated_neighbours=set()
        minesCount = self.agentBoard[row][column]
        if(minesCount < 0):
            return updated_neighbours
        (unrevealedList,safeCount,revealedMines) = self.getKnowledge(row, column)
        effectiveMinesCount = minesCount - revealedMines
        # newInfo = 0;
        # if mines count is equal to revealedMines then all remaining are safe and can be queried
        if(minesCount == revealedMines):
            for (r,c) in unrevealedList:
                # Safe to query these elements
                self.agentBoard[r][c] = -3;
                updated_neighbours.add((r,c))
                # newInfo = 1
        # Adding neighbors who are definately a mine to reveal them
        if(effectiveMinesCount == len(unrevealedList)):
            for (r,c) in unrevealedList:
                if(self.improvement):
                    self.effectiveTotalMines -= 1
                self.agentBoard[r][c] = -1;
                updated_neighbours.add((r, c))
                # newInfo = 1
        return updated_neighbours

    # when exploring on copy matrix by assumption this method tells us if there is inconsistency with our knowledge
    # Returns True if there is an inconsistency and vice versa
    def checkInconsistencyCell(self,row,col):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 or j == 0:
                    continue
                elif 0 <= row + i < self.dimension and 0 <= col + j < self.dimension:
                    minesCount = self.agentBoard[row+i][col+j]
                    if(minesCount < 0):
                        continue
                    else:
                        (unrevealedList,safeCount,revealedMines) = self.getKnowledge(row+i, col+j)
                        effectiveMinesCount = minesCount - revealedMines
                        if(len(unrevealedList) == 0 and effectiveMinesCount != 0):
                            return True
                        elif(len(unrevealedList) == 0):
                            continue
                        else:
                            prob = float(effectiveMinesCount)/float(len(unrevealedList))
                            if(prob < 0 or prob > 1):
                                return True
        return False

    #Consistency of all the Changed Elements are checked
    def checkInconsistencySet(self,changedElements):
        while changedElements:
            (p,q) = changedElements.pop()
            if(self.checkInconsistencyCell(p,q)):
                return True
        return False
    # Satisfiability of each cell is checked by putting it safe and then mine if safe fails
    def checkSat(self, row, column):
        isMine = self.checkSatVal(row, column, -3)      #Setting the cell safe
        if(isMine):
            # self.agentBoard[row][column] = -1
            return -1
        else:
            isNotMine = self.checkSatVal(row, column, -1)       #Setting the cell Mine
            if(isNotMine):
                # self.agentBoard[row][column] = -3
                return -3
            else:
                return -2                                   #Set -2 if unclear
    # Start of checking satisfiability of an element on substituting it mine or safe cell
    def checkSatVal(self, row, column, val):
        copyBoard = Agent(self, 1) #Create a copy board
        # copyBoard.agentBoard[row][column] = val
        changedElements = copyBoard.updateKnowledge(row,column, val, False)     #Updating copy board neighbors
        return copyBoard.checkInconsistencySet(changedElements)

    # Updating Probability of each cell based on effectiveMinesCount and UnrevealedList
    def updateProbability(self):
        unrevealedCount = self.getUnknownCount()
        for row in range(self.dimension):
            for col in range(self.dimension):
                if(self.improvement and self.agentBoard[row][col] == -2):
                    self.probabilityMatrix[row][col] = float(self.effectiveTotalMines)/float(unrevealedCount)
                else:
                    self.probabilityMatrix[row][col] = 2
        # pdb.set_trace()
        for row in range(self.dimension):
            for col in range(self.dimension):
                unrevealedList, safe_revealed, revealed_mines = self.getKnowledge(row,col)
                if self.agentBoard[row][col]>=0 and len(unrevealedList) != 0:
                    minesCount = self.agentBoard[row][col]
                    effectiveMinesCount = minesCount - revealed_mines
                    probability = float(effectiveMinesCount)/float(len(unrevealedList))
                    for (i,j) in unrevealedList:
                        if(self.improvement):
                            self.probabilityMatrix[i][j] = max(self.probabilityMatrix[i][j], probability)
                        else:
                            if(self.probabilityMatrix[i][j] == 2):
                                self.probabilityMatrix[i][j] = probability
                            else:
                                self.probabilityMatrix[i][j] = max(self.probabilityMatrix[i][j], probability)
                elif(self.agentBoard[row][col] == -1):
                    self.probabilityMatrix[row][col] = 3.0
    # All cells with probability less than 1
    def getMinProbabilityAll(self):
        minProb = []
        self.updateProbability()
        (a,b) = np.where(self.probabilityMatrix <= 1)
        for i in range(len(a)):
            minProb.append((self.probabilityMatrix[a[i]][b[i]],a[i],b[i]))
        minProb.sort()
        return minProb
    # Gives minimum probability cells for given number of count
    def getMinProbability(self, noOfMin):
        minProb = []
        self.updateProbability()
        (a,b) = np.where(self.probabilityMatrix <= 1)
        for i in range(len(a)):
            minProb.append((self.probabilityMatrix[a[i]][b[i]],a[i],b[i]))
        minProb.sort()
        return minProb[:noOfMin]
    
    def expandInference(self):
        minProbList = self.getMinProbabilityAll()
        bombs = [(x,y) for (p,x,y) in minProbList if p == 1]
        for (x,y) in bombs:
            self.updateKnowledge(x,y,-1,True)
        safes = [(x,y) for (p,x,y) in minProbList if p == 0]
        for (x,y) in safes:
            self.updateKnowledge(x,y,self.env.reveal(x,y),True)

# Gives number of effectivemines around a cell(Total-revealed)    
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
