from . import utils
from .post_request import post_request
from .config_param import config_param


def create_aircraft(
    aircraft_id,
    type,
    latitude,
    longitude,
    heading,
    speed,
    altitude=None,
    flight_level=None,
):

    """
    Create new aircraft

    Parameters
    ----------
    aircraft_id : str
        A string aircraft identifier. For the BlueSky simulator, this has to be
        at least three characters.
    type : str
        A string ICAO aircraft type designator.
    latitude : double
        A double in the range ``[-90, 90]``. The aircraft's initial latitude.
    longitude : double
        A double in the range ``[-180, 180)``. The aircraft's initial longitude.
    heading : double
        A double in the range ``[0, 360)``. The aircraft's initial heading in
        degrees.
    altitude : double
        A double in the range ``[0, 6000]``. The aircraft's initial altitude in
        feet. For altitudes in excess of 6000ft a flight level should be
        specified instead.
    flight_level : int
        An integer of 60 or more. The aircraft's initial flight level.
    speed : double
        A non-negative double. The aircraft's initial calibrated air speed in
        knots (KCAS).

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Raises
    ------
    Exception
        Raises error if inputs are invalid or if aircraft already exists.

    Notes
    -----
    Either the altitude or flight_level argument must be given, but not both.

    Examples
    --------
    >>> pydodo.create_aircraft("BAW123", "B744", 0, 0, 0, flight_level = 250, speed = 200)
    """

    utils._validate_id(aircraft_id)
    utils._validate_string(type, "aircraft type")
    utils._validate_latitude(latitude)
    utils._validate_longitude(longitude)
    utils._validate_heading(heading)
    utils._validate_speed(speed)

    assert (
        altitude is None or flight_level is None
    ), "Only altitude or flight level should be provided, not both"
    alt = utils.parse_alt(altitude, flight_level)

    body = {
        "acid": aircraft_id,
        "type": type,
        "lat": latitude,
        "lon": longitude,
        "hdg": heading,
        "alt": alt,
        "spd": speed,
    }

    return post_request(config_param("endpoint_create_aircraft"), body)
