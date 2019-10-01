import pytest

from pydodo import (
    aircraft_position,
    all_positions,
    reset_simulation,
    create_aircraft,
    loss_of_separation
)
from pydodo.utils import ping_bluebird

bb_resp = ping_bluebird()

aircraft_id = "TST1001"
type = "B744"
latitude = 51
longitude = 0
heading = 0
flight_level = 250
speed = 0

aircraft_id_2 = "TST2002"
type_2 = "C744"
latitude_2 = 50
longitude_2 = -1
heading_2 = 0
flight_level_2 = 200
speed_2 = 0


@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_loss_of_separation():
    """
    Tests loss_of_separation returns correct separation score.
    """
    cmd = reset_simulation()
    assert cmd == True

    cmd = create_aircraft(aircraft_id = aircraft_id,
                          type = type,
                          latitude = latitude,
                          longitude = longitude,
                          heading = heading,
                          flight_level = flight_level,
                          speed = speed)
    assert cmd == True

    cmd = create_aircraft(aircraft_id = aircraft_id_2,
                          type = type_2,
                          latitude = latitude_2,
                          longitude = longitude_2,
                          heading = heading_2,
                          flight_level = flight_level_2,
                          speed = speed_2)
    assert cmd == True

    score1 = loss_of_separation(aircraft_id, aircraft_id_2)
    assert score1 == 0

    score2 = loss_of_separation(aircraft_id, aircraft_id)
    assert score2 == -1

    score3 = loss_of_separation(aircraft_id_2, aircraft_id_2)
    assert score3 == -1
