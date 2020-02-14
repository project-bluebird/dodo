import os
import pytest
import time

from pydodo import (
    async_change_altitude,
    async_change_heading,
    async_change_speed,
    batch,
    reset_simulation,
    all_positions,
    simulation_step
)
from pydodo.bluebird_connect import ping_bluebird

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
def test_async_request(upload_test_sector_scenario):
    """
    Tests async_request() function
    """

    cmd = reset_simulation()
    assert cmd == True

    upload_test_sector_scenario()

    # Get the position
    position = all_positions()
    acid1, acid2 = position.index

    commands = []
    commands.append(
        async_change_altitude(aircraft_id=acid1, flight_level=100)
    )
    commands.append(async_change_heading(aircraft_id=acid1, heading=90))

    results = batch(commands)

    assert results == True

    resp = simulation_step()
    assert resp == True

    new_position = all_positions()
    assert new_position.loc[acid1, "current_flight_level"] < position.loc[acid1, "current_flight_level"]
    assert new_position.loc[acid1, "longitude"] > position.loc[acid1, "longitude"]

    # send more commands - return to original values
    more_commands = []
    more_commands.append(
        async_change_altitude(aircraft_id=acid1, flight_level=400)
    )
    more_commands.append(async_change_speed(aircraft_id=acid1, speed=100))

    results = batch(more_commands)

    assert results == True

    # send an invalid and a valid command
    commands_wrong = []
    commands_wrong.append(async_change_heading(aircraft_id=acid1, heading=0))
    commands_wrong.append(async_change_speed(aircraft_id=acid1, speed=-5))

    with pytest.raises(Exception):
        results = batch(commands_wrong)
