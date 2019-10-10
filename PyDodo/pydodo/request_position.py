import requests
import json
import numpy as np
import pandas as pd

from .config_param import config_param
from .utils import construct_endpoint_url
from . import utils

endpoint = config_param("endpoint_aircraft_position")
url = construct_endpoint_url(endpoint)


def position_call(aircraft_id=None):
    """
    Make a call to the BlueBird aircraft position (POS) endpoint.

    Parameters
    ----------
    aircraft_id: str, optional
        A string aircraft identifier, or None (the default).

    Returns
    -------
    dict of {str : dict}
        A dictionary with aircraft IDs as keys and aircraft position information
        contained in a dictionary. If aircraft ID is not found, position dictionary
        is empty. If there are no aircraft found in the simulation, an empty
        dictionary is returned.

    Notes
    -----
    If no aircraft ID is provided, returns position information for all aircraft
    in simulation.

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
        return json.loads(resp.text)
    elif resp.status_code == config_param("status_code_aircraft_id_not_found"):
        return {aircraft_id: {}}
    elif resp.status_code == config_param("status_code_no_aircraft_found"):
        return {}
    else:
        raise requests.HTTPError(resp.text)


def normalise_positions_units(df):
    """
    Normalise units of measurement in the positions data.
    """
    _SCALE_METRES_TO_FEET = 3.280839895

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
        BlueBird response returned by position_call().

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

    If response is empty, an empty data frame is returned.

    If response doesn't contain position information for an aircraft ID, the
    returned dataframe contains a row of missing values for that ID.
    """
    # map between BlueBird pos names and our pos column names
    _POS_COL_MAP = {
        "actype": "type",
        "alt": "altitude",
        "gs": "ground_speed",
        "lat": "latitude",
        "lon": "longitude",
        "vs": "vertical_speed",
    }

    if not bool(response):
        return pd.DataFrame({col: [] for col in _POS_COL_MAP.values()})

    sim_t = response.pop("sim_t", None)

    pos_dict = {
        aircraft: (
            response[aircraft]
            if bool(response[aircraft])
            else {col: np.nan for col in _POS_COL_MAP.values()}
        )
        for aircraft in response.keys()
    }
    pos_df = pd.DataFrame.from_dict(pos_dict, orient="index")
    pos_df = pos_df.rename(columns=_POS_COL_MAP)

    if sim_t is not None:
        pos_df.sim_t = sim_t

    return normalise_positions_units(pos_df)


def all_positions():
    """
    Get all aircraft positions.

    Parameters
    ----------
    NONE

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

    If the response from Bluebird contains an error status code, an exception is
    thrown.

    Examples:
    ---------
    >>> pydodo.all_positions()
    """
    pos = position_call()
    return process_pos_response(pos)


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
    utils._validate_id_list(aircraft_id)

    if type(aircraft_id) == str:
        pos = position_call(aircraft_id)
        return process_pos_response(pos)
    elif type(aircraft_id) == list:
        all_pos_df = all_positions()  # get all aircraft in simulation
        return all_pos_df.reindex(aircraft_id)  # filter requested IDs
