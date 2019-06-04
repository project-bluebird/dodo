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
    flight_level=None
    ):
    """
	Create new aircraft. Raises error if inputs are invalid or if aircraft already exists.
	"""
    utils._validate_id(aircraft_id)
    utils._validate_string(type, "aircraft type")
    utils._validate_latitude(latitude)
    utils._validate_longitude(longitude)
    utils._validate_heading(heading)
    utils._validate_speed(speed)
    assert (
        altitude is None or flight_level is None
    ), "Only altitude or flight level should be provided, not both"
    alt = utils.parse_alt(altitude, flight_level)

    body = {
        "acid": aircraft_id,
        "type": type,
        "lat": latitude,
        "lon": longitude,
        "hdg": heading,
        "alt": alt,
        "spd": speed,
    }

    return post_request(config_param("endpoint_create_aircraft"), body)
