"""
Get position information for a single or multiple aircrafts. Can request specific aircraft ID or all aircrafts in the simulation.
"""

import requests
import json
import numpy as np

from .utils import construct_endpoint_url

def _check_aircraft_id(aircraft_id):
    """Check that aircraft_id is a string or a list of strings."""
    try:
        return bool(aircraft_id) and all(isinstance(elem, str) for elem in aircraft_id)
    except:
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
    endpoint="pos"
    url = construct_endpoint_url(endpoint)
    resp = requests.get(url, json={"acid": "all"})
    if resp.status_code == 200:
        json_data = json.loads(resp.text)
        pos_data = [{key:format_output(json_data[key])} for key in json_data.keys()]
        return pos_data
    return []

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
        return pos_data
    # elif resp.status_code == 404:
    else:
        return {aircraft_id: np.nan}

def aircraft_position(aircraft_id="all"):
    """
    Get position of aircraft, all or by aircraft_id.

    :param aircraft_id: 'all', single aircraft ID or list of aircraft IDs
    :return: list of aircraft position dictionaries, one for each aircraft_id
    """
    assert _check_aircraft_id(aircraft_id), 'Invalid input {} for aircraft id'.format(aircraft_id)

    if aircraft_id == 'all':
        aircraft_positions = get_all_request()
    elif type(aircraft_id) == list:
        aircraft_positions = [get_pos_request(id) for id in aircraft_id]
    else:
        aircraft_positions = [get_pos_request(aircraft_id)]
    return aircraft_positions
