import requests
import json

from . import utils
from .utils import post_request
from .config_param import config_param


def episode_log(filename):
    """
    Get the episode log and save to file in the working directory.

    :param filename: A string indicating name of file to save episode log under.
    :return :
    """
    utils._validate_string(filename, "filename")

    endpoint = config_param("endpoint_episode_log")
    url = utils.construct_endpoint_url(endpoint)

    resp = requests.get(url)
    resp.raise_for_status()

    content = json.loads(resp.text)
    ep_log = content["lines"
    with open(f'{filename}.log', 'w') as f:
        f.writelines(ep_log)
    return True


def shutdown():
    """
    Shut down the BlueBird server.
    """
    return post_request(config_param("endpoint_shutdown"))
