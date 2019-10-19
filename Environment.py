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


    def reveal(self,row,column):
        if self.mazeCells[row][column] == -1 :
            return -1;  
        
        count = 0
        if row >= 1:
            if column>=1 and self.mazeCells[row-1][column-1] == -1:
                count +=1
            if column<self.dimension-1 and self.mazeCells[row-1][column+1] == -1:
                count +=1
            if self.mazeCells[row-1][column] == -1:
                count +=1

        if column >= 1:
            if row<self.dimension-1 and self.mazeCells[row+1][column-1] == -1:
                count +=1
            if self.mazeCells[row][column-1] == -1:
                count +=1

        if row < self.dimension-1:
            if column<self.dimension-1 and self.mazeCells[row+1][column+1] == -1:
                count +=1
            if self.mazeCells[row+1][column] == -1:
                count +=1

        if column < self.dimension-1 and self.mazeCells[row][column+1] == -1:
            count +=1
        
        return count
