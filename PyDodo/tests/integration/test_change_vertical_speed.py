import pytest
import time

from pydodo import change_vertical_speed, change_altitude, reset_simulation, create_aircraft, aircraft_position
from pydodo.utils import ping_bluebird

# test if can connect to BlueBird
bb_resp = ping_bluebird()


@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_change_vertical_speed():
    cmd = reset_simulation()
    assert cmd == True

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
    assert position.loc[aircraft_id]['vertical_speed'] == 0

    # Give command to ascend
    new_flight_level = 400
    cmd = change_altitude(aircraft_id = aircraft_id,
                          flight_level = new_flight_level)

    # Test with an invalid speed.
    invalid_vertical_speed = -1
    with pytest.raises(AssertionError):
        change_vertical_speed(aircraft_id = aircraft_id,
                     vertical_speed = invalid_vertical_speed)

    # Give the command to change speed.
    new_speed = 10
    cmd = change_vertical_speed(aircraft_id = aircraft_id,
                                vertical_speed = new_speed)
    assert cmd == True

    # TO DO: Check that vertical speed has changed.
