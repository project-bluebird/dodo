import pytest
import os
import time

import pandas as pd

from pydodo import (
    reset_simulation,
    upload_scenario,
    upload_sector,
    all_positions,
    aircraft_position,
    list_route,
    simulation_step,
    simulation_info,
    set_simulation_rate_multiplier,
)
from pydodo.bluebird_connect import ping_bluebird
from pydodo.config_param import config_param

bb_resp = ping_bluebird()


@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_upload_scenario(rootdir):
    """
    Runs through a basic scenario covering all the main functionality
    (no aircraft commands are sent).
    """

    resp = reset_simulation()
    assert resp == True

    # 1. SIMULATION SHOULD BE EMPTY

    info0 = simulation_info()
    assert info0["scenario_name"] is None
    assert len(info0["aircraft_ids"]) == 0

    # 2. LOAD SECTOR AND SCENARIO

    test_scenario_file = os.path.join(rootdir, "dodo-test-scenario")
    test_sector_file = os.path.join(rootdir, "dodo-test-sector")

    resp = upload_sector(filename=f"{test_sector_file}.geojson",sector_name="test_sector")
    assert resp == True

    resp = upload_scenario(filename=f"{test_scenario_file}.json",scenario_name="test_scenario")
    assert resp == True

    # 3. CHECK SIMULATION HAS AIRCRAFT WITH POSITIONS AND ROUTES

    info = simulation_info()
    assert info["scenario_name"] == "test_scenario"
    assert len(info["aircraft_ids"]) == 2

    pos = all_positions()
    assert isinstance(pos, pd.DataFrame)
    assert len(pos.index) == 2

    acid1, acid2 = pos.index

    route1 = list_route(acid1)
    route2 = list_route(acid2)

    assert isinstance(route1, dict)
    assert isinstance(route2, dict)
    assert len(route1["route_waypoints"]) == 5
    assert len(route2["route_waypoints"]) == 5

    # 4. STEP FORWARD THE SIMULATION & CHECK IT ADVANCED (5 x 1 second scenario time)
    for i in range(5):
        info1 = simulation_info()
        resp = simulation_step()
        assert resp == True

    info2 = simulation_info()

    assert info2["scenario_time"] - info1["scenario_time"] == pytest.approx(1.0)

    # EXPECT CHANGE IN AIRCRAFT LATITUDES
    # aircraft 1 is travelling from latitude ~51 to ~53
    # aircraft 2 is heading in the opposite direction

    pos1 = all_positions()
    assert pos.loc[acid1, "longitude"] == pos1.loc[acid1, "longitude"]
    assert pos.loc[acid1, "latitude"] < pos1.loc[acid1, "latitude"]

    assert pos.loc[acid2, "longitude"] == pos1.loc[acid2, "longitude"]
    assert pos.loc[acid2, "latitude"] > pos1.loc[acid2, "latitude"]

    # 5. CHANGE STEP SIZE & TAKE STEP
    # SIMULATION SHOULD MOVE FOWARD BY MORE THAN BEFORE (10 second scenario time)
    resp = set_simulation_rate_multiplier(10)
    assert resp == True

    resp = simulation_step()
    assert resp == True

    info3 = simulation_info()
    assert info3["scenario_time"] - info2["scenario_time"] == pytest.approx(10.0)

    # CHANGE IN AIRCRAFT LATITUDE SHOULD BE MORE IN THIS SINGLE 10s STEP
    # COMPARED TO PREVIOUS 5 x 1 second STEPS
    # pos2 = all_positions()
    # assert (
    #     abs(pos2.loc[acid1, "latitude"] - pos1.loc[acid1, "latitude"]) >
    #     abs(pos1.loc[acid1, "latitude"] - pos.loc[acid1, "latitude"])
    # )
    # assert (
    #     abs(pos2.loc[acid2, "latitude"] - pos1.loc[acid2, "latitude"]) >
    #     abs(pos1.loc[acid2, "latitude"] - pos.loc[acid2, "latitude"])
    # )
