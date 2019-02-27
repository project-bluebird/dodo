import requests

from . import settings


def construct_endpoint_url(endpoint):
	return '{}/api/v{}/{}'.format(get_bluebird_url(), settings.API_VERSION, endpoint)


def get_bluebird_url():
	return 'http://{}:{}'.format(settings.BB_HOST, settings.BB_PORT)


def ping_bluebird():
	endpoint = "pos"

	url = construct_endpoint_url(endpoint)
	print('ping bluebird on {}'.format(url))

	# /pos endpoint only supports GET requests, this should return an error if BlueBird is running
	# on the specified host
	try:
		resp = requests.post(url)
	except requests.exceptions.ConnectionError as e:
		print(e)
		return False

	if resp.status_code == 405:
		return True

	return False


def _check_latitude(lat):
	return abs(lat) <= 90


def _check_longitude(lon):
	return -180 <= lon < 180


def _check_heading(hdg):
	return 0 <= hdg < 360


def _check_speed(spd):
	return spd >= 0


def _check_string_input(input):
    """Check that input is a non-empty string"""
    if type(input) == str:
        return len(input) >= 1
    return False

def _check_altitude(alt):
	return 0 <= alt <= settings.default['feet_altitude_upper_limit']

def _check_flight_level(fl):
	return fl >= settings.default['flight_level_lower_limit']

def parse_alt(alt, fl):
	if alt is not None:
		assert _check_altitude(alt), 'Invalid value {} for altitude'.format(alt)
		alt = str(alt)
	else:
		assert fl is not None, 'Must specify a valid altitude or a flight level'
		assert _check_flight_level(fl), 'Invalid value {} for flight_level'.format(fl)
		alt = "FL{}".format(fl)

	return alt

def _check_id_list(aircraft_id):
    return bool(aircraft_id) and all(isinstance(elem, str) and len(elem) >= 1 for elem in aircraft_id)
