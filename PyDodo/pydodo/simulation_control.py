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
    utils._validate_string(filename, "file path")
    utils._validate_multiplier(multiplier)

    body = {"filename": filename, "multiplier": multiplier}
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


def define_waypoint(waypoint_name, latitude, longitude, waypoint_type=None):
    """
    Define a custom waypoint.
    """
    utils._validate_string(waypoint_name, "waypoint name")
    utils._validate_latitude(latitude)
    utils._validate_longitude(longitude)

    body = {"wpname": waypoint_name, "lat": latitude, "lon": longitude}
    if waypoint_type != None:
        utils._validate_string(waypoint_type, "waypoint type")
        body["type"] = waypoint_type

    return post_request(config_param("endpoint_define_waypoint"), body)
