import requests

from . import utils
from .utils import post_request
from .config_param import config_param


def create_aircraft(
    aircraft_id,
    type,
    latitude,
    longitude,
    heading,
    speed,
    altitude=None,
    flight_level=None,
):
    """
	Create new aircraft. Raises error if inputs are invalid or if aircraft already exists.
	"""
    utils._check_string_input(aircraft_id, "aircraft_id")
    utils._check_string_input(type, "type")
    utils._check_latitude(latitude)
    utils._check_longitude(longitude)
    utils._check_heading(heading)
    utils._check_speed(speed)
    assert (
        altitude is None or flight_level is None
    ), "Only altitude or flight level should be provided, not both"
    alt = utils.parse_alt(altitude, flight_level)

    json = {
        "acid": aircraft_id,
        "type": type,
        "lat": latitude,
        "lon": longitude,
        "hdg": heading,
        "alt": alt,
        "spd": speed,
    }

    return post_request(config_param("endpoint_create_aircraft"), json)
