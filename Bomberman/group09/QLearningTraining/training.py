# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '../QLearningTraining')
sys.path.insert(2, '..')
import time
# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../groupNN')

# Uncomment this if you want the empty test character
from monsters.stupid_monster import StupidMonster
from monsters.selfpreserving_monster import SelfPreservingMonster

# Uncomment this if you want the interactive character
from interactivecharacter import InteractiveCharacter
from QAgent import QAgent
from events import Event
# Create the game
g = Game.fromfile('map.txt')

# TODO Add your character

# Uncomment this if you want the test character
# g.add_character(TestCharacter("me",  # name
#                               "C",   # avatar
#                                0, 0, # position
#                                1     # variant
# ))


# Uncomment this if you want the interactive character
#g.add_character(InteractiveCharacter("me", # name
#                                     "C",  # avatar
#                                     0, 0  # position
#))

# Run!

# Use this if you want to press ENTER to continue at each step
# g.go(0)

# Use this if you want to proceed automatically
# Run!
winCount = 0
loseCount = 0
for episode in range(10000):
    time.sleep(0.01)
    if episode % 100 == 0:
        print("Game: {}".format(episode))
        print("Lost: {}".format(loseCount))
        print("Won: {}".format(winCount))
    g = Game.fromfile('map.txt')
    agent = QAgent("me", # name
                              "C",  # avatar
                              0, 1,  # position
                                "../QLearningTraining/QTable.csv", True)

    # g.add_monster(StupidMonster("stupid", # name
    #                         "S",      # avatar
    #                         3, 9      # position
    # ))
    # g.add_monster(SelfPreservingMonster("selfpreserving", # name
    #                                 "S",              # avatar
    #                                 3, 9,             # position
    #                                 1                 # detection range
    # ))    
    g.add_character(agent)
    g.go(1)
    loseFlag = True
    for event in g.world.events:
        if event.tpe == Event.CHARACTER_FOUND_EXIT:
            agent.we_won()
            winCount += 1
            loseFlag = False
    
    if loseFlag:
        agent.we_died()
        loseCount +=1

  
print("Lost: {}".format(loseCount))
print("Won: {}".format(winCount))