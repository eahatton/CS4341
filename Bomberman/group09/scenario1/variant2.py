# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.stupid_monster import StupidMonster
from events import Event

from datetime import datetime

# TODO This is your code!
sys.path.insert(1, '../group09')
from testcharacter import TestCharacter
from interactivecharacter import InteractiveCharacter

exit = 0
killed_self = 0
killed_by_monster = 0

for i in range(1000):
    # Create the game
    random.seed(datetime.now()) # TODO Change this if you want different random choices
    g = Game.fromfile('map.txt')
    g.add_monster(StupidMonster("stupid", # name
                                "S",      # avatar
                                 3, 9      # position
    ))

    # TODO Add your character
    g.add_character(TestCharacter("me", # name
                                  "C",  # avatar
                                  0, 0, # position
                                  1     # Variant
    ))

    # g.add_character(InteractiveCharacter("me", "c", 0,0))


    # Run!
    g.go(1)

    events = g.world.events
    print(len(events))
    for e in events:
        event = e.tpe
        if event == Event.BOMB_HIT_CHARACTER:
            killed_self += 1
        elif event == Event.CHARACTER_KILLED_BY_MONSTER:
            killed_by_monster += 1
        elif event == Event.CHARACTER_FOUND_EXIT:
            exit += 1

print("Found Exit:", exit)
print("Killed by bomb:", killed_self)
print("Killed by monster:", killed_by_monster)

