import requests

from .config_param import config_param
from .utils import post_request


def load_scenario(filename):
    """
    Load scenario from file and start the simulation.

    :param filename : A string, path to scenario file
    :return :
    """
    assert filename, "Must provide scenario file path"

    json={"filename": filename}
    return post_request(config_param('endpoint_load_scenario'), json)
