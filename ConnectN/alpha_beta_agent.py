import math
import agent

###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth

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

    # Calculates the heuristic of the brd
    #
    # Returns the heuristic value
    def heuristic(self, brd):
        """Calculate the heuristic of the board"""
