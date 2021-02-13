import random
import game
import agent
import alpha_beta_agent as aba
from datetime import datetime

# Set random seed for reproducibility
random.seed(datetime.now())

def runTourney(w,h,t,p1,p2,games):
    g = game.Game(w,h,t,p1,p2)
    player1 = 0
    for a in range(games):
        winner = g.go()
        if winner == 1:
            player1 += 1
    print("Player 1 was first, and won ", player1, "of ", games)
    print("Player 2 was second, and won ", games-player1, "of ", games)
    g = game.Game(w,h,t,p2,p1)
    player1 = 0
    for a in range(games):
        winner = g.go()
        if winner == 1:
            player1 += 1
    print("Player 1 was second, and won ", player1, "of ", games)
    print("Player 2 was first, and won ", games - player1, "of ", games)


#
# Random vs. Random
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.RandomAgent("random1"),       # player 1
#               agent.RandomAgent("random2"))       # player 2

#
# Human vs. Random
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human"),    # player 1
#               agent.RandomAgent("random"))        # player 2

#
# Random vs. AlphaBeta
#
g = game.Game(7, # width
              6, # height
              4, # tokens in a row to win
              agent.RandomAgent("random"),        # player 1
              aba.AlphaBetaAgent("alphabeta", 6,1)) # player 2

#
# Human vs. AlphaBeta
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human"),    # player 1
#               aba.AlphaBetaAgent("alphabeta", 7,1)) # player 2

#
# Human vs. Human
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human1"),   # player 1
#               agent.InteractiveAgent("human2"))   # player 2

#
# AlphaBeta vs AlphaBeta
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               aba.AlphaBetaAgent("alphabeta1", 4, 1),        # player 1
#               aba.AlphaBetaAgent("alphabeta2", 6, 1))        # player 2

# Execute the game
outcome = g.go()

# runTourney(7,6,4,
#            aba.AlphaBetaAgent("alphabeta1", 6, 1),  # player 1
#            aba.AlphaBetaAgent("alphabeta2", 4, 1),  # player 2
#            10)

