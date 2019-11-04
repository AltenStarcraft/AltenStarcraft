
from pysc2.lib import actions as sc2_actions
from pysc2.env import environment
from pysc2.lib import features
from pysc2.lib import actions
from pysc2.agents import base_agent

_PLAYER_SELF = 1
_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index

_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index
_PLAYER_ID = features.SCREEN_FEATURES.player_id.index
_ARMY = 48
_BEACON = 3  # beacon/minerals

# ACTIONS
_NO_OP = actions.FUNCTIONS.no_op.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_MOVE_SCREEN = actions.FUNCTIONS.Move_screen.id

_NOT_QUEUED = [0]
_SELECT_ALL = [0]

class PySc2HelperFunctions():
    def __init__(self):
        print("PySc2 helper functions initialized")
        self.marine_is_selected = False
        self.no_units_found_bug_active = False

    def get_marine_position(self, obs):
        unit_type = obs.observation['feature_screen'][_UNIT_TYPE]
        unit_y, unit_x = (unit_type == _ARMY).nonzero()
        # There is a bug where if the unit is very close to the beacon the unit is not found, 
        # this is a workaround for this issue
        if len(unit_y) == 0 or len(unit_x) == 0:
            self.no_units_found_bug_active = True
            return self.get_beacon_position(obs)
        if (unit_y.mean() == 0 and unit_x.mean() == 0):
            self.no_units_found_bug_active = True
            return self.get_beacon_position(obs)
            
        self.no_units_found_bug_active = False
        return unit_x.mean(), unit_y.mean()
        
    def get_beacon_position(self, obs):
        beacon_type = obs.observation["feature_screen"][_PLAYER_RELATIVE]
        beacon_y, beacon_x = (beacon_type == _BEACON).nonzero()
        # When there are no beacons 
        if len(beacon_y) == 0 or len(beacon_x) == 0:
            return 0,0
        return beacon_x.mean(), beacon_y.mean()

    # score is the number of beacons obtained
    def get_score(self, obs):
        return obs.observation['score_cumulative'][0]
    
    def map_position_to_grid_position(self, y, x, BLOCK_SIZE):
        y = int(y // BLOCK_SIZE)
        x = int(x // BLOCK_SIZE)
        return x, y

    def create_move_to_position_action(self, x, y):
        return actions.FunctionCall(_MOVE_SCREEN, [_NOT_QUEUED, [x,y]])

    def create_do_nothing_action(self):
        return actions.FunctionCall(_NO_OP, [])

    def create_select_army_action(self):
        self.marine_is_selected = True
        return actions.FunctionCall(_SELECT_ARMY, [_NOT_QUEUED])

    def marine_is_on_position(self, obs, x_expected, y_expected):
        x_actual, y_actual = self.get_marine_position(obs)
        
        margin = 3
        if self.no_units_found_bug_active:
            margin = 10
        return (abs(x_actual - x_expected) < margin and abs(y_actual - y_expected) < margin) or (x_expected == 0 and y_expected == 0)

    def is_marine_selected(self, obs):
        print(self.marine_is_selected)
        return _SELECT_ARMY in obs.observation['available_actions'] and self.marine_is_selected
