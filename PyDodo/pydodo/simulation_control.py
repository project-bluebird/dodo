import requests

from . import utils
from .utils import post_request
from .config_param import config_param


def load_scenario(scenario, multiplier=1.0):
    """
    Load scenario from file and start the simulation.

    :param filename : A string, path to scenario file
    :return :
    """
    utils._validate_string(scenario, "file path")
    utils._validate_multiplier(multiplier)

    body = {"filename": scenario, "multiplier": multiplier}
    return post_request(config_param("endpoint_load_scenario"), body)


def reset_simulation():
    """
    Reset the simulation.
    """
    return post_request(config_param("endpoint_reset_simulation"))


def pause_simulation():
    """
    Pause the simulation.
    """
    return post_request(config_param("endpoint_pause_simulation"))


def resume_simulation():
    """
    Resume the simulation.
    """
    return post_request(config_param("endpoint_resume_simulation"))


def set_simulation_rate_multiplier(multiplier):
    utils._validate_multiplier(multiplier)

    body = {"multiplier": multiplier}
    return post_request(config_param("endpoint_set_simulation_rate_multiplier"), body)
