import sys
sys.path.insert(0,'..bomberman')

from entity import CharacterEntity
from itertools import product, starmap
import math
class DNQAgent(CharacterEntity):

    def __init__(self,name,avatar,x,y,inter):
        CharacterEntity.__init__(self,name,avatar,x,y)
        self.wrld = None
        self.bombPlaced = False
        self.bombTimer = 11
        self.agentX, self.agentY = x,y
        self.exitX, self.exitY = -1,-1
        self.bombX, self.bombY = -1, -1
        self.inter = inter
        self.lastState = ''
        self.lastAction = ''


    def do(self, wrld):
        self.wrld = wrld
        if self.exitX == -1 and self.exitY == -1:
            self.exitX,self.exitY = self.getExitCordinates()
        if self.inter:
            self.interactiveMoves()
        # else:
        #     self.QAgent(self)


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

    def move(self,dx,dy):

        self.agentX = max(0, min((self.agentX + dx), self.wrld.width()-1))
        self.agentY = max(0, min((self.agentY + dy), self.wrld.height()-1))
        if self.bombPlaced:
            self.bombTimer -= 1
            if self.bombTimer == 0:
                self.bombTimer = 11
                self.bombX,self.bombY = -1,-1
                self.bombPlaced = False

        # Test Prints
        # print("Agent Coordinates: {} {}".format(self.agentX, self.agentY))
        # print("Bomb Timer: {}".format(self.bombTimer))
        # print("Neighboring Cells: {}".format(self.getNeighborcells()))
        # print("Wall Channel: {}".format(self.getWallChannel()))
        # print("Explosion Channel: {}".format(self.getExplosionChannel()))
        # print("Monster Channel: {}".format(self.getMonsterChannel()))
        # print("In Detonation Zone: {}".format(self.inDetonationZone()))
        # print("Exit Path: {}".format(self.getExitPath()))
        print(self.createState())
        super(DNQAgent, self).move(dx,dy)

    def place_bomb(self):
        super(DNQAgent, self).place_bomb()
        self.bombX, self.bombY = self.agentX,self.agentY
        self.bombPlaced = True
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
                wallChannel.append(0)
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
                if self.bombTimer < 6:
                    return (1,1)
                else: return (1,0)
            else:
                return (0,0)


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

    def createState(self):
        state = []
        for i in self.getWallChannel():
            state.append(i)

        for i in self.getExplosionChannel():
            state.append(i)

        for i in self.getMonsterChannel():
            state.append(i)

        inDet = self.inDetonationZone()
        state.append(inDet[0])
        state.append(inDet[1])

        eX,eY = self.getExitPath()
        state.append(eX)
        state.append(eY)

        return str(state)