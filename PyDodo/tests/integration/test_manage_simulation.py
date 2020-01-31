import pytest
import os
import time

import pandas as pd

from pydodo import (
    create_aircraft,
    reset_simulation,
    pause_simulation,
    resume_simulation,
    aircraft_position,
    all_positions,
    set_simulation_rate_multiplier,
    list_route,
    simulation_step,
)
from pydodo.bluebird_connect import ping_bluebird
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

    resp = simulation_step()
    assert resp == True

    pos1 = aircraft_position(aircraft_id)
    assert pos1.loc[aircraft_id]["latitude"] > pos0.loc[aircraft_id]["latitude"]
        
    # resp = set_simulation_rate_multiplier(1.5)
    # assert resp == True
