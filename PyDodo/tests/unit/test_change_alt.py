"""
Test change_altitude function raises exception if valid inputs are used
"""

import pytest

from pydodo.change_altitude import change_altitude

@pytest.mark.parametrize(
    "aircraft_id,altitude,flight_level,vertical_speed",
    [('TST1001', 6000, 60, None),
    ('TST1001', None, 250, -5),
    ('', 250, None, None)]
    )
def test_change_altitude(aircraft_id, altitude, flight_level, vertical_speed):
    with pytest.raises(AssertionError):
        change_altitude(aircraft_id, altitude, flight_level, vertical_speed)
