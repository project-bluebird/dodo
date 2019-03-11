
import requests
import json
import numpy as np
import pandas as pd

from .config_param import config_param
from . import utils

endpoint = config_param('endpoint_aircraft_position')
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


def normalise_positions_units(df):
    """Normalise units of measurement in the positions data."""
    SCALE_METRES_TO_FEET = 3.280839895

    # Bluesky returns altitude in metres, not feet.
    if config_param('simulator') == config_param("bluesky_simulator"):
        df.loc[:, "altitude"] = SCALE_METRES_TO_FEET * df["altitude"]
        df.loc[:, "altitude"] = df["altitude"].round(2)
    return df


def null_pos_df(aircraft_id=None):
    """
    Returns empty dataframe if no ID is provided otherwise dataframe with NAN.
    """
    if aircraft_id == None:
        df = pd.DataFrame({
            "altitude":[],
            "ground_speed":[],
            "latitude":[],
            "longitude":[],
            "vertical_speed":[]
            })
    else:
        df = pd.DataFrame({
            "altitude":np.nan,
            "ground_speed":np.nan,
            "latitude":np.nan,
            "longitude":np.nan,
            "vertical_speed":np.nan
            }, index=[aircraft_id])
    return df


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
    elif resp.status_code == config_param('status_code_aircraft_id_not_found'):
        return null_pos_df(aircraft_id)
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
            pos_df = get_position(aircraft_id)
        elif type(aircraft_id) == list:
            assert utils._check_id_list(aircraft_id), 'Invalid input {} for aircraft id'.format(aircraft_id)
            pos_df = pd.concat([get_position(id) for id in aircraft_id])
        else:
            raise AssertionError("Invalid input {} for aircraft id".format(aircraft_id))

        #assert not pos_df.isnull().all().all(), 'None of the {} aircraft IDs were found'.format(aircraft_id)
        return normalise_positions_units(pos_df)


def all_positions():
    """
    Get dataframe with position information for all aircraft in simulation.
    """
    resp = requests.get(url, params={"acid": "all"})

    # if response other than 200, raise
    resp.raise_for_status()

    json_data = json.loads(resp.text)
    if json_data != {}:
        pos_data = {aircraft:format_output(json_data[aircraft]) for aircraft in json_data.keys()}
        pos_df = pd.DataFrame.from_dict(pos_data, orient='index')
    else:
        pos_df = null_pos_df()
    return normalise_positions_units(pos_df)
