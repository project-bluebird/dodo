import requests

from . import settings
from . import utils

endpoint = settings.default['endpoint_create_aircraft']
url = utils.construct_endpoint_url(endpoint)

def create_aircraft(aircraft_id, type, latitude, longitude, heading, altitude, flight_level, speed):
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

	resp = requests.post(url, json=json)

	# if response is 4XX or 5XX, raise exception
	resp.raise_for_status()
	return True