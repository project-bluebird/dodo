import pytest
import pandas as pd
import numpy as np

from pydodo import aircraft_position, all_positions, reset_simulation, create_aircraft
from pydodo.utils import ping_bluebird

bb_resp = ping_bluebird()

# TWO EXAMPLE AIRCRAFT
aircraft_id = "TST1001"
type = "B744"
latitude = 0
longitude = 0
heading = 0
flight_level = 250
speed = 200

aircraft_id_2 = "TST2002"
type_2 = "C744"
latitude_2 = 0
longitude_2 = 0
heading_2 = 180
flight_level_2 = 200
speed_2 = 300


@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_no_positions():
    """
    Expect empty dataframe when no aircraft exist.
    """
    cmd = reset_simulation()
    assert cmd == True

    pos_df = all_positions()
    assert pos_df.empty


@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_wrong_id():
    """
    Expect a row in a dataframe with NAN if requested aircraft not in simulation.
    """
    cmd = reset_simulation()
    assert cmd == True

    pos = aircraft_position(aircraft_id)
    assert pos.loc[aircraft_id].isnull().all()

    cmd = create_aircraft(
        aircraft_id=aircraft_id,
        type=type,
        latitude=latitude,
        longitude=longitude,
        heading=heading,
        flight_level=flight_level,
        speed=speed,
    )
    assert cmd == True

    pos = aircraft_position([aircraft_id, aircraft_id_2])
    assert len(pos.index) == 2
    assert pos.loc[aircraft_id_2].isnull().all()


@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_all_positions():
    cmd = reset_simulation()
    assert cmd == True

    cmd = create_aircraft(
        aircraft_id=aircraft_id,
        type=type,
        latitude=latitude,
        longitude=longitude,
        heading=heading,
        flight_level=flight_level,
        speed=speed,
    )
    assert cmd == True

    pos = all_positions()
    assert isinstance(pos, pd.DataFrame)
    assert len(pos.index) == 1
    assert pos.loc[aircraft_id]["type"] == type
    assert pos.loc[aircraft_id]["latitude"] > 0
    assert pos.loc[aircraft_id]["longitude"] == 0
    assert pos.loc[aircraft_id]["vertical_speed"] == 0
    assert pos.loc[aircraft_id]["altitude"] == flight_level * 100

    # aircraft initial speed may differ from indicated speed
    assert pos.loc[aircraft_id]["ground_speed"] > 150

    # check that dataframe has sim_t attribute
    assert isinstance(pos.sim_t, int)

    cmd = create_aircraft(
        aircraft_id=aircraft_id_2,
        type=type_2,
        latitude=latitude_2,
        longitude=longitude_2,
        heading=heading_2,
        flight_level=flight_level_2,
        speed=speed_2,
    )
    assert cmd == True

    pos = all_positions()
    assert isinstance(pos, pd.DataFrame)
    assert len(pos.index) == 2
    assert pos.loc[aircraft_id]["type"] == type
    assert pos.loc[aircraft_id]["latitude"] > 0
    assert pos.loc[aircraft_id]["longitude"] == 0
    assert pos.loc[aircraft_id]["vertical_speed"] == 0
    assert pos.loc[aircraft_id]["altitude"] == flight_level * 100

    # aircraft initial speed may differ from indicated speed
    assert pos.loc[aircraft_id]["ground_speed"] > 150

    assert pos.loc[aircraft_id_2]["type"] == type_2
    assert pos.loc[aircraft_id_2]["latitude"] < 0
    assert round(pos.loc[aircraft_id_2]["longitude"], 2) == 0
    assert pos.loc[aircraft_id_2]["vertical_speed"] == 0
    assert pos.loc[aircraft_id_2]["altitude"] == flight_level_2 * 100

    # aircraft initial speed may differ from indicated speed
    assert pos.loc[aircraft_id_2]["ground_speed"] > 150

    # check that dataframe has sim_t attribute
    assert isinstance(pos.sim_t, int)


@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_aircraft_position():
    cmd = reset_simulation()
    assert cmd == True

    cmd = create_aircraft(
        aircraft_id=aircraft_id,
        type=type,
        latitude=latitude,
        longitude=longitude,
        heading=heading,
        flight_level=flight_level,
        speed=speed,
    )
    assert cmd == True

    cmd = create_aircraft(
        aircraft_id=aircraft_id_2,
        type=type_2,
        latitude=latitude_2,
        longitude=longitude_2,
        heading=heading_2,
        flight_level=flight_level_2,
        speed=speed_2,
    )
    assert cmd == True

    pos = aircraft_position(aircraft_id)
    assert isinstance(pos, pd.DataFrame)
    assert len(pos.index) == 1
    assert pos.loc[aircraft_id]["type"] == type
    assert pos.loc[aircraft_id]["latitude"] > 0
    assert pos.loc[aircraft_id]["longitude"] == 0
    assert pos.loc[aircraft_id]["vertical_speed"] == 0
    assert pos.loc[aircraft_id]["altitude"] == flight_level * 100

    # aircraft initial speed may differ from indicated speed
    assert pos.loc[aircraft_id]["ground_speed"] > 150

    # check that dataframe has sim_t attribute
    assert isinstance(pos.sim_t, int)

    pos = aircraft_position([aircraft_id, aircraft_id_2])
    assert len(pos.index) == 2
