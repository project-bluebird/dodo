import requests

from .config_param import config_param


def post_request(endpoint, body=None):
    """
    Common format for POST requests to BlueBird.
    """
    url = construct_endpoint_url(endpoint)
    resp = requests.post(url, json=body)
    # if response is 4XX or 5XX, raise exception
    resp.raise_for_status()
    return True


def construct_endpoint_url(endpoint):
    return "{0}/{1}/{2}/{3}".format(
        get_bluebird_url(),
        config_param("api_path"),
        config_param("api_version"),
        endpoint,
    )


def get_bluebird_url():
    return "http://{}:{}".format(config_param("host"), config_param("port"))


def ping_bluebird():
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
    """Validate that input is a non-empty string"""
    assert input and type(input) == str, "Invalid input {} for {}".format(input, param)


def _validate_id(aircraft_id):
    """Validate aircraft_id is non-empty string (and length >= 3 if using bluesky)"""
    if config_param("simulator") == config_param("bluesky_simulator"):
        assert (
            type(aircraft_id) == str and len(aircraft_id) >= 3
        ), "Invalid input {} for aircraft ID".format(aircraft_id)
    else:
        _validate_string(aircraft_id, "aircraft ID")


def _validate_altitude(alt):
    return 0 <= alt <= config_param("feet_altitude_upper_limit")


def _validate_flight_level(fl):
    return fl >= config_param("flight_level_lower_limit")


def parse_alt(alt, fl):
    if alt is not None:
        assert _validate_altitude(alt), "Invalid value {} for altitude".format(alt)
        alt = str(alt)
    else:
        assert fl is not None, "Must specify a valid altitude or a flight level"
        assert _validate_flight_level(fl), "Invalid value {} for flight_level".format(fl)
        alt = "FL{}".format(fl)
    return alt


def _validate_multiplier(dtmult):
    assert dtmult > 0, "Invalid value {} for multiplier".format(dtmult)

