import requests
import json
import numpy as np
import pandas as pd

from .config_param import config_param
from .utils import construct_endpoint_url
from . import utils

endpoint = config_param("endpoint_aircraft_position")
url = construct_endpoint_url(endpoint)

_POS_COL_NAMES = ["type", "altitude", "ground_speed", "latitude", "longitude",
"vertical_speed"]
_SCALE_METRES_TO_FEET = 3.280839895


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
    dict
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

    return {
        "type": aircraft_pos["actype"],
        "altitude": aircraft_pos["alt"],
        "ground_speed": aircraft_pos["gs"],
        "latitude": aircraft_pos["lat"],
        "longitude": aircraft_pos["lon"],
        "vertical_speed": aircraft_pos["vs"],
    }


def normalise_positions_units(df):
    """
    Normalise units of measurement in the positions data.
    """
    # Bluesky returns altitude in metres, not feet.
    if config_param("simulator") == config_param("bluesky_simulator"):
        df.loc[:, "altitude"] = (_SCALE_METRES_TO_FEET * df["altitude"]).round(2)
    return df


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
    return normalise_positions_units(pos_df)


def position_call(aircraft_id = None):
    """
    Make a call to the BlueBird aircraft position (POS) endpoint.

    Parameters
    ----------
    aircraft_id: str, optional
        A string aircraft identifier, or None (the default).

    Returns
    -------
    pandas.DataFrame
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

    If the given aircraft ID does not exist in the simulation, dataframe with a
    row of missing values is returned.

    If the response from Bluebird contains an error status code, an exception is
    thrown.

    Examples
    ---------
    >>> pydodo.request_position.position_call()
    >>> pydodo.request_position.position_call("BAW123")
    """

    if aircraft_id == None:
        aircraft_id = "all"
    resp = requests.get(url, params={config_param("query_aircraft_id"): aircraft_id})
    if resp.status_code == 200:
        return process_pos_response(resp)
    elif resp.status_code == config_param("status_code_aircraft_id_not_found"):
        return pd.DataFrame(
            {key: np.nan for key in _POS_COL_NAMES},
            index=[aircraft_id]
        )
    elif resp.status_code == config_param("status_code_no_aircraft_found"):
        return pd.DataFrame({col: [] for col in _POS_COL_NAMES})
    else:
        raise requests.HTTPError(resp.text)


def all_positions():
    """
    Get all aircraft positions.

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

    return position_call()


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
        return position_call(aircraft_id)
    elif type(aircraft_id) == list and bool(aircraft_id):
        for aircraft in aircraft_id:
            utils._validate_id(aircraft)
        all_pos = position_call() # get all aircraft in simulation
        return all_pos.reindex(aircraft_id)  # filter requested IDs
    else:
        raise AssertionError("Invalid input {} for aircraft id".format(aircraft_id))
