import pytest
import pandas as pd
import numpy as np

from pydodo import aircraft_position, all_positions, reset_simulation, create_aircraft
from pydodo.utils import ping_bluebird


bb_resp = ping_bluebird()
@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_no_positions():
    """
    Expect empty dataframe when no aircraft exist.
    """
    reset_simulation()

    pos_df = all_positions()
    assert pos_df.empty

@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_wrong_id():
    """
    Expect dataframe with NAN if request aircraft not in simulation.
    """
    reset_simulation()

    pos_df = aircraft_position("TEST1")
    assert pos_df.equals(
        pd.DataFrame({
            "altitude":np.nan,
            "ground_speed":np.nan,
            "latitude":np.nan,
            "longitude":np.nan,
            "vertical_speed":np.nan
            }, index=['TEST1'])
    )

@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_positions():
    cmd = reset_simulation()
    assert cmd == True

    aircraft_id = "TST1001"
    type = "B744"
    latitude = 0
    longitude = 0
    heading = 0
    flight_level = 250
    speed = 200

    cmd = create_aircraft(aircraft_id = aircraft_id,
                          type = type,
                          latitude = latitude,
                          longitude = longitude,
                          heading = heading,
                          flight_level = flight_level,
                          speed = speed)
    assert cmd == True

    pos = all_positions()
    assert isinstance(pos, pd.DataFrame)
    assert len(pos.index) == 1
    assert pos.loc[aircraft_id]['latitude'] > 0
    assert pos.loc[aircraft_id]['longitude'] == 0
    assert pos.loc[aircraft_id]['vertical_speed'] == 0
    assert pos.loc[aircraft_id]['altitude'] == flight_level * 100

    aircraft_id_2 = "TST2002"
    type_2 = "C744"
    latitude_2 = 0
    longitude_2 = 0
    heading_2 = 180
    flight_level_2 = 200
    speed_2 = 300

    cmd = create_aircraft(aircraft_id = aircraft_id_2,
                          type = type_2,
                          latitude = latitude_2,
                          longitude = longitude_2,
                          heading = heading_2,
                          flight_level = flight_level_2,
                          speed = speed_2)
    assert cmd == True

    pos = all_positions()
    assert isinstance(pos, pd.DataFrame)
    assert len(pos.index) == 2
    assert pos.loc[aircraft_id]['latitude'] > 0
    assert pos.loc[aircraft_id]['longitude'] == 0
    assert pos.loc[aircraft_id]['vertical_speed'] == 0
    assert pos.loc[aircraft_id]['altitude'] == flight_level * 100

    assert pos.loc[aircraft_id_2]['latitude'] < 0
    assert round(pos.loc[aircraft_id_2]['longitude'], 2) == 0
    assert pos.loc[aircraft_id_2]['vertical_speed'] == 0
    assert pos.loc[aircraft_id_2]['altitude'] == flight_level_2 * 100

    # aircraft initial speed may differ from indicated speed
    assert pos.loc[aircraft_id_2]['ground_speed'] > 150
