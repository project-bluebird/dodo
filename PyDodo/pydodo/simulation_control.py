from . import utils
from .post_request import post_request
from .config_param import config_param


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
