"""
Test change_altitude function raises exception if valid inputs are used
"""

import pytest

from pydodo.change_altitude import change_altitude
from pydodo.change_heading import change_heading
from pydodo.change_speed import change_speed
from pydodo.change_vertical_speed import change_vertical_speed

@pytest.mark.parametrize(
    "aircraft_id,altitude,flight_level,vertical_speed",
    [('TST1001', 6000, 60, None),
    ('TST1001', None, 250, -5),
    ('', 250, None, None)]
    )
def test_change_altitude(aircraft_id, altitude, flight_level, vertical_speed):
    with pytest.raises(AssertionError):
        change_altitude(aircraft_id, altitude, flight_level, vertical_speed)

@pytest.mark.parametrize(
    "aircraft_id,heading",
    [('TST1001', -1),
    ('TST1001', 360),
    ('', 0)]
    )
def test_change_heading(aircraft_id, heading):
    with pytest.raises(AssertionError):
        change_heading(aircraft_id, heading)

@pytest.mark.parametrize(
    "aircraft_id,speed",
    [('TST1001', -1),
    ('', 0)]
    )
def test_change_speed(aircraft_id, speed):
    with pytest.raises(AssertionError):
        change_speed(aircraft_id, speed)

@pytest.mark.parametrize(
    "aircraft_id,vertical_speed",
    [('TST1001', -1),
    ('', 0)]
    )
def test_change_vertical_speed(aircraft_id, vertical_speed):
    with pytest.raises(AssertionError):
        change_vertical_speed(aircraft_id, vertical_speed)
