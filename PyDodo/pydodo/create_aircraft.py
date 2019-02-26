import requests

from . import settings
from .utils import construct_endpoint_url

endpoint = settings.default['endpoint_create_aircraft']

def _check_latitude(lat):
	return abs(lat) <= 90


def _check_longitude(lon):
	return -180 <= lon < 180


def _check_heading(hdg):
	return 0 <= hdg < 360


def _check_altitude(alt):
	return 0 <= alt <= settings.default['feet_altitude_upper_limit']


def _check_flight_level(fl):
	return fl >= settings.default['flight_level_lower_limit']


def _check_speed(spd):
	return spd >= 0


def _check_string_input(input):
    """Check that input is a non-empty string"""
    if type(input) == str:
        return len(input) >= 1
    return False


def parse_alt(alt, fl):
	if alt is not None:
		assert _check_altitude(alt), 'Invalid value {} for altitude'.format(alt)
		alt = str(alt)
	else:
		assert fl is not None, 'Must specify a valid altitude or a flight level'
		assert _check_flight_level(fl), 'Invalid value {} for flight_level'.format(fl)
		alt = "FL{}".format(fl)

	return alt


def create_aircraft(aircraft_id, type, latitude, longitude, heading, altitude, flight_level, speed):
	"""
	Create new aircraft. Raises error if inputs are invalid or if aircraft already exists.
	"""
	url = construct_endpoint_url(endpoint)

	assert _check_string_input(aircraft_id), 'Invalid value {} for aircraft_id'.format(aircraft_id)
	assert _check_string_input(type), 'Invalid value {} for type'.format(type)
	assert _check_latitude(latitude), 'Invalid value {} for latitude'.format(latitude)
	assert _check_longitude(longitude), 'Invalid value {} for longitude'.format(longitude)
	assert _check_heading(heading), 'Invalid value {} for heading'.format(heading)
	assert _check_speed(speed), 'Invalid value {} for speed'.format(speed)
	assert altitude is None or flight_level is None, 'Only altitude or flight level should be provided, not both'
	alt = parse_alt(altitude, flight_level)

	json = {'acid': aircraft_id, 'type': type, 'lat': latitude, 'lon': longitude,
			'hdg': heading, 'alt': alt, 'spd': speed}

	resp = requests.post(url, json=json)

	# if response is 4XX or 5XX, raise exception
	resp.raise_for_status()
	return True
