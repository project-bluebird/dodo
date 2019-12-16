from .config_param import config_param


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
    assert input and isinstance(input, str), "Invalid input {} for {}".format(
        input, param_name
    )


def _validate_id(aircraft_id):
    """Assert aircraft_id is non-empty string (and length >= 3 if using BlueSky)."""
    _validate_string(aircraft_id, "aircraft ID")
    if config_param("simulator") == config_param("bluesky_simulator"):
        assert (
            len(aircraft_id) >= 3,
            "Invalid input {} for aircraft ID".format(aircraft_id),
        )


def _validate_id_list(aircraft_id):
    """
    Assert each aircraft_id in a list is non-empty string (and length >= 3
    if using BlueSky).
    """
    assert isinstance(aircraft_id, str) or (
        isinstance(aircraft_id, list) and bool(aircraft_id)
    ), "Invalid input {} for aircraft ID".format(aircraft_id)
    if isinstance(aircraft_id, str):
        _validate_id(aircraft_id)
    elif isinstance(aircraft_id, list):
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
    return fl >= config_param("flight_level_lower_limit") and fl <= config_param(
        "flight_level_upper_limit"
    )


def _parse_alt(alt, fl):
    """
    Assert either alt (altitude) or fl (flight level) argument is given, but not
    both. Assert the provided value is a double in the correct range. Return the
    argument that is not None (if fl, return as string starting with "FL").
    """
    assert (
        alt is None or fl is None
    ), "Either altitude or flight level should be specified, not both."
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
