import os
import math
import pytest

import numpy as np

from geopy import distance
from pydodo.config_param import config_param

major_semiaxis, _, _FLATTENING = distance.ELLIPSOIDS['WGS-84']
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


def convert_lla_to_ECEF(lat, lon, alt = 0, radius=_EARTH_RADIUS, f=_FLATTENING ):
    """
    Calculates ECEF coordinates of a point from lat, lon and alt.

    :param alt: altitude in metres.
    :param radius: Earth radius in metres (WGS84).
    :param f: ellipsoidal flattening (WGS84).
    :return:
    """
    lat_r = np.deg2rad(lat)
    lon_r = np.deg2rad(lon)

    e2 = 1 - (1 - f) * (1 - f)
    N = radius / np.sqrt(1 - e2 * np.power(np.sin(lat_r), 2))

    x = (N + alt) * np.cos(lat_r) * np.cos(lon_r)
    y = (N + alt) * np.cos(lat_r) * np.sin(lon_r)
    z = ((1-e2) * N + alt) * np.sin(lat_r)

    return (x,y,z)


@pytest.fixture
def expected_great_circle():
    return great_circle


@pytest.fixture
def lla_to_ECEF():
    return convert_lla_to_ECEF


@pytest.fixture
def earth_radius():
    return _EARTH_RADIUS
