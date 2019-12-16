import sys
import requests

from .config_param import config_param

_BB_HOST = config_param("host")
_BB_PORT = config_param("port")
_BB_API_VERSION = config_param("api_version")


def bluebird_config(
    host=config_param("host"),
    port=config_param("port"),
    version=config_param("api_version")
    ):
    """
    Set BlueBird host, port and version parameters.
    Default values are taken from the config file.

    Parameters
    ----------
    host : str
        BlueBird host (e.g., 'localhost' or '0.0.0.0').
    port : int
        BlueBird port (e.g., 5001).
    version : str
        BlueBird version (e.g., 'v1' or 'v2')
    """

    this_module = sys.modules[__name__]
    setattr(this_module, "_BB_HOST", host)
    setattr(this_module, "_BB_PORT", port)
    setattr(this_module, "_BB_API_VERSION", version)
    return True


def get_bluebird_url():
    """
    Get the URL of the BlueBird API.

    Parameters
    ----------
    NONE

    Returns
    -------
    str
        BlueBird URL.

    Examples
    --------
    >>> pydodo.utils.get_bluebird_url()
    """
    return "http://{}:{}".format(_BB_HOST, _BB_PORT)


def construct_endpoint_url(endpoint):
    """
    Construct a BlueBird endpoint URL.

    Parameters
    ----------
    endpoint : str
        The Bluebird API endpoing to call.

    Returns
    -------
    str
        BlueBird endpoint URL.

    Examples
    --------
    >>> pydodo.utils.construct_endpoint_url(endpoint = "ic")
    """
    return "{0}/{1}/{2}/{3}".format(
        get_bluebird_url(),
        config_param("api_path"),
        _BB_API_VERSION,
        endpoint,
    )


def ping_bluebird():
    """
    Check communication with BlueBird.

    Parameters
    ----------
    NONE

    Returns
    -------
    boolean
        TRUE indicates that a request to the BlueBird URL was successful.

    Examples
    --------
    >>> pydodo.bluebird_connect.ping_bluebird()
    """
    endpoint = config_param("endpoint_aircraft_position")

    url = construct_endpoint_url(endpoint)
    print("ping bluebird on {}".format(url))

    # /pos endpoint only supports GET requests, this should return an error if BlueBird is running
    # on the specified host
    try:
        resp = requests.post(url)
    except requests.exceptions.ConnectionError as e:
        print(e)
        return False

    if resp.status_code == 405:
        return True
    return False
