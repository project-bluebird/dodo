
import pytest
import pandas as pd

from pydodo import SimurghEnv, set_simulator_mode, reset_simulation, load_scenario

from pydodo.utils import ping_bluebird
from pydodo.config_param import config_param

bb_resp = ping_bluebird()
bluesky_sim = config_param("simulator") == config_param("bluesky_simulator")


@pytest.fixture
def target():
    return SimurghEnv()

@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_env(target):

    cmd = set_simulator_mode("agent")
    assert cmd == True

    resp = reset_simulation()
    assert resp == True

    resp = load_scenario("scenario/8.SCN")
    assert resp == True

    obs, reward, done, info = target.step(0)
    assert isinstance(obs, pd.DataFrame)
    assert isinstance(reward, int)
    assert isinstance(done, bool)
    assert isinstance(info, dict)

    obs, reward, done, info = target.step(1)
    assert isinstance(obs, pd.DataFrame)
    assert isinstance(reward, int)
    assert isinstance(done, bool)
    assert isinstance(info, dict)
