# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game
from events import Event

# TODO This is your code!
sys.path.insert(1, '../group09')
from testcharacter import TestCharacter
from interactivecharacter import InteractiveCharacter


# Create the game
g = Game.fromfile('map.txt')

# TODO Add your character
g.add_character(TestCharacter("me", # name
                               "C",  # avatar
                               0, 0,  # position
                                 1
))



#g.add_character(InteractiveCharacter("me", "c", 0,0))


# Run!
g.go(1)

