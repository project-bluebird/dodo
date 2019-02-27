
from . import settings
from . import utils

endpoint = settings.default['endpoint_change_vertical_speed']
url = utils.construct_endpoint_url(endpoint)

def change_vertical_speed(aircraft_id, vertical_speed):
    """
    Change aircraft speed, raise error if inputs are invalid or not successful
    """
    assert utils._check_string_input(aircraft_id), 'Invalid input {} for aircraft id'.format(aircraft_id)
    assert utils._check_speed(vertical_speed), 'Invalid input {} for vertical speed'

    json = {'acid': aircraft_id, 'vspd': speed}

    resp = requests.post(url, json=json)

    # if response is 4XX or 5XX, raise exception
    resp.raise_for_status()
    return True
