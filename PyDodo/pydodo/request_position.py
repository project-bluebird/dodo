
import requests
import json
import numpy as np
import pandas as pd

from . import settings
from . import utils

endpoint = settings.default['endpoint_aircraft_position']
url = utils.construct_endpoint_url(endpoint)

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

def get_position(aircraft_id):
    """
    Get position dataframe for single aircraft_id.
    """
    resp = requests.get(url, params={"acid": aircraft_id})
    if resp.status_code == 200:
        json_data = json.loads(resp.text)
        pos_data = {aircraft_id:format_output(json_data)}
        pos_dict = pd.DataFrame.from_dict(pos_data, orient='index')
        return pos_dict
    elif resp.status_code == settings.default['status_code_aircraft_id_not_found']:
        return pd.DataFrame({
            "altitude":np.nan,
            "ground_speed":np.nan,
            "latitude":np.nan,
            "longitude":np.nan,
            "vertical_speed":np.nan
            }, index=[aircraft_id])
    else:
        raise requests.HTTPError(resp.text)

def aircraft_position(aircraft_id):
        """
        Get position dataframe for aircraft_id.

        :param aircraft_id : string or a list of strings
        :return : dataframe with position data or NULL if aircraft_id does not exist
        """
        if type(aircraft_id) == str:
            assert utils._check_string_input(aircraft_id), 'Invalid input {} for aircraft id'.format(aircraft_id)
            output = get_position(aircraft_id)
        elif type(aircraft_id) == list:
            assert utils._check_id_list(aircraft_id), 'Invalid input {} for aircraft id'.format(aircraft_id)
            output = pd.concat([get_position(id) for id in aircraft_id])
        else:
            raise AssertionError("Invalid input {} for aircraft id".format(aircraft_id))

        #assert not output.isnull().all().all(), 'None of the {} aircraft IDs were found'.format(aircraft_id)
        return output

def all_positions():
    """
    Get dataframe with position information for all aircraft in simulation.
    """
    resp = requests.get(url, params={"acid": "all"})

    # if response other than 200, raise
    resp.raise_for_status()

    json_data = json.loads(resp.text)
    pos_data = {aircraft:format_output(json_data[aircraft]) for aircraft in json_data.keys()}
    pos_dict = pd.DataFrame.from_dict(pos_data, orient='index')
    return pos_dict
