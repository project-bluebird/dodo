from . import utils
from .utils import post_request
from .config_param import config_param


def create_scenario(filename, scenario):
    """
    Create scenario file on the simulator host.

    :param filename: A string, path to scenario file on local machine.
    :param scenario: A string, name of file to store scenario under on the simulator host.
    :return :
    """
    utils._validate_string(filename, "filename")
    utils._validate_string(scenario, "scenario")

    content = [line.rstrip('\n') for line in open(filename)]

    body = {"scn_name": scenario, "content": content}
    return post_request(config_param("endpoint_create_scenario"), body)


def load_scenario(scenario, multiplier=1.0):
    """
    Load scenario and start the simulation.
    The scenario must exist on the simulator host.

    Parameters
    ----------
    filename : str
        A string that contains the path to where the scenario file is located
    multiplier : double
        ...

    Returns
    -------
        ...

    Examples
    --------
    >>> pydodo.create_aircraft.load_scenario()
    >>>

    """
    utils._validate_string(scenario, "scenario")
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


def set_simulator_mode(mode):
    assert mode == 'agent' or mode == 'sandbox', 'Invalid value {} for mode'.format(mode)

    body = {"mode": mode}
    return post_request(config_param("endpoint_simulator_mode"), body)


def simulation_step():
    return post_request(config_param("endpoint_simulation_step"))
