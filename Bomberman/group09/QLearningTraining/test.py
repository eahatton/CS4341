# This is necessary to find the main code
import sys

sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')
sys.path.insert(2, '.')
import numpy as np
import pandas as pd
import copy

# Import necessary stuff
from game import Game
from collections import defaultdict
from real_world import RealWorld
from events import Event
import csv
import numpy as np

# TODO This is your code!
sys.path.insert(1, '../groupNN')

# Uncomment this if you want the empty test character
from testcharacter import TestCharacter

# Uncomment this if you want the interactive character
from interactivecharacter import InteractiveCharacter
from DNQAgent import DNQAgent
from monsters.stupid_monster import StupidMonster
from monsters.selfpreserving_monster import SelfPreservingMonster

# Create the game
# g = Game.fromfile('map.txt')
# # TODO Add your character

# Uncomment this if you want the test character
# g.add_character(TestCharacter("me",  # name
#                               "C",   # avatar
#                                0, 0, # position
#                                1     # variant
# ))

# Uncomment this if you want the interactive character
# g.add_character(DNQAgent("me",  # name
#                          "C",  # avatar
#                          0, 0,  # position
#                          True  # interactive
#                          ))


# g.add_monster(SelfPreservingMonster("aggressive", # name
#                             "A",      # avatar
#                             3, 9,      # position
#                             2
# ))
# Run!

# Use this if you want to press ENTER to continue at each step
# g.go(0)

# Use this if you want to proceed automatically
# g.go(1)

class QLearning(Game):

    def __init__(self, width, height, max_time, bomb_time, expl_duration, expl_range,
                 sprite_dir="../../bomberman/sprites/"):
        super(QLearning, self).__init__(width,height,max_time,bomb_time,expl_duration,expl_range,sprite_dir)
        self.world = RealWorld.from_params(width, height, max_time, bomb_time, expl_duration, expl_range)
        # self.sprite_dir = sprite_dir
        # self.load_gui(width, height)
        self.QTable = self.addQTable()
        self.discount_factor = 1
        self.alpha = 1
        self.epsilon = 0.1
        self.agent = None
        self.pureagent = None

    # @classmethod
    # def fromfile(cls, fname, sprite_dir="../../bomberman/sprites/"):
    #     super(QLearning, cls).fromfile(fname, sprite_dir)

    def addQTable(self):
        return self.importQTable()
        # return defaultdict(lambda: np.zeros(10))

    def add_monster(self, m):
        super(QLearning, self).add_monster(m)
        # self.world.add_monster(m)

    def add_character(self, c):
        if self.pureagent is None:
            self.pureagent = copy.copy(c)
        super(QLearning, self).add_character(c)
        self.agent = c
        if self.agent.inter:
            self.epsilon = 0.1
            self.alpha = 0.0
            self.discount_factor = 0.0


    def createEpsilonGreedyPolicy(self,epsilon):
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

    def qLearning(self, num_episodes):
        policy = self.createEpsilonGreedyPolicy(self.epsilon)
        winCount = 0
        loseCount = 0
        if self.agent.inter:
            num_episodes = 1
        
        update_on = num_episodes-1/4
        for ith_episode in range(num_episodes+1):
            if (ith_episode) % 100 == 0:
                self.saveQTable()
                print("Episode: {}".format(ith_episode))
            # if ith_episode % update_on:
            #     self.alpha -= 0.1
            #     self.epsilon -= 0.01
            #     self.discount_factor -= 0.1
            self.resetEnv()
            state = self.agent.getState()
            # print(state)

            while not self.done():
                action_probabilities  = policy(state)
                action = np.random.choice(np.arange(
                    len(action_probabilities)),
                    p = action_probabilities
                )
                next_state, reward = self.step(action)
                if self.agent.inter:
                    print(next_state,reward)
                for event in self.world.events:
                    if event.tpe == Event.BOMB_HIT_CHARACTER:
                        loseCount += 1
                        reward = -1000
                    elif event.tpe == Event.CHARACTER_FOUND_EXIT:
                        winCount += 1
                        reward = 1
                    # elif event.tpe == Event.BOMB_HIT_WALL:
                    #     reward += 50

                best_next_action = np.argmax(self.QTable[next_state])
                td_target = reward + self.discount_factor * self.QTable[next_state][best_next_action]
                td_delta = td_target - self.QTable[state][action]
                self.QTable[state][action] += self.alpha * td_delta

                state = next_state
        print("Lost: {}".format(loseCount))
        print("Won: {}".format(winCount))

    def step(self,action):
        if self.agent.inter:
            self.world.printit()
            input("Press enter to contiue")
        next_state, reward = self.agent.step(action)
        (self.world,self.events) = self.world.next()
        self.world.next_decisions()
        return next_state, reward
            
    def resetEnv(self):
        self.world = self.fromfile('map.txt').world
        self.world.remove_character(self.agent)
        self.agent = copy.copy(self.pureagent)
        self.add_character(self.agent)
        self.agent.addWorld(self.world)
        (self.world, self.events) = self.world.next()
        self.world.next_decisions()

    def go(self, wait=0):
        super(QLearning, self).go(wait)

    def saveQTable(self):
        with open("QTable.csv", "w", newline='') as f:
            w = csv.writer(f)
            for key, val in self.QTable.items():
                w.writerow([key, *val])
        f.close()

    def importQTable(self, file="QTable.csv"):
        QTable = defaultdict(lambda: np.zeros(10))
        try:
            with open(file, 'r') as f:
                r = csv.reader(f)
                for k, *v in r:
                    QTable[k] = np.array(list(map(float, v)))
        except Exception as inst:
            print(type(inst))  # the exception instance
            print(inst.args)  # arguments stored in .args
            print(inst)  # __str__ allows args to be printed directly,
            return QTable
        return QTable


q = QLearning.fromfile('map.txt')
q.add_character(DNQAgent("me",  # name
                         "C",  # avatar
                         0, 0,  # position
                         True  # interactive
                         ))
q.qLearning(1000)
q.saveQTable()
