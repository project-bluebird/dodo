import pytest
import math

from pydodo import (
    geodesic_distance,
    great_circle_distance,
    vertical_distance,
    euclidean_distance
)

def test_geodesic_distance():
  from_lat = 51.507389
  from_lon = 0.127806

  to_lat = 50.6083
  to_lon = -1.9608

  result = geodesic_distance(from_lat, from_lon, to_lat, to_lon)

  # Compare to the result calculated using ArcGIS (to within 1% error):
  assert result == pytest.approx(1000*176.92, 0.01)


def deg2rad(deg):
    return (deg * math.pi) / 180


def test_great_circle_distance():
    from_lat = 51.507389
    from_lon = 0.127806

    to_lat = 50.6083
    to_lon = -1.9608

    result = great_circle_distance(from_lat, from_lon, to_lat, to_lon)

    # Compare to the result computed using the Haversine formula:
    dlat = from_lat - to_lat
    dlon = from_lon - to_lon

    a = (math.sin(deg2rad(dlat)/2))**2 + math.cos(deg2rad(from_lat)) * math.cos(deg2rad(to_lat)) * (math.sin(deg2rad(dlon)/2))**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    #R = 6378137 # Radius of the earth
    R = 6371009 # GeoPy assumed raius of the earth
    expected = R * c

    assert result == pytest.approx(expected)


def test_vertical_distance():
    from_alt = 300
    to_alt = 150

    result = vertical_distance(from_alt, to_alt)

    expected = from_alt - to_alt

    assert result == expected
