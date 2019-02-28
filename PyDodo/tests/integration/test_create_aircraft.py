"""
Test create_aircraft function:
- returns True if valid inputs are used
- raises error if try to create already existing aircraft (repeat same request twice)
"""

import pytest

from pydodo import create_aircraft, reset_simulation
from pydodo.utils import ping_bluebird

from requests.exceptions import HTTPError

# Valid input parameter values
aircraft_id = "TST1001"
type = "B744"
latitude = 0
longitude = 0
heading = 0
altitude = None
flight_level = 250
speed = 200

# test if can connect to BlueBird
bb_resp = ping_bluebird()

@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_output_create_aircraft():

    # reset so that no aircraft exist
    reset_simulation()

    output = create_aircraft(aircraft_id, type, latitude, longitude,
                             heading, altitude, flight_level, speed)
    assert output == True

    with pytest.raises(HTTPError):
         output = create_aircraft(aircraft_id, type, latitude, longitude,
                                  heading, altitude, flight_level, speed)
