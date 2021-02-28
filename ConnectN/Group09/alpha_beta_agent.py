import sys
<<<<<<< HEAD:ConnectN/alpha_beta_agent.py
import board
import random
import time

=======
import agent
from . import heuristic1
from . import heuristic2
>>>>>>> origin/master:ConnectN/Group09/alpha_beta_agent.py


###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""


    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    # PARAM [int]    player: 1 for player 1, 2 for player 2
    def __init__(self, name, max_depth, heuristic):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth
        # Which heuristic to run
        self.h = heuristic

        # Needed for second heuristic, not used in the first
        self.board = None
        self.n = None
        self.scoreBrd = {
            1:0,
            2:0
        }

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        # Return the column from a call to max_value
<<<<<<< HEAD:ConnectN/alpha_beta_agent.py
        tic = time.perf_counter()
        val = self.max_value(brd, -sys.maxsize+1, sys.maxsize, self.max_depth)[1]
        toc = time.perf_counter()
        print("{} Took".format(self.name), toc-tic, "to take turn")
        return val
=======
        if brd.w == 7:
            self.max_depth = 6
        elif brd.w == 10:
            self.max_depth = 4

        return self.max_value(brd, -sys.maxsize+1, sys.maxsize, self.max_depth)[1]

>>>>>>> origin/master:ConnectN/Group09/alpha_beta_agent.py
    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ

    # Takes in:
    #       A board
    #       The alpha value
    #       The Beta value
    #       The depth we are supposed to look for a move
    #
    # Returns a tuple (value, column) where value is the max possible value and column is the column that
    #           was used to create this play
    def max_value(self, brd, alpha, beta, depth):
        """Get the max value"""
        # if Terminal or depth is 0 return the heuristic and col -1
        # call min_value on all successor boards
        # start pruning
        successors = self.get_successors(brd)
        if depth == 0 or brd.get_outcome() != 0 or len(successors) == 0:
            return self.heuristic(brd), -1
        else:
            value = -sys.maxsize+1
            col = -1
            for b in successors:
                bValue = self.min_value(b[0], alpha, beta, depth-1)[0]
                if bValue > value:
                    value = bValue
                    col = b[1]
                if value >= beta:
                    return value, col
                alpha = max(alpha, value)
            return value, col

    # Takes in:
    #       A board
    #       The alpha value
    #       The Beta value
    #       The depth we are supposed to look for a move
    #
    # Returns a tuple (value, column) where value is the min possible value and column is the column that
    #           was used to create this play
    def min_value(self, brd, alpha, beta, depth):
        """Gets the min value"""
        # if Terminal or depth is 0 return the heuristic and col -1
        # call max_value on all successor boards
        # start pruning
        successors = self.get_successors(brd)
        if depth == 0 or brd.get_outcome() != 0 or len(successors) ==0:
            return self.heuristic(brd), -1
        else:
            value = sys.maxsize
            col = -1
            for b in successors:
                bValue = self.max_value(b[0], alpha, beta, depth-1)[0]
                if bValue < value:
                    value = bValue
                    col = b[1]
                if value <= alpha:
                    return value, col
                beta = min(beta, value)
            return value, col

<<<<<<< HEAD:ConnectN/alpha_beta_agent.py
    def checkState(self,x,y,dx,dy):
        state = self.board[y][x]
        if state == 0:
            for i in range(self.n):
                nY = y + (dy*i)
                nX = x + (dx*i)
                if self.board[nY][nX] != 0:
                    state = self.board[nY][nX]
                    break
        if state == 0:
            return
        cnt = 0
        for i in range(self.n):
            nY = y + (dy*i)
            nX = x + (dx*i)
            if(nY >= 0 and nX >= 0):
                if self.board[nY][nX] == state:
                    cnt+=1
                elif self.board[nY][nX] == 0:
                    continue
                else:
                    return
            else:
                return
        # if cnt == self.n:
        #     self.scoreBrd[state] = self.scoreBrd[state] + math.floor(math.pow(self.n,(cnt-1)))
        # else:
        #     self.scoreBrd[state] = self.scoreBrd[state] + math.floor(math.pow(self.n, (cnt-1)))
        self.scoreBrd[state] = self.scoreBrd[state] + math.floor(math.pow(self.n, (cnt-1)))
        
=======
>>>>>>> origin/master:ConnectN/Group09/alpha_beta_agent.py

    
    # Calculates the heuristic of the brd
    #
    # Returns the heuristic value
    def heuristic(self, brd):
        """Calculate the heuristic of the board"""
        if self.h == 1:
            return heuristic1.heuristic1(self, brd)
        elif self.h == 2:
            return heuristic2.heuristic2(self, brd)


# DO NOT REMOVE THIS. MAKE SURE IT IS THE LAST THING IN THE SCRIPT
# We can optimize the depth value
THE_AGENT = AlphaBetaAgent("Group09", 4, 1)
