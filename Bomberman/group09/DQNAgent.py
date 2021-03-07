import matplotlib 
import numpy as np 
import pandas as pd 
# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game
from testcharacter import TestCharacter

# TODO This is your code!
sys.path.insert(1, '../groupNN')

class DQNAgent:
  def __init__(self,tChar):
      super().__init__()
      self.reward = 0
      self.gamma = 0.9
      self.tChar = tChar

  def test():
    print('hello')

  def createEpsilonGreedyPolicy(Q, epsilon, num_actions): 
      """ 
      Creates an epsilon-greedy policy based 
      on a given Q-function and epsilon. 
        
      Returns a function that takes the state 
      as an input and returns the probabilities 
      for each action in the form of a numpy array  
      of length of the action space(set of possible actions). 
      """
      def policyFunction(state): 
    
          Action_probabilities = np.ones(num_actions, 
                  dtype = float) * epsilon / num_actions 
                    
          best_action = np.argmax(Q[state]) 
          Action_probabilities[best_action] += (1.0 - epsilon) 
          return Action_probabilities 
    
      return policyFunction 
    
  def qLearning(env, num_episodes, discount_factor = 0.9, alpha = 0.6, epsilon = 0.1):
    return



# # Create the game
# random.seed(123) # TODO Change this if you want different random choices
# g = Game.fromfile('map.txt')
g = Game.fromfile('map.txt')
t = TestCharacter("me", "C", 0,0)

DQNAgent.test()

