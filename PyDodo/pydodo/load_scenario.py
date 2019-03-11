import requests

from . import settings
from .utils import construct_endpoint_url

endpoint = settings.default['endpoint_load_scenario']

def load_scenario(filename):
    """
    Load scenario from file and start the simulation.

    :param filename : A string, path to scenario file
    :return : 
    """
    assert filename, "Must provide scenario file path"

    url = construct_endpoint_url(endpoint)
    resp = requests.post(url, json={"filename": filename})

    # if response is 4XX or 5XX, raise exception
    resp.raise_for_status()
    return True
