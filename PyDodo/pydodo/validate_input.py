
from .config_param import config_param


def _check_latitude(lat):
    assert abs(lat) <= 90, "Invalid value {} for latitude".format(lat)


def _check_longitude(lon):
    assert -180 <= lon < 180, "Invalid value {} for longitude".format(lon)


def _check_heading(hdg):
    assert 0 <= hdg < 360, "Invalid value {} for heading".format(hdg)


def _check_speed(spd):
    assert spd >= 0, "Invalid value {} for speed".format(spd)


def _check_type_string(input, arg):
    """Check that input is a non-empty string"""
    assert type(input) == str and len(input) >= 1, "Invalid input {} for {}".format(
        input, arg
    )


def _check_altitude(alt):
    return 0 <= alt <= config_param("feet_altitude_upper_limit")


def _check_flight_level(fl):
    return fl >= config_param("flight_level_lower_limit")


def parse_alt(alt, fl):
    if alt is not None:
        assert _check_altitude(alt), "Invalid value {} for altitude".format(alt)
        alt = str(alt)
    else:
        assert fl is not None, "Must specify a valid altitude or a flight level"
        assert _check_flight_level(fl), "Invalid value {} for flight_level".format(fl)
        alt = "FL{}".format(fl)
    return alt


def _check_id_list(aircraft_id):
    """Check list of aircraft IDs"""
    assert bool(aircraft_id) and all(
        isinstance(elem, str) and len(elem) >= 1 for elem in aircraft_id
    ), "Invalid input for aircraft id in {}".format(aircraft_id)
