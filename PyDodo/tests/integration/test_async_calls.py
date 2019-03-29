import pytest

from pydodo import (async_change_altitude, async_change_heading,
                    batch, reset_simulation, create_aircraft)
from pydodo.utils import ping_bluebird

# test if can connect to BlueBird
bb_resp = ping_bluebird()

@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_async_request():
    """
    Tests async_request() function
    """
    reset_simulation()

    aircraft_id = "TST1001"
    type = "B744"
    latitude = 0
    longitude = 0
    heading = 0
    flight_level = 250
    speed = 200

    cmd = create_aircraft(aircraft_id = aircraft_id,
                          type = type,
                          latitude = latitude,
                          longitude = longitude,
                          heading = heading,
                          flight_level = flight_level,
                          speed = speed)
    assert cmd == True

    commands = []
    commands.append(async_change_altitude(aircraft_id = aircraft_id, flight_level = 200))
    commands.append(async_change_heading(aircraft_id = aircraft_id, heading = 90))
    results = batch(commands)

    assert results[0] == True
    assert results[1] == True
