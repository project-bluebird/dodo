import pytest
import time

from pydodo import (
    change_heading,
    reset_simulation,
    all_positions,
    simulation_step,
)
from pydodo.bluebird_connect import ping_bluebird

# test if can connect to BlueBird
bb_resp = ping_bluebird()


@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_change_heading(upload_test_sector_scenario):

    cmd = reset_simulation()
    assert cmd == True

    upload_test_sector_scenario()

    # Get the position
    position = all_positions()
    acid1, acid2 = position.index

    # Test with an invalid heading.
    invalid_heading = 400
    with pytest.raises(AssertionError):
        change_heading(aircraft_id=acid1, heading=invalid_heading)

    # Give the command to change heading.
    # Aircraft is originally headed north (0 degrees)
    new_heading = 90
    cmd = change_heading(aircraft_id=acid1, heading=new_heading)
    assert cmd == True

    # Check that the heading has changed.
    resp = simulation_step()
    assert resp == True

    new_position = all_positions()
    assert new_position.loc[acid1, "longitude"] > position.loc[acid1, "longitude"]
