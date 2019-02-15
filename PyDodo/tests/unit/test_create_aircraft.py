"""
Test create_aircraft function raises error if incorrect inputs are provided.

Function returns True if valid inputs are used and connection to bluebird exists.
"""

import pytest
import numpy as np

from pydodo.create_aircraft import create_aircraft
from pydodo.utils import ping_bluebird

# Valid input parameter values
aircraft_id = "TST1001"
type = "B744"
latitude = 0
longitude = 0
heading = 0
altitude = np.nan
flight_level = 250
speed = 200

bb_resp = ping_bluebird()
@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_output_create_aircraft():
    """
    For valid inputs, check function returns True (if can connect to bluebird)
    """
    output = create_aircraft(aircraft_id, type, latitude, longitude,
                             heading, altitude, flight_level, speed)
    assert output == True

@pytest.mark.parametrize(
    "acid,tp",
    [("", "B744"), ("TST1001", "")]
)
def test_input_aircraft_info(acid, tp):
    """
    Check incorrect aircraft_id and type inputs raise error
    """
    with pytest.raises(AssertionError):
        create_aircraft(acid, tp, latitude, longitude,
                        heading, altitude, flight_level, speed)

@pytest.mark.parametrize("lat", [91, -90.1])
def test_input_latitude(lat):
    """
    Check incorrect latitude inputs raise error
    """
    with pytest.raises(AssertionError):
        create_aircraft(aircraft_id, type, lat, longitude,
                        heading, altitude, flight_level, speed)

@pytest.mark.parametrize("lon", [180, -180.1])
def test_input_longitude(lon):
    """
    Check incorrect longitude inputs raise error
    """
    with pytest.raises(AssertionError):
        create_aircraft(aircraft_id, type, latitude, lon,
                        heading, altitude, flight_level, speed)

@pytest.mark.parametrize("hdg", [-0.1, 360])
def test_input_heading(hdg):
    """
    Check incorrect heading inputs raise error
    """
    with pytest.raises(AssertionError):
        create_aircraft(aircraft_id, type, latitude, longitude,
                        hdg, altitude, flight_level, speed)

@pytest.mark.parametrize(
    "alt,fl",
    [(6000,250), (6001, np.nan), (np.nan, 59)]
    )
def test_input_alt_fl(alt, fl):
    """
    Check incorrect combination of altitude and flight level inputs raise error
    """
    with pytest.raises(AssertionError):
        create_aircraft(aircraft_id, type, latitude, longitude,
                        heading, alt, fl, speed)

@pytest.mark.parametrize("spd", [-0.1])
def test_input_speed(spd):
    """
    Check incorrect speed inputs raise error
    """
    with pytest.raises(AssertionError):
        create_aircraft(aircraft_id, type, latitude, longitude,
                        heading, altitude, flight_level, spd)
