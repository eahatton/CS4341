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
from monsters.stupid_monster import StupidMonster
from monsters.selfpreserving_monster import SelfPreservingMonster
# Uncomment this if you want the interactive character
from interactivecharacter import InteractiveCharacter
from DNQAgent import DNQAgent
from events import Event
# Create the game
g = Game.fromfile('map.txt')

# TODO Add your character
agent = DNQAgent("me",  # name
                         "C",  # avatar
                         0, 0,  # position
                         True  # interactive
                         )
# Uncomment this if you want the test character
g.add_monster(StupidMonster("stupid", # name
                            "S",      # avatar
                            3, 5,     # position
))
g.add_monster(SelfPreservingMonster("aggressive", # name
                                    "A",          # avatar
                                    3, 13,        # position
                                    2             # detection range
))
g.add_character(agent)

g.go(1)

