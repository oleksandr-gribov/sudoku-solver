from board import Board

class Solver:

    ##########################################
    ####   Constructor
    ##########################################
    def __init__(self,filename):
        self.board = Board(filename)
        self.solve()

    ##########################################
    ####   Solver
    ##########################################

    #recursively selects the most constrained unsolved space and attempts
    #to assign a value to it
    #
    #upon completion, it will leave the board in the solved state (or original
    #state if a solution does not exist)
    def solve(self):
        pass





if __name__ == "__main__":

    #change this to the input file that you'd like to test
    s = Solver('testBoard_dastardly.csv')
    s.solve()

