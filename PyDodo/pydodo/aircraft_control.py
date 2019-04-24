import requests

from . import utils
from .utils import post_request
from .config_param import config_param


def change_altitude(aircraft_id, altitude=None, flight_level=None, vertical_speed=None):
    """
    Change aircraft altitude.
    """
    utils._check_id(aircraft_id)
    assert (
        altitude is None or flight_level is None
    ), "Only altitude or flight level should be provided, not both"
    alt = utils.parse_alt(altitude, flight_level)

    json = {"acid": aircraft_id, "alt": alt}

    if vertical_speed:
        utils._check_speed(vertical_speed)
        json["vs"] = vertical_speed
    return post_request(config_param("endpoint_change_altitude"), json)


def change_heading(aircraft_id, heading):
    """
    Change aircraft heading.
    """
    utils._check_id(aircraft_id)
    utils._check_heading(heading)

    json = {"acid": aircraft_id, "hdg": heading}
    return post_request(config_param("endpoint_change_heading"), json)


def change_speed(aircraft_id, speed):
    """
    Change aircraft speed.
    """
    utils._check_id(aircraft_id)
    utils._check_speed(speed)

    json = {"acid": aircraft_id, "spd": speed}
    return post_request(config_param("endpoint_change_speed"), json)


def change_vertical_speed(aircraft_id, vertical_speed):
    """
    Change aircraft vertical speed.
    """
    utils._check_id(aircraft_id)
    utils._check_speed(vertical_speed)

    json = {"acid": aircraft_id, "vspd": vertical_speed}
    return post_request(config_param("endpoint_change_vertical_speed"), json)
