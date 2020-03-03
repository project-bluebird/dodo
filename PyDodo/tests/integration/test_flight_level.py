import pytest

from pydodo import reset_simulation
from pydodo import current_flight_level, cleared_flight_level, requested_flight_level
from pydodo.bluebird_connect import ping_bluebird

bb_resp = ping_bluebird()


@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_flight_level():
    cmd = reset_simulation()
    assert cmd == True

    # resp = load_scenario("scenario/8.SCN")
    # assert resp == True
    #
    # assert current_flight_level("SCN1001") == 6096
    # assert cleared_flight_level("SCN1001") == 6096
    # assert requested_flight_level("SCN1001") == None
    #
    # assert current_flight_level("SCN1005") == 2438
    # assert cleared_flight_level("SCN1005") == 2438
    # assert requested_flight_level("SCN1005") == None
