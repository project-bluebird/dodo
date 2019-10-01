import pandas as pd
import numpy as np
from geopy import distance
from scipy.spatial.distance import euclidean

from .config_param import config_param
from . import request_position
from . import utils

# Default for major (equatorial) radius and flattening are 'WGS-84' values.
major_semiaxis, minor_semiaxis, _FLATTENING = distance.ELLIPSOIDS['WGS-84']
_EARTH_RADIUS = major_semiaxis * 1000 # convert to metres


def geodesic_distance(from_lat, from_lon, to_lat, to_lon, major_semiaxis=_EARTH_RADIUS, flattening=_FLATTENING):
    """
    Get geodesic distance between two (lat, lon) points in metres.

    Parameters
    ----------
    from_lat : double
        A double in the range ``[-90, 90]``. The `from` point's latitude.
    from_lon : double
        A double in the range ``[-180, 180]``. The `from` point's longitude.
    to_lat : double
        A double in the range ``[-90, 90]``. The `to` point's latitude.
    to_lon : double
        A double in the range ``[-180, 180]``. The `to` point's longitude.
    major_semiaxis : double
        An optional double. The major (equatorial) radius of the ellipsoid. The
        default value is for WGS84.
    flattening : double
        An optional double. Ellipsoid flattening. The default value is for
        WGS84.

    Returns
    -------
    geodesic_distance : double
        A double, geodesic distance between two points.

    Examples
    --------
    >>> pydodo.geodesic_distance()
    >>>

    """

    utils._validate_latitude(from_lat)
    utils._validate_longitude(from_lon)
    utils._validate_latitude(to_lat)
    utils._validate_longitude(to_lon)
    utils._validate_is_positive(major_semiaxis, 'major_semiaxis')
    utils._validate_is_positive(flattening, 'flattening')

    # For GeoPy need to provide (major_semiaxis, minor_semiaxis, flattening) but
    # only major_semiaxis & flattening vals are used --> ignore minor_semiaxis
    return distance.geodesic(
        (from_lat, from_lon),
        (to_lat, to_lon),
        ellipsoid=(major_semiaxis/1000, minor_semiaxis, flattening) # convert to km
        ).meters


def great_circle_distance(from_lat, from_lon, to_lat, to_lon, radius=_EARTH_RADIUS):
    """
    Get great-circle distance between two (lat, lon) points in metres.

    Parameters
    ----------
    from_lat : double
        A double in the range ``[-90, 90]``. The `from` point's latitude.
    from_lon : double
        A double in the range ``[-180, 180]``. The `from` point's longitude.
    to_lat : double
        A double in the range ``[-90, 90]``. The `to` point's latitude.
    to_lon : double
        A double in the range ``[-180, 180]``. The `to` point's longitude.
    radius : double
        An optional double. The radius of the earth in metres. The default value
        is 6378137 m.

    Returns
    -------
    great_circle_distance : double
        A double, the great-circle distance between two points.

    Examples
    --------
    >>> pydodo.great_circle_distance()
    >>>

    """
    utils._validate_latitude(from_lat)
    utils._validate_longitude(from_lon)
    utils._validate_latitude(to_lat)
    utils._validate_longitude(to_lon)
    utils._validate_is_positive(radius, 'radius')

    return distance.great_circle(
        (from_lat, from_lon),
        (to_lat, to_lon),
        radius=radius/1000 # convert to km
        ).meters


def vertical_distance(from_alt, to_alt):
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
        A double, verticle distance between two points.

    Examples
    --------
    >>> pydodo.vertical_distance()
    >>>

    """
    utils._validate_is_positive(from_alt, 'altitude')
    utils._validate_is_positive(to_alt, 'altitude')

    return abs(from_alt - to_alt)


def lla_to_ECEF(lat, lon, alt = 0, radius=_EARTH_RADIUS, f=_FLATTENING ):
    """
    Calculates ECEF coordinates of a point from lat, lon and alt.

    Parameters
    ----------

    lat : double

    lon : double

    alt : int
        Altitude in meters
    radius : double
        Earth radius in metres (WGS84).
    f : double
        Ellipsoidal flattening (WGS84).

    Returns
    -------
    ....

    Notes
    -----
    https://en.wikipedia.org/wiki/ECEF

    Examples
    --------
    >>> pydodo.distance_measures.lla_to_ECEF()
    >>>

    """

    lat_r = np.deg2rad(lat)
    lon_r = np.deg2rad(lon)

    e2 = 1 - (1 - f) * (1 - f)
    N = radius / np.sqrt(1 - e2 * np.power(np.sin(lat_r), 2))

    x = (N + alt) * np.cos(lat_r) * np.cos(lon_r)
    y = (N + alt) * np.cos(lat_r) * np.sin(lon_r)
    z = ((1-e2) * N + alt) * np.sin(lat_r)

    return (x,y,z)


def euclidean_distance(from_lat, from_lon, from_alt, to_lat, to_lon, to_alt, major_semiaxis=_EARTH_RADIUS, flattening=_FLATTENING):
    """
    Get euclidean distance between two (lat, lon, alt) points in metres. The
    points are converted to ECEF coordinates to calculate distance.

    Parameters
    ----------
    from_lat : double
        A double in the range ``[-90, 90]``. The `from` point's latitude.
    from_lon : double
        A double in the range ``[-180, 180]``. The `from` point's longitude.
    from_alt : double
        A non-negatige double. The from point's altitude in metres.
    to_lat : double
         A double in the range ``[-90, 90]``. The `to` point's latitude.
    to_lon : double
        A double in the range ``[-180, 180]``. The `to` point's longitude.
    to_alt : double
        A non-negatige double. The `to` point's altitude in metres.
    major_semiaxis : double
        An optional double. The major (equatorial) radius of the ellipsoid. The
        default value is for WGS84.
    flattening : double
        An optional double. Ellipsoid flattening. The default value is for
        WGS84.

    Returns
    -------
    euclidean_distance : double
        A double, euclidean distance between two points.

    Notes
    -----
    https://en.wikipedia.org/wiki/ECEF

    Examples
    --------
    >>> pydodo.euclidean_distance()
    >>>

    """
    utils._validate_latitude(from_lat)
    utils._validate_longitude(from_lon)
    utils._validate_is_positive(from_alt, 'altitude')
    utils._validate_latitude(to_lat)
    utils._validate_longitude(to_lon)
    utils._validate_is_positive(to_alt, 'altitude')
    utils._validate_is_positive( major_semiaxis, ' major_semiaxis')

    from_ECEF = lla_to_ECEF(from_lat, from_lon, from_alt,  major_semiaxis, flattening)
    to_ECEF = lla_to_ECEF(to_lat, to_lon, to_alt,  major_semiaxis, flattening)

    return euclidean(from_ECEF, to_ECEF)


def get_distance(from_pos, to_pos, measure, radius=_EARTH_RADIUS, flattening=_FLATTENING):
    """
    Get distance (geodesic, great circle, vertical or euclidean) between the positions of a pair of aircraft.

    Parameters
    ----------
    from_pos : pandas.Series
        A pandas Series holding the from aircraft position data.
    to_pos : pandas.Series
        A pandas Series holding the to aircraft position data.
    measure : str
        A string, one of ``['geodesic', 'great_circle', 'vertical', 'euclidean']``.
    radius : double
        Earth radius/major_semiaxis in metres.
    flattening : double
        An optional double. Ellipsoid flattening. The default value is for
        WGS84. param passed to geodesic_distance.

    Examples
    --------
    >>> pydodo.distance_measures.get_distance()
    >>>

    """
    if measure == 'geodesic':
        return geodesic_distance(
            from_pos['latitude'],
            from_pos['longitude'],
            to_pos['latitude'],
            to_pos['longitude'],
            major_semiaxis=radius,
            flattening=flattening
        )
    elif measure == 'great_circle':
        return great_circle_distance(
            from_pos['latitude'],
            from_pos['longitude'],
            to_pos['latitude'],
            to_pos['longitude'],
            radius=radius
        )
    elif measure == 'vertical':
        return vertical_distance(
            from_pos['altitude'],
            to_pos['altitude']
        )
    elif measure == 'euclidean':
        return euclidean_distance(
            from_pos['latitude'],
            from_pos['longitude'],
            from_pos['altitude'],
            to_pos['latitude'],
            to_pos['longitude'],
            to_pos['altitude'],
            major_semiaxis=radius,
            flattening=flattening
        )


def get_pos_df(from_aircraft_id, to_aircraft_id):
    """
    Get position for all unique aircraft listed in from_aircraft_id & to_aircraft_id.
    Altitude is returned in feet by all_positions() so convert it to metres.

    Parameters
    ----------
    from_aircraft_id : str
        A list of strings of aircraft IDs.
    to_aircraft_id : str
        A list of strings of aircraft IDs.

    Returns
    -------
    pos_df : pandas.DataFrame
       A dataframe of current positions (aircraft_id are row indexes), NaN if requested aircraft ID does not exist.

    Examples
    --------
    >>> pydodo.distance_measures.get_pos_df()
    >>>

    """

    utils._validate_id_list(from_aircraft_id)
    utils._validate_id_list(to_aircraft_id)

    ids = list(set(from_aircraft_id + to_aircraft_id))

    all_pos = request_position.all_positions()
    pos_df = all_pos.reindex(ids)

    SCALE_FEET_TO_METRES = 0.3048
    pos_df.loc[:, "altitude"] = SCALE_FEET_TO_METRES * pos_df["altitude"]

    return pos_df


def get_separation(from_aircraft_id, to_aircraft_id, measure, radius=_EARTH_RADIUS, flattening=_FLATTENING):
    """
    Get separation (geodesic, great circle, vertical or euclidean) betweel all pairs of "from" and "to" aircraft.

    Parameters
    ----------
    from_aircraft_id : str
        A string or list of strings of aircraft IDs.
    to_aircraft_id : str
       An optional string or list of strings of aircraft IDs.
    measure : str
        A string, one of ``['geodesic', 'great_circle', 'vertical', 'euclidean']``.
    radius : double
        Earth radius/major_semiaxis in metres.
    flattening : double
        param passed to geodesic_distance.

    Returns
    -------
    sep_df : pandas.DataFrame
       A dataframe with separation between all from_aircraft_id and to_aircraft_id pairs of aircraft.

    Examples
    --------
    >>> pydodo.get_separation()
    >>>

    """
    assert measure in ['geodesic', 'great_circle', 'vertical', 'euclidean'], 'Invalid value {} for measure'.format(measure)
    if to_aircraft_id == None:
        to_aircraft_id = from_aircraft_id.copy()
    if not isinstance(from_aircraft_id, list): from_aircraft_id = [ from_aircraft_id ]
    if not isinstance(to_aircraft_id, list): to_aircraft_id = [ to_aircraft_id ]

    pos_df = get_pos_df(from_aircraft_id, to_aircraft_id)

    all_distances = []
    for from_id in from_aircraft_id:
        distances = [
            get_distance(pos_df.loc[from_id], pos_df.loc[to_id], measure=measure, radius=radius, flattening=flattening)
            if not (pos_df.loc[from_id].isnull().any() or pos_df.loc[to_id].isnull().any())
            else np.nan
            for to_id in to_aircraft_id
        ]
        all_distances.append(distances)

    return pd.DataFrame(
        all_distances,
        columns = to_aircraft_id,
        index = from_aircraft_id
    )


def geodesic_separation(from_aircraft_id, to_aircraft_id=None, major_semiaxis=_EARTH_RADIUS, flattening=_FLATTENING):
    """
    Get geodesic separation in metres between the positions of all from_aircraft_id and to_aircraft_id pairs of aircraft.

    Parameters
    ----------

    from_aircraft_id : str
        A string vector of aircraft IDs.
    to_aircraft_id : str
        An optional string vector of aircraft IDs. If not provided, ``to_aircraft_id=from_aircraft_id``
    major_semiaxis : double
        An optional double. The major (equatorial) radius of the ellipsoid. The
        default value is for WGS84.
    flattening : double
        An optional double. Ellipsoid flattening. The default value is for
        WGS84.

    Returns
    -------

    df : pandas.DataFrame
        A dataframe of doubles with from_aircraft_id as row names and
        to_aircraft_id as column names. The values are the geodesic distance in
        metres between the positions of the aircraft pair at each
        ``[from_aircraft_id, to_aircraft_id]`` index.

    Examples
    --------
    >>> pydodo.geodesic_separation()
    >>>
    """
    return get_separation(from_aircraft_id, to_aircraft_id, measure='geodesic', radius=major_semiaxis, flattening=flattening)


def great_circle_separation(from_aircraft_id, to_aircraft_id=None, radius=_EARTH_RADIUS):
    """
    Get great circle separation in metres between the positions of all from_aircraft_id and to_aircraft_id pairs of aircraft.

    Parameters
    ----------

    from_aircraft_id : str
        A string vector of aircraft IDs.
    to_aircraft_id : str
        An optional string vector of aircraft IDs. If not provided, ``to_aircraft_id=from_aircraft_id``
    radius : double
        An optional double. The radius of the earth in metres. The default value
        is 6378137 m.

    Returns
    -------

    df : pandas.DataFrame, dtype=double
        A dataframe of doubles with `from_aircraft_id` as row names and
        `to_aircraft_id` as column names. The values are the great circle distance in
        metres between the positions of the aircraft pair at each
        ``[from_aircraft_id, to_aircraft_id]`` index.

    Examples
    --------
    >>> pydodo.great_circle_separation()
    >>>
    """
    return get_separation(from_aircraft_id, to_aircraft_id, measure='great_circle', radius=radius)


def vertical_separation(from_aircraft_id, to_aircraft_id=None):
    """
    Get vertical separation in metres between the positions of all from_aircraft_id and to_aircraft_id pairs of aircraft.

    Parameters
    ----------

    from_aircraft_id : str
        A string vector of aircraft IDs.
    to_aircraft_id : str
        An optional string vector of aircraft IDs. If not provided, ``to_aircraft_id=from_aircraft_id``

    Returns
    -------

    df : pandas.DataFrame, dtype=double
        A dataframe of doubles with from_aircraft_id as row names and
        to_aircraft_id as column names. The values are the vertical distance in
        metres between the positions of the aircraft pair at each
        ``[from_aircraft_id, to_aircraft_id]`` index.

    Examples
    --------
    >>> pydodo.vertical_separation()
    >>>
    """
    return get_separation(from_aircraft_id, to_aircraft_id, measure='vertical')


def euclidean_separation(from_aircraft_id, to_aircraft_id=None,  major_semiaxis=_EARTH_RADIUS, flattening=_FLATTENING):
    """
    Get euclidean separation in metres between the positions of all
    from_aircraft_id and to_aircraft_id pairs of aircraft. The aircraft
    positions are converted to ECEF coordinates to calculate separation.

    Parameters
    ----------

    from_aircraft_id : str
        A string vector of aircraft IDs.
    to_aircraft_id : str
        An optional string vector of aircraft IDs. If not provided, ``to_aircraft_id=from_aircraft_id``
    major_semiaxis : double
        An optional double. The major (equatorial) radius of the ellipsoid. The
        default value is for WGS84.
    flattening : double
        An optional double. Ellipsoid flattening. The default value is for
        WGS84.

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

    Examples
    --------
    >>> pydodo.euclidean_separation()
    >>>
    """
    return get_separation(from_aircraft_id, to_aircraft_id, measure='euclidean',  radius=major_semiaxis, flattening=flattening)
