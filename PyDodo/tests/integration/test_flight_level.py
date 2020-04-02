import pytest

from pydodo import reset_simulation, all_positions
from pydodo import current_flight_level, cleared_flight_level, requested_flight_level
from pydodo.bluebird_connect import ping_bluebird

bb_resp = ping_bluebird()


@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_flight_level(upload_test_sector_scenario):

    cmd = reset_simulation()
    assert cmd == True

    upload_test_sector_scenario()

    # Get the position
    position = all_positions()
    acid1, acid2 = position.index

    assert cleared_flight_level(acid1) == 400
    assert requested_flight_level(acid1) == 400

    # In BlueSky overflier aircraft is inialised below requested flight level
    assert 39995 < current_flight_level(acid1) <= 40000

    assert cleared_flight_level(acid2) == 200
    assert requested_flight_level(acid2) == 400
    assert current_flight_level(acid2) == 20000
