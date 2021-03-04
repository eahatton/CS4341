# This is necessary to find the main code
from colorama import Fore, Back
from entity import CharacterEntity
import sys

from entity import CharacterEntity
import numpy as np

sys.path.insert(0, '../bomberman')
# Import necessary stuff


class InteractiveCharacter(CharacterEntity):

    def do(self, wrld):
        # Commands
        dx, dy = 0, 0
        bomb = False
        # Handle input
        for c in input("How would you like to move (w=up,a=left,s=down,d=right,b=bomb)? "):
            if 'w' == c:
                dy -= 1
            if 'a' == c:
                dx -= 1
            if 's' == c:
                dy += 1
            if 'd' == c:
                dx += 1
            if 'b' == c:
                bomb = True
        # Execute commands
        self.move(dx, dy)
        if bomb:
            self.place_bomb()