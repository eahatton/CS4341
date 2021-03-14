import sys
sys.path.insert(0,'..bomberman')
import random

from entity import CharacterEntity
from itertools import product, starmap
import math
from collections import defaultdict
import numpy as np
import pandas as pd
import csv

random.seed(1)

class DeepAgent(CharacterEntity):
    def __init__(self,name,avatar,x,y):
        CharacterEntity.__init__(self,name,avatar,x,y)
        self.name = name
        self.avatar = avatar
        self.startX, self.startY = x,y
        self.wrld = None
        self.bombPlaced = False
        self.bombTimer = 11
        self.agentX, self.agentY = self.startX,self.startY
        self.agentLX,self.agentLY = self.startX,self.startY
        self.exitX, self.exitY = -1,-1
        self.bombX, self.bombY = -1, -1
        self.locations = set('0,0')

    def do(self, wrld):
        self.wrld = wrld
        if self.exitX == -1 and self.exitY == -1:
            self.exitX,self.exitY = self.getExitCordinates()
        pass

    def wallAhead(self,dx,dy):
        try:
            return self.wrld.wall_at(self.agentX+dx,self.agentY+dy)
        except:
            return True

    def move(self,dx,dy):
        self.agentLX, self.agentLY = self.agentX,self.agentY
        if not self.wallAhead(dx,dy):
            self.agentX = max(0, min((self.agentX + dx), self.wrld.width()-1))
            self.agentY = max(0, min((self.agentY + dy), self.wrld.height()-1))
        if self.bombPlaced:
            self.bombTimer -= 1
            if self.bombTimer == -1:
                self.bombTimer = 11
                self.bombX,self.bombY = -1,-1
                self.bombPlaced = False
        super(DeepAgent, self).move(dx,dy)
        return self.getReward()

    def place_bomb(self):
        reward = 0
        super(DeepAgent, self).place_bomb()
        if not self.bombPlaced:
            reward = 1
            self.bombPlaced =  True
        else:
            reward = -1
        return reward

    def getExitCordinates(self):
        for x in range(self.wrld.width()):
            for y in range(self.wrld.height()):
                if self.wrld.exit_at(x,y):
                    return (x,y)

    def getDistance(self, x1,y1,x2,y2):
        return math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))
    
    def getReward(self):
        # print(self.agentX,self.agentY)
        # self.locations.add("{},{}".format(self.agentX,self.agentY))
        # if "{},{}".format(self.agentX,self.agentY) in self.locations:
        #     return -1
        cur_Distance = self.getDistance(self.agentX,self.agentY,self.exitX,self.exitY)
        last_Distance = self.getDistance(self.agentLX,self.agentLY,self.exitX,self.exitY)
        if self.agentLX == self.agentX and self.agentLY == self.agentY:
            return 0
        elif cur_Distance > last_Distance:
            return 0
        elif cur_Distance < last_Distance:
            return 0
        else:
            return 0
    
    """
    0 = no move
    1 = down
    2 = right
    3 = down right
    4 = Up
    5 = Left
    6 = Up left
    7 = Down right
    8 = Down Left
    9 = Place bomb
    """
    def step(self,action):
        self.lastAction = action
        dx,dy = 0,0
        if action == 0:
            return self.move(0,0)
        elif action == 1:
            return self.move(0,1)
        elif action == 2:
            return self.move(1,0)
        elif action == 3:
            return self.move(1,1)
        elif action == 4:
            return self.move(0,-1)
        elif action ==5:
            return self.move(-1,0)
        elif action == 6:
            return self.move(-1,-1)
        elif action == 7:
            return self.move(-1,1)
        elif action == 8:
            return self.move(1,-1)
        elif action == 9:
            self.move(0,0)
            return self.place_bomb()