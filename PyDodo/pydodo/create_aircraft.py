import requests

from .utils import construct_endpoint_url


def _check_latitude(lat):
	return abs(lat) <= 90


def _check_longitude(lon):
	return -180 <= lon < 180


def _check_heading(hdg):
	return 0 <= hdg < 360


def _check_altitude(alt):
	return 0 <= alt < 6000


def _check_flight_level(fl):
	return int(fl[2:]) > 60


def _check_speed(spd):
	return spd >= 0


endpoint = 'cre'


def parse_alt(alt, fl):
	if alt is not None:
		assert _check_altitude(alt), 'Invalid value {} for altitude'.format(alt)
		alt = str(alt)
	else:
		assert fl is not None, 'Must specify a valid altitude or a flight level'
		assert _check_flight_level(fl), 'Invalid value {} for flight_level'.format(fl)
		alt = fl

	return alt


def create_aircraft(aircraft_id, type, latitude, longitude, heading, altitude, flight_level, speed):
	url = construct_endpoint_url(endpoint)

	assert _check_latitude(latitude), 'Invalid value {} for latitude'.format(latitude)
	assert _check_longitude(longitude), 'Invalid value {} for longitude'.format(longitude)
	assert _check_heading(heading), 'Invalid value {} for heading'.format(heading)
	assert _check_speed(speed), 'Invalid value {} for speed'.format(speed)
	alt = parse_alt(altitude, flight_level)

	json = {'acid': aircraft_id, 'type': type, 'lat': latitude, 'lon': longitude, 'hdg': heading,
	        'alt': alt, 'spd': speed}

	resp = requests.post(url, json=json)

	# print('{} - {}'.format(resp.status_code, resp.json()))
	if resp.status_code == 200:
		return True
	return False
