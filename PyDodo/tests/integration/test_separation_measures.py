import pytest
import math
import pyproj
import pandas as pd
from scipy.spatial.distance import euclidean

from pydodo import (
    aircraft_position,
    all_positions,
    reset_simulation,
    create_aircraft,
    geodesic_separation,
    great_circle_separation,
    vertical_separation,
    euclidean_separation
)
from pydodo.utils import ping_bluebird

bb_resp = ping_bluebird()

# TWO EXAMPLE AIRCRAFT
aircraft_id = "TST1001"
type = "B744"
latitude = 51.507389
longitude = 0.127806
heading = 0
flight_level = 250
speed = 0

aircraft_id_2 = "TST2002"
type_2 = "C744"
latitude_2 = 50.6083
longitude_2 = -1.9608
heading_2 = 0
flight_level_2 = 200
speed_2 = 0

SCALE_FEET_TO_METRES = 0.3048


@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_separation(expected_great_circle):
    """
    Tests that all separation functions return a dataframe using a variety of inputs.
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

    pos1 = geodesic_separation(from_aircraft_id = [aircraft_id, aircraft_id_2], to_aircraft_id = [aircraft_id, aircraft_id_2])
    assert isinstance(pos1, pd.DataFrame)
    assert pos1.loc[aircraft_id, aircraft_id_2] == pytest.approx(1000*176.92, 0.01)

    pos2 = great_circle_separation(from_aircraft_id = [aircraft_id, aircraft_id_2], to_aircraft_id = aircraft_id)
    assert isinstance(pos2, pd.DataFrame)
    expected = expected_great_circle(latitude, longitude, latitude_2, longitude_2)
    assert pos2.loc[aircraft_id_2, aircraft_id] == pytest.approx(expected, 0.01)

    pos3 = vertical_separation(from_aircraft_id = aircraft_id, to_aircraft_id = [aircraft_id, aircraft_id_2])
    assert isinstance(pos3, pd.DataFrame)
    ## altitude is provided as flight_level, which must be converted to:
    # feet (*100) and then to metres (*0.3048)
    assert pos3.loc[aircraft_id, aircraft_id_2] == abs(flight_level - flight_level_2)*100*SCALE_FEET_TO_METRES

    pos4 = euclidean_separation(from_aircraft_id = aircraft_id, to_aircraft_id = aircraft_id_2)
    assert isinstance(pos4, pd.DataFrame)

    ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
    lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')

    from_ECEF = pyproj.transform(lla, ecef, longitude, latitude, flight_level*100*SCALE_FEET_TO_METRES)
    to_ECEF = pyproj.transform(lla, ecef, longitude_2, latitude_2, flight_level_2*100*SCALE_FEET_TO_METRES)

    assert pos4.loc[aircraft_id, aircraft_id_2] == pytest.approx(euclidean(from_ECEF, to_ECEF), 0.01)
