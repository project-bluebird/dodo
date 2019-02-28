"""
Test aircraft_position and all_positions functions:
    - raise error if invalid aircraft_id is used
    - output a dataframe
"""

import pytest
from unittest.mock import patch
import pandas as pd
import requests
import json

from pydodo import aircraft_position, all_positions
from pydodo.utils import ping_bluebird, construct_endpoint_url

from requests.exceptions import HTTPError

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

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            self.text = json.dumps(json_data)
            self.raise_for_status = requests.exceptions.HTTPError

    if kwargs['params']["acid"] == 'all':
        return MockResponse(
            {"TEST1":{"_validTo": "Mon, 25 Feb 2019 17:35:07 GMT", "lat":55.945336, "lon":-3.187299, "hdg":123.45, "alt":7620,  "gs":250.25, "vs":0}}
            , 200)
    elif kwargs['params']["acid"] == 'TEST1':
        # return dictionary
        return MockResponse({"_validTo": "Mon, 25 Feb 2019 17:35:07 GMT","lat":55.945336, "lon":-3.187299, "hdg":123.45, "alt":7620,  "gs":250.25, "vs":0}, 200)

    return MockResponse(None, 404)

@patch('requests.get', side_effect=mocked_requests_get)
def test_output_format(mock_get):
    """
    Check request output is formatted correctly
    """
    output = pd.DataFrame.from_dict({"TEST1":{"altitude":7620,  "ground_speed":250.25, "latitude":55.945336, "longitude":-3.187299,  "vertical_speed":0}}, orient='index')

    json_data_all = all_positions()
    assert json_data_all.equals(output)
#
    json_data_id = aircraft_position("TEST1")
    assert json_data_id.equals(output)

# @patch('requests.get', side_effect=mocked_requests_get)
# def test_id_not_found(mock_get):
#     """
#     If get 404 on all entered aircraft_id, raise error
#     """
#     with pytest.raises(AssertionError):
#         aircraft_position("123")
