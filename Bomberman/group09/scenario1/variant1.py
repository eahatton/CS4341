# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../groupNN')

# Uncomment this if you want the empty test character
#from testcharacter import TestCharacter

# Uncomment this if you want the interactive character
from interactivecharacter import InteractiveCharacter
from testcharacter import TestCharacter

# Create the game
g = Game.fromfile('map.txt')

# TODO Add your character
t = TestCharacter("me", "C", 0,0)
# Uncomment this if you want the test character
g.add_character(t)

# # Uncomment this if you want the interactive character
# g.add_character(InteractiveCharacter("me", # name
#                                      "C",  # avatar
#                                      0, 0  # position
# ))

# Run!

# Use this if you want to press ENTER to continue at each step
# g.go(0)

# Use this if you want to proceed automatically
g.go(1)
for i in g.world.events:
    if 'killed itself' in i.__str__() or 'was killed by' in i.__str__():
        t.reward += -1000
    elif 'found the exit' in i.__str__():
        t.reward += 1000

print(t.reward)