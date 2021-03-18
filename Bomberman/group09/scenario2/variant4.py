# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster
from events import Event

# TODO This is your code!
sys.path.insert(1, '../group09')
from testcharacter import TestCharacter
from datetime import datetime

exited = 0
killed = 0
bombed = 0

for i in range(1000):
    # Create the game
    random.seed(datetime.now()) # TODO Change this if you want different random choices
    g = Game.fromfile('map.txt')
    g.add_monster(SelfPreservingMonster("aggressive", # name
                                        "A",          # avatar
                                        3, 13,        # position
                                        2             # detection range
    ))

    # TODO Add your character
    g.add_character(TestCharacter("me", # name
                                  "C",  # avatar
                                  0, 0  # position
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
print("Killed:", killed)
print("Bombed:", bombed)
