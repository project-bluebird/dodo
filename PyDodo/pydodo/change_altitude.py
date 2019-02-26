
from . import settings
from . import utils

endpoint = settings.default['endpoint_change_altitude']
url = utils.construct_endpoint_url(endpoint)

def change_altitude(aircraft_id, altitude=None, flight_level=None, vertical_speed=None):
    """
    Change aircraft altitude, raise error if inputs are invalid or not successful
    """
    assert utils._check_string_input(aircraft_id), 'Invalid input {} for aircraft id'.format(aircraft_id)
    assert altitude is None or flight_level is None, 'Only altitude or flight level should be provided, not both'
    alt = utils.parse_alt(altitude, flight_level)

    json = {'acid': aircraft_id, 'alt': alt}

    if vertical_speed:
        assert utils._check_speed(vertical_speed), 'Invalid input {} for vertical speed'.format(vertical_speed)
        json['vs'] = vertical_speed

    resp = requests.post(url, json=json)

    # if response is 4XX or 5XX, raise exception
    resp.raise_for_status()
    return True
