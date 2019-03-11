import pytest

from pydodo import change_heading, reset_simulation, create_aircraft, aircraft_position
from pydodo.utils import ping_bluebird

# test if can connect to BlueBird
bb_resp = ping_bluebird()

@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_change_heading():
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

    # Check the altitude.
    position = aircraft_position(aircraft_id)

    # In the returned data frame aircraft_id is uppercase.
    aircraft_id = aircraft_id.upper()
    assert position.loc[aircraft_id]['longitude'] == 0

    # Test with an invalid heading.
    invalid_heading = 400
    with pytest.raises(AssertionError):
        change_heading(aircraft_id = aircraft_id, heading = invalid_heading)

    # Give the command to change heading.
    new_heading = 90
    cmd = change_heading(aircraft_id = aircraft_id, heading = new_heading)
    assert cmd == True

    # Check that the heading has changed.
    new_position = aircraft_position(aircraft_id)
    assert new_position.loc[aircraft_id]["longitude"] > 0
