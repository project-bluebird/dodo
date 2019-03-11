import pytest
import time

from pydodo import change_speed, reset_simulation, create_aircraft, aircraft_position
from pydodo.utils import ping_bluebird

# test if can connect to BlueBird
bb_resp = ping_bluebird()

@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_change_speed():
    reset_simulation()

    aircraft_id = "TST1001"
    type = "B744"
    latitude = 0
    longitude = 0
    heading = 0
    flight_level = 250
    speed = 265

    cmd = create_aircraft(aircraft_id = aircraft_id,
                          type = type,
                          latitude = latitude,
                          longitude = longitude,
                          heading = heading,
                          flight_level = flight_level,
                          speed = speed)
    assert cmd == True

    # Check the altitude.
    position = aircraft_position(aircraft_id)

    # In the returned data frame aircraft_id is uppercase.
    aircraft_id = aircraft_id.upper()
    # Aircaft initial speed differs from specified speed.
    assert position.loc[aircraft_id]['ground_speed'] < 198

    # Test with an invalid speed.
    invalid_speed = -1
    with pytest.raises(AssertionError):
        change_speed(aircraft_id = aircraft_id, speed = invalid_speed)

    # Give the command to change speed.
    new_speed = 400
    cmd = change_speed(aircraft_id = aircraft_id, speed = new_speed)
    assert cmd == True

    # Wait for the ground speed to increase.
    time.sleep(0.5)

    # Check that the heading has changed.
    new_position = aircraft_position(aircraft_id)
    assert new_position.loc[aircraft_id]["ground_speed"] > 198
