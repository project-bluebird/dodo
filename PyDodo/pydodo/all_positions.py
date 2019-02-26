"""
Get position information for all aircraft in simulation

Return aircraft positions as pandas dataframe.
"""

import requests
import json
import numpy as np
import pandas as pd

from . import settings
from . import utils

endpoint = settings.default['endpoint_aircraft_position']
url = utils.construct_endpoint_url(endpoint)

def format_output(aircraft_pos):
    """
    Format aircraft position dictionary returned by bluebird.
    """
    position_formatted = {
        "altitude":aircraft_pos["alt"],
        "ground_speed":aircraft_pos["gs"],
        "latitude":aircraft_pos["lat"],
        "longitude":aircraft_pos["lon"],
        "vertical_speed":aircraft_pos["vs"]
    }
    return position_formatted

def all_positions():
    """
    Get position dictionary for all aircraft.
    """
    resp = requests.get(url, params={"acid": "all"})

    # if response other than 200, raise
    resp.raise_for_status()

    json_data = json.loads(resp.text)
    pos_data = {aircraft:format_output(json_data[aircraft]) for aircraft in json_data.keys()}
    pos_dict = pd.DataFrame.from_dict(pos_data, orient='index')
    return pos_dict
