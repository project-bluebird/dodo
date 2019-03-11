import requests

from .config_param import config_param
from .utils import construct_endpoint_url

endpoint = config_param('endpoint_reset_simulation')

def reset_simulation():
    """
    Reset the simulation.
    """
    url = construct_endpoint_url(endpoint)
    resp = requests.post(url)

    # if response is 4XX or 5XX, raise exception
    resp.raise_for_status()
    return True
