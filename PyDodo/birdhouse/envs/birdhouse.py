"""
Implements Open AI gym like environment

see: https://github.com/openai/gym/blob/master/docs/creating-environments.md
"""
import gym
from gym import spaces
from gym.utils import seeding
import itertools

from pydodo.episode_log import episode_log
from pydodo import change_altitude
from pydodo.metrics import loss_of_separation
from pydodo.request_position import all_positions
from pydodo.simulation_control import simulation_step, reset_simulation, pause_simulation


class SimurghEnv(gym.Env):
    """Simple birdhouse environment

    ...

    """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        # TODO: make sure BlueBird (and BlueSky) are running
        # TODO: make sure simulator mode is "agent"
        # TODO: start scenario
        # Q: where/how is sector and scenario info specified?

        self.action_space = None
        self.observation_space = None

        self.seed()

        # Start the first game
        # self.reset()

    def seed(self, seed=None):
        """Sets the seed for this env's random number generator(s).

        Note:
            Some environments use multiple pseudorandom number generators.
            We want to capture all such seeds used in order to ensure that
            there aren't accidental correlations between multiple generators.

            See: https://github.com/openai/gym/blob/master/gym/utils/seeding.py for details in
            np_random() and hash_seed() functions

        Returns:
            list<bigint>: Returns the list of seeds used in this env's random
              number generators. The first value in the list should be the
              "main" seed, or the value which a reproducer should pass to
              'seed'. Often, the main seed equals the provided 'seed', but
              this won't be true if seed=None, for example.
        """

        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        """
        Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.

        Stepping forward the agent (take agent selected action) is not
        necessarily the same as stepping forward the simulation.


        Accepts an action and returns a tuple (observation, reward, done, info).

        Args:
            action (object): an action provided by the agent

        Returns:
            observation (object): agent's observation of the current environment
            reward (float) : amount of reward returned after previous action
            done (bool): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
        """
        # assert self.action_space.contains(action)
        if action is not None:
            # print(all_positions().index)
            print("HELLO WORLD!")
            change_altitude(action[0], flight_level=action[1])
        simulation_step()

        aircraft_pos = all_positions()
        aircraft_pairs = itertools.combinations(aircraft_pos.index, r=2)
        separations = [
             loss_of_separation(acid1, acid2) for acid1, acid2 in aircraft_pairs
         ]

        # print(sum(separations))

        reward = sum(separations)
        print(reward)
        # observation, reward, done, info
        return all_positions(), reward, True, {}

        val = self.np_random.randint(49, 50)
        if val == action == 50:
            # observation, reward, done, info
            reward = -1.0
            return 0, reward, False, {}

        # TODO: take action
        # NOTE: this requires knowing what altitude to request of which aircraft
        # --> probably need to determine some ACTION_MAPPING

        # NOTE: below is not required - could run in 'sandbox' mode
        # simulation_step()

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
        # return obs, sum(separations), done, {}

    def reset(self):
        """Resets the state of the environment and returns an initial observation.
        Returns:
            observation (object): the initial observation.
        """
        # NOTE: below resets simulation and clears all aircraft data
        # TODO: reload and resume scenario on reset
        reset_simulation()

    def close(self):
        """Override close in your subclass to perform any necessary cleanup.
        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        # Q: what does close mean in this context?
        pause_simulation()
        episode_log()

    def render(self, mode='human'):
        """Renders the environment.

        - human: render to the current display or terminal and
          return nothing. Usually for human consumption.

        """

        print("Check Twicher on http://localhost:8080")
