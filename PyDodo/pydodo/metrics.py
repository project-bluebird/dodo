import json
import requests

import numpy as np

from . import utils
from .bluebird_connect import construct_endpoint_url
from .config_param import config_param

endpoint = config_param("endpoint_metrics")
url = construct_endpoint_url(endpoint)


def _metrics_call(metric, args):
    """
    Make a call to the BlueBird METRIC endpoint.

    Parameters
    ----------
    metric: str
        Name of the metric.
    args: str
        Arguments to pass to the metric function (aircraft_id or a pair of IDs).

    Returns
    -------
    double:
        Score returned by the metric (NaN if any of the aircraft specified in
        args does not exist in the simulation)
    """
    resp = requests.get(url, params={"name": metric, "args": args})
    if resp.status_code == 200:
        json_data = json.loads(resp.text)
        score = json_data[metric]
    elif resp.status_code == config_param("status_code_no_aircraft_found"):
        score = np.nan
    else:
        raise requests.HTTPError(resp.text)
    return score


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

    return _metrics_call(
        config_param("loss_of_separation"),
        "{},{}".format(from_aircraft_id, to_aircraft_id)
        )


def sector_exit(aircraft_id):
    """
    Return sector exit metric for aircraft.

    Parameters
    ----------
    aircraft_id: str
        A string aircraft identifier.

    Returns
    -------
    double
        A sector exit score for aircraft (NaN if the aircraft_id does not exist
        in the simulation or the aircraft has not yet exited sector).

    Notes
    -----
    If an invalid ID is given, or the call to Bluebird fails, an exception is
    thrown.

    Examples
    --------
    >>> pydodo.sector_exit('BAW123')
    """
    utils._validate_id(aircraft_id)

    return _metrics_call(config_param("sector_exit"), aircraft_id)
