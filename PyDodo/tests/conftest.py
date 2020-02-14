import os
import math
import pytest

import numpy as np

from geopy import distance
from pydodo.config_param import config_param
from pydodo import upload_sector, upload_scenario

major_semiaxis, _, _ = distance.ELLIPSOIDS["WGS-84"]
_EARTH_RADIUS = major_semiaxis * 1000

_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture
def rootdir():
    return _ROOT_DIR


def deg2rad(deg):
    """Convert degrees to radians"""
    return (deg * math.pi) / 180


def great_circle(from_lat, from_lon, to_lat, to_lon):
    """Calculate great circle distance using the Haversine formula"""
    dlat = from_lat - to_lat
    dlon = from_lon - to_lon

    a = (math.sin(deg2rad(dlat) / 2)) ** 2 + math.cos(deg2rad(from_lat)) * math.cos(
        deg2rad(to_lat)
    ) * (math.sin(deg2rad(dlon) / 2)) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    expected = _EARTH_RADIUS * c
    return expected


@pytest.fixture
def expected_great_circle():
    return great_circle


@pytest.fixture
def earth_radius():
    return _EARTH_RADIUS


def test_sector_scenario():
    test_scenario_file = os.path.join(_ROOT_DIR, "dodo-test-scenario")
    test_sector_file = os.path.join(_ROOT_DIR, "dodo-test-sector")
    upload_sector(filename=f"{test_sector_file}.geojson",sector_name="test_sector")
    upload_scenario(filename=f"{test_scenario_file}.json",scenario_name="test_scenario")


@pytest.fixture
def upload_test_sector_scenario():
    return test_sector_scenario
