
import gym
import itertools

from .episode_log import episode_log
from .metrics import loss_of_separation
from .request_position import all_positions
from .simulation_control import simulation_step, reset_simulation


class SimurghEnv(gym.Env):

    def __init__(self):
        self.action_spcace = None
        self.observation_scape = None

    def step(self, action):
        """
        :param action: integer
        :return: obs (object), reward (float), done (bool), info (dict)
        """
        # TODO: take action

        simulation_step()

        aircraft_ids = all_positions().index
        aircraft_pairs = itertools.combinations(aircraft_ids, r=2)
        separations = [
            loss_of_separation(aircraft_id_1, aircraft_id_2)
            for aircraft_id_1, aircraft_id_2 in aircraft_pairs
        ]

        obs = all_positions()
        done = (obs.shape[0] == 0) # are there still aircraft

        return obs, sum(separations), done, {}

    def reset(self):
        reset_simulation()

    def close(self):
        episode_log()

    def render(self, mode='human'):
        print("Check Twicher")
