"""
- Incorrect aircraft_id inputs raise error
- Output is a dataframe
"""

import pytest
from unittest.mock import patch
import pandas as pd
import requests
import json

from pydodo.aircraft_position import aircraft_position, get_pos_request, get_all_request
from pydodo.utils import ping_bluebird
from pydodo.utils import construct_endpoint_url

@pytest.mark.parametrize(
    "aircraft_id",
    [123, "", [], ["TEST"]]
    )
def test_input_aircraft_id(aircraft_id):
    """
    Check incorrectly formatted aircraft_id raises error
    """
    with pytest.raises(AssertionError):
        aircraft_position(aircraft_id)

def test_request_format():
    """
    Check aircraft_position sends request in correct format
    """
    with patch.object(requests, 'get') as mock_get:
        url = construct_endpoint_url("pos")

        aircraft_position()
        mock_get.assert_called_with(url, params={"acid":"all"})

        aircraft_position('all')
        mock_get.assert_called_with(url, params={"acid":"all"})

        aircraft_position('TEST1')
        mock_get.assert_called_with(url, params={"acid":"TEST1"})

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            self.text = json.dumps(json_data)

    if kwargs['params']["acid"] == 'all':
        return MockResponse(
            {"TEST1":{"_validTo": "Mon, 25 Feb 2019 17:35:07 GMT", "lat":55.945336, "lon":-3.187299, "hdg":123.45, "alt":7620,  "gs":250.25, "vs":0}}
            , 200)
    elif kwargs['params']["acid"] == 'TEST1':
        # return dictionary
        return MockResponse({"_validTo": "Mon, 25 Feb 2019 17:35:07 GMT","lat":55.945336, "lon":-3.187299, "hdg":123.45, "alt":7620,  "gs":250.25, "vs":0}, 200)

    return MockResponse(None, 404)


## CHECK FORMATTING FOR WHEN NOTHING IS RETURNED OR WHEN AN ERROR IS RAISED
@patch('requests.get', side_effect=mocked_requests_get)
def test_output_format(mock_get):
    """
    Check request output is formatted correctly
    """
    output = pd.DataFrame.from_dict({"TEST1":{"altitude":7620,  "ground_speed":250.25, "latitude":55.945336, "longitude":-3.187299,  "vertical_speed":0}}, orient='index')

    json_data = get_all_request()
    assert json_data.equals(output)

    json_data_2 = get_pos_request("TEST1")
    assert json_data_2.equals(output)
