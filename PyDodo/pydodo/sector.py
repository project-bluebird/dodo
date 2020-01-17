import json

from . import utils
from .post_request import post_request
from .config_param import config_param


def create_sector(filename, sector):
    """
    Create sector on the simulator host.

    Parameters
    ----------
    filename : str
        A string indicating path to sector geojson file on the local machine.
    sector : str
        A string indicating name to store sector under on the simulator host.

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Examples
    --------
    >>> pydodo.create_scenario(filename = "~/Documents/test_sector.geojson", sector = "test")
    """
    utils._validate_string(filename, "filename")
    utils._validate_string(sector, "sector")

    with open(filename, "r") as f:
        content = json.load(f)

    body = {"name": sector, "content": content}
    return post_request(config_param("endpoint_create_sector"), body)
