import json
import requests

from . import utils
from .utils import construct_endpoint_url
from .config_param import config_param

endpoint = config_param("endpoint_metrics")
url = construct_endpoint_url(endpoint)


def aircraft_separation(from_aircraft_id, to_aircraft_id):
    """
    Get aircraft separation score between two aircraft.

    Parameters
    ----------
    from_aircraft_id: str
        A string aircraft identifier.
    to_aircraft_id: str
        A string aircraft identifier.

    Returns
    -------
    double
        A separation score between two aircraft.

    Examples
    --------
    >>> pydodo.aircraft_separation('BAW123', 'BAW456')
    >>>
    """
    utils._validate_id(from_aircraft_id)
    utils._validate_id(to_aircraft_id)

    resp = requests.get(
        url,
        params={
            "name": "aircraft_separation",
            "args":f'{from_aircraft_id},{to_aircraft_id}'
        })
    resp.raise_for_status()
    json_data = json.loads(resp.text)
    return json_data['aircraft_separation']
