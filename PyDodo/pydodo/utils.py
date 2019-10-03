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
    ----------
    TRUE if successful. Otherwise an exception is thrown.

    Examples
    ----------
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
    ----------
    str
        BlueBird endpoint URL.

    Examples
    ----------
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
    ----------
    str
        BlueBird URL.

    Examples
    ----------
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
    ----------
    boolean
        TRUE indicates that a request to the BlueBird URL was successful.

    Examples
    ----------
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
    assert abs(lat) <= 90, "Invalid value {} for latitude".format(lat)


def _validate_longitude(lon):
    assert -180 <= lon < 180, "Invalid value {} for longitude".format(lon)


def _validate_heading(hdg):
    assert 0 <= hdg < 360, "Invalid value {} for heading".format(hdg)


def _validate_speed(spd):
    assert spd >= 0, "Invalid value {} for speed".format(spd)


def _validate_string(input, param):
    #Validate that input for param is a non-empty string
    assert input and type(input) == str, "Invalid input {} for {}".format(input, param)


def _validate_id(aircraft_id):
    #Validate aircraft_id is non-empty string (and length >= 3 if using BlueSky)
    if config_param("simulator") == config_param("bluesky_simulator"):
        assert (
            isinstance(aircraft_id, str) and len(aircraft_id) >= 3
        ), "Invalid input {} for aircraft ID".format(aircraft_id)
    else:
        _validate_string(aircraft_id, "aircraft ID")


def _validate_id_list(aircraft_id):
    #Validate string list of aircraft IDs.
    if isinstance(aircraft_id, str):
        _validate_id(aircraft_id)
    elif isinstance(aircraft_id, list) and bool(aircraft_id):
        for aircraft in aircraft_id:
            _validate_id(aircraft)


def _check_altitude(alt):
    return 0 <= alt <= config_param("feet_altitude_upper_limit")


def _check_flight_level(fl):
    return fl >= config_param("flight_level_lower_limit") and fl <= config_param("flight_level_upper_limit")


def parse_alt(alt, fl):
    # Check only altitude or flight level is given & values are within limits
    assert alt is None or fl is None, "Either altitude or flight level should be specified, not both."
    if alt is not None:
        assert _check_altitude(alt), "Invalid value {} for altitude".format(alt)
        alt = str(alt)
    else:
        # return flight level in correct string format
        assert fl is not None, "Must specify a valid altitude or a flight level"
        assert _check_flight_level(fl), "Invalid value {} for flight_level".format(fl)
        alt = "FL{}".format(fl)
    return alt


def _validate_multiplier(dtmult):
    assert dtmult > 0, "Invalid value {} for multiplier".format(dtmult)


def _validate_is_positive(val, measure):
    #Validate that input val for measure is non negative.
    assert val >= 0, "Invalid value {} for {}".format(val, measure)
