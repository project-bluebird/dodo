"""
Get position information for a single or multiple aircrafts. Can request specific aircraft ID or all aircrafts in the simulation.

Return requested aircraft positions as pandas dataframe. Rows are NULL if aircraft ID does not exist.
"""

import requests
import json
import numpy as np
import pandas as pd

from .utils import construct_endpoint_url

def _check_aircraft_id(aircraft_id):
    """Check that aircraft_id is a string or a list of strings."""
    try:
        return bool(aircraft_id) and all(isinstance(elem, str) and len(elem) >= 3 for elem in aircraft_id)
    except:
        return False

def format_output(aircraft_pos):
    """
    Format aircraft position dictionary returned by bluebird.
    """
    position_formatted = {
        "acid":aircraft_pos["acid"],
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
    endpoint="pos"
    url = construct_endpoint_url(endpoint)
    resp = requests.get(url, json={"acid": "all"})
    if resp.status_code == 200:
        json_data = json.loads(resp.text)
        pos_data = {aircraft["acid"]:format_output(aircraft) for aircraft in json_data}
        pos_dict = pd.DataFrame.from_dict(pos_data, orient='index')
        return pos_dict
    return False

def get_pos_request(aircraft_id):
    """
    Get position dictionary for aircraft_id.

    :param aircraft_id :
    :return : dictionary with position data or NULL if aircraft_id does not exist
    """
    endpoint="pos"
    url = construct_endpoint_url(endpoint)
    resp = requests.get(url, json={"acid": aircraft_id})
    if resp.status_code == 200:
        json_data = json.loads(resp.text)
        pos_data = {aircraft_id:format_output(json_data)}
        pos_dict = pd.DataFrame.from_dict(pos_data, orient='index')
        return pos_dict
    # elif resp.status_code == 404:
    else:
        return pd.DataFrame({
            "acid":aircraft_id,
            "altitude":np.nan,
            "ground_speed":np.nan,
            "latitude":np.nan,
            "longitude":np.nan,
            "vertical_speed":np.nan
            }, index=[aircraft_id])

def aircraft_position(aircraft_id="all"):
    """
    Get position of aircraft, all or by aircraft_id.

    :param aircraft_id: 'all', single aircraft ID or list of aircraft IDs
    :return: list of aircraft position dictionaries, one for each aircraft_id
    """
    assert _check_aircraft_id(aircraft_id), 'Invalid input {} for aircraft id, must be string with at least three characters'.format(aircraft_id)

    if aircraft_id == 'all':
        aircraft_positions = get_all_request()
    elif type(aircraft_id) == list:
        aircraft_positions = pd.concat([get_pos_request(id) for id in aircraft_id])
    else:
        aircraft_positions = get_pos_request(aircraft_id)
    return aircraft_positions
