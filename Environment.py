import numpy as np
import random
import copy

#random.seed(1)
class Environment:
    def __init__(self, d, n):
        '''
        d -> int : Dimension of board
        n -> int : Number of mines
        '''
        self.dimension = d
        self.no_of_mines = n
        self.mazeCells = np.array([0]*((d*d)-n) + [-1]*(n))
        np.random.shuffle(self.mazeCells)
        self.mazeCells = np.reshape(self.mazeCells,(d,d))


    def reveal(self,row,column, val=False,first = False):
        '''
        row,col -> int: The current row and column coordinates of the Cell.
        first -> Boolean value weather the move is first move or not. 
                 We assume that there cannot be a mine in the first move of the game and the 
                 agent will get a knowledge to further play the game.
        returns : The value of the current cell i.e. the number of mines in the neighbouring cells
        '''
        if val:
            if first == False and self.mazeCells[row][column] == -1 :
                return -1
            count = 0
            p0=0.4
            if random.uniform(0,1)>p0:
                for i in [-1,0,1]:
                    for j in [-1,0,1]:
                        if(i == 0 and j == 0):
                            continue
                        elif 0<=row+i<self.dimension and 0<=column+j<self.dimension :
                            if self.mazeCells[row+i][column+j] == -1:
                                count +=1
                self.mazeCells[row][column] = count
                return count
            else:
                return -3
        else:
            if first == False and self.mazeCells[row][column] == -1 :
                return -1
            count = 0
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if(i == 0 and j == 0):
                        continue
                    elif 0<=row+i<self.dimension and 0<=column+j<self.dimension :
                        if self.mazeCells[row+i][column+j] == -1:
                            count +=1
            self.mazeCells[row][column] = count
            return count
