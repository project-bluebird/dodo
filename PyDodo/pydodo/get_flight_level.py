import requests
import json

from .config_param import config_param
from . import utils

endpoint = config_param("endpoint_aircraft_flight_level")
url = utils.construct_endpoint_url(endpoint)


def get_flight_level(aircraft_id):
    """
    Get a dictionary with the aircraft's current, requested and cleared flight levels.

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.

    Returns
    -------
    dict
        Flight level dictionary with keys:
        
        ``"fl_current"``
            The aircraft's current flight level in meters.
        ``"fl_requested"``
            The aircraft's requested flight level in meters.
        ``"fl_cleared"``
            The aircraft's cleared flight level in meters.

    Examples
    --------
    >>> pydodo.get_flight_level.get_flight_level("BAW123")
    """
    utils._validate_id(aircraft_id)
    resp = requests.get(url, params={config_param("query_aircraft_id"): aircraft_id})
    resp.raise_for_status()
    return json.loads(resp.text)


def requested_flight_level(aircraft_id):
    """
    Get the aircraft's requested flight level (in meters). Can only be returned
    if the aircraft has a defined route.

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.

    Returns
    -------
    flight_level : double
        A non-negative double. The aircraft's requested flight level in meters.
        If an invalid ID is given, or the call to Bluebird fails, an exception
        is thrown.

    Examples
    --------
    >>> pydodo.requested_flight_level("BAW123")
    """

    return get_flight_level(aircraft_id)['fl_requested']


def cleared_flight_level(aircraft_id):
    """
     Get the aircraft's cleared flight level (in meters). The initial cleared
     flight level is set to the initial altitude when a scenario is loaded.

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.

    Returns
    -------
    cleared_flight_level : double
        A non-negative double. The aircraft's cleared flight level in meters. If
        an invalid ID is given, or the call to Bluebird fails, an exception is
        thrown.

    Examples
    --------
    >>> pydodo.cleared_flight_level("BAW123")
    """

    return get_flight_level(aircraft_id)['fl_cleared']


def current_flight_level(aircraft_id):
    """
    Get the aircraft's current flight level (in meters).

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.

    Returns
    -------
    current_flight_level : double
        A non-negative double. The aircraft's current flight level in meters. If
        an invalid ID is given, or the call to Bluebird fails, an exception is
        thrown.

    Examples
    --------
    >>> pydodo.current_flight_level("BAW123")
    """

    return get_flight_level(aircraft_id)['fl_current']
