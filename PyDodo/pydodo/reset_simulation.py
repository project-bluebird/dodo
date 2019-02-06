from .utils import construct_endpoint_url
import requests

def reset_simulation():
    endpoint = "ic"
    url = construct_endpoint_url(endpoint)
    r = requests.post(url)

    if r.status_code == 418:
        return True
    if r.status_code == 202:
        return True
