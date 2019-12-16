import pytest
import time

from pydodo import change_altitude, reset_simulation, create_aircraft, aircraft_position
from pydodo.bluebird_connect import ping_bluebird

# test if can connect to BlueBird
bb_resp = ping_bluebird()


@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_change_altitude():
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
    assert position.loc[aircraft_id]["altitude"] == pytest.approx(flight_level * 100)

    # Give the command to ascend.
    new_flight_level = 400
    cmd = change_altitude(aircraft_id=aircraft_id, flight_level=new_flight_level)
    assert cmd == True

    # Check that the new altitude exceeds the original one.
    time.sleep(1)
    new_position = aircraft_position(aircraft_id)
    assert new_position.loc[aircraft_id]["altitude"] > flight_level * 100
