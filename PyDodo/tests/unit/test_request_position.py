import pytest
from unittest.mock import patch
import pandas as pd
import requests
import json
from requests.exceptions import HTTPError

from pydodo import aircraft_position, all_positions
from pydodo.utils import ping_bluebird, construct_endpoint_url


@pytest.mark.parametrize(
    "aircraft_id",
    [123, "", [], ["TEST", 123]]
    )
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

    if kwargs['params']["acid"] == 'all' or kwargs['params']["acid"] == 'TEST1':
        return MockResponse(
            {"TEST1":{"_validTo": "Mon, 25 Feb 2019 17:35:07 GMT", "actype": type, "lat":latitude, "lon":longitude, "hdg":heading, "alt":altitude,  "gs":speed, "vs":vertical_speed}, 'sim_t':0}, 200)

    return MockResponse(None, 404)


@patch('requests.get', side_effect=mocked_requests_get)
def test_output_format(mock_get):
    """
    Check request output is formatted correctly.
    """
    alt = round(altitude*3.280839895, 2)
    output = pd.DataFrame.from_dict({"TEST1":{"type": type, "altitude":alt,  "ground_speed":speed, "latitude":latitude, "longitude":longitude,  "vertical_speed":vertical_speed}}, orient='index')

    json_data_all = all_positions()
    assert json_data_all.equals(output)
#
    json_data_id = aircraft_position("TEST1")
    assert json_data_id.equals(output)
