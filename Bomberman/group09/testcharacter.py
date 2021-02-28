# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class TestCharacter(CharacterEntity):

    
    def __init__(self, name, avatar, x, y, varient):
        CharacterEntity.__init__(self, name, avatar, x, y)
        self.varient = varient


    def do(self, wrld):
        # Your code here
        if self.varient == 1:
            self.astar()
        elif self.varient == 2:
            self.minimax()
        elif self.varient >= 3:
            self.expectimax()
        pass


    def astar(self):
        pass


    def minimax(self):
        pass

    def expectimax(self):
        pass


