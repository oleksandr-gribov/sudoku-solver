import csv
import itertools

class Board():

    ##########################################
    ####   Constructor
    ##########################################
    def __init__(self, filename):

        #initialize all of the variables
        self.n2 = 0
        self.n = 0
        self.spaces = 0
        self.board = None
        self.valsInRows = None
        self.valsInCols = None
        self.valsInBoxes = None
        self.unSolved = None

        #load the file and initialize the in-memory board with the data
        self.loadSudoku(filename)


    #loads the sudoku board from the given file
    def loadSudoku(self, filename):

        with open(filename) as csvFile:
            self.n = -1
            reader = csv.reader(csvFile)
            for row in reader:

                #Assign the n value and construct the approriately sized dependent data
                if self.n == -1:
                    self.n = int(len(row) ** (1/2))
                    if not self.n ** 2 == len(row):
                        raise Exception('Each row must have n^2 values! (See row 0)')
                    else:
                        self.n2 = len(row)
                        self.spaces = self.n ** 4
                        self.board = {}
                        self.valsInRows = [set() for _ in range(self.n2)]
                        self.valsInCols = [set() for _ in range(self.n2)]
                        self.valsInBoxes = [set() for _ in range(self.n2)]
                        self.unSolved = set(itertools.product(range(self.n2), range(self.n2)))

                #check if each row has the correct number of values
                else:
                    if len(row) != self.n2:
                        raise Exception('Each row mus\t have the same number of values. (See row ' + str(reader.line_num - 1) + ')')

                #add each value to the correct place in the board; record that the row, col, and box contains value
                for index, item in enumerate(row):
                    if not item == '':
                        self.board[(reader.line_num-1, index)] = int(item)
                        self.valsInRows[reader.line_num-1].add(int(item))
                        self.valsInCols[index].add(int(item))
                        self.valsInBoxes[self.rcToBox(reader.line_num-1, index)].add(int(item))
                        self.unSolved.remove((reader.line_num-1, index))

    ##########################################
    ####   Move Functions
    ##########################################

    #gets the unsolved space with the most current constraints
    def getMostConstrainedUnsolvedSpace(self):

        unsolved_board = {}
        for row, column in self.unSolved:
            possible_vals = set()
            for val in range(1, 10):
                if val not in self.valsInRows[row] \
                        and val not in self.valsInCols[column] \
                        and val not in self.valsInBoxes[self.rcToBox(row, column)]:
                    possible_vals.add(val)
            unsolved_board[(row, column)] = possible_vals

        min_len = float('inf')
        most_constrained = ()
        for key, value in unsolved_board.items():
            if len(value) < min_len:
                min_len = len(value)
                most_constrained = key

        return most_constrained

    #returns True if the move is not blocked by any constraints
    def isValidMove(self,row, column, val):
        if val not in self.valsInRows[row] and val not in self.valsInCols[column] and val not in self.valsInBoxes[self.rcToBox(row, column)]:
            return True
        return False
    #makes a move, records that its in the row, col, and box, and removes the space from unSolved
    def makeMove(self, row, col, val):
        self.board[(row, col)] = val
        self.valsInRows[row].add(val)
        self.valsInBoxes[self.rcToBox(row, col)].add(val)
        self.valsInCols[col].add(val)
        self.unSolved.remove((row, col))

    #removes the move, its record in its row, col, and box, and adds the space back to unSolved
    def removeMove(self, row, col,  val):
        del self.board[(row, col)]
        self.valsInCols[col].remove(val)
        self.valsInBoxes[self.rcToBox(row, col)].remove(val)
        self.valsInRows[row].remove(val)
        self.unSolved.add((row, col))


    ##########################################
    ####   Utility Functions
    ##########################################

    #converts a given row and column to its inner box number
    def rcToBox(self, row, col):
        return self.n * (row // self.n) + col // self.n


    #prints out a command line representation of the board
    def print(self):
        for r in range(self.n2):
            #add row divider
            if r % self.n == 0 and not r == 0:
                print("  " + "---" * self.n2)

            row = ""

            for c in range(self.n2):

                if (r,c) in self.board:
                    val = self.board[(r,c)]
                else:
                    val = None

                #add column divider
                if c % self.n == 0 and not c == 0:
                    row += " | "
                else:
                    row += "  "

                #add value placeholder
                if val is None:
                    row += "_"
                else:
                    row += str(val)
            print(row)

