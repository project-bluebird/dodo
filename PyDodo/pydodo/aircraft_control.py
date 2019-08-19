from . import utils
from .utils import post_request
from .config_param import config_param


def change_altitude(aircraft_id, altitude=None, flight_level=None, vertical_speed=None):
    """
    Change aircraft altitude.

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.
    altitude : double, default=None
        A double in the range [0, 6000]. The requested altitude in feet. For
        altitudes in excess of 6000ft a flight level should be specified
        instead.
    flight_level : int, default=None
        An integer of 60 or more. The requested flight level.
    vertical_speed : double, default=None [optional]

    Returns
    -------
    True : boolean
        TRUE if successful. Otherwise an exception is thrown.

    Examples
    --------
    >>> pydodo.aircraft_control.change_altitude('BA1', ...)
    >>>
    """

    utils._validate_id(aircraft_id)
    assert (
        altitude is None or flight_level is None
    ), "Only altitude or flight level should be provided, not both"
    alt = utils.parse_alt(altitude, flight_level)

    body = {config_param("query_aircraft_id"): aircraft_id, "alt": alt}

    if vertical_speed:
        utils._validate_speed(vertical_speed)
        body["vs"] = vertical_speed
    return post_request(config_param("endpoint_change_altitude"), body)


def change_heading(aircraft_id, heading):
    """
    Change aircraft heading.
    """
    utils._validate_id(aircraft_id)
    utils._validate_heading(heading)

    body = {config_param("query_aircraft_id"): aircraft_id, "hdg": heading}
    return post_request(config_param("endpoint_change_heading"), body)


def change_speed(aircraft_id, speed):
    """
    Change aircraft speed.
    """
    utils._validate_id(aircraft_id)
    utils._validate_speed(speed)

    body = {config_param("query_aircraft_id"): aircraft_id, "spd": speed}
    return post_request(config_param("endpoint_change_speed"), body)


def change_vertical_speed(aircraft_id, vertical_speed):
    """
    Change aircraft vertical speed.
    """
    utils._validate_id(aircraft_id)
    utils._validate_speed(vertical_speed)

    body = {config_param("query_aircraft_id"): aircraft_id, "vspd": vertical_speed}
    return post_request(config_param("endpoint_change_vertical_speed"), body)


def direct_to_waypoint(aircraft_id, waypoint_name):
    """
    Change aircraft heading toward a waypoint.
    """
    utils._validate_id(aircraft_id)
    utils._validate_string(waypoint_name, "waypoint name")

    body = {config_param("query_aircraft_id"): aircraft_id, "waypoint": waypoint_name}
    return post_request(config_param("endpoint_direct_to_waypoint"), body)
