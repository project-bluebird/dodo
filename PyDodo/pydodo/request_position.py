
import requests
import json
import numpy as np
import pandas as pd

from .config_param import config_param
from . import utils

endpoint = config_param("endpoint_aircraft_position")
url = utils.construct_endpoint_url(endpoint)


def format_pos_output(aircraft_pos):
    """
    Format position dictionary for an aircraft returned by bluebird.
    """
    position_formatted = {
        "altitude": aircraft_pos["alt"],
        "ground_speed": aircraft_pos["gs"],
        "latitude": aircraft_pos["lat"],
        "longitude": aircraft_pos["lon"],
        "vertical_speed": aircraft_pos["vs"],
    }
    return position_formatted


def process_response(response):
    """
    Process response from POS request.
    """
    json_data = json.loads(response.text)
    pos_dict = {
        aircraft: format_pos_output(json_data[aircraft])
        for aircraft in json_data.keys()
        if aircraft != 'sim_t'
    }
    pos_df = pd.DataFrame.from_dict(pos_dict, orient="index")
    pos_df.sim_t = json_data['sim_t']
    return pos_df


def normalise_positions_units(df):
    """Normalise units of measurement in the positions data."""
    SCALE_METRES_TO_FEET = 3.280839895

    # Bluesky returns altitude in metres, not feet.
    if config_param("simulator") == config_param("bluesky_simulator"):
        df.loc[:, "altitude"] = SCALE_METRES_TO_FEET * df["altitude"]
        df.loc[:, "altitude"] = df["altitude"].round(2)
    return df


def null_pos_df(aircraft_id=None):
    """
    Returns empty dataframe if no ID is provided otherwise dataframe with NANs.
    """

    if aircraft_id == None:
        df = pd.DataFrame(
            {
                "altitude": [],
                "ground_speed": [],
                "latitude": [],
                "longitude": [],
                "vertical_speed": [],
            }
        )
    else:
        df = pd.DataFrame(
            {
                "altitude": np.nan,
                "ground_speed": np.nan,
                "latitude": np.nan,
                "longitude": np.nan,
                "vertical_speed": np.nan,
            },
            index=[aircraft_id],
        )
    return df


def all_positions():
    """
    Get dataframe with position information for all aircraft in simulation.

    Returns NULL dataframe if no aircraft found in simulation.
    """
    resp = requests.get(url, params={config_param("query_aircraft_id"): "all"})
    if resp.status_code == 200:
        pos_df = process_response(resp)
        return normalise_positions_units(pos_df)
    elif resp.status_code == config_param("status_code_no_aircraft_found"):
        return null_pos_df()
    else:
        raise requests.HTTPError(resp.text)


def get_position(aircraft_id):
    """
    Get position dataframe for single aircraft_id.
    """
    resp = requests.get(url, params={config_param("query_aircraft_id"): aircraft_id})
    if resp.status_code == 200:
        return process_response(resp)
    elif resp.status_code == config_param("status_code_aircraft_id_not_found"):
        return null_pos_df(aircraft_id)
    else:
        raise requests.HTTPError(resp.text)


def aircraft_position(aircraft_id):
    """
    Get position dataframe for aircraft_id.

    :param aircraft_id : string or a list of strings
    :return : dataframe with position data, NaN if aircraft_id does not exist
    """
    if type(aircraft_id) == str:
        utils._check_string_input(aircraft_id, "aircraft_id")
        pos_df = get_position(aircraft_id)
    elif type(aircraft_id) == list:
        utils._check_id_list(aircraft_id)
        all_pos = all_positions()
        pos_df = all_pos.ix(aircraft_id) #filter requested IDs
    else:
        raise AssertionError("Invalid input {} for aircraft id".format(aircraft_id))
    return normalise_positions_units(pos_df)
