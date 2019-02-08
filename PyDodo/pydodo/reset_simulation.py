import requests

from .utils import construct_endpoint_url

def reset_simulation():
    """
    Reset the simulation.

    :return : boolean, TRUE indicates success
    """
    endpoint = "ic"
    url = construct_endpoint_url(endpoint)
    resp = requests.post(url)

    # code 418 is temporary
    if resp.status_code == 418:
        return True
    if resp.status_code == 202:
        return True
    return False
