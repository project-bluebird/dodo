import json

from . import utils
from .post_request import post_request
from .config_param import config_param


def create_scenario(filename, scenario):
    """
    Create scenario file on the simulator host.

    Parameters
    ----------
    filename : str
        A string indicating path to scenario json file on the local machine.
    scenario : str
        A string indicating name to store scenario under on the simulator host.

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Examples
    --------
    >>> pydodo.create_scenario(filename = "~/Documents/test_scenario.json", scenario = "test")
    """
    utils._validate_string(filename, "filename")
    utils._validate_string(scenario, "scenario")

    with open(filename, "r") as f:
        content = json.load(f)

    body = {"name": scenario, "content": content}
    return post_request(config_param("endpoint_create_scenario"), body)


def load_scenario(scenario, multiplier=1.0):
    """
    Load a scenario and start the simulation.

    Parameters
    ----------
    filename : str
        A string indicating name of scenario file on the simulator host
        (<scenario>.scn).
    multiplier : double
        An optional double. Simulation rate multiplier.

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Notes
    -----
    The scenario must exist on the simulator host.

    Examples
    --------
    >>> pydodo.load_scenario("test")
    """
    utils._validate_string(scenario, "scenario")
    utils._validate_multiplier(multiplier)

    body = {"filename": scenario, "multiplier": multiplier}
    return post_request(config_param("endpoint_load_scenario"), body)


def upload_scenario(filename, scenario_name):
    """
    Upload scenario to the simulator host.

    Parameters
    ----------
    filename : str
        A string indicating path to scenario json file on the local machine.
    scenario_name : str
        A string indicating name to store scenario under on the simulator host.

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Examples
    --------
    >>> pydodo.upload_scenario(filename = "~/Documents/test_scenario.json", scenario_name = "test_scenario")
    """
    utils._validate_string(filename, "filename")
    utils._validate_string(scenario_name, "scenario_name")

    with open(filename, "r") as f:
        content = json.load(f)

    body = {"name": scenario_name, "content": content}
    return post_request(config_param("endpoint_upload_scenario"), body)
