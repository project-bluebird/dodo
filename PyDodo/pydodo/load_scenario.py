import requests

from . import settings
from .utils import construct_endpoint_url

endpoint = settings.default['endpoint_load_scenario']

def load_scenario(filename):
    """
    Load scenario from file and start the simulation.

    :param filename : A string, path to scenario file relative to BlueSkye root directory
    :return : A boolean, TRUE indicates success
    """

    url = construct_endpoint_url(endpoint)
    resp = requests.post(url, json={"filename": filename})

    if resp.status_code == 200:
        return True
    return False
