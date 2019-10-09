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
    """
    Format aircraft position dictionary returned by BlueBird API.

    Parameters
    ----------
    aircraft_pos : dict
        Dictionary of aircraft position information returned by BlueBird with keys:

        ``"actype"``
            A string ICAO aircraft type designator.
        ``"alt"``
            The aircraft's altitude in metres.
        ``"gs"``
            The aircraft's ground speed in knots.
        ``"lat"``
            The aircraft's latitude.
        ``"lon"``
            The aircraft's longitude.
        ``"vs"``
            The aircraft's vertical speed in feet/min.

    Returns
    -------
    position_formatted : dict
        Dictionary of formatted aircraft position information with keys:

        ``"type"``
            A string ICAO aircraft type designator.
        ``"altitude"``
            The aircraft's altitude in metres.
        ``"ground_speed"``
            The aircraft's ground speed in knots.
        ``"latitude"``
            The aircraft's latitude.
        ``"longitude"``
            The aircraft's longitude.
        ``"vertical_speed"``
            The aircraft's vertical speed in feet/min.
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
    Process JSON response from BlueBird POS enndpoint request and return the
    aircraft position information as a data frame.

    Parameters
    ----------
    response : JSON <dict>

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
    This dataframe also contains a metadata attribute named `sim_t` containing
    the simulator time in seconds since the start of the scenario.
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
    """
    Normalise units of measurement in the positions data.
    """

    SCALE_METRES_TO_FEET = 3.280839895

    # Bluesky returns altitude in metres, not feet.
    if config_param("simulator") == config_param("bluesky_simulator"):
        df.loc[:, "altitude"] = SCALE_METRES_TO_FEET * df["altitude"]
        df.loc[:, "altitude"] = df["altitude"].round(2)
    return df


def null_pos_df(aircraft_id=None):
    """
    Returns an empty dataframe if no aircraft_id is provided otherwise
    dataframe with NANs.

    Parameters
    ----------
    aircraft_id : str, optional

    Returns
    -------
    pos_df : pandas.DataFrame
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
    ---------
    >>> pydodo.all_positions()
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
    Get position dataframe for a single aircraft_id.

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.

    Returns
    -------
    pos_df : pandas.DataFrame
        Dataframe indexed by **uppercase** aircraft ID with columns:
    | - ``type``: A string ICAO aircraft type designator.
    | - ``altitude``: A non-negatige double. The aircraft's altitude in feet.
    | - ``ground_speed``: A non-negative double. The aircraft's ground speed in knots.
    | - ``latitude``: A double in the range ``[-90, 90]``. The aircraft's latitude.
    | - ``longitude``: A double in the range ``[-180, 180)``. The aircraft's longitude.
    | - ``vertical_speed``: A double. The aircraft's vertical speed in feet/min (units according to BlueSky docs).

    Notes
    -----
    This dataframe also contains a metadata attribute named `sim_t` containing
    the simulator time in seconds since the start of the scenario.

    If the given aircraft ID does not exist in the simulation, the returned
    dataframe is a row of missing values.

    If an invalid ID is given, or the call to Bluebird fails, an exception is
    thrown.
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
    Get the position of a single or multiple aircraft based on their IDs.

    Parameters
    ----------
    aircraft_id : str, [str]
        A string or a list of strings representing aircraft identifiers. For the
        BlueSky simulator, each ID must contain at least three characters.

    Returns
    -------
    pos_df : pandas.DataFrame
        Dataframe indexed by **uppercase** aircraft ID with columns:
    | - ``type``: A string ICAO aircraft type designator.
    | - ``altitude``: A non-negatige double. The aircraft's altitude in feet.
    | - ``ground_speed``: A non-negative double. The aircraft's ground speed in knots.
    | - ``latitude``: A double in the range ``[-90, 90]``. The aircraft's latitude.
    | - ``longitude``: A double in the range ``[-180, 180)``. The aircraft's longitude.
    | - ``vertical_speed``: A double. The aircraft's vertical speed in feet/min (units according to BlueSky docs).

    Notes
    -----
    This dataframe also contains a metadata attribute named sim_t containing the
    simulator time in seconds since the start of the scenario.

    If any of the given aircraft IDs does not exist in the simulation, the
    returned dataframe contains a row of missing values for that ID.

    If an invalid ID is given, or the call to Bluebird fails, an exception is
    thrown.

    Examples
    ---------
    >>> pydodo.aircraft_position("BAW123")
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
