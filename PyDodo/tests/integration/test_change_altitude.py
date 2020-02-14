import pytest
import time

from pydodo import (
    change_altitude,
    reset_simulation,
    all_positions,
    simulation_step,
)
from pydodo.bluebird_connect import ping_bluebird

# test if can connect to BlueBird
bb_resp = ping_bluebird()


@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_change_altitude(upload_test_sector_scenario):

    cmd = reset_simulation()
    assert cmd == True

    upload_test_sector_scenario()

    # Get the position
    position = all_positions()
    acid1, acid2 = position.index

    # Give the command to descend.
    new_flight_level = 100
    cmd = change_altitude(aircraft_id=acid1, flight_level=new_flight_level)
    assert cmd == True

    # Check that the new altitude is below the original one.
    resp = simulation_step()
    assert resp == True

    new_position = all_positions()
    assert new_position.loc[acid1, "current_flight_level"] < position.loc[acid1, "current_flight_level"]
