import requests
import json
import numpy as np
import pandas as pd

from .config_param import config_param
from .utils import construct_endpoint_url
from . import utils

endpoint = config_param("endpoint_aircraft_position")
url = construct_endpoint_url(endpoint)


def format_pos_info(aircraft_pos):
    # TODO: Update docstrings
    """
    Format position dictionary for an aircraft returned by bluebird.

    Parameters
    ----------
    aircraft_pos :

    Returns
    -------
    position_formatted :

    Examples:
    >>> pydodo.request_position.format_pos_info()
    >>>
    """

    position_formatted = {
        "type": aircraft_pos["actype"],
        "altitude": aircraft_pos["alt"],
        "ground_speed": aircraft_pos["gs"],
        "latitude": aircraft_pos["lat"],
        "longitude": aircraft_pos["lon"],
        "vertical_speed": aircraft_pos["vs"],
    }
    return position_formatted


def process_pos_response(response):
    """
    Process response from POS request.

    Parameters
    ----------
    response : JSON <dict>

    Returns
    -------
    pos_df : pandas.DataFrame

    Examples:
    >>> pydodo.request_position.process_pos_response()
    >>>
    """

    json_data = json.loads(response.text)
    pos_dict = {
        aircraft: format_pos_info(json_data[aircraft])
        for aircraft in json_data.keys()
        if aircraft != "sim_t"
    }
    pos_df = pd.DataFrame.from_dict(pos_dict, orient="index")
    pos_df.sim_t = json_data["sim_t"]
    return pos_df


def normalise_positions_units(df):
    # TODO: Update docstrings
    """
    Normalise units of measurement in the positions data.

    Parameters
    ----------
    response : pandas.DataFrame

    Returns
    -------
    pos_df : pandas.DataFrame

    Examples:
    >>> pydodo.request_position.normalise_positions_units()
    >>>
    """

    SCALE_METRES_TO_FEET = 3.280839895

    # Bluesky returns altitude in metres, not feet.
    if config_param("simulator") == config_param("bluesky_simulator"):
        df.loc[:, "altitude"] = SCALE_METRES_TO_FEET * df["altitude"]
        df.loc[:, "altitude"] = df["altitude"].round(2)
    return df


def null_pos_df(aircraft_id=None):
    # TODO: Update docstrings
    """
    Returns empty dataframe if no ID is provided otherwise dataframe with NANs.

    Parameters
    ----------
    aircraft_id : str

    Returns
    -------
    pos_df : pandas.DataFrame

    Examples:
    >>> pydodo.request_position.null_pos_df()
    >>>
    """

    null_dict = {
        "type": [],
        "altitude": [],
        "ground_speed": [],
        "latitude": [],
        "longitude": [],
        "vertical_speed": [],
    }
    if aircraft_id == None:
        return pd.DataFrame(null_dict)
    else:
        nan_dict = {key: np.nan for key in null_dict.keys()}
        return pd.DataFrame(nan_dict, index=[aircraft_id])


def all_positions():
    """
    Get dataframe with position information for all aircraft in simulation.

    Returns NULL dataframe if no aircraft found in simulation.

    Parameters
    ----------
    NONE

    Returns
    -------
    all_pos_df : pandas.DataFrame
        Dataframe indexed by **uppercase** aircraft ID with columns:
    | - ``type``: A string ICAO aircraft type designator.
    | - ``altitude``: A non-negatige double. The aircraft's altitude in feet.
    | - ``ground_speed``: A non-negative double. The aircraft's ground speed in knots.
    | - ``latitude``: A double in the range ``[-90, 90]``. The aircraft's latitude.
    | - ``longitude``: A double in the range ``[-180, 180]``. The aircraft's longitude.
    | - ``vertical_speed``: A double. The aircraft's vertical speed in feet/min (units according to BlueSky docs).

    Notes
    -----
    This dataframe also contains a metadata attribute named `sim_t` containing
    the simulator time in seconds since the start of the scenario.

    If no aircraft exists an empty data frame is returned.

    If the response from Bluebird contains an error status code, an exception is
    thrown.

    Examples:
    >>> pydodo.all_positions()
    >>>
    """

    resp = requests.get(url, params={config_param("query_aircraft_id"): "all"})
    if resp.status_code == 200:
        pos_df = process_pos_response(resp)
        return normalise_positions_units(pos_df)
    elif resp.status_code == config_param("status_code_no_aircraft_found"):
        return null_pos_df()
    else:
        raise requests.HTTPError(resp.text)


def get_position(aircraft_id):
    """
    Get position dataframe for single aircraft_id.

    Parameters
    ----------
    aircraft_id : str
        A string or vector of strings representing one or more aircraft IDs. For
        the BlueSky simulator, each ID must contain at least three characters.

    Returns
    -------
    pos_df : pandas.DataFrame
        Dataframe indexed by **uppercase** aircraft ID with columns:
    | - ``type``: A string ICAO aircraft type designator.
    | - ``altitude``: A non-negatige double. The aircraft's altitude in feet.
    | - ``ground_speed``: A non-negative double. The aircraft's ground speed in knots.
    | - ``latitude``: A double in the range ``[-90, 90]``. The aircraft's latitude.
    | - ``longitude``: A double in the range ``[-180, 180]``. The aircraft's longitude.
    | - ``vertical_speed``: A double. The aircraft's vertical speed in feet/min (units according to BlueSky docs).

    Notes
    -----
    This dataframe also contains a metadata attribute named sim_t containing the
    simulator time in seconds since the start of the scenario.

    If any of the given aircraft IDs does not exist in the simulation, the
    returned dataframe contains a row of missing values for that ID.

    If an invalid ID is given, or the call to Bluebird fails, an exception is
    thrown.

    Examples:
    >>> pydodo.request_position.get_position()
    >>>
    """

    resp = requests.get(url, params={config_param("query_aircraft_id"): aircraft_id})
    if resp.status_code == 200:
        return process_pos_response(resp)
    elif resp.status_code == config_param("status_code_aircraft_id_not_found"):
        return null_pos_df(aircraft_id)
    else:
        raise requests.HTTPError(resp.text)


def aircraft_position(aircraft_id):
    """
    Get position dataframe for aircraft_id.

    Parameters
    ----------
    aircraft_id : str, [str]
        string or a list of strings. For the BlueSky simulator, this has to be
        at least three characters.

    Returns
    -------
    aircraft_pos : pandas.DataFrame
        Dataframe with position data, ``NaN`` if aircraft_id does not exist

    Examples:
    >>> pydodo.aircraft_position()
    >>>
    """

    if type(aircraft_id) == str:

        utils._validate_id(aircraft_id)
        pos_df = get_position(aircraft_id)
    elif type(aircraft_id) == list and bool(aircraft_id):
        for aircraft in aircraft_id:
            utils._validate_id(aircraft)
        all_pos = all_positions()
        pos_df = all_pos.reindex(aircraft_id)  # filter requested IDs
    else:
        raise AssertionError("Invalid input {} for aircraft id".format(aircraft_id))
    return normalise_positions_units(pos_df)
