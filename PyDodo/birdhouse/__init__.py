from gym.envs.registration import register

register(
    id='birdhouse-v0',
    entry_point='birdhouse.envs:BirdhouseEnv',
)
