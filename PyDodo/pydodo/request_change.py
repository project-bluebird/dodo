import requests

from .config_param import config_param
from . import utils

def post_change_request(param, json):
    """
    Common format for requesting aircraft change from BlueBird.
    """
    endpoint = config_param(param)
    url = utils.construct_endpoint_url(endpoint)
    resp = requests.post(url, json=json)
    resp.raise_for_status()
    return True

def change_altitude(aircraft_id, altitude=None, flight_level=None, vertical_speed=None):
    """
    Change aircraft altitude.
    """
    assert utils._check_string_input(aircraft_id), 'Invalid input {} for aircraft id'.format(aircraft_id)
    assert altitude is None or flight_level is None, 'Only altitude or flight level should be provided, not both'
    alt = utils.parse_alt(altitude, flight_level)

    json = {'acid': aircraft_id, 'alt': alt}
    if vertical_speed:
        assert utils._check_speed(vertical_speed), 'Invalid input {} for vertical speed'.format(vertical_speed)
        json['vs'] = vertical_speed
    return post_change_request('endpoint_change_altitude', json)


def change_heading(aircraft_id, heading):
    """
    Change aircraft heading.
    """
    assert utils._check_string_input(aircraft_id), 'Invalid input {} for aircraft id'.format(aircraft_id)
    assert utils._check_heading(heading), 'Invalid input {} for heading'

    json = {'acid': aircraft_id, 'hdg': heading}
    return post_change_request('endpoint_change_heading', json)


def change_speed(aircraft_id, speed):
    """
    Change aircraft speed.
    """
    assert utils._check_string_input(aircraft_id), 'Invalid input {} for aircraft id'.format(aircraft_id)
    assert utils._check_speed(speed), 'Invalid input {} for speed'

    json = {'acid': aircraft_id, 'spd': speed}
    return post_change_request('endpoint_change_speed', json)


def change_vertical_speed(aircraft_id, vertical_speed):
    """
    Change aircraft vertical speed.
    """
    assert utils._check_string_input(aircraft_id), 'Invalid input {} for aircraft id'.format(aircraft_id)
    assert utils._check_speed(vertical_speed), 'Invalid input {} for vertical speed'

    json = {'acid': aircraft_id, 'vspd': vertical_speed}
    return post_change_request('endpoint_change_vertical_speed', json)
