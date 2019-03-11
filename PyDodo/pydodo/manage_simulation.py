import requests

from .config_param import config_param
from .utils import construct_endpoint_url

def post_request(param):
    """
    Common format for posting simulation request to BlueBird.
    """
    endpoint = config_param(param)
    url = construct_endpoint_url(endpoint)
    resp = requests.post(url)

    # if response is 4XX or 5XX, raise exception
    resp.raise_for_status()
    return True

def reset_simulation():
    """
    Reset the simulation.
    """
    return post_request('endpoint_reset_simulation')

def pause_simulation():
    """
    Pause the simulation.
    """
    return post_request('endpoint_pause_simulation')

def resume_simulation():
    """
    Resume the simulation.
    """
    return post_request('endpoint_resume_simulation')
