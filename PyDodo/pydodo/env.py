
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

        # TODO: make sure simulator mode is "agent"
        # Q: where is sector and scenario info specified?

    def step(self, action):
        """
        :param action:
        :return: obs (object), reward (float), done (bool), info (dict)
        """

        # TODO: take action
        # this requires knowing what altitude to request of which aircraft
        # need to determine some ACTION_MAPPING

        simulation_step()

        aircraft_ids = all_positions().index
        aircraft_pairs = itertools.combinations(aircraft_ids, r=2)
        separations = [
            loss_of_separation(acid1, acid2) for acid1, acid2 in aircraft_pairs
        ]

        obs = all_positions()
        done = (obs.shape[0] == 0) # are there any remaining aircraft

        return obs, sum(separations), done, {}

    def reset(self):

        # TODO: below resets simulation and clears all aircraft data
        # --> need to reload and resume scenario
        reset_simulation()

    def close(self):

        # TODO: what does close mean in this environment?
        print("Shut down BlueSky and BlueBird.")
        episode_log()

    def render(self, mode='human'):

        print("Check Twicher.")
