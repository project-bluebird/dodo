from . import utils
from .post_request import post_request
from .config_param import config_param


def create_scenario(filename, scenario):
    """
    Create scenario file on the simulator host.

    Parameters
    ----------
    filename : str
        A string indicating path to scenario file on the local machine.
    scenario : str
        A string indicating name to store scenario under on the simulator host
        (<scenario>.scn).

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Examples
    --------
    >>> pydodo.create_scenario(filename = "~/Documents/test_scenario.scn", scenario = "test")
    """
    utils._validate_string(filename, "filename")
    utils._validate_string(scenario, "scenario")

    content = [line.rstrip("\n") for line in open(filename)]

    body = {"scn_name": scenario, "content": content}
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


def reset_simulation():
    """
    Reset simulation to the start of the currently running scenario.

    Parameters
    ----------
    NONE

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Examples
    --------
    >>> pydodo.reset_simulation()
    """
    return post_request(config_param("endpoint_reset_simulation"))


def pause_simulation():
    """
    Pause the simulation.

    Parameters
    ----------
    NONE

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Examples
    --------
    >>> pydodo.pause_simulation()
    """
    return post_request(config_param("endpoint_pause_simulation"))


def resume_simulation():
    """
    Resume the simulation after a pause

    Parameters
    ----------
    NONE

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Examples
    --------
    >>> pydodo.resume_simulation()
    """
    return post_request(config_param("endpoint_resume_simulation"))


def set_simulation_rate_multiplier(multiplier):
    """
    Sets the simulation rate multiplier for the current simulation. By default
    this multiplier is equal to one (real-time operation). If set to another
    value, the simulation will run faster (or slower) than real-time, with a
    fixed multiplier as provided. For example, a multiplier of 2 would cause the
    simulation to run twice as fast: 60 simulation minutes take 30 actual
    minutes.

    Parameters
    ----------
    multiplier : double
        A positive double.

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Examples
    --------
    >>> pydodo.set_simulation_rate_multiplier(2)
    >>> pydodo.set_simulation_rate_multiplier(0.5)
    """
    utils._validate_multiplier(multiplier)

    body = {"multiplier": multiplier}
    return post_request(config_param("endpoint_set_simulation_rate_multiplier"), body)


def simulation_step():
    """
    Step forward through the simulation. Step size is based on the simulation
    rate multiplier. Can only be used if simulator is in agent mode, otherwise
    an exception is thrown.

    Parameters
    ----------
    NONE

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Examples
    --------
    >>> pydodo.simulation_step()
    """
    return post_request(config_param("endpoint_simulation_step"))
