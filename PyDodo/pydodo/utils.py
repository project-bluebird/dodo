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
