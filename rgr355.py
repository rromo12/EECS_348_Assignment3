#!/usr/bin/env python
# EECS 348
# Group: Rene Romo(rgr355) Tessa Haldes(tah210) Camille Warren(cew361)


import struct, string, math
from copy import *
import time
import timeit
class SudokuBoard:
    """This will be the sudoku board game object your player will manipulate."""
  
    def __init__(self, size, board):
      """the constructor for the SudokuBoard"""
      self.BoardSize = size #the size of the board
      self.CurrentGameBoard= board #the current state of the game board
      self.Domains = self.domains()

    def empty_domains(self):
        """Returns False if Empty List in Domains otherwise true"""
        domains=self.Domains
        size = self.BoardSize
        for row in range(size):
            for col in range(size):
                if(domains[row][col]==[]):
                    return True
        return False

    def get_domain(self, row, col):
        """Returns Domain of a Single Cell"""
        BoardArray = self.CurrentGameBoard
        init_dom = []
        #if the cell is set then domain is just it's current value
        if (BoardArray[row][col] != 0):
            dom = [(BoardArray[row][col])]
        else:
        #otherwise check row, column and smallgrid
            for i in range(1, self.BoardSize+1):
                init_dom.append(i) #sets domain to contain all possible values
            #Check Column
            temp = init_dom
            for c in range(0, self.BoardSize):
                if (BoardArray[row][c] != 0):
                    temp[(BoardArray[row][c])-1] = 0
                    #removes same values in column

            #Check Row
            for r in range(0, self.BoardSize):
                if (BoardArray[r][col] != 0 ):
                    temp[(BoardArray[r][col])-1] = 0
                    #removes same values in row

            subsquare = int(math.sqrt(self.BoardSize))
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                   if(BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]!=0):
                        temp[(BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]) - 1] = 0

            for val in range(1, self.BoardSize):
                if (temp[self.BoardSize-val] == 0):
                    dom = temp
                    dom.pop(self.BoardSize-val)
        return dom

    def domains(self):
        """Generates an array of arrays in the same format of GameBoard with the domains of corresponding cells"""
        domains=[]
        temp=deepcopy(self.CurrentGameBoard)
        list = self.empty_cells()
        for cell in list:
            domains.append(self.get_domain(cell[0],cell[1]))
            temp[cell[0]][cell[1]]= self.get_domain(cell[0],cell[1])
        return temp

    def update_domain(self,row,col,val):
        """Updates Domains of Current Board after a move is made"""
        domains = self.Domains

        for c in range(0, self.BoardSize):
            if(isinstance(domains[row][c],list)):
                if val in domains[row][c]: domains[row][c].remove(val)

        for r in range(0, self.BoardSize):
            if(isinstance(domains[r][col],list)):
                if val in domains[r][col]: domains[r][col].remove(val)

        subsquare = int(math.sqrt(self.BoardSize))
        SquareRow = row // subsquare
        SquareCol = col // subsquare
        for i in range(subsquare):
            for j in range(subsquare):
                if(isinstance(domains[SquareRow*subsquare+i][SquareCol*subsquare+j],list)):
                   if val in domains[SquareRow*subsquare+i][SquareCol*subsquare+j]: domains[SquareRow*subsquare+i][SquareCol*subsquare+j].remove(val)
        self.Domains=domains                
         
    def set_value(self, row, col, value):
        global consistency
        """This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""
        #add the value to the appropriate position on the board
        self.CurrentGameBoard[row][col]=value
        consistency+=1
        self.update_domain(row,col,value)
        #return a new board of the same size with the value added
        return SudokuBoard(self.BoardSize, self.CurrentGameBoard)
                                                                  
    def empty_cells(self):
        """Returns a list of the row and col of Empty Cells"""
        ec_list=[]
        for row in range(self.BoardSize):
            for col in range(self.BoardSize):
                if(self.CurrentGameBoard[row][col] == 0):
                    ec_list.append([row, col])
        return ec_list
    
    def no_zeroes(self):
        """Gets rid of zeros in domain created when deepcopying a sudoku board"""
        domains = self.Domains
        for row in range(self.BoardSize):
            for col in range(self.BoardSize):
                if(isinstance(domains[row][col],list)):
                    if 0 in domains[row][col]: domains[row][col].remove(0)    
        self.Domains = domains
                                                         
    def print_board(self):
        """Prints the current game board. Leaves unassigned spots blank."""
        div = int(math.sqrt(self.BoardSize))
        dash = ""
        space = ""
        line = "+"
        sep = "|"
        for i in range(div):
            dash += "----"
            space += "    "
        for i in range(div):
            line += dash + "+"
            sep += space + "|"
        for i in range(-1, self.BoardSize):
            if i != -1:
                print "|",
                for j in range(self.BoardSize):
                    if self.CurrentGameBoard[i][j] > 9:
                        print self.CurrentGameBoard[i][j],
                    elif self.CurrentGameBoard[i][j] > 0:
                        print "", self.CurrentGameBoard[i][j],
                    else:
                        print "  ",
                    if (j+1 != self.BoardSize):
                        if ((j+1)//div != j/div):
                            print "|",
                        else:
                            print "",
                    else:
                        print "|"
            if ((i+1)//div != i/div):
                print line
            else:
                print sep

def parse_file(filename):
    """Parses a sudoku text file into a BoardSize, and a 2d array which holds
    the value of each cell. Array elements holding a 0 are considered to be
    empty."""

    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val
    
    return board
    
def is_complete(sudoku_board):
    """Takes in a sudoku board and tests to see if it has been filled in
    correctly."""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    #check each cell on the board for a 0, or if the value of the cell
    #is present elsewhere within the same row, column, or square
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col]==0:
                return False
            for i in range(size):
                if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                    return False
                if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                    return False
            #determine which square the cell is in
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                            == BoardArray[row][col])
                        and (SquareRow*subsquare + i != row)
                        and (SquareCol*subsquare + j != col)):
                            return False
    return True

def is_consistent(sudoku_board):
    """Takes in a sudoku board and tests to see if it is legal"""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    #check if each value
    #is present elsewhere within the same row, column, or square
    for row in range(size):
        for col in range(size):
            for i in range(size):
                if ((BoardArray[row][i] == BoardArray[row][col]) and (i != col) and (BoardArray[row][i]!=0)):
                    return False
                if ((BoardArray[i][col] == BoardArray[row][col]) and (i != row) and (BoardArray[i][col]!=0)):
                    return False
            #determine which square the cell is in
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                            == BoardArray[row][col])
                        and (SquareRow*subsquare + i != row)
                        and (SquareCol*subsquare + j != col) 
                        and (BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]!=0)):
                            return False
    return True

def solve_backtracking(sudoku_board,forward_checking, MCV, MRV,LCV):
    """implementation of backtracking"""
    global consistency
    global limit
    #basecase
    if(is_complete(sudoku_board)): 
        return sudoku_board
    if(consistency>limit):
        return False 
    #select an unassigned variable 
    unassigned = sudoku_board.empty_cells()
    currcell= unassigned.pop()

    #possible values for current cell, in this case 1:sizeof board
    D = range(1,sudoku_board.BoardSize+1)
    #for each value v in D do
    for v in D:
        #if v is consistent then
        temp=deepcopy(sudoku_board.set_value(currcell[0],currcell[1],v))
        if(is_consistent(temp)):
            #add (X=v) to a
            temp.set_value(currcell[0],currcell[1],v)
            #result <- CPS-Backtracking
            result = solve_backtracking(temp,forward_checking, MCV, MRV,LCV)
            #if result != failure then return
            if (result != False):
                return result 
    return False
    
def MRV_select(sudoku_board,celllist):
    """Return location [row,col] of unassigned variable with least remaining values"""
       min = sudoku_board.BoardSize
       if (celllist ==[]):
           return 0 
       for cell in celllist:
           if(len(sudoku_board.Domains[cell[0]][cell[1]]) < min):
               min =len(sudoku_board.Domains[cell[0]][cell[1]])
               mincell=cell
       return mincell


def MCV_select(sudoku_board,celllist):
    """returns location of unassigned variable involved in most constraints"""
    max=-1
    templist=[]
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    for cell in celllist:
        #check the row col and grid of the cell to see how many empty spaces remain
        for row in range(size):
            ##same col
            if (BoardArray[row][cell[1]]==0 and (not row == cell[0])):
               if [row,cell[1]]   not in templist: templist.append([row,cell[1]])

        for col in range(size):            
             ##same row
             if (BoardArray[cell[0]][col]==0 and (not col == cell[1])):
                        if [cell[0],col]   not in templist: templist.append([cell[0],col])
                #determine which square the cell is in
        row=cell[0]
        col=cell[1]
        SquareRow = row // subsquare
        SquareCol = col // subsquare
        for i in range(subsquare):
            for j in range(subsquare):
                if(BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]==0 and (not (SquareRow*subsquare+i ==cell[0] and SquareCol*subsquare+j==cell[1]))):
                        if [[SquareRow*subsquare+i],[SquareCol*subsquare+j]] not in templist: templist.append([SquareRow*subsquare+i,SquareCol*subsquare+j])


        tempmax=0
        tempmax=len([list(x) for x in set(tuple(x) for x in templist)])
        if(tempmax>max):
            max=tempmax
            retcell=cell
        templist=[]
    return retcell

def LCV_select(sudoku_board,cell,domain):
    """returns value which would constrain the least ammount of unassigned variables"""
    curmin=0
    retv = 0
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    min = 24
    subsquare = int(math.sqrt(size))
    for v in domain:
        for row in range(size):
            ##same col
            if (v in sudoku_board.get_domain(row,cell[1]) and (not row == cell[0])):
               curmin+=1

        for col in range(size):            
             ##same row
             if (v in sudoku_board.get_domain(cell[0],col) and (not col == cell[1])):
                curmin+=1
                #determine which square the cell is in
        row=cell[0]
        col=cell[1]
        SquareRow = row // subsquare
        SquareCol = col // subsquare
        for i in range(subsquare):
            for j in range(subsquare):
                if(v in sudoku_board.get_domain(SquareRow*subsquare+i,SquareCol*subsquare+j) and (not (SquareRow*subsquare+i ==cell[0] and SquareCol*subsquare+j==cell[1]))):
                        curmin+=1

            
        if(curmin<=min and not v == 0):
                min = curmin
                retv=v
        curmin=0
    return retv
        
     #for each value in domain count the number of cells in the row/column/subsquare that have that value in their domain
     #return the value with the min number of cells which have that number in their domain
     #remove the value from domain

def solve_forwardchecking(sudoku_board, forward_checking, MCV, MRV,LCV):
    """Forward Checking+heuristics"""
    global consistency
    global limit
    #basecase
    if(consistency>limit):
        return False 
    if(is_complete(sudoku_board)): 
        return sudoku_board

    #select an unassigned variable,use random, MRV or MCV
    unassigned = sudoku_board.empty_cells()
    
    if(MRV):
        currcell= MRV_select(sudoku_board,unassigned)
    elif(MCV):
        currcell= MCV_select(sudoku_board,unassigned)
    else:
        currcell= unassigned.pop()
    #possible values for current cell
    if(is_complete(sudoku_board)): 
        return sudoku_board
    D = sudoku_board.Domains[currcell[0]][currcell[1]]

    #print D
    #for each value v in D do
    for v in range(len(D)):
        #if v is consistent then 
        #select v from D here with lcv() or just next value
        if(LCV):
            v=LCV_select(sudoku_board,currcell,D)
            D.remove(v)
        else:
            v=D[v]
       
        #print sudoku_board.Domains
        tempD= deepcopy(D)
        temp=deepcopy(sudoku_board.set_value(currcell[0],currcell[1],v))
        temp.no_zeroes()
        D=tempD
        #print "Making Move " + str(currcell) + " " + str(v)
        #print "Domain \n"
        #print temp.Domains
        #print temp.empty_domains()
        if (temp.empty_domains()):
            continue
        if(is_consistent(temp)):

            #add (X=v) to a
            temp.set_value(currcell[0],currcell[1],v)
            #result <- CPS-Backtracking
            result = solve_forwardchecking(temp,forward_checking, MCV, MRV,LCV)
            #if result != failure then return
            if (result != False):
                return result 
    return False

def init_board(file_name):
    """Creates a SudokuBoard object initialized with values from a text file"""
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)

def solve(initial_board, forward_checking = False, MRV = False, MCV = False,LCV = False):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """
    
    global consistency
    global limit
    consistency=0
    limit = 10000
    start = timeit.default_timer()
    if(forward_checking):
        print "Solving with forward checking"
        if(MRV):
            print " using MRV"
        if(MCV):
            print " using MCV"
        if(LCV):
            print " using LCV"
        sb_solved=solve_forwardchecking(initial_board,forward_checking,MCV,MRV,LCV)
    else:
        sb_solved=solve_backtracking(initial_board,forward_checking,MCV,MRV,LCV)
    
    
    if (not consistency>limit):
        sb_solved.print_board()   
    stop = timeit.default_timer()
    print "Runtime was: " + str(stop-start)
    print "Consistency Checks: " + str(consistency) 
    
    return sb_solved



def main():
    
    sb =init_board("16_16.sudoku")
    sb.print_board()
    print "Solving"
    fb=solve(sb,True,False,True,False)

    
   
     
if __name__ == "__main__":
    main()