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

            ``"route"``
                A dictionary with waypoint names as keys and related waypoint
                information contained in a dictionary. If the aircraft does not
                have a route, the route dictionary is empty.
    """
    resp = requests.get(url, params={config_param("query_aircraft_id"): aircraft_id})
    if resp.status_code == 200:
        return json.loads(resp.text)
    elif (
        resp.status_code == 500
        and config_param("err_msg_aircraft_has_no_route") in resp.text
    ):
        return {config_param("query_aircraft_id"): aircraft_id, "route": {}}
    else:
        raise requests.HTTPError(resp.text)


def _format_wpt_info(waypoint):
    """
    Format route dictionary of waypoints returned by BlueBird API.

    Parameters
    ----------
    waypoint : dict
        Dictionary of waypoint information returned by BlueBird with keys:

            ``"req_alt"``
                The aircraft's requested altitude at waypoint (in feet or flight levels).
            ``"req_spd"``
                The aircraft's requested speed at waypoint.
            ``"is_current"``
                Whether aircraft is currently headed to this waypoint.

    Returns
    -------
    wpt_formatted : dict
        Dictionary of formatted waypoint information with keys:

            ``"requested_altitutde"``
                The aircraft's requested altitude at waypoint in feet.
            ``"requested_speed"``
                The aircraft's requested speed at waypoint.
            ``"current"``
                Whether aircraft is currently headed to this waypoint.
    """
    wpt_formatted = {
        "requested_altitude": waypoint["req_alt"],
        "requested_speed": waypoint["req_spd"],
        "current": waypoint["is_current"],
    }

    # if altitude is a flight level string (e.g., FL250), convert to FEET
    alt = wpt_formatted["requested_altitude"]
    if isinstance(alt, str):
        wpt_formatted["requested_altitude"] = int(alt[2:]) * 100

    return wpt_formatted


def _process_listroute_response(response):
    """
    Process JSON response from BlueBird LISTROUTE endpoint request and return
    the route information of an aircraft as a data frame.

    Parameters
    ----------
    response : JSON <dict>
        BlueBird response returned by route_call().

    Returns
    -------
    df : pandas.DataFrame
            A  dataframe indexed by waypoint name with columns:
        | - ``requested_altitude``: A non-negatige double. The aircraft's requested altitude in feet at waypoint.
        | - ``requested_speed``: A non-negative double. The aircraft's requested speed at waypoint.
        | - ``current``: A boolean indicating whether the aircraft is currently heading toward this waypoint.

    Notes
    -----
    This dataframe also contains metadata attributes named `aircraft_id` and
    `sim_t` containing the simulator time in seconds since the start of the
    scenario.
    """
    if not bool(response["route"]):
        df = pd.DataFrame(
            {"requested_altitude": [], "requested_speed": [], "current": []}
        )
    else:
        route_dict = {
            wpt["wpt_name"]: _format_wpt_info(wpt) for wpt in response["route"]
        }
        df = pd.DataFrame.from_dict(route_dict, orient="index")
        wpt_order = route_dict.keys()
        df = df.reindex(wpt_order)
        df.sim_t = response["sim_t"]
    df.aircraft_id = response[config_param("query_aircraft_id")]

    return df


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
    df : pandas.DataFrame
        A  dataframe indexed by waypoint name with columns:
    | - ``requested_altitude``: A non-negatige double. The aircraft's requested altitude in feet at waypoint.
    | - ``requested_speed``: A non-negative double. The aircraft's requested speed at waypoint.
    | - ``current``: A boolean indicating whether the aircraft is currently heading toward this waypoint.

    Notes
    -----
    This dataframe also contains metadata attributes named `aircraft_id` and
    `sim_t` containing the simulator time in seconds since the start of the
    scenario.

    If no aircraft exists with the given ID, or the ID is invalid, an exception
    is thrown.

    If the corresponding aircraft has no route information, an empty dataframe
    is returned and the `sim_t` metadata attribute is omitted.

    If any other error occurs (e.g. a failure to parse the route information),
    an exception is thrown.

    Examples
    --------
    >>> pydodo.list_route("BAW123")
    """

    utils._validate_id(aircraft_id)

    route = _route_call(aircraft_id)
    return _process_listroute_response(route)
