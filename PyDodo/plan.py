import gym
import birdhouse

env = gym.make("birdhouse-v1")

action = None

for _ in range(10):
    # ENVIRONMENT STEP
    obs, reward, done, info = env.step(action)
    # AGENT - ACTION SELECTION
    # --> choose plan wit biggest absolute difference between current and requested flight levels
    # and send to requested FL (unless the difference is < 10 FL)
    obs["FL_diff"] = (obs['requested_flight_level'] - obs['current_flight_level']/100).abs()
    max_diff =  obs.loc[obs['FL_diff'].idxmax()]
    if max_diff['FL_diff'] >= 10:
        callsign = max_diff.name
        req_fl = max_diff['requested_flight_level']
        action = (callsign, req_fl)
    else:
        action = None
