"""
Get position information for a single or all aircrafts currently in the simulation.

Return requested aircraft position(s) as pandas dataframe. Rows are NULL if aircraft ID does not exist.
"""

import requests
import json
import numpy as np
import pandas as pd

from . import settings
from .utils import construct_endpoint_url

endpoint = settings.default['endpoint_aircraft_position']

def _check_aircraft_id(aircraft_id):
    """Check that aircraft_id is a non-empty string"""
    if type(aircraft_id) == str:
        return len(aircraft_id) >= 1
    return False

def format_output(aircraft_pos):
    """
    Format aircraft position dictionary returned by bluebird.
    """
    position_formatted = {
        "altitude":aircraft_pos["alt"],
        "ground_speed":aircraft_pos["gs"],
        "latitude":aircraft_pos["lat"],
        "longitude":aircraft_pos["lon"],
        "vertical_speed":aircraft_pos["vs"]
    }
    return position_formatted

def get_all_request():
    """
    Get position dictionary for all aircraft.
    """
    url = construct_endpoint_url(endpoint)
    resp = requests.get(url, params={"acid": "all"})
    if resp.status_code == 200:
        json_data = json.loads(resp.text)
        pos_data = {aircraft:format_output(json_data[aircraft]) for aircraft in json_data.keys()}
        pos_dict = pd.DataFrame.from_dict(pos_data, orient='index')
        return pos_dict
    else:
        # TO DO: CHANGE WHAT IS RETURNED
        return resp.status_code

def get_pos_request(aircraft_id):
    """
    Get position dictionary for aircraft_id.

    :param aircraft_id :
    :return : dataframe with position data or NULL if aircraft_id does not exist
    """
    url = construct_endpoint_url(endpoint)
    resp = requests.get(url, params={"acid": aircraft_id})
    if resp.status_code == 200:
        json_data = json.loads(resp.text)
        pos_data = {aircraft_id:format_output(json_data)}
        pos_dict = pd.DataFrame.from_dict(pos_data, orient='index')
        return pos_dict
    elif resp.status_code == 404: #aircraft_id NOT FOUND
        return pd.DataFrame({
            "altitude":np.nan,
            "ground_speed":np.nan,
            "latitude":np.nan,
            "longitude":np.nan,
            "vertical_speed":np.nan
            }, index=[aircraft_id])
    else:
        # TO DO: CHANGE WHAT IS RETURNED
        return resp.status_code

def aircraft_position(aircraft_id="all"):
    """
    Get position of aircraft, all or by aircraft_id.

    :param aircraft_id: 'all' or single aircraft ID
    :return: dataframe with aircraft positions, row for each aircraft_id
    """
    assert _check_aircraft_id(aircraft_id), 'Invalid input {} for aircraft id'.format(aircraft_id)

    if aircraft_id == 'all':
        aircraft_positions = get_all_request()
    else:
        aircraft_positions = get_pos_request(aircraft_id)
    return aircraft_positions
