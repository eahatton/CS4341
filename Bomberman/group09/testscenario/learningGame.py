import sys

sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')
sys.path.insert(2, '../groupNN')
import random
from game import Game
from events import Event
from DNQAgent import DNQAgent

random.seed(1)
class QTraining(Game):
    def __init__(self, width, height, max_time, bomb_time, expl_duration, expl_range, sprite_dir="../../bomberman/sprites/"):
        super(QTraining, self).__init__(width,height,max_time,bomb_time,expl_duration,expl_range,sprite_dir)
        self.agent = None

    def add_character(self, c):
        super(QTraining, self).add_character(c)
        self.agent = c
    
    def go(self,wait=0, view=False):
        lostFlag = False
        if wait ==0:
            def step():
                input("Press Enter to continue or CTRL-C to stop...")
        else:
            def step():
                pass
        while not self.done():
            (self.world, self.events) = self.world.next()
            if view:
                self.draw()
            step()
            self.world.next_decisions()
        for event in self.events:
            if event.tpe == Event.BOMB_HIT_CHARACTER:
                lostFlag = True
                if view:
                    print("Our Last State: {}".format(self.agent.lastState))
                    print("Our Last Action: {}".format(self.agent.lastAction))
                self.agent.QTable[self.agent.lastState][self.agent.lastAction] += -1000

        self.agent.saveQTable()
        return lostFlag


loseCount = 0
winCount = 0
for episode in range(1000):
    if episode % 100 == 0:
        print("Game: {}".format(episode))
    g = QTraining.fromfile('map.txt')

    agent = DNQAgent("me",
                        "C",
                        0,0,
                        False)
    g.add_character(agent)
    if g.go(1,False):
        loseCount += 1
    else:
        winCount +=1

print("Lost: {}".format(loseCount))
print("Won: {}".format(winCount))