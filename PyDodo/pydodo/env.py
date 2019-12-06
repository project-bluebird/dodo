"""
Implements Open AI gym like environment
see: https://github.com/openai/gym/blob/master/docs/creating-environments.md
"""


import gym
import itertools

from .episode_log import episode_log
from .metrics import loss_of_separation
from .request_position import all_positions
from .simulation_control import simulation_step, reset_simulation, pause_simulation


class SimurghEnv(gym.Env):

    def __init__(self):

        self.action_space = None
        self.observation_space = None

        # TODO: make sure BlueBird (and BlueSky) are running
        # TODO: make sure simulator mode is "agent"
        # TODO: start scenario
        # Q: where/how is sector and scenario info specified?

    def step(self, action):
        """
        :param action:
        :return: obs (object), reward (float), done (bool), info (dict)
        """

        # TODO: take action
        # NOTE: this requires knowing what altitude to request of which aircraft
        # --> probably need to determine some ACTION_MAPPING

        simulation_step()

        aircraft_ids = all_positions().index
        aircraft_pairs = itertools.combinations(aircraft_ids, r=2)
        separations = [
            loss_of_separation(acid1, acid2) for acid1, acid2 in aircraft_pairs
        ]

        # TODO: get sector exit scores

        # TODO: determine the environment/state features to return as obs(ervation)
        obs = all_positions()

        # NOTE: define end of episode as no aircraft in simulation
        # Q: is this sufficient?
        done = (obs.shape[0] == 0)

        # TODO: reward should be some weighted sum of separations AND sector exits
        return obs, sum(separations), done, {}

    def reset(self):

        # NOTE: below resets simulation and clears all aircraft data
        # TODO: reload and resume scenario on reset
        reset_simulation()

    def close(self):

        # Q: what does close mean in this context?
        pause_simulation()
        episode_log()

    def render(self, mode='human'):

        print("Check Twicher on http://localhost:8080")
