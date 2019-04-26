import requests
import asyncio
import aiohttp

from . import utils
from .utils import construct_endpoint_url, post_request
from .config_param import config_param


def batch(commands):
    """
    Execute list of aircraft control commands asynchronously.

    :param commands: list of aircraft control commands to execute
    :returns: list of results (either True or Exception for each command)
    """
    if type(commands) != list:
        futures = [commands]
    else:
        futures = commands

    loop = asyncio.get_event_loop()
    tasks = asyncio.gather(*futures, return_exceptions=True)
    results = loop.run_until_complete(tasks)
    loop.close()
    return results


async def async_change_altitude(aircraft_id, altitude=None, flight_level=None, vertical_speed=None):
    """
    Change aircraft altitude.
    """
    utils._validate_id(aircraft_id)
    assert (
        altitude is None or flight_level is None
    ), "Only altitude or flight level should be provided, not both"
    alt = utils.parse_alt(altitude, flight_level)

    json = {config_param("query_aircraft_id"): aircraft_id, "alt": alt}

    if vertical_speed:
        utils._validate_speed(vertical_speed)
        json["vs"] = vertical_speed

    async with aiohttp.ClientSession(raise_for_status=True) as session:
        url = construct_endpoint_url(config_param("endpoint_change_altitude"))
        async with session.post(url, json=json) as response:
            return True


async def async_change_heading(aircraft_id, heading):
    """
    Change aircraft heading.
    """
    utils._validate_id(aircraft_id)
    utils._validate_heading(heading)

    json = {config_param("query_aircraft_id"): aircraft_id, "hdg": heading}
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        url = construct_endpoint_url(config_param("endpoint_change_heading"))
        async with session.post(url, json=json) as response:
            return True
