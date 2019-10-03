from . import utils
from .utils import post_request
from .config_param import config_param


def change_altitude(aircraft_id, altitude=None, flight_level=None, vertical_speed=None):
    """
    Request an aircraft to change altitude.

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.
    altitude : double, default=None
        A double in the range ``[0, 6000]``. The requested altitude in feet. For
        altitudes in excess of 6000ft a flight level should be specified
        instead.
    flight_level : int, default=None
        An integer of 60 or more. The requested flight level.
    vertical_speed : A non-negative double. The requested vertical speed in feet/min, default=None [optional]

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Examples
    --------
    >>> pydodo.change_altitude("BAW123", flight_level = 450)
    >>> pydodo.change_altitude("BAW123", altitude = 5000)
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
    Request an aircraft to change heading.

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.
    heading : double
        A double in the range ``[0, 360]``. The requested heading in degrees.

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Examples
    --------
    >>> pydodo.change_heading("BAW123", heading = 90)
    """

    utils._validate_id(aircraft_id)
    utils._validate_heading(heading)

    body = {config_param("query_aircraft_id"): aircraft_id, "hdg": heading}
    return post_request(config_param("endpoint_change_heading"), body)


def change_speed(aircraft_id, speed):
    """
    Request an aircraft to change speed.

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.
    speed : double
        A non-negative double. The requested calibrated air speed in knots
        (KCAS).

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Examples
    --------
    >>> pydodo.change_speed("BAW123", speed = 90)
    """

    utils._validate_id(aircraft_id)
    utils._validate_speed(speed)

    body = {config_param("query_aircraft_id"): aircraft_id, "spd": speed}
    return post_request(config_param("endpoint_change_speed"), body)


def change_vertical_speed(aircraft_id, vertical_speed):
    """
    Request an aircraft to change vertical speed.

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.
    vertical_speed : double
        A double. The requested vertical speed in feet/min (units according to
        BlueSky docs).

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Examples
    --------
    >>> pydodo.change_vertical_speed("BAW123", vertical_speed = 10)
    """

    utils._validate_id(aircraft_id)
    utils._validate_speed(vertical_speed)

    body = {config_param("query_aircraft_id"): aircraft_id, "vspd": vertical_speed}
    return post_request(config_param("endpoint_change_vertical_speed"), body)


def direct_to_waypoint(aircraft_id, waypoint_name):
    """
    Request aircraft to change heading toward a waypoint.

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.
    waypoint_name : str
        A string waypoint identifier. The waypoint to direct the aircraft to.

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Notes
    -----
    The waypoint must exist on the aircraft route.

    Examples
    --------
    >>> pydodo.direct_to_waypoint("BAW123",  waypoint_name = "TESTWPT")
    """

    utils._validate_id(aircraft_id)
    utils._validate_string(waypoint_name, "waypoint name")

    body = {config_param("query_aircraft_id"): aircraft_id, "waypoint": waypoint_name}
    return post_request(config_param("endpoint_direct_to_waypoint"), body)
