import requests
import json
import pandas as pd

from . import utils
from .post_request import post_request
from .config_param import config_param
from .bluebird_connect import construct_endpoint_url

endpoint = config_param("endpoint_list_route")
url = construct_endpoint_url(endpoint)


def _route_call(aircraft_id):
    """
    Make a call to the BlueBird LISTROUTE endpoint.

    Parameters
    ----------
    aircraft_id: str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.

    Returns
    -------
    dict :
        A dictionary with keys:

            ``"callsign"``
                A string aircraft identifier.

            ``"next_waypoint"``
                A string. Name of waypoint the aircraft is currently headed toward.

            ``"route_name"``
                A string name of the route.

            ``"route_waypoints"``
                A list of strings. All the waypoints on the route.

    Notes
    -----
    If the aircraft has no route information, a dictionary with just
    the callsign is returned.
    """
    resp = requests.get(url, params={config_param("query_aircraft_id"): aircraft_id})
    if resp.status_code == 200:
        return json.loads(resp.text)
    elif response.status == config_param("status_code_aircraft_has_no_route"):
        return {config_param("query_aircraft_id"): aircraft_id}
    else:
        raise requests.HTTPError(resp.text)


def _process_listroute_response(response):
    """
    Process JSON response from BlueBird LISTROUTE endpoint request.
    - Rename "callsign" key as "aircraft_id".

    Parameters
    ----------
    response : JSON <dict>
        BlueBird response returned by _route_call().
    """
    response["aircraft_id"] = response.pop(config_param("query_aircraft_id"))
    return response


def list_route(aircraft_id):
    """
    Get the route information of an aircraft as a data frame whose row names are
    waypoint names.

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.

    Returns
    -------
    dict :
        A dictionary with keys:

            ``"aircraft_id"```
                A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.

            ``"next_waypoint"``
                A string. Name of waypoint the aircraft is currently headed toward.

            ``"route_name"``
                A string name of the route.

            ``"route_waypoints"``
                A list of strings. All the waypoints on the route.

    Notes
    -----
    If no aircraft exists with the given ID, or the ID is invalid, an exception
    is thrown.

    If the corresponding aircraft has no route information, a dictionary with just
    the aircraft_id is returned.

    If any other error occurs (e.g. a failure to parse the route information),
    an exception is thrown.

    Examples
    --------
    >>> pydodo.list_route("BAW123")
    """

    utils._validate_id(aircraft_id)

    route = _route_call(aircraft_id)
    return _process_listroute_response(route)
