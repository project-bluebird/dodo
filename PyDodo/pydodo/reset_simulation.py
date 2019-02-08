import requests

from .utils import construct_endpoint_url

def reset_simulation():
    endpoint = "ic"
    url = construct_endpoint_url(endpoint)
    resp = requests.post(url)

    if resp.status_code == 418:
        return True
    if resp.status_code == 202:
        return True
