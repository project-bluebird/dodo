# Dodo specification

# Overview

Dodo is a scaffold for air traffic control (ATC) agents implemented in Python and R (PyDodo and rdodo respectively). It provides a set of commands for communicating with [BlueBird](https://github.com/alan-turing-institute/bluebird), an API for communicating with ATC simulators (e.g, [BlueSky](https://github.com/alan-turing-institute/bluesky)).

A shared `config.yaml` file exists for both rdodo and PyDodo, specifying common required parameters, settings and test cases.

TO DO:  
A separate `config.yaml` should exist for each simulator with an easy way of specifying which to use.

# Commands

### Create scenario simulation

**Function name:** `create_simulation`

**Parameters:**
- `filename`: A string indicating path to scenario file. The path is relative to the simulator (e.g., BlueSky) root directory (e.g., `scenario/8.SCN`).

**Return value:** A boolean, `TRUE` indicates success.

**Description:** Load scenario file and begin simulation.

### Reset the simulation

**Function name:** `reset_simulation`

**Parameters:**

**Return value:** A boolean, `TRUE` indicates success.

**Description:** Reset simulation to the start of the currently running scenario (if one is running).

### Create aircraft

**Function name:** `create_aircraft`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.
- `type`: A string ICAO aircraft type designator.
- `latitude`: A double in the range [-90, 90]. The aircraft's latitude.
- `longitude`: A double in the range [-180, 180). The aircraft's longitude.
- `heading`: A double in the range [0, 360). The aircraft's heading in degrees.
- `altitude`: A double in the range [0, 6000]. The aircraft's altitude in feet. For altitudes in excess of 6000ft a flight level should be specified instead.
- `flight_level`: A integer of 60 or more. The aircraft's flight level.
- `speed`: A non-negative double. The aircraft's speed in knots (KCAS).

Either the `altitude` or `flight_level` argument must be given, but not both.

**Return value:** A boolean, `TRUE` indicates success.

**Description:** Initiate a new aircraft in the simulation at the given position, heading and speed.

### Get aircraft position

**Function name:** `aircraft_position`

**Parameters:**
- `aircraft_id`: Optional string `all` or single aircraft ID. For the BlueSky simulator, this has to be at least three characters.

**Return value:** Dataframe indexed by aircraft ID with columns:
  - `aircraft_id`: A string aircraft identifier.
  - `altitude`: A double in the range [0, 6000]. The aircraft's altitude in feet.
  - `ground_speed`: A non-negative double. The aircraft's ground speed in knots.
  - `latitude`: A double in the range [-90, 90]. The aircraft's latitude.
  - `longitude`: A double in the range [-180, 180). The aircraft's longitude.
  - `vertical_speed`: A double. The aircraft's vertical speed in feet/min (units according to BlueSky docs).

If aircraft ID does not exist, returns row with NULLs for that aircraft ID.

**Description:** Get position information for a single or all aircrafts currently in the simulation.

### Change aircraft altitude

**Function name:** `change_aircraft_altitude`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.
- `altitude`: A double in the range [0, 6000]. The aircraft's altitude in feet.
- `vertical_speed`: A optional double. The aircraft's vertical speed in feet/min (units according to BlueSky docs).

**Return value:** A boolean, `TRUE` indicates success.

**Description:** Request change to aircraft altitude.

### Change aircraft heading

**Function name:** `change_aircraft_heading`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.
- `heading`: A double in the range [0, 360). The aircraft's heading in degrees.

**Return value:** A boolean, `TRUE` indicates success.

**Description:** Request change to aircraft heading.

### Change aircraft vertical speed

**Function name:** `change_aircraft_vertical_speed`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.
- `vertical_speed`: A double. The aircraft's vertical speed in feet/min (units according to BlueSky docs).

**Return value:** A boolean, `TRUE` indicates success.

**Description:** Request change to aircraft vertical speed.

### Change aircraft speed

**Function name:** `change_aircraft_speed`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.
- `speed`: A non-negative double. The aircraft's speed in knots.

**Return value:** A boolean, `TRUE` indicates success.

**Description:** Request change to aircraft speed.