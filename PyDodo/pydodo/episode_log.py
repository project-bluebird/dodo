import requests
import json
import os

from . import utils
from .utils import post_request
from .config_param import config_param


def episode_log():
    """
    Get the episode log and save to file in the working directory in a ``logs`` subdirectory.

    Parameters
    ----------
    NONE

    Returns
    -------
    log : str
        A string, the relative path to the log file. An exception is thrown if
        an error occurs.

    Examples
    --------
    >>> pydodo.episode_log()
    """
    endpoint = config_param("endpoint_episode_log")
    url = utils.construct_endpoint_url(endpoint)

    resp = requests.get(url)
    resp.raise_for_status()

    content = json.loads(resp.text)
    ep_log = content["lines"]
    file_path = content["cur_ep_file"].split("bluebird/")[-1]
    directory = "/".join(file_path.split("/")[:-1])

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_path, 'w') as f:
        f.writelines(ep_log)

    return file_path
