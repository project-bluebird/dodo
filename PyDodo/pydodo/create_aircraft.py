import requests

from . import validate_input
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
    flight_level=None
):
    """
	Create new aircraft. Raises error if inputs are invalid or if aircraft already exists.
	"""
    validate_input._check_type_string(aircraft_id, "aircraft_id")
    validate_input._check_type_string(type, "type")
    validate_input._check_latitude(latitude)
    validate_input._check_longitude(longitude)
    validate_input._check_heading(heading)
    validate_input._check_speed(speed)
    assert (
        altitude is None or flight_level is None
    ), "Only altitude or flight level should be provided, not both"
    alt = validate_input.parse_alt(altitude, flight_level)

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
