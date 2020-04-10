from gym.envs.registration import register

register(
    id='birdhouse-v1',
    entry_point='birdhouse.envs:BirdhouseEnv',
)
