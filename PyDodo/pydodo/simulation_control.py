
import requests

from . import utils
from .utils import post_request
from .config_param import config_param


def load_scenario(filename, multiplier=1.0):
    """
    Load scenario from file and start the simulation.

    :param filename : A string, path to scenario file
    :return :
    """
    assert filename, "Must provide scenario file path"
    utils._check_multiplier(multiplier)

    json = {"filename": filename, "multiplier": multiplier}
    return post_request(config_param("endpoint_load_scenario"), json)


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
    utils._check_multiplier(multiplier)

    json = {"multiplier": multiplier}
    return post_request(config_param("endpoint_set_simulation_rate_multiplier"), json)


def define_waypoint(name, latitude, longitude, type=None):
    """
    Define a custom waypoint.
    """
    assert name, "Must provide waypoint name"
    utils._check_latitude(latitude)
    utils._check_longitude(longitude)

    json = {"wpname": name, "lat": latitude, "lon": longitude}
    if type != None:
        assert type and isinstance(type, str), "Invalid input {} for waypoint type".format(type)
        json["type"] = type

    return post_request(config_param("endpoint_define_waypoint"), json)
