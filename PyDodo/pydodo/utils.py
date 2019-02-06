from . import settings


def construct_endpoint_url(endpoint):
	return '{}/api/v{}/{}'.format(get_bluebird_url(), settings.API_VERSION, endpoint)


def get_bluebird_url():
	return '{}:{}'.format(settings.BB_HOST, settings.BB_PORT)
