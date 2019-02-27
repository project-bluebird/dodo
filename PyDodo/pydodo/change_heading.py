
from . import settings
from . import utils

endpoint = settings.default['endpoint_change_heading']
url = utils.construct_endpoint_url(endpoint)

def change_heading(aircraft_id, heading):
    """
    Change aircraft heading, raise error if inputs are invalid or not successful
    """
    assert utils._check_string_input(aircraft_id), 'Invalid input {} for aircraft id'.format(aircraft_id)
    assert utils._check_heading(heading), 'Invalid input {} for heading'

    json = {'acid': aircraft_id, 'hdg': heading}

    resp = requests.post(url, json=json)

    # if response is 4XX or 5XX, raise exception
    resp.raise_for_status()
    return True
