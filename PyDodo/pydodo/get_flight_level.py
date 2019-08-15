import requests
import json

from .config_param import config_param
from . import utils

endpoint = config_param("endpoint_aircraft_flight_level")
url = utils.construct_endpoint_url(endpoint)


def get_flight_level(aircraft_id):
    utils._validate_id(aircraft_id)
    resp = requests.get(url, params={config_param("query_aircraft_id"): aircraft_id})
    resp.raise_for_status()
    return json.loads(resp.text)


def requested_flight_level(aircraft_id):
    return get_flight_level(aircraft_id)['fl_requested']


def cleared_flight_level(aircraft_id):
    return get_flight_level(aircraft_id)['fl_cleared']


def current_flight_level(aircraft_id):
    return get_flight_level(aircraft_id)['fl_current']
