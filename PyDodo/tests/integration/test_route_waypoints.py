import pytest
import time
from requests.exceptions import HTTPError
import pandas as pd

from pydodo import (
    reset_simulation,
    all_positions,
    list_route,
)
from pydodo.bluebird_connect import ping_bluebird

# test if can connect to BlueBird
bb_resp = ping_bluebird()


@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_route_waypoints(upload_test_sector_scenario):
    """
    Test list_route(), direct_to_waypoint()
    """

    cmd = reset_simulation()
    assert cmd == True

    upload_test_sector_scenario()

    # Get the position
    position = all_positions()
    acid1, acid2 = position.index

    route1 = list_route(acid1)
    route2 = list_route(acid2)

    assert route1["aircraft_id"] == acid1
    assert route2["aircraft_id"] == acid2

    assert route1["next_waypoint"] == 'FIYRE'
    assert route1["route_name"] == 'ASCENSION'
    assert len(route1["route_waypoints"]) == 5

    assert route2["next_waypoint"] == 'SPIRT'
    assert route2["route_name"] == 'FALLEN'
    assert len(route2["route_waypoints"]) == 5

    route2["route_waypoints"].reverse()
    assert all([
        wp1 == wp2 for wp1, wp2
        in zip(route1["route_waypoints"], route2["route_waypoints"])
        ])
