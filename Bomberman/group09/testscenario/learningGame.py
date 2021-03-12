import sys
import numpy as np 
import itertools 
import csv
from collections import defaultdict

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
        self.QTable = ""
        self.readQTable()

    def add_character(self, c):
        super(QTraining, self).add_character(c)
        self.agent = c
    
    def go(self,wait=0, view=False,discount_factor = 0.9, 
                            alpha = 0.8, epsilon = 0.1):
        lostFlag = False
        if wait ==0:
            def step():
                input("Press Enter to continue or CTRL-C to stop...")
        else:
            def step():
                pass
        policy = self.createEpsilonGreedyPolicy(epsilon) 
        state = ""
        for t in itertools.count():
            (self.world, self.events) = self.world.next()
            if view:
                self.draw()
            step()
            self.world.next_decisions()
            action_probabilities = policy(state)
            action = np.random.choice(np.arange( 
                      len(action_probabilities)), 
                       p = action_probabilities) 
            next_state, reward = self.agent.step(action)
            for event in self.events:
                if event.tpe == Event.BOMB_HIT_CHARACTER:
                    lostFlag = True
                    reward = -100
                    if view:
                        print("Our Last State: {}".format(state))
                        print("Our Last Action: {}".format(action))
                elif event.tpe == Event.CHARACTER_FOUND_EXIT:
                    reward = 100
            best_next_action = np.argmax(self.QTable[next_state])
            td_target = reward + discount_factor * self.QTable[next_state][best_next_action]
            td_delta = td_target - self.QTable[state][action]
            self.QTable[state][action] += alpha * td_delta
            if self.done():
                break
            state = next_state
        self.saveQTable()
        return lostFlag

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