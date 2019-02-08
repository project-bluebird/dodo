import requests
import json

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
    key_map = {
        "alt": "altitude",
        "gs": "ground_speed",
        "lat": "latitude",
        "lon": "longitude",
        "vs": "vertical_speed"
        }
    data = {
        key_map[key]: aircraft_pos[key]
        for key in aircraft_pos.keys()
        if key in key_map.keys()
        }
    return data

def get_pos_request(aircraft_id):
    """
    Get position dictionary for aircraft_id from bluebird. Bluebird accepts
    either single aircraft_id or 'all'. Return NULL if aircraft_id doesn't exist.
    """
    endpoint="pos"
    url = construct_endpoint_url(endpoint)
    resp = requests.get(url, json={"acid": aircraft_id})

    if resp.status_code == 200:
        json_data = json.loads(resp.text)
        if aircraft_id == 'all':
            pos_data = {key:format_output(json_data[key]) for key in json_data.keys()}
        else:
            pos_data = {aircraft_id:format_output(json_data)}
        return pos_data
    return {aircraft_id: None}

def aircraft_position(aircraft_id="all"):
    """
    Get position of aircraft,  all or by aircraft_id.

    :param aircraft_id: str or vector of str of aircraft IDs
    :return: list of aircraft position dictionaries, one for each aircraft_id
    """
    assert _check_aircraft_id(aircraft_id), 'Invalid input {} for aircraft id'.format(aircraft_id)

    if type(aircraft_id) == list:
        aircraft_positions = [get_pos_request(id) for id in aircraft_id_list]
    else:
        aircraft_positions = [get_pos_request(aircraft_id)]
    return aircraft_positions
