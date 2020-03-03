import requests
import json

from .bluebird_connect import construct_endpoint_url
from .config_param import config_param


def simulation_info():
    """
    Get the simulation info from BlueBird.

    Parameters
    ----------
    NONE

    Returns
    -------
    dict :
        A dictionary with keys:

        ``"aircraft_ids"``:
        A list of strings of (identifiers of aircraft currently in the simulation).

        ``"dt"``:
        A positive double, the step size of the underlying simulation physics model.

        ``"mode"``:
        The simulator mode. See [bluebird docs](https://github.com/alan-turing-institute/bluebird/blob/develop/docs/SimulatorModes.md)
        for more information.

        ``"scenario_name"``:
        A string name of the current scenario. None if no sector is loaded.

        ``"scenario_time"``:
        A positive double, the number of seconds since the start of the scenario.

        ``"sector_name"``:
        A string name of the current sector. None if no sector is loaded.

        ``"seed"``:
        A 32-bit int. The random seed of the simulator (if set).

        ``"sim_type"``:
        A string, the name of the simulator running (e.g., BlueSky).

        ``"speed"``:
        A positive double, the speed of the current simulation. The default value
        of 1 corresponds to real-time operation. If set to another value, the
        simulation will run faster (or slower) than real-time (e.g., speed of 2
        corresponds to simulation running twice as fast).

        ``"state"``:
        A string describing state of the simulator (INIT, HOLD, RUN or END).

        ``"utc_datetime":
        UTC datetime.

    Examples
    --------
    >>> pydodo.simulation_info()
    """
    endpoint = config_param("endpoint_simulation_info")
    url = construct_endpoint_url(endpoint)

    resp = requests.get(url)
    resp.raise_for_status()

    info = json.loads(resp.text)
    info["aircraft_ids"] = info.pop("callsigns")

    return info
