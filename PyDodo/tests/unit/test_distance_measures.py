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

  result = geodesic_distance(0.123456789, 0.123456789, 0.123456789, 0.123456789)
  assert result == 0


@pytest.mark.parametrize(
    "from_lat,from_lon,to_lat,to_lon",
    [(51.507389, 0.127806, 50.6083, -1.9608),
    (0, 0, 0, 0),
    (89, 40, 89.1, 40)
    ]
)
def test_great_circle_distance(expected_great_circle,from_lat,from_lon,to_lat,to_lon):

    result = great_circle_distance(from_lat, from_lon, to_lat, to_lon)

    expected = expected_great_circle(from_lat, from_lon, to_lat, to_lon)

    assert result == pytest.approx(expected)


@pytest.mark.parametrize(
    "from_alt,to_alt",
    [(0, 0), (150, 300)]
)
def test_vertical_distance(from_alt, to_alt):

    result = vertical_distance(from_alt, to_alt)

    expected = abs(from_alt - to_alt)

    assert result == expected


@pytest.mark.parametrize(
    "from_lat,from_lon,to_lat,to_lon,from_alt,to_alt",
    [(-91, -180, 90, -180, -1, 1),
    (-90, -180, 90, -180.5, -1, 1),
    (-90, -180, 90, 180, 1, -1)
    ]
)
def test_wrong_inputs(from_lat,from_lon,to_lat,to_lon,from_alt,to_alt):
     with pytest.raises(AssertionError):
         geodesic_distance(from_lat, from_lon, to_lat, to_lon)

     with pytest.raises(AssertionError):
         great_circle_distance(from_lat, from_lon, to_lat, to_lon)

     with pytest.raises(AssertionError):
         euclidean_distance(from_lat, from_lon, from_alt, to_lat, to_lon, to_alt)

     with pytest.raises(AssertionError):
         vertical_distance(from_alt, to_alt)
