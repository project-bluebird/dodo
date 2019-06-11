import pandas as pd
from geopy import distance

from . import request_position
from . import utils


def geodesic_distance(from_lat, from_long, to_lat, to_long):
    """
    Get geodesic distance between two points in metres.
    """
    utils._validate_latitude(from_lat)
    utils._validate_longitude(from_long)
    utils._validate_latitude(to_lat)
    utils._validate_longitude(to_long)

    return distance.geodesic((from_lat, from_long), (to_lat, to_long)).meters


def great_circle_distance(from_lat, from_long, to_lat, to_long):
    """
    Get great-circle distance between two points in metres.
    """
    utils._validate_latitude(from_lat)
    utils._validate_longitude(from_long)
    utils._validate_latitude(to_lat)
    utils._validate_longitude(to_long)

    return distance.great_circle((from_lat, from_long), (to_lat, to_long)).meters


def vertical_distance(from_alt, to_alt):
    """
    Get vertical distance between two points.
    Altitude (`from_alt` and `to_alt`) is given in metres.
    """
    utils._validate_altitude(from_alt)
    utils._validate_altitude(to_alt)

    return abs(from_alt - to_alt)


def euclidean_distance(from_lat, from_long, from_alt, to_lat, to_long, to_alt):
    """
    Get euclidean distance between two points in metres.
    """
    utils._validate_latitude(from_lat)
    utils._validate_longitude(from_long)
    utils._validate_altitude(from_alt)
    utils._validate_latitude(to_lat)
    utils._validate_longitude(to_long)
    utils._validate_altitude(to_alt)

    pass


def get_distance(from_pos, to_pos, measure=None):
    """
    Get distance (geodesic, great circle, vertical or euclidean) between the positions of a pair of aircraft.

    :param from_pos: A pandas Series holding the from aircraft position data.
    :param to_pos: A pandas Series holding the to aircraft position data.
    :param measure: A string, one of ['geodesic', 'great_circle', 'vertical', 'euclidean'].
    """
    if measure == 'geodesic':
        return geodesic_distance(
            from_pos['latitude'],
            from_pos['longitude'],
            to_pos['latitude'],
            to_pos['longitude']
        )
    elif measure == 'great_circle':
        return great_circle_distance(
            from_pos['latitude'],
            from_pos['longitude'],
            to_pos['latitude'],
            to_pos['longitude']
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
            to_pos['longitude']
            to_pos['altitude']
        )


def get_pos_df(from_aircraft_id, to_aircraft_id):
    """
    Get position for all unique aircraft listed in from_aircraft_id & to_aircraft_id.

    :param from_aircraft_id: A list of strings of aircraft IDs.
    :param to_aircraft_id: A list of strings of aircraft IDs.
    :returm: A dataframe of current positions (aircraft_id are row indexes), NaN if requested aircraft ID does not exist.
    """
    utils._validate_id_list(from_aircraft_id)
    utils._validate_id_list(to_aircraft_id)

    ids = list(set(from_aircraft_id + to_aircraft_id))

    all_pos = request_position.all_positions()
    pos_df = all_pos.reindex(ids)

    return pos_df


def get_separation(from_aircraft_id, to_aircraft_id=None, measure=None):
    """
    Get separation (geodesic, great circle, vertical or euclidean) betweel all pairs of aircraft.

    :param from_aircraft_id: A string or list of strings of aircraft IDs.
    :param to_aircraft_id: A string or list of strings of aircraft IDs.
    :param measure: A string, one of ['geodesic', 'great_circle', 'vertical', 'euclidean'].
    :return : A dataframe with separation between all from_aircraft_id and to_aircraft_id pairs of aircraft.
    """
    if to_aircraft_id == None:
        to_aircraft_id = from_aircraft_id.copy()
    if not isinstance(from_aircraft_id, list): from_aircraft_id = [ from_aircraft_id ]
    if not isinstance(to_aircraft_id, list): to_aircraft_id = [ to_aircraft_id ]

    pos_df = get_pos_df(from_aircraft_id, to_aircraft_id)

    all_distances = []
    for from_id in from_aircraft_id:
        distances = [
            get_distance(pos_df.loc[from_id], pos_df.loc[to_id], measure=measure)
            for to_id in to_aircraft_id
        ]
        all_distances.append(distances)

    return pd.DataFrame(
        all_distances,
        columns = to_aircraft_id,
        index = from_aircraft_id
    )


def geodesic_separation(from_aircraft_id, to_aircraft_id=None):
    """
    Get geodesic separation in metres between the positions of all from_aircraft_id and to_aircraft_id pairs of aircraft.
    """
    return get_separation(from_aircraft_id, to_aircraft_id, measure='geodesic')


def great_circle_separation(from_aircraft_id, to_aircraft_id=None):
    """
    Get great circle separation in metres between the positions of all from_aircraft_id and to_aircraft_id pairs of aircraft.
    """
    return get_separation(from_aircraft_id, to_aircraft_id, measure='great_circle')


def vertical_separation(from_aircraft_id, to_aircraft_id=None):
    """
    Get vertical separation in metres between the positions of all from_aircraft_id and to_aircraft_id pairs of aircraft.
    """
    return get_separation(from_aircraft_id, to_aircraft_id, measure='vertical')


def euclidean_separation(from_aircraft_id, to_aircraft_id=None):
    """
    Get euclidean separation in metres between the positions of all from_aircraft_id and to_aircraft_id pairs of aircraft.
    """
    pass
