import os
import argparse

from .PySc2HelperFunctions import PySc2HelperFunctions

import pandas as pd
import numpy as np

ACTION_UP = 'UP'
ACTION_RIGHT = 'RIGHT'
ACTION_DOWN = 'DOWN'
ACTION_LEFT = 'LEFT'

smart_actions = [ ACTION_UP, ACTION_RIGHT, ACTION_DOWN, ACTION_LEFT ]

import re
BLOCK_SIZE = 5

class MyAgent():
    def __init__(self):
        self.print_all_actions()
        self.qlearn = QLearningTable(actions=list(range(len(smart_actions))))
            
        self.armySelected = False
        self.previous_action = None
        self.previous_state = None
        self.previousMapScore = 1
        self.targetX = 0
        self.targetY = 0
        self.armyMoved = False
        self.helperFunctions = PySc2HelperFunctions()
        self.previousAction = self.helperFunctions.create_do_nothing_action()
        
    def print_all_actions(self):
        i = 0
        while i < len(smart_actions):
            print("Action: %s, %s" % (i, smart_actions[i]))
            i += 1

    def get_state(self, obs):                        
        army_x, army_y = self.helperFunctions.get_marine_position(obs)
        print("Army X:",army_x, " Y:",army_y)

        beacon_x, beacon_y = self.helperFunctions.get_beacon_position(obs)
        print("Beacon X:",beacon_x, " Y:",beacon_y)

        current_state = [ beacon_x >= army_x, beacon_x <= army_x, beacon_y >= army_y, beacon_y <= army_y]
        print(current_state)
        return current_state
    
    def do_action(self, smart_action, obs):
        smart_action = smart_actions[smart_action]
        print("Selected action: %s" % smart_action)
       
        action = self.helperFunctions.create_do_nothing_action()

        if not (self.helperFunctions.is_marine_selected(obs)):
            print("SELECT MARINEEEE")
            return self.helperFunctions.create_select_army_action()

        x,y = self.helperFunctions.get_marine_position(obs)
        print(("unit pos = %s, %s" % (x, y)))
        moveDistance = 7
        
        if smart_action == ACTION_UP:
            y = y + moveDistance
        if smart_action == ACTION_DOWN:
            y = y - moveDistance
        
        if smart_action == ACTION_RIGHT:
            x = x + moveDistance
        if smart_action == ACTION_LEFT:
            x = x - moveDistance
        
        if x < 5:
            x = 5
        if x > 78:
            x = 78
            
        if y < 5:
            y = 5 
        if y > 58:
            y = 58
            
        action = self.helperFunctions.create_move_to_position_action(x, y)
        print(("target pos = %s, %s" % (x, y)))
        self.targetX = x 
        self.targetY = y
        self.armyMoved = True
        self.previousAction = action
        return action
    
    def get_reward(self, obs):     
        army_x, army_y = self.helperFunctions.get_marine_position(obs)
        beacon_x, beacon_y = self.helperFunctions.get_beacon_position(obs)
        delta_y = abs(army_y - beacon_y) * -1
        delta_x = abs(army_x - beacon_x) * -1
        
        reward = delta_y + delta_x + 150
        #reward = reward * reward
        
        mapScore = obs.observation['score_cumulative'][0] + 1
        if mapScore > self.previousMapScore:
            print(("mapScore = %s   self.previousMapScore = %s" % (mapScore, self.previousMapScore)))
            self.previousMapScore = mapScore
            reward = reward * 5
        
        print(("reward = %s" % (reward)))
        return reward
    
    def step(self, obs):
        
        if self.helperFunctions.marine_is_on_position(obs, self.targetX, self.targetY):
            current_state = self.get_state(obs)
            if self.previous_action is not None:
                reward = self.get_reward(obs)
                self.do_learning(self.previous_state, current_state, self.previous_action, reward)
            else:
                reward = 0
            
            selected_action = self.select_action(current_state)    
            action = self.do_action(selected_action, obs)
            print(action)
            
            # update current state
            self.previous_state = current_state
            self.previous_action = selected_action
            return action
		
        print('sleep')
        return self.previousAction
        # return self.previousAction

    def do_learning(self, previous_state, current_state, previous_action, reward):    
        # update learning
        self.qlearn.learn(str(previous_state), previous_action,
                              reward, str(current_state))
      
    def select_action(self, state, eps=0.5):
        action = self.qlearn.choose_action(str(state))
        return action


class QLearningTable():
    def __init__(self, actions, learning_rate=0.8, reward_decay=0.5, e_greedy=0.5):
        self.actions = actions
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        print("QTABLE: %s" % (self.q_table))

    def choose_action(self, observation):
        self.check_state_exist(observation)

        if np.random.uniform() < self.epsilon:
            # exploitation
            state_action = self.q_table.ix[observation, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))
            action = state_action.idxmax()
        else:
            # exploration
            action = np.random.choice(self.actions)
        return action

    def learn(self, state, action, reward, state_):
        self.check_state_exist(state_)
        self.check_state_exist(state)
        # print("State = %s, %s" % (state, type(state)))
        # print("Action = %s, %s" % (action, type(action)))

        q_predict = self.q_table.ix[state, action]
        q_target = reward + self.gamma * self.q_table.ix[state_, :].max()

        # update
        self.q_table.ix[state, action] += self.lr * (q_target - q_predict)

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # Append
            self.q_table = self.q_table.append(pd.Series([0]*len(self.actions), index=self.q_table.columns, name=state))
