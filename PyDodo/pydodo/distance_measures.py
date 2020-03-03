import pandas as pd
import numpy as np
from geopy import distance
from scipy.spatial.distance import euclidean

from .config_param import config_param
from .request_position import aircraft_position
from . import utils

# Default for major (equatorial) radius and flattening are 'WGS-84' values.
major_semiaxis, minor_semiaxis, _FLATTENING = distance.ELLIPSOIDS["WGS-84"]
_EARTH_RADIUS = major_semiaxis * 1000  # convert to metres


def geodesic_distance(from_lat, from_lon, to_lat, to_lon, **kwargs):
    """
    Get geodesic distance between two (lat, lon) points in metres.

    Parameters
    ----------
    from_lat : double
        A double in the range ``[-90, 90]``. The `from` point's latitude.
    from_lon : double
        A double in the range ``[-180, 180)``. The `from` point's longitude.
    to_lat : double
        A double in the range ``[-90, 90]``. The `to` point's latitude.
    to_lon : double
        A double in the range ``[-180, 180)``. The `to` point's longitude.
    **kwargs:
        major_semiaxis : double, optional
            The major (equatorial) radius of the ellipsoid. The default value is for WGS84.
        flattening : double, optional
            Ellipsoid flattening. The default value is for WGS84.

    Returns
    -------
    geodesic_distance : double
        The geodesic distance between two points.

    Examples
    --------
    >>> >>> pydodo.geodesic_distance(from_lat = 51.5 , from_lon = 0.12, to_lat = 50.6, to_lon = -1.9)
    """
    major_semiaxis = (
        _EARTH_RADIUS if "major_semiaxis" not in kwargs else kwargs["major_semiaxis"]
    )
    flattening = _FLATTENING if "flattening" not in kwargs else kwargs["flattening"]

    utils._validate_latitude(from_lat)
    utils._validate_longitude(from_lon)
    utils._validate_latitude(to_lat)
    utils._validate_longitude(to_lon)
    utils._validate_is_positive(major_semiaxis, "major_semiaxis")
    utils._validate_is_positive(flattening, "flattening")

    # For GeoPy need to provide (major_semiaxis, minor_semiaxis, flattening) but
    # only major_semiaxis & flattening vals are used --> ignore minor_semiaxis
    return distance.geodesic(
        (from_lat, from_lon),
        (to_lat, to_lon),
        ellipsoid=(major_semiaxis / 1000, minor_semiaxis, flattening),  # convert to km
    ).meters


def great_circle_distance(from_lat, from_lon, to_lat, to_lon, **kwargs):
    """
    Get great-circle distance between two (lat, lon) points in metres.

    Parameters
    ----------
    from_lat : double
        A double in the range ``[-90, 90]``. The `from` point's latitude.
    from_lon : double
        A double in the range ``[-180, 180)``. The `from` point's longitude.
    to_lat : double
        A double in the range ``[-90, 90]``. The `to` point's latitude.
    to_lon : double
        A double in the range ``[-180, 180)``. The `to` point's longitude.
    **kwargs
        radius : double, optional
            The radius of the earth in metres. The default value is for WGS84.

    Returns
    -------
    great_circle_distance : double
        The great-circle distance between two points.

    Examples
    --------
    >>> pydodo.great_circle_distance(from_lat = 51.5 , from_lon = 0.12, to_lat = 50.6, to_lon = -1.9)
    """
    radius = _EARTH_RADIUS if "radius" not in kwargs else kwargs["radius"]

    utils._validate_latitude(from_lat)
    utils._validate_longitude(from_lon)
    utils._validate_latitude(to_lat)
    utils._validate_longitude(to_lon)
    utils._validate_is_positive(radius, "radius")

    return distance.great_circle(
        (from_lat, from_lon), (to_lat, to_lon), radius=radius / 1000  # convert to km
    ).meters


def vertical_distance(from_alt, to_alt, **kwargs):
    """
    Get vertical distance in metres between two altitudes (provided in metres).

    Parameters
    ----------
    from_alt : double
        A non-negatige double. The `from` point's altitude in metres.
    to_alt : double
        A non-negatige double. The `to` point's altitude in metres.

    Returns
    -------
    vertical_distance : double
        The verticle distance between two points.

    Examples
    --------
    >>> pydodo.vertical_distance(from_alt = 200, to_alt = 350)
    """
    utils._validate_is_positive(from_alt, "altitude")
    utils._validate_is_positive(to_alt, "altitude")

    return abs(from_alt - to_alt)


def _lla_to_ECEF(lat, lon, alt=0, radius=_EARTH_RADIUS, f=_FLATTENING):
    """
    Calculates ECEF coordinates of a point from lat, lon and alt.

    Parameters
    ----------

    lat : double

    lon : double

    alt : int
        Altitude in meters
    radius : double, optional
        Earth radius in metres (WGS84).
    f : double, optional
        Ellipsoidal flattening (WGS84).

    Returns
    -------
    (double, double, double)
        The (x, y, z) ECEF coordinates.

    Notes
    -----
    https://en.wikipedia.org/wiki/ECEF

    Examples
    --------
    >>> pydodo.distance_measures.lla_to_ECEF(lat = 51.5 , lon = 0.12, alt = 200)
    """

    lat_r = np.deg2rad(lat)
    lon_r = np.deg2rad(lon)

    e2 = 1 - (1 - f) * (1 - f)
    N = radius / np.sqrt(1 - e2 * np.power(np.sin(lat_r), 2))

    x = (N + alt) * np.cos(lat_r) * np.cos(lon_r)
    y = (N + alt) * np.cos(lat_r) * np.sin(lon_r)
    z = ((1 - e2) * N + alt) * np.sin(lat_r)

    return (x, y, z)


def euclidean_distance(from_lat, from_lon, from_alt, to_lat, to_lon, to_alt, **kwargs):
    """
    Get euclidean distance between two (lat, lon, alt) points in metres. The
    points are converted to ECEF coordinates to calculate distance.

    Parameters
    ----------
    from_lat : double
        A double in the range ``[-90, 90]``. The `from` point's latitude.
    from_lon : double
        A double in the range ``[-180, 180)``. The `from` point's longitude.
    from_alt : double
        A non-negatige double. The from point's altitude in metres.
    to_lat : double
         A double in the range ``[-90, 90]``. The `to` point's latitude.
    to_lon : double
        A double in the range ``[-180, 180)``. The `to` point's longitude.
    to_alt : double
        A non-negatige double. The `to` point's altitude in metres.
    **kwargs:
        major_semiaxis : double, optional
            The major (equatorial) radius of the ellipsoid. The default value is for WGS84.
        flattening : double, optional
            Ellipsoid flattening. The default value is for WGS84.

    Returns
    -------
    euclidean_distance : double
        The euclidean distance between two points.

    Notes
    -----
    https://en.wikipedia.org/wiki/ECEF

    Examples
    --------
    >>> pydodo.euclidean_distance(from_lat = 51.5 , from_lon = 0.12, from_alt = 200, to_lat = 50.6, to_lon = -1.9, to_alt = 350)
    """
    major_semiaxis = (
        _EARTH_RADIUS if "major_semiaxis" not in kwargs else kwargs["major_semiaxis"]
    )
    flattening = _FLATTENING if "flattening" not in kwargs else kwargs["flattening"]

    utils._validate_latitude(from_lat)
    utils._validate_longitude(from_lon)
    utils._validate_is_positive(from_alt, "altitude")
    utils._validate_latitude(to_lat)
    utils._validate_longitude(to_lon)
    utils._validate_is_positive(to_alt, "altitude")
    utils._validate_is_positive(major_semiaxis, " major_semiaxis")

    from_ECEF = _lla_to_ECEF(from_lat, from_lon, from_alt, major_semiaxis, flattening)
    to_ECEF = _lla_to_ECEF(to_lat, to_lon, to_alt, major_semiaxis, flattening)

    return euclidean(from_ECEF, to_ECEF)


def _get_pos_df(from_aircraft_id, to_aircraft_id):
    """
    Get position for all unique aircraft listed in from_aircraft_id & to_aircraft_id.

    Parameters
    ----------
    from_aircraft_id : [str]
        A list of strings of aircraft IDs.
    to_aircraft_id : [str]
       A list of strings of aircraft IDs.

    Returns
    -------
    pos_df : pandas.DataFrame
       A dataframe of current positions (aircraft_id are row indexes) with
       altitude in metres. All row values are NaN if requested aircraft ID does not exist.

    Examples
    --------
    >>> pydodo.distance_measures.get_pos_df(from_aircraft_id = ["BAW123"], to_aircraft_id = ["KLM456"])
    """

    utils._validate_id_list(from_aircraft_id)
    utils._validate_id_list(to_aircraft_id)

    ids = list(set(from_aircraft_id + to_aircraft_id))
    pos_df = aircraft_position(ids)
    SCALE_FEET_TO_METRES = 0.3048
    pos_df.loc[:, "current_flight_level"] = SCALE_FEET_TO_METRES * pos_df["current_flight_level"]
    return pos_df


def _get_separation(from_aircraft_id, to_aircraft_id, distance_f, **kwargs):
    """
    Get separation (geodesic, great circle, vertical or euclidean) between all pairs of "from" and "to" aircraft.

    Parameters
    ----------
    from_aircraft_id : str, [str]
        A string or list of strings of aircraft IDs.
    to_aircraft_id : str, [str], optional
       An optional string or list of strings of aircraft IDs. If not provided, ``to_aircraft_id=from_aircraft_id``
    distance_f : function
        One of ``[geodesic_distance, great_circle_distance, vertical_distance, euclidean_distance]``.
    **kwargs:
        major_semiaxis : double, optional
            The major (equatorial) radius of the ellipsoid. The default value is for WGS84.
        radius : double, optional
            Earth radius/major_semiaxis in metres. The default valus is for WGS84.
        flattening : double, optional
            Ellipsoid flattening. The default value is for WGS84.

    Returns
    -------
    sep_df : pandas.DataFrame
       A dataframe with separation between all from_aircraft_id and to_aircraft_id pairs of aircraft.

    Notes
    -----
    If any of the given aircraft IDs does not exist in the simulation, the
    returned dataframe contains a row or column of missing values for that ID.

    Examples
    --------
    >>> pydodo.distance_measures.get_separation(from_aircraft_id = "BAW123", to_aircraft_id = "KLM456", measure = "euclidean")
    >>> pydodo.distance_measures.get_separation(from_aircraft_id = ["BAW123", "KLM456"], measure = "great_circle")
    """
    major_semiaxis = (
        _EARTH_RADIUS if "major_semiaxis" not in kwargs else kwargs["major_semiaxis"]
    )
    radius = _EARTH_RADIUS if "radius" not in kwargs else kwargs["radius"]
    flattening = _FLATTENING if "flattening" not in kwargs else kwargs["flattening"]

    if not isinstance(from_aircraft_id, list):
        from_aircraft_id = [from_aircraft_id]
    if to_aircraft_id == None:
        to_aircraft_id = from_aircraft_id.copy()
    if not isinstance(to_aircraft_id, list):
        to_aircraft_id = [to_aircraft_id]

    pos_df = _get_pos_df(from_aircraft_id, to_aircraft_id)
    all_distances = []
    for from_id in from_aircraft_id:
        if pos_df.loc[from_id][["current_flight_level", "longitude", "latitude"]].isnull().any():
            distances = [np.nan] * len(to_aircraft_id)
        else:
            distances = [
                distance_f(
                    from_lat=pos_df.loc[from_id]["latitude"],
                    from_lon=pos_df.loc[from_id]["longitude"],
                    from_alt=pos_df.loc[from_id]["current_flight_level"],
                    to_lat=pos_df.loc[to_id]["latitude"],
                    to_lon=pos_df.loc[to_id]["longitude"],
                    to_alt=pos_df.loc[to_id]["current_flight_level"],
                    major_semiaxis=major_semiaxis,
                    radius=radius,
                    flattening=flattening,
                )
                if not pos_df.loc[to_id][["current_flight_level", "longitude", "latitude"]].isnull().any()
                else np.nan
                for to_id in to_aircraft_id
            ]
        all_distances.append(distances)

    return pd.DataFrame(all_distances, columns=to_aircraft_id, index=from_aircraft_id)


def geodesic_separation(
    from_aircraft_id,
    to_aircraft_id=None,
    major_semiaxis=_EARTH_RADIUS,
    flattening=_FLATTENING,
):
    """
    Get geodesic separation in metres between the positions of all from_aircraft_id and to_aircraft_id pairs of aircraft.

    Parameters
    ----------
    from_aircraft_id : str, [str]
        A string or list of strings of aircraft IDs.
    to_aircraft_id : str, [str], optional
       An optional string or list of strings of aircraft IDs. If not provided, ``to_aircraft_id=from_aircraft_id``
    major_semiaxis : double, optional
        The major (equatorial) radius of the ellipsoid. The default value is for WGS84.
    flattening : double, optional
        Ellipsoid flattening. The default value is for WGS84.

    Returns
    -------
    df : pandas.DataFrame
        A dataframe of doubles with from_aircraft_id as row names and
        to_aircraft_id as column names. The values are the geodesic distance in
        metres between the positions of the aircraft pair at each
        ``[from_aircraft_id, to_aircraft_id]`` index.

    Notes
    -----
    If any of the given aircraft IDs does not exist in the simulation, the
    returned dataframe contains a row or column of missing values for that ID.

    Examples
    --------
    >>> pydodo.geodesic_separation(from_aircraft_id = "BAW123", to_aircraft_id = "KLM456")
    >>> pydodo.geodesic_separation(from_aircraft_id = ["BAW123", "KLM456"])
    """
    return _get_separation(
        from_aircraft_id,
        to_aircraft_id,
        distance_f=geodesic_distance,
        major_semiaxis=major_semiaxis,
        flattening=flattening,
    )


def great_circle_separation(
    from_aircraft_id, to_aircraft_id=None, radius=_EARTH_RADIUS
):
    """
    Get great circle separation in metres between the positions of all from_aircraft_id and to_aircraft_id pairs of aircraft.

    Parameters
    ----------
    from_aircraft_id : str, [str]
        A string or list of strings of aircraft IDs.
    to_aircraft_id : str, [str], optional
       An optional string or list of strings of aircraft IDs. If not provided, ``to_aircraft_id=from_aircraft_id``
    radius : doubl, optional
        The radius of the earth in metres. The default value for WGS84.

    Returns
    -------
    df : pandas.DataFrame, dtype=double
        A dataframe of doubles with `from_aircraft_id` as row names and
        `to_aircraft_id` as column names. The values are the great circle distance in
        metres between the positions of the aircraft pair at each
        ``[from_aircraft_id, to_aircraft_id]`` index.

    Notes
    -----
    If any of the given aircraft IDs does not exist in the simulation, the
    returned dataframe contains a row or column of missing values for that ID.

    Examples
    --------
    >>> pydodo.great_circle_separation(from_aircraft_id = "BAW123", to_aircraft_id = "KLM456")
    >>> pydodo.great_circle_separation(from_aircraft_id = ["BAW123", "KLM456"])
    """
    return _get_separation(
        from_aircraft_id,
        to_aircraft_id,
        distance_f=great_circle_distance,
        radius=radius,
    )


def vertical_separation(from_aircraft_id, to_aircraft_id=None):
    """
    Get vertical separation in metres between the positions of all from_aircraft_id and to_aircraft_id pairs of aircraft.

    Parameters
    ----------
    from_aircraft_id : str, [str]
        A string or list of strings of aircraft IDs.
    to_aircraft_id : str, [str], optional
       An optional string or list of strings of aircraft IDs. If not provided, ``to_aircraft_id=from_aircraft_id``

    Returns
    -------
    df : pandas.DataFrame, dtype=double
        A dataframe of doubles with from_aircraft_id as row names and
        to_aircraft_id as column names. The values are the vertical distance in
        metres between the positions of the aircraft pair at each
        ``[from_aircraft_id, to_aircraft_id]`` index.

    Notes
    -----
    If any of the given aircraft IDs does not exist in the simulation, the
    returned dataframe contains a row or column of missing values for that ID.

    Examples
    --------
    >>> pydodo.vertical_separation(from_aircraft_id = "BAW123", to_aircraft_id = "KLM456")
    >>> pydodo.vertical_separation(from_aircraft_id = ["BAW123", "KLM456"])
    """
    return _get_separation(
        from_aircraft_id, to_aircraft_id, distance_f=vertical_distance
    )


def euclidean_separation(
    from_aircraft_id,
    to_aircraft_id=None,
    major_semiaxis=_EARTH_RADIUS,
    flattening=_FLATTENING,
):
    """
    Get euclidean separation in metres between the positions of all
    from_aircraft_id and to_aircraft_id pairs of aircraft. The aircraft
    positions are converted to ECEF coordinates to calculate separation.

    Parameters
    ----------
    from_aircraft_id : str, [str]
        A string or list of strings of aircraft IDs.
    to_aircraft_id : str, [str], optional
       An optional string or list of strings of aircraft IDs. If not provided, ``to_aircraft_id=from_aircraft_id``
    major_semiaxis : double, optional
        The major (equatorial) radius of the ellipsoid. The default value is for WGS84.
    flattening : double, optional
        Ellipsoid flattening. The default value is for WGS84.

    Returns
    -------
    df : pandas.DataFrame
        A dataframe of doubles with `from_aircraft_id` as row names and
        `to_aircraft_id` as column names. The values are the euclidean distance in
        metres between the positions of the aircraft pair at each
        ``[from_aircraft_id, to_aircraft_id]`` index.

    Notes
    -----
    https://en.wikipedia.org/wiki/ECEF

    If any of the given aircraft IDs does not exist in the simulation, the
    returned dataframe contains a row or column of missing values for that ID.

    Examples
    --------
    >>> pydodo.euclidean_separation(from_aircraft_id = "BAW123", to_aircraft_id = "KLM456")
    >>> pydodo.euclidean_separation(from_aircraft_id = ["BAW123", "KLM456"])
    """
    return _get_separation(
        from_aircraft_id,
        to_aircraft_id,
        distance_f=euclidean_distance,
        major_semiaxis=major_semiaxis,
        flattening=flattening,
    )
