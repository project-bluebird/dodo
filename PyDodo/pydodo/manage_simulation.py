import requests

from .utils import post_request


def reset_simulation():
    """
    Reset the simulation.
    """
    return post_request('endpoint_reset_simulation')


def pause_simulation():
    """
    Pause the simulation.
    """
    return post_request('endpoint_pause_simulation')


def resume_simulation():
    """
    Resume the simulation.
    """
    return post_request('endpoint_resume_simulation')


def set_simulation_rate_multiplier(multiplier):
    assert multiplier > 0, 'Invalid value {} for multiplier'.format(multiplier)

    json = {'multiplier': multiplier}
    return post_request('endpoint_set_simulation_rate_multiplier', json)
