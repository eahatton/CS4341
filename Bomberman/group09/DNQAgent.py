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
class DNQAgent(CharacterEntity):

    def __init__(self,name,avatar,x,y,inter):
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
        self.inter = inter
        self.lastState = ''
        self.lastAction = ''
        self.QTable = ""
        self.readQTable()
        self.nextAction = 0

    def restart(self,wrld):
        CharacterEntity.__init__(self,self.name,self.avatar,self.startX,self.startY)
        self.agentX,self.angentY = self.startX,self.startY
        self.agentLX,self.agentLY = self.startX,self.startY
        self.bombTimer = 11
        self.bombX, self.bombY = -1, -1


    def do(self, wrld):
        self.wrld = wrld
        if self.exitX == -1 and self.exitY == -1:
            self.exitX,self.exitY = self.getExitCordinates()
        if self.inter:
            self.interactiveMoves()
        else:
            # self.qLearning()
            pass

    def interactiveMoves(self):
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

        # Test Prints
        # print("Agent Coordinates: {} {}".format(self.agentX, self.agentY))
        # print("Neighboring Cells: {}".format(self.getNeighborcells()))
        # print("Wall Channel: {}".format(self.getWallChannel()))
        # print("Explosion Channel: {}".format(self.getExplosionChannel()))
        # print("Monster Channel: {}".format(self.getMonsterChannel()))
        # print("In Detonation Zone: {}".format(self.inDetonationZone()))
        # print("Exit Path: {}".format(self.getExitPath()))
        # print(self.getState())
        super(DNQAgent, self).move(dx,dy)
        # print("Agent Old Coordinates: {} {}".format(self.agentLX, self.agentLY))
        # print("Agent Coordinates: {} {}".format(self.agentX, self.agentY))
        # print("Wall Channel: {}".format(self.getWallChannel()))
        # print("Det Channel: {}".format(self.getDetonationChannel()))
        # print("Explosion Channel: {}".format(self.getExplosionChannel()))
        # print("Exit Path: {}".format(self.getExitPath()))
        # print("Bomb Timer: {}".format(self.bombTimer))
        # print("Bomb Location: {}, {}".format(self.bombX,self.bombY))
        # print("State: {}".format(self.getState()))
        self.lastState = self.getState()
        return self.getState(), self.getReward()
        #
        #     print("We Died :(")

    def place_bomb(self):
        reward = 0
        super(DNQAgent, self).place_bomb()
        if not self.bombPlaced:
            reward = 1
            self.bombPlaced =  True
        else:
            reward = -1
        return self.getState(), reward
    # Return a list of all neighbors with their cordinates, if out of bounds, the cell is (-1,-1)

    """
    [1] Character Position
    [2] Cell Above
    [3] Cell Bellow
    [4] Cell Left
    [5] Cell Left-Above
    [6] Cell Left-Down
    [7] Cell Right
    [8] Cell Right-Above
    [9] Cell Right-Down
    """
    def getNeighborcells(self):
        cells = starmap(lambda a,b: (self.agentX+a, self.agentY+b), product((0,-1,+1), (0,-1,+1)))
        # Lambda function to only keep neighboring cells in bounds, any [-1,-1] cells are through aways
        return list(map(lambda cell : [-1,-1] if (cell[0]==-1 or cell[1]==-1 or cell[0] > self.wrld.width()-1 or cell[1] > self.wrld.height()-1) else cell ,cells))
    # def QAgent(self):
    #     return

    def getWallChannel(self):
        neighborCells = self.getNeighborcells()
        wallChannel = []
        for cell in neighborCells:
            if cell == [-1,-1]:
                wallChannel.append(1)
            else:
                if self.wrld.wall_at(cell[0],cell[1]):
                    wallChannel.append(1)
                else:
                    wallChannel.append(0)
        return wallChannel

    def getExplosionChannel(self):
        neighborCells = self.getNeighborcells()
        explosionChannel = []
        for cell in neighborCells:
            if cell == [-1,-1]:
                explosionChannel.append(0)
            else:
                if self.wrld.explosion_at(cell[0],cell[1]) is not None:
                    explosionChannel.append(1)
                else:
                    explosionChannel.append(0)
        return explosionChannel

    def inDetonationZone(self):
        inRangeFlag = False
        if self.bombTimer == 11:
            return (0,0)
        else:
            if self.agentX == self.bombX and self.agentY == self.bombY:
                inRangeFlag= True
            elif self.agentX == self.bombX and self.agentY != self.bombY and not inRangeFlag:
                for i in range(-5,5,1):
                    if self.agentY == self.bombY + i:
                        inRangeFlag = True
            elif self.agentX != self.bombX and self.agentY == self.bombY and not inRangeFlag:
                for i in range(-5,5,1):
                    if self.agentX == self.bombX + i:
                        inRangeFlag = True
            if inRangeFlag:
                return (1,1)
                # if self.bombTimer < 6:
                #     return (1,1)
                # else: return (1,0)
            else:
                return (0,0)

    def getDetonationChannel(self):
        neighboringCells = self.getNeighborcells()
        detChannel = []
        aPFlag = True
        for cell in neighboringCells:
            aPFlag = True
            if self.bombTimer >= 3:
                detChannel.append(0)
            else:
                if cell[0] == self.bombX and cell[1] == self.bombY:
                    detChannel.append(1)
                elif cell[0] == self.bombX and cell[1] != self.bombY:
                    for i in range(-5, 5, 1):
                        if cell[1] == self.bombY + i:
                            detChannel.append(1)
                            aPFlag = False
                    if aPFlag:
                        detChannel.append(0)
                elif cell[0] != self.bombX and cell[1] == self.bombY:
                    for i in range(-5, 5, 1):
                        if cell[0] == self.bombX + i:
                            detChannel.append(1)
                            aPFlag = False
                    if aPFlag:
                        detChannel.append(0)
                else: detChannel.append(0)

        return detChannel


    def getMonsterChannel(self):
        monsterChannel = []
        mX,mY = self.getMonsterLocation()
        if mX != -1 and mY != -1:
            pX, pY = self.getMonsterPath()
            # monsterChannel.append(1/self.getDistance(self.agentX,mX,self.agentY,mY))
            monsterChannel.append(1)
            monsterChannel.append(pX)
            monsterChannel.append(pY)
        else:
            monsterChannel.append(0)
            monsterChannel.append(0)
            monsterChannel.append(0)
        return monsterChannel

    def getMonsterLocation(self):
        for x in range(self.agentX-4, self.agentX+4, 1):
            for y in range(self.agentY-4, self.agentY+4,1):
                try:
                    if self.wrld.monsters_at(x,y):
                        return (x,y)
                except:
                    continue
        return (-1,-1)

    def getExitCordinates(self):
        for x in range(self.wrld.width()):
            for y in range(self.wrld.height()):
                if self.wrld.exit_at(x,y):
                    return (x,y)

    def getExitPath(self):
        x,y = 0,0
        if self.agentX > self.exitX:
            x = -1
        if self.agentX < self.exitX:
            x = 1
        if self.agentY > self.exitY:
            y = -1
        if self.agentY < self.exitY:
            y = 1
        return x,y

    def getMonsterPath(self):
        x,y = 0,0
        mX, mY = self.getMonsterLocation()
        if self.agentX >mX:
            x = -1
        if self.agentX < mX:
            x = 1
        if self.agentY > mY:
            y = -1
        if self.agentY < mY:
            y = 1
        return x,y

    def getDistance(self, x1,y1,x2,y2):
        return math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))

    def getState(self):
        state = []
        for i in self.getWallChannel():
            state.append(i)

        for i in np.logical_or(self.getExplosionChannel(),self.getDetonationChannel()):
            if i:
                state.append(1)
            else:
                state.append(0)

        for i in self.getMonsterChannel():
            state.append(i)
        #
        # inDet = self.inDetonationZone()
        # state.append(inDet[0])
        # state.append(inDet[1])

        if self.bombPlaced:
            state.append(0)
        else:
            state.append(1)

        eX,eY = self.getExitPath()
        state.append(eX)
        state.append(eY)

        return str(state)

    def getReward(self):
        # self.locations.add("{},{}".format(self.agentX,self.agentY))
        # if "{},{}".format(self.agentX,self.agentY) in self.locations:
        #     return -1
        cur_Distance = self.getDistance(self.agentX,self.agentY,self.exitX,self.exitY)
        last_Distance = self.getDistance(self.agentLX,self.agentLY,self.exitX,self.exitY)
        if self.agentLX == self.agentX and self.agentLY == self.agentY:
            return -1
        elif cur_Distance > last_Distance:
            # if "{},{}".format(self.agentX,self.agentY) in self.locations:
            #     return -2
            # else:
                return -1
        elif cur_Distance < last_Distance:
            return 1
        else:
            return -1
    
    def rewardAtWall(self):
        dx,dy = self.getExitPath()
        print("dx: {} dy: {}".format(dx,dy))
        try:
            return self.wrld.wall_at(self.agentX+dx,self.agentY+dy)
        except:
            return False

    def createEpsilonGreedyPolicy(self, epsilon):
        """
        Creates an epsilon-greedy policy based
        on a given Q-function and epsilon.

        Returns a function that takes the state
        as an input and returns the probabilities
        for each action in the form of a numpy array
        of length of the action space(set of possible actions).
        """

        def policyFunction(state):
            Action_probabilities = np.ones(10,
                                           dtype=float) * epsilon / 10

            best_action = np.argmax(self.QTable[state])
            Action_probabilities[best_action] += (1.0 - epsilon)
            return Action_probabilities

        return policyFunction


    def qLearning(self, discount_factor=0.8 ,
                  alpha=0.8, epsilon=0.0):
        policy = self.createEpsilonGreedyPolicy(epsilon)
        state = self.getState()
        action_probabilities = policy(state)

        action = np.random.choice(np.arange(
            len(action_probabilities)),
            p=action_probabilities
        )

        self.step(action)
        next_state = self.getState()
        reward = self.getReward()

        #TD Update
        best_next_action = np.argmax(self.QTable[next_state])
        td_target = reward + discount_factor * self.QTable[next_state][best_next_action]
        td_delta = td_target - self.QTable[state][action]
        self.QTable[state][action] += alpha * td_delta
    
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

    def saveQTable(self):
        with open("QTable.csv", "w", newline='') as f:
            w = csv.writer(f)
            for key, val in self.QTable.items():
                w.writerow([key, *val])
        f.close()

    def readQTable(self,file="QTable.csv"):
        self.QTable = defaultdict(lambda: np.zeros(10))
        with open(file,'r') as f:
            r = csv.reader(f)
            for k, *v in r:
                self.QTable[k] = np.array(list(map(float,v)))

    def setNextAction(self,action):
        self.nextAction = action