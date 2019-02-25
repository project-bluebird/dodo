import requests

from . import settings
from .utils import construct_endpoint_url

endpoint = settings.default['endpoint_reset_simulation']

def reset_simulation():
    """
    Reset the simulation.

    :return : boolean, TRUE indicates success
    """
    url = construct_endpoint_url(endpoint)
    resp = requests.post(url)

    if resp.status_code == 200:
        return True
    return False
