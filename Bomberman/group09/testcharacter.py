# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from itertools import product, starmap
from events import Event

class TestCharacter(CharacterEntity):
    def __init__(self, name, avatar, x, y):
        CharacterEntity.__init__(self,name,avatar,x,y)
        self.eX,self.eY = -1,-1
        self.meX, self.meY = 0,0
        self.bX, self.bY = -1,-1
        self.bombT = 10

    def findExitCord(self,wrld):
        for y in range(wrld.height()):
            for x in range(wrld.width()):
                if wrld.exit_at(x,y):
                    return x,y      
    
    def do(self, wrld):
        self.testFunction(wrld)

    def startFunction(self,wrld):
        if self.eX == -1 and self.eY == -1:
            self.eX, self.eY = self.findExitCord(wrld)
        print("meX: {0}, meY: {1}".format(self.meX,self.meY))
        print(self.eX,self.eY)
        self.interactiveMove(wrld)


    # returns 4 values, 
    '''
    [Left,Up,Right,Down] = [0,0,1,1] <- Exit is right and down
    return 0,0,1,1
    '''
    def exitDistance(self,wrld):
        x,y = 0,0
        if self.meX > self.eX:
            x = -1
        if self.meX < self.eX:
            x = 1
        if self.meY > self.eY:
            y = -1
        if self.meY < self.eY:
            y = 1
        return x,y

    # function that loops through all 9 positons around me, I am only checking 1 cell near me
    def neighbors(self):
        cells = starmap(lambda a,b: (self.meX+a,self.meY+b), product((0,-1,+1),(0,-1,+1)))
        ls = []
        for item in cells:
            if item[0] >= 0 and item[1] >= 0:
                ls.append(item)
            else: 
                ls.append((-1,-1))
        return iter(ls)
        
    ## Function that creates my wall channels, 1 if there is a wall 0 other wise
    def createWallChannel(self,wrld):
        neighorCells = self.neighbors()
        wallChannel = []
        for cell in neighorCells:
            if cell == (-1,-1):
                wallChannel.append(0)
            else:
                if wrld.wall_at(cell[0],cell[1]):
                    wallChannel.append(1)
                else:
                    wallChannel.append(0)
        return wallChannel

    ## Function that checks if anything near me is about to kill me
    def createMonsterChannel(self,wrld):
        neighorCells = list(self.neighbors())
        monsterChannel = []
        for cell in neighorCells:
            if cell == (-1,-1):
                monsterChannel.append(0)
            else:
                if wrld.monsters_at(cell[0],cell[1]) is not None:
                    monsterChannel.append(1)
                else:
                    monsterChannel.append(0)
        return monsterChannel
    
    ## Function that checks if anything near me is fire
    def createFireChannel(self,wrld):
        neighorCells = list(self.neighbors())
        fireChannel = []
        for cell in neighorCells:
            if cell == (-1,-1):
                fireChannel.append(0)
            else:
                if wrld.explosion_at(cell[0],cell[1]) is not None:
                    fireChannel.append(1)
                else:
                    fireChannel.append(0)
        return fireChannel

    def inDetonationZone(self):
        if self.bombT == 10:
            return 0
        else:
            if self.meX == self.bX and self.bY == self.meY:
                return 1/self.bombT
            elif self.meX == self.bX and self.meY != self.bY:
                if self.meY == self.bY-1 or self.meY == self.bY-2 or self.meY == self.bY-3 or self.meY == self.bY-4 or self.meY == self.bY+1 or self.meY == self.bY+2 or self.meY == self.bY+3 or self.meY == self.bY+4:
                    return 1/self.bombT
                else:
                    return 0
            elif self.meY == self.bY and self.meX != self.bX:
                if self.meX == self.bX-1 or self.meX == self.bX-2 or self.meX == self.bX-3 or self.meX == self.bX-4 or self.meX == self.bX+1 or self.meX == self.bX+2 or self.meX == self.bX+3 or self.meX == self.bX+4:
                    return 1/self.bombT
                else:
                    return 0
        return 0

    def interactiveMove(self,wrld):
    # Commands
        dx, dy = 0, 0
        bomb = False
        if self.bX != -1 and self.bY != -1:
            self.bombT -= 1
        if self.bombT <= 0:
            self.bX = -1
            self.bY = -1
            self.bombT = 10
        # Handle input
        for c in input("How would you like to move (w=up,a=left,s=down,d=right,b=bomb)? "):
            print(len(c))
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
        self.makeMovement(wrld,dx,dy)
        if bomb:
            if self.bombT == 10:
                self.bX = self.meX
                self.bY = self.meY
            self.place_bomb()

    # Used to keep track of movement
    def makeMovement(self,wrld, dx,dy):
        rdx = dx
        rdy = dy

        if self.meX == 0 and dx == -1 or self.meX >= wrld.width()-1 and dx == 1:
            dx = 0
        elif self.meY==0 and dy == -1 or self.meY >= wrld.height()-1 and dy == 1:
            dy = 0
        elif not wrld.empty_at(self.meX+dx,self.meY+dy):
            dx=0 
            dy=0
        self.meX += dx
        self.meY += dy

        self.reward()

        self.move(rdx,rdy)

    def reward(self):
        print("Got to reward")
        if self.meX == self.eX and self.meY == self.eY:
            print("Got to exit")
            return 10000 
    
    def testFunction(self,wrld):
        
