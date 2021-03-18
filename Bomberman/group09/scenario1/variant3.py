# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster
from events import Event

from datetime import datetime

# TODO This is your code!
sys.path.insert(1, '../group09')
from testcharacter import TestCharacter


exited = 0
bombed = 0
killed = 0

for i in range(10):
    # Create the game
    random.seed(datetime.now()) # TODO Change this if you want different random choices
    g = Game.fromfile('map.txt')
    g.add_monster(SelfPreservingMonster("selfpreserving", # name
                                         "S",              # avatar
                                        3, 9,             # position
                                        1                 # detection range
    ))

    # TODO Add your character
    g.add_character(TestCharacter("me", # name
                                  "C",  # avatar
                                  0, 0,  # position
                                  1
    ))
    
    # Run!
    g.go(1)

    events = g.world.events
    for e in events:
        if e.tpe == Event.CHARACTER_FOUND_EXIT:
            exited += 1
        elif e.tpe == Event.BOMB_HIT_CHARACTER:
            bombed += 1
        elif e.tpe == Event.CHARACTER_KILLED_BY_MONSTER:
            killed += 1


print("Exited:", exited)
print("Bombed:", bombed)
print("Killed:", killed)
