import pytest
import time
from requests.exceptions import HTTPError

from pydodo import (
    reset_simulation,
    create_aircraft,
    aircraft_position,
    define_waypoint,
    add_waypoint,
    direct_to_waypoint
)
from pydodo.utils import ping_bluebird

# test if can connect to BlueBird
bb_resp = ping_bluebird()


@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_direct_to_waypoint():
    cmd = reset_simulation()
    assert cmd == True

    aircraft_id = "TST1001"
    type = "B744"
    latitude = 0
    longitude = 0
    heading = 0
    flight_level = 250
    speed = 200

    cmd = create_aircraft(
        aircraft_id=aircraft_id,
        type=type,
        latitude=latitude,
        longitude=longitude,
        heading=heading,
        flight_level=flight_level,
        speed=speed,
    )
    assert cmd == True

    # Check the altitude.
    position = aircraft_position(aircraft_id)

    # In the returned data frame aircraft_id is uppercase.
    aircraft_id = aircraft_id.upper()
    assert position.loc[aircraft_id]["longitude"] == 0

    cmd = define_waypoint("new_waypoint", 45, 45)
    assert cmd == True

    # Test with an invalid waypoint, it has not been added to flight route yet
    wpt = "new_waypoint"
    with pytest.raises(HTTPError):
        direct_to_waypoint(aircraft_id=aircraft_id, waypoint_name=wpt)

    cmd = add_waypoint(aircraft_id=aircraft_id, waypoint_name=wpt)
    assert cmd == True

    # Give the command to head to waypoint.
    cmd = direct_to_waypoint(aircraft_id=aircraft_id, waypoint_name=wpt)
    assert cmd == True

    # Check that the heading has changed.
    time.sleep(1)
    new_position = aircraft_position(aircraft_id)
    assert new_position.loc[aircraft_id]["longitude"] > 0
