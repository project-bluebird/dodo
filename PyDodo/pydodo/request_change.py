import requests

from .config_param import config_param
from . import utils

def change_altitude(aircraft_id, altitude=None, flight_level=None, vertical_speed=None):
    """
    Change aircraft altitude.
    """
    assert utils._check_string_input(aircraft_id), 'Invalid input {} for aircraft id'.format(aircraft_id)
    assert altitude is None or flight_level is None, 'Only altitude or flight level should be provided, not both'
    alt = utils.parse_alt(altitude, flight_level)

    endpoint = config_param('endpoint_change_altitude')
    url = utils.construct_endpoint_url(endpoint)

    json = {'acid': aircraft_id, 'alt': alt}
    if vertical_speed:
        assert utils._check_speed(vertical_speed), 'Invalid input {} for vertical speed'.format(vertical_speed)
        json['vs'] = vertical_speed
    resp = requests.post(url, json=json)
    resp.raise_for_status()
    return True

def change_heading(aircraft_id, heading):
    """
    Change aircraft heading.
    """
    assert utils._check_string_input(aircraft_id), 'Invalid input {} for aircraft id'.format(aircraft_id)
    assert utils._check_heading(heading), 'Invalid input {} for heading'

    endpoint = config_param('endpoint_change_heading')
    url = utils.construct_endpoint_url(endpoint)

    json = {'acid': aircraft_id, 'hdg': heading}
    resp = requests.post(url, json=json)
    resp.raise_for_status()
    return True

def change_speed(aircraft_id, speed):
    """
    Change aircraft speed.
    """
    assert utils._check_string_input(aircraft_id), 'Invalid input {} for aircraft id'.format(aircraft_id)
    assert utils._check_speed(speed), 'Invalid input {} for speed'

    endpoint = config_param('endpoint_change_speed')
    url = utils.construct_endpoint_url(endpoint)

    json = {'acid': aircraft_id, 'spd': speed}
    resp = requests.post(url, json=json)
    resp.raise_for_status()
    return True

def change_vertical_speed(aircraft_id, vertical_speed):
    """
    Change aircraft vertical speed.
    """
    assert utils._check_string_input(aircraft_id), 'Invalid input {} for aircraft id'.format(aircraft_id)
    assert utils._check_speed(vertical_speed), 'Invalid input {} for vertical speed'

    endpoint = config_param('endpoint_change_vertical_speed')
    url = utils.construct_endpoint_url(endpoint)

    json = {'acid': aircraft_id, 'vspd': vertical_speed}
    resp = requests.post(url, json=json)
    resp.raise_for_status()
    return True
