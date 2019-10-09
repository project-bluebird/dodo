import requests

from .config_param import config_param


def post_request(endpoint, body=None):
    """
    Make a POST requests to the BlueBird API.

    Parameters
    ----------
    endpoint : str
        The Bluebird API endpoing to call.
    body : str
        A dictionary.

    Returns
    -------
    TRUE if successful. Otherwise an exception is thrown.

    Examples
    --------
    >>> endpoint = pydodo.config_param.config_param("endpoint_create_aircraft")
    >>> body = {"acid"="BAW123", "type"="B744", "lat"=0, "lon"=0, "hdg"=0, "alt"=20000, "spd"=240}
    >>> pydodo.utils.post_request(endpoint = endpoint, body = body)
    """
    url = construct_endpoint_url(endpoint)
    resp = requests.post(url, json=body)
    # if response is 4XX or 5XX, raise exception
    resp.raise_for_status()
    return True


def construct_endpoint_url(endpoint):
    """
    Construct a BlueBird endpoint URL.

    Parameters
    ----------
    endpoint : str
        The Bluebird API endpoing to call.

    Returns
    -------
    str
        BlueBird endpoint URL.

    Examples
    --------
    >>> pydodo.utils.construct_endpoint_url(endpoint = "ic")
    """
    return "{0}/{1}/{2}/{3}".format(
        get_bluebird_url(),
        config_param("api_path"),
        config_param("api_version"),
        endpoint,
    )


def get_bluebird_url():
    """
    Get the URL of the BlueBird API.

    Parameters
    ----------
    NONE

    Returns
    -------
    str
        BlueBird URL.

    Examples
    --------
    >>> pydodo.utils.get_bluebird_url()
    """
    return "http://{}:{}".format(config_param("host"), config_param("port"))


def ping_bluebird():
    """
    Check communication with BlueBird.

    Parameters
    ----------
    NONE

    Returns
    -------
    boolean
        TRUE indicates that a request to the BlueBird URL was successful.

    Examples
    --------
    >>> pydodo.utils.ping_bluebird()
    """
    endpoint = config_param("endpoint_aircraft_position")

    url = construct_endpoint_url(endpoint)
    print("ping bluebird on {}".format(url))

    # /pos endpoint only supports GET requests, this should return an error if BlueBird is running
    # on the specified host
    try:
        resp = requests.post(url)
    except requests.exceptions.ConnectionError as e:
        print(e)
        return False

    if resp.status_code == 405:
        return True
    return False


def _validate_latitude(lat):
    """Assert latitude is in the range ``[-90, 90]``."""
    assert abs(lat) <= 90, "Invalid value {} for latitude".format(lat)


def _validate_longitude(lon):
    """Assert longitude is in the range ``[-180, 180)``."""
    assert -180 <= lon < 180, "Invalid value {} for longitude".format(lon)


def _validate_heading(hdg):
    """Assert heading is in the range ``[0, 360)``."""
    assert 0 <= hdg < 360, "Invalid value {} for heading".format(hdg)


def _validate_speed(spd):
    """Assert speed is non-negative."""
    assert spd >= 0, "Invalid value {} for speed".format(spd)


def _validate_string(input, param_name):
    """Assert input is a non-empty string."""
    assert input and type(input) == str, "Invalid input {} for {}".format(input, param_name)


def _validate_id(aircraft_id):
    """Assert aircraft_id is non-empty string (and length >= 3 if using BlueSky)."""
    if config_param("simulator") == config_param("bluesky_simulator"):
        assert (
            isinstance(aircraft_id, str) and len(aircraft_id) >= 3
        ), "Invalid input {} for aircraft ID".format(aircraft_id)
    else:
        _validate_string(aircraft_id, "aircraft ID")


def _validate_id_list(aircraft_id):
    """
    Assert each aircraft_id in a list is non-empty string (and length >= 3
    if using BlueSky).
    """
    if isinstance(aircraft_id, str):
        _validate_id(aircraft_id)
    elif isinstance(aircraft_id, list) and bool(aircraft_id):
        for aircraft in aircraft_id:
            _validate_id(aircraft)


def _check_altitude(alt):
    """
    Assert alt (altitude) is non-negative and does not exceed the upper limit
    specified in config.
    """
    return 0 <= alt <= config_param("feet_altitude_upper_limit")


def _check_flight_level(fl):
    """
    Assert fl (flight level) is in the range [lower_limit, upper limit]
    specified in the config.
    """
    return fl >= config_param("flight_level_lower_limit") and fl <= config_param("flight_level_upper_limit")


def parse_alt(alt, fl):
    """
    Assert either alt (altitude) or fl (flight level) argument is given, but not
    both. Assert the provided value is a double in the correct range. Return the
    argument that is not None (if fl, return as string starting with "FL").
    """
    assert alt is None or fl is None, "Either altitude or flight level should be specified, not both."
    if alt is not None:
        assert _check_altitude(alt), "Invalid value {} for altitude".format(alt)
        alt = str(alt)
    else:
        assert fl is not None, "Must specify a valid altitude or a flight level"
        assert _check_flight_level(fl), "Invalid value {} for flight_level".format(fl)
        alt = "FL{}".format(fl)
    return alt


def _validate_multiplier(dtmult):
    """Assert dtmult is non-negative."""
    assert dtmult > 0, "Invalid value {} for multiplier".format(dtmult)


def _validate_is_positive(val, param_name):
    """Assert val is non-negative."""
    assert val >= 0, "Invalid value {} for {}".format(val, param_name)
