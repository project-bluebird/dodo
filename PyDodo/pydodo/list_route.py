import requests
import json
import pandas as pd

from . import utils
from .utils import post_request
from .config_param import config_param

endpoint = config_param("endpoint_list_route")
url = utils.construct_endpoint_url(endpoint)


def format_wpt_info(waypoint):
    """
    Format waypoint dictionary returned by BlueBird.

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


def process_listroute_response(response):
    """
    Process JSON response from BlueBird LISTROUTE endpoint request and return
    the route information of an aircraft as a data frame.

    Parameters
    ----------
    response : JSON <dict>

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
    json_data = json.loads(response.text)
    route_dict = {wpt["wpt_name"]: format_wpt_info(wpt) for wpt in json_data["route"]}
    df = pd.DataFrame.from_dict(route_dict, orient="index")

    wpt_order = route_dict.keys()
    df = df.reindex(wpt_order)

    df.sim_t = json_data["sim_t"]
    df.aircraft_id = json_data["acid"]

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

    resp = requests.get(url, params={config_param("query_aircraft_id"): aircraft_id})
    if resp.status_code == 200:
        return process_listroute_response(resp)
    elif (
        resp.status_code == 500
        and config_param("err_msg_aircraft_has_no_route") in resp.text
    ):
        df = pd.DataFrame(
            {"requested_altitude": [], "requested_speed": [], "current": []}
        )
        df.aircraft_id = aircraft_id
        return df
    else:
        raise requests.HTTPError(resp.text)


def define_waypoint(waypoint_name, latitude, longitude, waypoint_type=None):
    """
    Define a custom waypoint in the simulation.

    Parameters
    ----------
    waypoint_name : str
        A waypoint identifier.
    latitude : double
        A double in the range ``[-90, 90]``. The waypoint's latitude.
    longitude : double
        A double in the range ``[-180, 180]``. The waypoint's longitude.
    waypoint_type : str, optional
        Custom string which can be used to tag waypoints.

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Notes
    -----
    This function is only used for testing purposes.
    """
    utils._validate_string(waypoint_name, "waypoint name")
    utils._validate_latitude(latitude)
    utils._validate_longitude(longitude)

    body = {"wpname": waypoint_name, "lat": latitude, "lon": longitude}
    if waypoint_type != None:
        utils._validate_string(waypoint_type, "waypoint type")
        body["type"] = waypoint_type

    return post_request(config_param("endpoint_define_waypoint"), body)


def add_waypoint(
    aircraft_id, waypoint_name=None, altitude=None, flight_level=None, speed=None
    ):
    """
    Add waypoint to aircraft route. Can also optinally set altitude OR flight level
    and speed which should be achieved by this waypoint.

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.
    waypoint_name : str
        A waypoint identifier.
    altitude : double, optional
        A double in the range ``[0, 6000]``. The altitude in feet the aircraft
        should achieve by this waypoint. For altitudes in excess of 6000ft a
        flight level should be specified instead.
    flight_level : int, optional
        An integer of 60 or more. The flight level the aircraft should achieve
        by this waypoint.
    speed : double, optional
        A non-negative double. The calibrated air speed in knots (KCAS) that the
        aircraft should achieve by this waypoint.

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Notes
    -----
    This function is only used for testing purposes.

    Either the altitude or flight_level argument must be given, but not both.
    """
    utils._validate_id(aircraft_id)
    utils._validate_string(waypoint_name, "waypoint_name")
    body = {config_param("query_aircraft_id"): aircraft_id, "wpname": waypoint_name}

    if altitude != None or flight_level != None:
        alt = utils.parse_alt(altitude, flight_level)
        body["alt"] = alt
    if speed != None:
        utils._validate_speed(speed)
        body["spd"] = speed

    return post_request(config_param("endpoint_add_waypoint"), body)
