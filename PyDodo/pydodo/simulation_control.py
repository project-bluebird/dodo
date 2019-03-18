import requests

from .utils import post_request
from .config_param import config_param


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
    assert multiplier > 0, "Invalid value {} for multiplier".format(multiplier)

    json = {"multiplier": multiplier}
    return post_request(config_param("endpoint_set_simulation_rate_multiplier", json))
