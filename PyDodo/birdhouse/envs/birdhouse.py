import gym
from gym import spaces
from gym.utils import seeding

import pydodo as dodo
# DEFINE ACTIONS HERE


class BirdhouseEnv(gym.Env):
    """Simple birdhouse environment

    ...

    """
    metadata = {'render.modes': ['human']}

    def __init__(self, spots=37):
        self.n = spots + 1
        self.action_space = spaces.Discrete(self.n)
        # self.observation_space = spaces.Box( DIMENSIONS OF SECTOR?
        self.observation_space = spaces.Discrete(1)
        self.seed()

        # Start the first game
        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        """Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.

        Accepts an action and returns a tuple (observation, reward, done, info).

        Args:
            action (object): an action provided by the agent

        Returns:
            observation (object): agent's observation of the current environment
            reward (float) : amount of reward returned after previous action
            done (bool): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
        """
        assert self.action_space.contains(action)
        if action == self.n - 1:
            # observation, reward, done, info
            return 0, 0, True, {}
        # N.B. np.random.randint draws from [A, B) while random.randint draws from [A,B]
        val = self.np_random.randint(0, self.n - 1)
        if val == action == 0:
            reward = self.n - 2.0
        elif val != 0 and action != 0 and val % 2 == action % 2:
            print(dodo.all_positions().values)
            reward = 1.0
        else:
            reward = -1.0
        return 0, reward, False, {}

    def reset(self):
        return 0


