import pytest
from unittest.mock import patch
import pandas as pd
import requests
import json
from requests.exceptions import HTTPError

from pydodo import aircraft_position, all_positions, config_param
from pydodo.bluebird_connect import ping_bluebird, construct_endpoint_url


@pytest.mark.parametrize("aircraft_id", [123, "", [], ["TEST", 123]])
def test_input_aircraft_id(aircraft_id):
    """
    Check incorrectly formatted aircraft_id raises error
    """
    with pytest.raises(AssertionError):
        aircraft_position(aircraft_id)


type = "B744"
latitude = 55.945336
longitude = -3.187299
heading = 123.45
altitude = 76.2
speed = 250.25
vertical_speed = 0


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            self.text = json.dumps(json_data)
            self.raise_for_status = requests.exceptions.HTTPError

    if not "params" in kwargs.keys() or kwargs["params"][config_param("query_aircraft_id")] == "TEST1":
        return MockResponse(
            {
                "TEST1": {
                    "actype": type,
                    "current_fl": altitude,
                    "gs": speed,
                    "lat": latitude,
                    "lon": longitude,
                    "vs": vertical_speed,
                    "requested_fl": None,
                    "cleared_fl": None
                },
                "scenario_time": 0,
            },
            200,
        )

    return MockResponse(None, 404)


@patch("requests.get", side_effect=mocked_requests_get)
def test_output_format(mock_get):
    """
    Check request output is formatted correctly.
    """
    output = pd.DataFrame.from_dict(
        {
            "TEST1": {
                "aircraft_type": type,
                "current_flight_level": altitude,
                "ground_speed": speed,
                "latitude": latitude,
                "longitude": longitude,
                "vertical_speed": vertical_speed,
                "requested_flight_level": None,
                "cleared_flight_level": None
            },
        },
        orient="index",
    )
    output.sim_t = 0

    pos_all = all_positions()
    assert pos_all.equals(output)

    pos_id = aircraft_position("TEST1")
    assert pos_id.equals(output)
