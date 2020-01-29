import json

from . import utils
from .post_request import post_request
from .config_param import config_param


def upload_sector(filename, sector_name):
    """
    Upload sector to the simulator host.

    Parameters
    ----------
    filename : str
        A string indicating path to sector geojson file on the local machine.
    sector_name : str
        A string indicating name to store sector under on the simulator host.

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Examples
    --------
    >>> pydodo.upload_sector(filename = "~/Documents/test_sector.geojson", sector_name = "test_sector")
    """
    utils._validate_string(filename, "filename")
    utils._validate_string(sector_name, "sector_name")

    with open(filename, "r") as f:
        content = json.load(f)

    body = {"name": sector_name, "content": content}
    return post_request(config_param("endpoint_upload_sector"), body)
