# Dodo specification

# Overview

Dodo is a scaffold for air traffic control (ATC) agents implemented in Python and R (PyDodo and rdodo respectively). It provides a set of commands for communicating with [BlueBird](https://github.com/alan-turing-institute/bluebird), an API for communicating with ATC simulators (e.g, [BlueSky](https://github.com/alan-turing-institute/bluesky)).

A shared `config.yaml` file exists for both rdodo and PyDodo, specifying common required parameters, settings and test cases.

# Commands

## Load simulation

**Function name:** `load_simulation`

**Parameters:**
- `filename`: A string indicating path to scenario file. 

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Load scenario file and begin simulation.

Currently, the path is relative to the simulator (e.g., BlueSky) root directory (e.g., `scenario/8.SCN`). 

## Reset the simulation

**Function name:** `reset_simulation`

**Parameters:** None

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Reset simulation to the start of the currently running scenario.

## Create aircraft

**Function name:** `create_aircraft`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.
- `type`: A string ICAO aircraft type designator.
- `latitude`: A double in the range [-90, 90]. The aircraft's latitude.
- `longitude`: A double in the range [-180, 180). The aircraft's longitude.
- `heading`: A double in the range [0, 360). The aircraft's heading in degrees.
- `altitude`: A double in the range [0, 6000]. The aircraft's altitude in feet. For altitudes in excess of 6000ft a flight level should be specified instead.
- `flight_level`: An integer of 60 or more. The aircraft's flight level.
- `speed`: A non-negative double. The aircraft's speed in knots (KCAS).

Either the `altitude` or `flight_level` argument must be given, but not both.

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Initiate a new aircraft in the simulation at the given position, heading and speed.

## Get aircraft position

**Function name:** `aircraft_position`

**Parameters:**
- `aircraft_id`: Optional string `all` or single aircraft ID. For the BlueSky simulator, this has to be at least three characters.

**Return value:** Dataframe indexed by aircraft ID with columns:
  - `altitude`: A non-negatige double. The aircraft's altitude in feet.
  - `ground_speed`: A non-negative double. The aircraft's ground speed in knots.
  - `latitude`: A double in the range [-90, 90]. The aircraft's latitude.
  - `longitude`: A double in the range [-180, 180). The aircraft's longitude.
  - `vertical_speed`: A double. The aircraft's vertical speed in feet/min (units according to BlueSky docs).

If aircraft ID does not exist, returns row with NULLs for that aircraft ID.

If any parameter is invalid, or the response from Bluebird contains an error status code, an exception is thrown.

**Description:** Get position information for a single or all aircraft currently in the simulation.

## Change aircraft altitude

**Function name:** `change_altitude`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.
- `altitude`: A double in the range [0, 6000]. The aircraft's altitude in feet. For altitudes in excess of 6000ft a flight level should be specified instead.
- `flight_level`: An integer of 60 or more. The aircraft's flight level.
- `vertical_speed`: An optional double. The aircraft's vertical speed in feet/min (units according to BlueSky docs).

Either the `altitude` or `flight_level` argument must be given, but not both.

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Request change to aircraft altitude.

## Change aircraft heading

**Function name:** `change_heading`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.
- `heading`: A double in the range [0, 360). The aircraft's heading in degrees.

**Return value:** A boolean, `TRUE` indicates success.

**Description:** Request change to aircraft heading.

## Change aircraft vertical speed

**Function name:** `change_vertical_speed`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.
- `vertical_speed`: A double. The aircraft's vertical speed in feet/min (units according to BlueSky docs).

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Request change to aircraft vertical speed.

## Change aircraft speed

**Function name:** `change_speed`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.
- `speed`: A non-negative double. The aircraft's speed in knots.

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Request change to aircraft speed.
