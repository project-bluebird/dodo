import os
import pytest
import time

from pydodo import (
    async_change_altitude,
    async_change_heading,
    async_change_speed,
    async_change_vertical_speed,
    batch,
    reset_simulation,
    create_aircraft,
    aircraft_position,
)
from pydodo.utils import ping_bluebird

# test if can connect to BlueBird
bb_resp = ping_bluebird()


@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_bluesky_response():
    """Test that bluesky is running and responding before any other tests are run"""
    resp = reset_simulation()
    assert resp == True


@pytest.mark.skipif(
    os.environ.get("TRAVIS") == "true", reason="Skipping this test on Travis CI"
)
@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_async_request():
    """
    Tests async_request() function
    """
    resp = reset_simulation()
    assert resp == True

    aircraft_id = "TST1001"
    type = "B744"
    latitude = 0
    longitude = 0
    heading = 0
    flight_level = 250
    speed = 200
    vertical_speed = 0

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

    position = aircraft_position(aircraft_id)
    aircraft_id = aircraft_id.upper()
    assert position.loc[aircraft_id]["altitude"] == flight_level * 100
    assert position.loc[aircraft_id]["longitude"] == 0

    commands = []
    new_flight_level = 400
    new_heading = 90
    new_speed = 400
    new_vertical_speed = 1
    commands.append(
        async_change_altitude(aircraft_id=aircraft_id, flight_level=new_flight_level)
    )
    commands.append(async_change_heading(aircraft_id=aircraft_id, heading=new_heading))
    commands.append(async_change_speed(aircraft_id=aircraft_id, speed=new_speed))
    commands.append(
        async_change_vertical_speed(
            aircraft_id=aircraft_id, vertical_speed=new_vertical_speed
        )
    )

    results = batch(commands)

    assert results == True

    time.sleep(1)

    new_position = aircraft_position(aircraft_id)
    assert new_position.loc[aircraft_id]["altitude"] > flight_level * 100
    assert new_position.loc[aircraft_id]["longitude"] > 0

    # send more commands - return to original values
    more_commands = []
    more_commands.append(
        async_change_altitude(aircraft_id=aircraft_id, flight_level=flight_level)
    )
    more_commands.append(async_change_heading(aircraft_id=aircraft_id, heading=heading))
    more_commands.append(async_change_speed(aircraft_id=aircraft_id, speed=speed))

    results = batch(more_commands)

    assert results == True

    # send an invalid and a valid command
    commands_wrong = []
    commands_wrong.append(async_change_speed(aircraft_id=aircraft_id, speed=-5))
    commands_wrong.append(
        async_change_vertical_speed(aircraft_id=aircraft_id, vertical_speed=-5)
    )

    with pytest.raises(Exception):
        results = batch(commands_wrong)
