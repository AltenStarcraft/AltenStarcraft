
from pysc2.lib import actions as sc2_actions
from pysc2.env import environment
from pysc2.lib import features
from pysc2.lib import actions
from pysc2.agents import base_agent

from pysc2.agents.MyAgents.MyAgent import MyAgent

class MoveToBeaconAgent(base_agent.BaseAgent):
    def __init__(self):
        self.MyAgent = MyAgent()
        super(MoveToBeaconAgent, self).__init__()
    
    def step(self, obs):
        return self.MyAgent.step(obs)
