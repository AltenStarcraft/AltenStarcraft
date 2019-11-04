import os
import argparse

from .PySc2HelperFunctions import PySc2HelperFunctions

import pandas as pd
import numpy as np

import re
ACTION_MOVE_SCREEN = 'movescreen'
pattern = ACTION_MOVE_SCREEN + '_(\d+)_(\d+)'

smart_actions = [ ]
# Create actions to move over the screen
BLOCK_SIZE = 10
for mm_x in range(int(BLOCK_SIZE/2), 78, BLOCK_SIZE):
    for mm_y in range(int(BLOCK_SIZE/2), 58, BLOCK_SIZE):
        smart_actions.append(ACTION_MOVE_SCREEN + '_' + str(mm_x) + '_' + str(mm_y))
        print("ACTION_MOVE_SCREEN_",str(mm_x),"_",str(mm_y))

class MyAgent():
    def __init__(self):
        self.print_all_actions()
        self.qlearn = QLearningTable(actions=list(range(len(smart_actions))))
            
        self.previous_action = None
        self.previous_state = None
        self.xTarget = 0
        self.yTarget = 0
        self.helperFunctions = PySc2HelperFunctions()
        self.previousAction = self.helperFunctions.create_do_nothing_action()
        
    def print_all_actions(self):
        i = 0
        while i < len(smart_actions):
            print("Action: %s, %s" % (i, smart_actions[i]))
            i += 1

    def get_state(self, obs):                        
        army_y, army_x = self.helperFunctions.get_marine_position(obs)
        army_y, army_y = self.helperFunctions.map_position_to_grid_position(army_y, army_x, BLOCK_SIZE)
        print("Army X:",army_x, " Y:",army_y)

        beacon_y, beacon_x = self.helperFunctions.get_beacon_position(obs)
        beacon_y, beacon_x = self.helperFunctions.map_position_to_grid_position(beacon_y, beacon_x, BLOCK_SIZE)
        print("Beacon X:",beacon_x, " Y:",beacon_y)

        current_state = [ beacon_y, beacon_x ]
        print(("Current state = %s" % (current_state)))
        return current_state
    
    def do_action(self, smart_action, obs):
        smart_action = smart_actions[smart_action]
        print("Selected action: %s" % smart_action)

        # For this workshop we will hard code this so the marine is always selected 
        if not (self.helperFunctions.is_marine_selected(obs)):
            return self.helperFunctions.create_select_army_action()

        if ACTION_MOVE_SCREEN in smart_action:
            match = re.match(pattern, smart_action)
            if match is not None:
                self.xTarget, self.yTarget = int(match.group(1)), int(match.group(2))
            
        action = self.helperFunctions.create_move_to_position_action(self.xTarget, self.yTarget)
        print(("Target pos = %s, %s" % (self.xTarget, self.yTarget)))
        
        self.previousAction = action
        return action
    
    def get_reward(self, obs):     
        reward = obs.observation['score_cumulative'][0]
        print(("reward = %s" % (reward)))
        return reward
    
    def step(self, obs):
        if self.helperFunctions.marine_is_on_position(obs, self.xTarget, self.yTarget):
            # retrieve state
            current_state = self.get_state(obs)
            
            # learn (update Q-Table)
            if self.previous_action is not None:
                reward = self.get_reward(obs)
                self.do_learning(self.previous_state, current_state, self.previous_action, reward)
            
            # retrieve new action, from Q-Table
            selected_action = self.select_action(current_state) 
            
            # transform Q-Table action to StarCraft action
            action = self.do_action(selected_action, obs)
            print(action)
            
            # store previous state and action
            self.previous_state = current_state
            self.previous_action = selected_action
            return action

        else:
            print('marine still moving, waiting until marine is on position')
            return self.previousAction




    def do_learning(self, previous_state, current_state, previous_action, reward):    
        # update learning (update Q-Table)
        self.qlearn.learn(str(previous_state), previous_action,
                              reward, str(current_state))
      
    def select_action(self, state, eps=0.5):
        action = self.qlearn.choose_action(str(state))
        return action


class QLearningTable():
    def __init__(self, actions, learning_rate=0.2, reward_decay=0.5, e_greedy=0.5):
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
