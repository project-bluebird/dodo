import pytest
from requests.exceptions import HTTPError

from pydodo import create_aircraft, reset_simulation
from pydodo.utils import ping_bluebird

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

    output = create_aircraft(
        aircraft_id, type, latitude, longitude, heading, speed, altitude, flight_level
    )
    assert output == True

    with pytest.raises(HTTPError):
        create_aircraft(
            aircraft_id,
            type,
            latitude,
            longitude,
            heading,
            speed,
            altitude,
            flight_level,
        )
