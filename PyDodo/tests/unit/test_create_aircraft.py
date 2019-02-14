
import pytest
import numpy as np
from pydodo.create_aircraft import create_aircraft

# aircraft ID and type stay the same
aircraft_id = "TST1001"
type = "B744"

@pytest.mark.parametrize("latitude", [91, -90.1])
def test_input_latitude(latitude):
    """
    Check incorrect latitude inputs raise error
    """
    longitude = 0
    heading = 0
    altitude = np.nan
    flight_level = "FL250"
    speed = 200

    with pytest.raises(AssertionError):
        create_aircraft(aircraft_id, type, latitude, longitude,
                          heading, altitude, flight_level, speed)

@pytest.mark.parametrize("longitude", [180, -180.1])
def test_input_longitude(longitude):
    """
    Check incorrect longitude inputs raise error
    """
    latitude = 0
    heading = 0
    altitude = np.nan
    flight_level = "FL250"
    speed = 200

    with pytest.raises(AssertionError):
        create_aircraft(aircraft_id, type, latitude, longitude,
                          heading, altitude, flight_level, speed)

@pytest.mark.parametrize("heading", [-0.1, 360])
def test_input_heading(heading):
    """
    Check incorrect heading inputs raise error
    """
    longitude = 0
    latitude = 0
    altitude = np.nan
    flight_level = "FL250"
    speed = 200

    with pytest.raises(AssertionError):
        create_aircraft(aircraft_id, type, latitude, longitude,
                          heading, altitude, flight_level, speed)

@pytest.mark.parametrize(
    "altitude,flight_level",
    [(6000,"FL250"), (6001, np.nan), (np.nan, "FL59")]
    )
def test_input_alt_fl(altitude, flight_level):
    """
    Check incorrect combination of altitude and flight level inputs raise error
    """
    longitude = 0
    latitude = 0
    heading = 0
    speed = 200

    with pytest.raises(AssertionError):
        create_aircraft(aircraft_id, type, latitude, longitude,
                          heading, altitude, flight_level, speed)

@pytest.mark.parametrize("speed", [-0.1])
def test_input_speed(speed):
    """
    Check incorrect speed inputs raise error
    """
    longitude = 0
    latitude = 0
    heading = 0
    altitude = np.nan
    flight_level = "FL250"

    with pytest.raises(AssertionError):
        create_aircraft(aircraft_id, type, latitude, longitude,
                          heading, altitude, flight_level, speed)
