import requests

from .bluebird_connect import construct_endpoint_url

def post_request(endpoint, body=None):
    """
    Make a POST requests to the BlueBird API.

    Parameters
    ----------
    endpoint : str
        The Bluebird API endpoing to call.
    body : str
        A dictionary.

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Examples
    --------
    >>> endpoint = pydodo.config_param.config_param("endpoint_create_aircraft")
    >>> body = {"acid"="BAW123", "type"="B744", "lat"=0, "lon"=0, "hdg"=0, "alt"=20000, "spd"=240}
    >>> pydodo.utils.post_request(endpoint = endpoint, body = body)
    """
    url = construct_endpoint_url(endpoint)
    resp = requests.post(url, json=body)
    # if response is 4XX or 5XX, raise exception
    resp.raise_for_status()
    return True
