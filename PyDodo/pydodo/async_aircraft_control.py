import requests
import asyncio
import aiohttp

from concurrent.futures import ThreadPoolExecutor

from . import utils
from .utils import construct_endpoint_url
from .config_param import config_param


def batch(commands):
    """
    Send a batch of aircraft control commands and dispatch them asynchronously
    to Bluebird.

    Parameters
    ----------
    async_commands : list
        A list of aircraft control commands. In PyDodo, these need an ``async_``
        prefix. For example, ``batch([async_change_speed(...), async_change_altitude(...)]``.

    Returns
    -------
    TRUE if all commands were executed. Otherwise an exception is thrown.

    """

    if type(commands) != list:
        futures = [commands]
    else:
        futures = commands

    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    tasks = asyncio.gather(*futures, return_exceptions=True)
    results = loop.run_until_complete(tasks)
    loop.close()

    if results.count(True) == len(futures):
        return True
    else:
        raise Exception(";".join([str(resp) for resp in results if resp != True]))


async def async_change_altitude(aircraft_id, altitude=None, flight_level=None, vertical_speed=None):
    """
    Change aircraft altitude.

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.
    altitude : double, default=None
        A double in the range ``[0, 6000]``. The requested altitude in feet. For
        altitudes in excess of 6000ft a flight level should be specified
        instead.
    flight_level : int, default=None
        An integer of 60 or more. The requested flight level.
    vertical_speed : double, default=None [optional]

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Examples
    --------
    >>> pydodo.aircraft_control.change_altitude('BA1', ...)
    >>>
    """

    utils._validate_id(aircraft_id)
    assert (
        altitude is None or flight_level is None
    ), "Only altitude or flight level should be provided, not both"
    alt = utils.parse_alt(altitude, flight_level)

    body = {config_param("query_aircraft_id"): aircraft_id, "alt": alt}
    if vertical_speed:
        utils._validate_speed(vertical_speed)
        body["vs"] = vertical_speed
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        url = construct_endpoint_url(config_param("endpoint_change_altitude"))
        async with session.post(url, json=body) as response:
            return True


async def async_change_heading(aircraft_id, heading):
    """
    Change aircraft heading.

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.
    heading : double
        A double in the range ``[0, 360]``. The requested heading in degrees.

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Examples
    --------
    >>> pydodo.aircraft_control.change_heading('BA1', ...)
    >>>
    """

    utils._validate_id(aircraft_id)
    utils._validate_heading(heading)

    body = {config_param("query_aircraft_id"): aircraft_id, "hdg": heading}
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        url = construct_endpoint_url(config_param("endpoint_change_heading"))
        async with session.post(url, json=body) as response:
            return True


async def async_change_speed(aircraft_id, speed):
    """
    Change aircraft speed.

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.
    speed : double
        A non-negative double. The requested calibrated air speed in knots
        (KCAS).

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Examples
    --------
    >>> pydodo.aircraft_control.change_speed('BA1', ...)
    >>>
    """

    utils._validate_id(aircraft_id)
    utils._validate_speed(speed)

    body = {config_param("query_aircraft_id"): aircraft_id, "spd": speed}
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        url = construct_endpoint_url(config_param("endpoint_change_speed"))
        async with session.post(url, json=body) as response:
            return True


async def async_change_vertical_speed(aircraft_id, vertical_speed):
    """
    Change aircraft vertical speed.

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.
    vertical_speed : double
        A double. The requested vertical speed in feet/min (units according to
        BlueSky docs).

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Examples
    --------
    >>> pydodo.aircraft_control.change_vertical_speed('BA1', ...)
    >>>
    """

    utils._validate_id(aircraft_id)
    utils._validate_speed(vertical_speed)

    body = {config_param("query_aircraft_id"): aircraft_id, "vspd": vertical_speed}
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        url = construct_endpoint_url(config_param("endpoint_change_vertical_speed"))
        async with session.post(url, json=body) as response:
            return True


async def async_direct_to_waypoint(aircraft_id, waypoint_name):
    """
    Change aircraft heading toward a waypoint.

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.
    waypoint_name : str
        A string waypoint identifier. The waypoint to direct the aircraft to.

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Notes
    -----
    The waypoint must exist on the aircraft route.

    Examples
    --------
    >>> pydodo.aircraft_control.direct_to_waypoint('BA1', ...)
    >>>
    """

    utils._validate_id(aircraft_id)
    utils._validate_string(waypoint_name, "waypoint name")

    body = {config_param("query_aircraft_id"): aircraft_id, "waypoint": waypoint_name}
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        url = construct_endpoint_url(config_param("direct_to_waypoint"))
        async with session.post(url, json=body) as response:
            return True
