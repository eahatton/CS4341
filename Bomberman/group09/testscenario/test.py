# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../groupNN')

# Uncomment this if you want the empty test character
from testcharacter import TestCharacter

# Uncomment this if you want the interactive character
from interactivecharacter import InteractiveCharacter
from DNQAgent import DNQAgent
from monsters.stupid_monster import StupidMonster
from monsters.selfpreserving_monster import SelfPreservingMonster

# Create the game
g = Game.fromfile('map.txt')
# TODO Add your character

# Uncomment this if you want the test character
# g.add_character(TestCharacter("me",  # name
#                               "C",   # avatar
#                                0, 0, # position
#                                1     # variant
# ))

# Uncomment this if you want the interactive character
g.add_character(DNQAgent("me", # name
                                    "C",  # avatar
                                    0, 0,  # position
                                    True # interactive
))
# g.add_monster(SelfPreservingMonster("aggressive", # name
#                             "A",      # avatar
#                             3, 9,      # position
#                             2
# ))
# Run!

# Use this if you want to press ENTER to continue at each step
# g.go(0)

# Use this if you want to proceed automatically
g.go(1)
