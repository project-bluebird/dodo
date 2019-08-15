import pytest
import os
import time

import pandas as pd

from pydodo import (
    create_aircraft,
    reset_simulation,
    load_scenario,
    pause_simulation,
    resume_simulation,
    aircraft_position,
    all_positions,
    set_simulation_rate_multiplier,
    list_route,
    set_simulator_mode,
    simulation_step
)
from pydodo.utils import ping_bluebird
from pydodo.config_param import config_param

bb_resp = ping_bluebird()
bluesky_sim = config_param("simulator") == config_param("bluesky_simulator")


@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_simulation_control():
    """
    Test simulation endpoints
    - Pause Simulation
    - Resume Simulation
    - Reset Simulation
    - Simulation time
    - Simulator mode
    - Simulation step
    """
    aircraft_id = "TST1001"
    type = "B744"
    latitude = 0
    longitude = 0
    heading = 0
    altitude = None
    flight_level = 250
    speed = 200

    resp = reset_simulation()
    assert resp == True

    resp = create_aircraft(
        aircraft_id, type, latitude, longitude, heading, speed, altitude, flight_level
    )
    assert resp == True

    pos0 = aircraft_position(aircraft_id)

    resp = pause_simulation()
    assert resp == True

    pos1 = aircraft_position(aircraft_id)
    # check that position has changed since last position call
    assert pos1.loc[aircraft_id]["latitude"] > pos0.loc[aircraft_id]["latitude"]

    pos2 = aircraft_position(aircraft_id)
    # check that position has not changed since simulation was paused
    assert pos1.loc[aircraft_id]["latitude"] == pos2.loc[aircraft_id]["latitude"]

    resp = resume_simulation()
    assert resp == True

    pos3 = aircraft_position(aircraft_id)
    # check that position has changed since simulation was resumed
    assert pos3.loc[aircraft_id]["latitude"] > pos2.loc[aircraft_id]["latitude"]

    resp = set_simulation_rate_multiplier(1.5)
    assert resp == True

    cmd = set_simulator_mode("agent")
    assert cmd == True

    pos4 = aircraft_position(aircraft_id)

    time.sleep(1)

    pos5 = aircraft_position(aircraft_id)
    # using agent mode sets simulator on hold
    assert pos4.loc[aircraft_id]["latitude"] == pos5.loc[aircraft_id]["latitude"]

    cmd = simulation_step()
    assert cmd == True

    pos6 = aircraft_position(aircraft_id)
    assert pos6.loc[aircraft_id]["latitude"] > pos5.loc[aircraft_id]["latitude"]


@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
@pytest.mark.skipif(not bluesky_sim, reason="Not using BlueSky")
def test_load_bluesky():
    """
    Check that can load BlueSky scenario files (if using BlueSky) and specify
    the sim rate multiplier.
    """
    resp = load_scenario("scenario/8.scn")
    assert resp == True

    resp = load_scenario("scenario/8.scn", 1.5)
    assert resp == True


@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_load_fail():
    """
    Check fails if no scenario file is provided or wrong multiplier value provided.
    """
    with pytest.raises(AssertionError):
        load_scenario("")

    with pytest.raises(AssertionError):
        load_scenario("scenario/8.scn", 0)
