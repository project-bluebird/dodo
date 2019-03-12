import requests

from . import utils
from .utils import post_request
from .config_param import config_param


def create_aircraft(aircraft_id, type, latitude, longitude, heading, speed, altitude=None, flight_level=None):
	"""
	Create new aircraft. Raises error if inputs are invalid or if aircraft already exists.
	"""
	assert utils._check_string_input(aircraft_id), 'Invalid value {} for aircraft_id'.format(aircraft_id)
	assert utils._check_string_input(type), 'Invalid value {} for type'.format(type)
	assert utils._check_latitude(latitude), 'Invalid value {} for latitude'.format(latitude)
	assert utils._check_longitude(longitude), 'Invalid value {} for longitude'.format(longitude)
	assert utils._check_heading(heading), 'Invalid value {} for heading'.format(heading)
	assert utils._check_speed(speed), 'Invalid value {} for speed'.format(speed)
	assert altitude is None or flight_level is None, 'Only altitude or flight level should be provided, not both'
	alt = utils.parse_alt(altitude, flight_level)

	json = {'acid': aircraft_id, 'type': type, 'lat': latitude, 'lon': longitude,
			'hdg': heading, 'alt': alt, 'spd': speed}

	return post_request(config_param('endpoint_create_aircraft'), json)
