import os
import math
import pytest

import numpy as np

from geopy import distance
from pydodo.config_param import config_param

major_semiaxis, _, _ = distance.ELLIPSOIDS['WGS-84']
_EARTH_RADIUS = major_semiaxis * 1000


@pytest.fixture
def rootdir():
    return os.path.dirname(os.path.abspath(__file__))


def deg2rad(deg):
    """Convert degrees to radians"""
    return (deg * math.pi) / 180


def great_circle(from_lat, from_lon, to_lat, to_lon):
    """Calculate great circle distance using the Haversine formula"""
    dlat = from_lat - to_lat
    dlon = from_lon - to_lon

    a = (math.sin(deg2rad(dlat)/2))**2 + math.cos(deg2rad(from_lat)) * math.cos(deg2rad(to_lat)) * (math.sin(deg2rad(dlon)/2))**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    expected = _EARTH_RADIUS * c
    return expected


@pytest.fixture
def expected_great_circle():
    return great_circle


@pytest.fixture
def earth_radius():
    return _EARTH_RADIUS
