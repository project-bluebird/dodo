from .utils import construct_endpoint_url


def create_aircraft(data):
	endpoint = 'CRE'

	print(construct_endpoint_url(endpoint))
