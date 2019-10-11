import json
import requests

import numpy as np

from . import utils
from .utils import construct_endpoint_url
from .config_param import config_param

endpoint = config_param("endpoint_metrics")
url = construct_endpoint_url(endpoint)


def loss_of_separation(from_aircraft_id, to_aircraft_id):
    """
    Get loss of separation score between two aircraft.

    Parameters
    ----------
    from_aircraft_id: str
        A string aircraft identifier.
    to_aircraft_id: str
        A string aircraft identifier.

    Returns
    -------
    double
        A loss of separation score between two aircraft (NaN if one of the
        aircraft IDs does not exist in the simulation).

    Notes
    -----
    If an invalid ID is given, or the call to Bluebird fails, an exception is
    thrown.

    Examples
    --------
    >>> pydodo.loss_of_separation('BAW123', 'KLM456')
    """
    utils._validate_id(from_aircraft_id)
    utils._validate_id(to_aircraft_id)

    resp = requests.get(
        url,
        params={
            "name": "aircraft_separation",
            "args": "{},{}".format(from_aircraft_id, to_aircraft_id),
        },
    )
    if resp.status_code == 200:
        json_data = json.loads(resp.text)
        score = json_data["aircraft_separation"]
    elif resp.status_code == config_param("status_code_no_aircraft_found"):
        score = np.nan
    else:
        raise requests.HTTPError(resp.text)
    return score
