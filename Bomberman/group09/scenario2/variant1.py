# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game
from events import Event

# TODO This is your code!
sys.path.insert(1, '../groupNN')
from testcharacter import TestCharacter
from interactivecharacter import InteractiveCharacter
from QAgent import QAgent
import matplotlib.pyplot as plt
from monsters.stupid_monster import StupidMonster
from monsters.selfpreserving_monster import SelfPreservingMonster


# Create the game
g = Game.fromfile('map.txt')

# TODO Add your character
# g.add_character(TestCharacter("me", # name
#                               "C",  # avatar
#                               0, 0,  # position
#                                 1
# ))

agent = QAgent("me", # name
                              "C",  # avatar
                              0, 0,  # position
                                "../QLearningTraining/QTable.csv", True)
g.add_character(agent)

#g.add_character(InteractiveCharacter("me", "c", 0,0))


# Run!
winCount = 0
loseCount = 0
for episode in range(1000000):
  if episode % 100 == 0:
      agent.save_q_table()
      print("Game: {}".format(episode))
      print("Lost: {}".format(loseCount))
      print("Won: {}".format(winCount))
  g = Game.fromfile('map.txt')
  agent = QAgent("me", # name
                              "C",  # avatar
                              0, 0,  # position
                                "../QLearningTraining/QTable.csv", True)
  
  # g.add_monster(SelfPreservingMonster("aggressive", # name
  #                                   "A",          # avatar
  #                                   3, 5,        # position
  #                                   2             # detection range
  # ))
  g.add_character(agent)
  g.go(1)
  agent.do(g.world)
  loseFlag = True
  for event in g.world.events:
    if event.tpe == Event.CHARACTER_FOUND_EXIT:
      winCount += 1
      loseFlag = False
  
  if loseFlag:
    loseCount +=1

print("Lost: {}".format(loseCount))
print("Won: {}".format(winCount))