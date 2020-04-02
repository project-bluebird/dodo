import requests
import json

from . import utils
from .config_param import config_param
from .request_position import aircraft_position
from .bluebird_connect import construct_endpoint_url


def _get_flight_level(aircraft_id):
    """
    Get a dataframe with the aircraft's current, requested and cleared flight levels.

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.

    Returns
    -------
    pos_df : pandas.DataFrame
        Dataframe indexed by **uppercase** aircraft ID with columns:
    | - ``current_flight_level``: A non-negatige double. The aircraft's altitude in feet.
    | - ``requested_flight_level``: The aircraft's requested flight level.
    | - ``cleared_flight_level"`` : The aircraft's cleared flight level.

    Examples
    --------
    >>> pydodo.get_flight_level.get_flight_level("BAW123")
    """
    utils._validate_id(aircraft_id)
    return aircraft_position(aircraft_id)


def requested_flight_level(aircraft_id):
    """
    Get the aircraft's requested flight level. Can only be returned
    if the aircraft has a defined route.

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.

    Returns
    -------
    flight_level : double
        A non-negative double. The aircraft's requested flight level.
        If an invalid ID is given, or the call to Bluebird fails, an exception
        is thrown.

    Examples
    --------
    >>> pydodo.requested_flight_level("BAW123")
    """

    return _get_flight_level(aircraft_id).iloc[0]["requested_flight_level"]


def cleared_flight_level(aircraft_id):
    """
     Get the aircraft's cleared flight level. The initial cleared
     flight level is set to the initial altitude when a scenario is loaded.

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.

    Returns
    -------
    cleared_flight_level : double
        A non-negative double. The aircraft's cleared flight level. If
        an invalid ID is given, or the call to Bluebird fails, an exception is
        thrown.

    Examples
    --------
    >>> pydodo.cleared_flight_level("BAW123")
    """

    return _get_flight_level(aircraft_id).iloc[0]["cleared_flight_level"]


def current_flight_level(aircraft_id):
    """
    Get the aircraft's current flight level (in feet).

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.

    Returns
    -------
    current_flight_level : double
        A non-negative double. The aircraft's current flight level in feet. If
        an invalid ID is given, or the call to Bluebird fails, an exception is
        thrown.

    Examples
    --------
    >>> pydodo.current_flight_level("BAW123")
    """

    return _get_flight_level(aircraft_id).iloc[0]["current_flight_level"]
