import pytest
import os
import time

import pandas as pd

from pydodo import (
    reset_simulation,
    create_scenario,
    create_sector,
    all_positions,
    list_route,
)
from pydodo.bluebird_connect import ping_bluebird
from pydodo.config_param import config_param

from requests.exceptions import HTTPError

bb_resp = ping_bluebird()
bluesky_sim = config_param("simulator") == config_param("bluesky_simulator")


@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
# @pytest.mark.skipif(not bluesky_sim, reason="Not using BlueSky")
def test_create_scenario(rootdir):
    """
    Create scenario on the simulator host and load.
    Check two aircraft created succesfully with associated route.
    """

    test_scenario = "dodo-test-scenario"
    test_sector = "dodo-test-sector"
    test_scenario_file = os.path.join(rootdir, test_scenario)
    test_sector_file = os.path.join(rootdir, test_sector)

    resp = reset_simulation()
    assert resp == True

    # Can't load scenario without sector

    with pytest.raises(HTTPError):
        resp = create_scenario(filename="{}.json".format(test_scenario_file), scenario=test_scenario)

    # Define sector and then load scenario

    resp = create_sector(filename="{}.geojson".format(test_sector_file), sector=test_sector)
    assert resp == True

    resp = create_scenario(filename="{}.json".format(test_scenario_file), scenario=test_scenario)
    assert resp == True

    time.sleep(1)

    pos = all_positions()
    assert isinstance(pos, pd.DataFrame)
    assert len(pos.index) == 2

    aircraft_ids = pos.index

    # access route information for each aircraft
    route1 = list_route(aircraft_ids[0])
    route2 = list_route(aircraft_ids[1])

    assert isinstance(route1, pd.DataFrame)
    assert isinstance(route2, pd.DataFrame)
    assert len(route1.index) == 5
    assert len(route2.index) == 5
    assert len(route1.columns) == 3
    assert len(route2.columns) == 3
