import math
import agent
import sys
import board
import random
import time



###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""


    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth, heuristic):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth
        # Heuristic algorithm to use
        self.h = heuristic
        self.numChecks = 0

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
        tic = time.perf_counter()
        val = self.max_value(brd, -sys.maxsize+1, sys.maxsize, self.max_depth)[1]
        toc = time.perf_counter()
        print("Took", toc-tic, "to take turn")

        return val

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
        # Sort the successors to prune more
        return self.order_successors(succ)

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
            # Boards are sorted by heuristic high to low but we want to feed min the least appealing board for ourselves
            # first because it is most likely going to be the one we take
            successors.reverse()
            for b in successors:
                self.numChecks += 1
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
        if depth == 0 or brd.get_outcome() != 0 or len(successors) == 0:
            return self.heuristic(brd), -1
        else:
            value = sys.maxsize
            col = -1
            for b in successors:
                self.numChecks += 1
                bValue = self.max_value(b[0], alpha, beta, depth-1)[0]
                if bValue < value:
                    value = bValue
                    col = b[1]
                if value <= alpha:
                    return value, col
                beta = min(beta, value)
            return value, col

    # Calculates the heuristic of the brd
    #
    # Returns the heuristic value
    def heuristic(self, brd):
        """Calculate the heuristic of the board"""
        if self.h == 1:
            return self.heuristic1(brd)
        else:
            return 0

    def heuristic1(self, brd):
        value = 0
        for i in range(brd.h):
            for j in range(brd.w):
                value += self.check_line(brd, i, j, 1, 0)
                value += self.check_line(brd, i, j, 1, 1)
                value += self.check_line(brd, i, j, 0, 1)
                value += self.check_line(brd, i, j, 1, -1)
        return value

    def check_line(self, brd, i, j, dx, dy):
        count = 0
        player = brd.board[i][j]
        other = False
        for c in range(0, brd.n):
            if not other:
                cx = j + c*dx
                cy = i + c*dy
                # dump out of this line check we went out of bounds
                if cx < 0 or cx >= brd.w or cy < 0 or cy >= brd.h:
                    other = True
                    count = 0
                # Same piece or we haven't seen any pieces
                elif brd.board[cy][cx] == player or player == 0:
                    if player == 0:
                        player = brd.board[cy][cx]
                    if player != 0 and brd.board[cy][cx] == player:
                        count += 1
                # Dump out of this line check we found a different piece
                elif brd.board[cy][cx] != player and brd.board[cy][cx] != 0:
                    other = True
                    count = 0
        if player != 0:
            # count will be 0,1,3,9,27,81... for count = 0,1,2,3,4,5...
            count = math.floor(3 ** (count-1))
            # if the count was done on the opponent negate it
            if player != self.player:
                count *= -1
        else:
            count = 0
        return count


    def sort_tables(self, val):
        return self.heuristic(val[0])

    # Sort successors by how good the board already is (heuristic)
    def order_successors(self, succ):
        ordered = succ
        ordered.sort(key=self.sort_tables)
        return ordered



# DO NOT REMOVE THIS. MAKE SURE IT IS THE LAST THING IN THE SCRIPT
# We can optimize the depth value
THE_AGENT = AlphaBetaAgent("Group09", 4, 1)
