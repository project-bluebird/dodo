import requests

from .utils import construct_endpoint_url

def create_simulation(filename):
    """
    Load scenario from file and start the simulation.

    :param filename : A string, path to scenario file relative to BlueSkye root directory
    :return : A boolean, TRUE indicates success
    """
    endpoint = "ic"
    url = construct_endpoint_url(endpoint)
    resp = requests.post(url, json={"filename": filename})

    # code 418 is temporary
    if resp.status_code == 418:
        return True
    if resp.status_code == 202:
        return True
    return False
