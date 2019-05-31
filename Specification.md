# Dodo specification

# Overview

Dodo is a scaffold for air traffic control (ATC) agents implemented in Python and R (PyDodo and rdodo respectively). It provides a set of commands for communicating with [BlueBird](https://github.com/alan-turing-institute/bluebird), an API for communicating with ATC simulators (e.g, [BlueSky](https://github.com/alan-turing-institute/bluesky)).

A shared `config.yml` file exists for both rdodo and PyDodo, specifying common required parameters, settings and test cases.

## Contents

### Simulation commands

- [Load Scenario](#load-scenario) [TO DO]
- [Reset Simulation](#reset-the-simulation)
- [Pause Simulation](#pause-the-simulation)
- [Resume Simulation](#resume-the-simulation)
- [Set Simulation Rate Multiplier](#set-the-simulation-rate-multiplier)
- [Episode Log](#episode-log) [TO DO]
- [Shutdown](#shutdown) [TO DO]

### Aircraft commands

- [Create Aircraft](#create-aircraft)
- [Get aircraft position](#get-aircraft-position)
- [Get all aircraft positions](#get-all-aircraft-positions)
- [Change Altitude](#change-aircraft-altitude)
- [Change Heading](#change-aircraft-heading)
- [Change Speed](#change-aircraft-speed)
- [Change Vertical Speed](#change-aircraft-vertical-speed)
- [List Route](#list-aircraft-route)
- [Direct to Waypoint](#direct-aircaft-to-waypoint)

### Distance measures

- [Geodesic separation](#geodesic-separation) [TO DO]
- [Geodesic distance](#geodesic-distance) [TO DO]
- [Great-circle separation](#great-circle-separation) [TO DO]
- [Great-circle distance](#great-circle-distance) [TO DO]
- [Vertical separation](#vertical-separation) [TO DO]
- [Vertical distance](#vertical-distance) [TO DO]
- [Euclidean separation](#euclidean-separation) [TO DO]
- [Euclidean distance](#euclidean-distance) [TO DO]

# Commands

## Load scenario

**Function name:** `load_scenario`

**Parameters:**
- `filename`: A string indicating path to scenario file.
- `multiplier`: An optional double. Simulation rate multiplier.

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Load a scenario file and begin the simulation.

Currently, the path is relative to the simulator (e.g., BlueSky) root directory (e.g., `scenario/8.SCN`).

## Reset the simulation

**Function name:** `reset_simulation`

**Parameters:** None

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Reset simulation to the start of the currently running scenario.

## Pause the simulation

**Function name:** `pause_simulation`

**Parameters:** None

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Pause the simulation.

## Resume the simulation

**Function name:** `resume_simulation`

**Parameters:** None

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Resume the simulation after a pause.

## Set the simulation rate multiplier

**Function name:** `set_simulation_rate_multiplier`

**Parameters:**
- `multiplier`: A positive double.

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Sets the simulation rate multiplier for the current simulation. By default this multiplier is equal to one (real-time operation). If set to another value, the simulation will run faster (or slower) than real-time, with a fixed multiplier as provided. For example, a multiplier of 2 would cause the simulation to run twice as fast: 60 simulation minutes take 30 actual minutes.

## Create aircraft

**Function name:** `create_aircraft`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.
- `type`: A string ICAO aircraft type designator.
- `latitude`: A double in the range [-90, 90]. The aircraft's initial latitude.
- `longitude`: A double in the range [-180, 180). The aircraft's initial longitude.
- `heading`: A double in the range [0, 360). The aircraft's initial heading in degrees.
- `altitude`: A double in the range [0, 6000]. The aircraft's initial altitude in feet. For altitudes in excess of 6000ft a flight level should be specified instead.
- `flight_level`: An integer of 60 or more. The aircraft's initial flight level.
- `speed`: A non-negative double. The aircraft's initial calibrated air speed in knots (KCAS).

Either the `altitude` or `flight_level` argument must be given, but not both.

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Initiate a new aircraft in the simulation at the given position, heading and speed.

## Get aircraft position

**Function name:** `aircraft_position`

**Parameters:**
- `aircraft_id`: A string or vector of strings representing one or more aircraft IDs. For the BlueSky simulator, each ID must contain at least three characters.

**Return value:** Dataframe indexed by **uppercase** aircraft ID with columns:
  - `type`: A string ICAO aircraft type designator.
  - `altitude`: A non-negatige double. The aircraft's altitude in feet.
  - `ground_speed`: A non-negative double. The aircraft's ground speed in knots.
  - `latitude`: A double in the range [-90, 90]. The aircraft's latitude.
  - `longitude`: A double in the range [-180, 180). The aircraft's longitude.
  - `vertical_speed`: A double. The aircraft's vertical speed in feet/min (units according to BlueSky docs).

This dataframe also contains a metadata attribute named `sim_t` containing the simulator time in seconds since the start of the scenario.

If any of the given aircraft IDs does not exist in the simulation, the returned dataframe contains a row of missing values for that ID.

If an invalid ID is given, or the call to Bluebird fails, an exception is thrown.

**Description:** Get position information for a single aircraft currently in the simulation.

## Get all aircraft positions

**Function name:** `all_positions`

**Parameters:** None

**Return value:** Dataframe indexed by **uppercase** aircraft ID with columns:
  - `type`: A string ICAO aircraft type designator.
  - `altitude`: A non-negatige double. The aircraft's altitude in feet.
  - `ground_speed`: A non-negative double. The aircraft's ground speed in knots.
  - `latitude`: A double in the range [-90, 90]. The aircraft's latitude.
  - `longitude`: A double in the range [-180, 180). The aircraft's longitude.
  - `vertical_speed`: A double. The aircraft's vertical speed in feet/min (units according to BlueSky docs).

This dataframe also contains a metadata attribute named `sim_t` containing the simulator time in seconds since the start of the scenario.

If no aircraft exists an empty data frame is returned.

If the response from Bluebird contains an error status code, an exception is thrown.

**Description:** Get position information for all aircraft currently in the simulation.

## Change aircraft altitude

**Function name:** `change_altitude`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.
- `altitude`: A double in the range [0, 6000]. The requested altitude in feet. For altitudes in excess of 6000ft a flight level should be specified instead.
- `flight_level`: An integer of 60 or more. The requested flight level.
- `vertical_speed`: An optional double. The requested vertical speed for the climb/descent in feet/min (units according to BlueSky docs).

Either the `altitude` or `flight_level` argument must be given, but not both.

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Request change to aircraft altitude.

## Change aircraft heading

**Function name:** `change_heading`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.
- `heading`: A double in the range [0, 360). The requested heading in degrees.

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Request change to aircraft heading.

## Change aircraft vertical speed

**Function name:** `change_vertical_speed`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.
- `vertical_speed`: A double. The requested vertical speed in feet/min (units according to BlueSky docs).

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Request change to aircraft vertical speed.

## Change aircraft speed

**Function name:** `change_speed`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.
- `speed`: A non-negative double. The requested calibrated air speed in knots (KCAS).

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Request change to aircraft speed.

## List aircraft route

**Function name:** `list_route`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.

**Return value:** A  dataframe indexed by waypoint name with columns:
- `requested_altitude`: A non-negatige double. The aircraft's requested altitude in feet at waypoint.
- `requested_speed`: A non-negative double. The aircraft's requested speed at waypoint.
- `current`: A boolean indicating whether the aircraft is currently heading toward this waypoint.

This dataframe also contains metadata attributes named `aircraft_id` and `sim_t` containing the simulator time in seconds since the start of the scenario.

If no aircraft exists with the given ID, or the ID is invalid, an exception is thrown.

If the corresponding aircraft has no route information, an empty dataframe is returned and the `sim_t` metadata attribute is omitted.

If any other error occurs (e.g. a failure to parse the route information), an exception is thrown.

**Description:** Get a dataframe of waypoints on an aircraft's route.

## Direct aircaft to waypoint

**Function name:** `direct_to_waypoint`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.
- `waypoint_name`: A string waypoint identifier. The waypoint to direct the aircraft to.

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Request aircraft to change heading toward the waypoint. The waypoint must exist on the aircraft route.

## Geodesic separation

**Function name:** `geodesic_separation`

**Parameters:**
- `from`: A string vector of aircraft IDs.
- `to`: An optional string vector of aircraft IDs. If not provided, `to`=`from`.

**Return value:** A structured array of doubles with `from` aircraft IDs as row names and `to` aircraft IDs as column names. The values are the geodesic distance in metres between the positions of the aircraft pair at each [`from`, `to`] index.

**Description:** Get geodesic separation in metres between the positions of all `from` and `to` pairs of aircraft. 

## Geodesic distance

**Function name:** `geodesic_distance`

**Parameters:**
- `from_lat`: A double in the range [-90, 90]. The `from` point's latitude.
- `from_long`: A double in the range [-180, 180). The `from` point's longitude.
- `to_lat`: A double in the range [-90, 90]. The `to` point's latitude.
- `to_long`: A double in the range [-180, 180). The `to` point's longitude.

**Return value:** A double, geodesic distance between two points. 

**Description:** Get geodesic distance between two points defined in terms of [latitude, longitude].

## Great-circle separation

**Function name:** `great_circle_separation`

**Parameters:**
- `from`: A string vector of aircraft IDs.
- `to`: An optional string vector of aircraft IDs. If not provided, `to`=`from`.

**Return value:** A structured array of doubles with `from` aircraft IDs as row names and `to` aircraft IDs as column names. The values are the great-circle distance in metres between the positions of the aircraft pair at each [`from`, `to`] index.

**Description:** Get great-circle separation in metres between the positions of all `from` and `to` pairs of aircraft. 

## Great-circle distance

**Function name:** `great_circle_distance`

**Parameters:**
- `from_lat`: A double in the range [-90, 90]. The `from` point's latitude.
- `from_long`: A double in the range [-180, 180). The `from` point's longitude.
- `to_lat`: A double in the range [-90, 90]. The `to` point's latitude.
- `to_long`: A double in the range [-180, 180). The `to` point's longitude.

**Return value:** A double, the great-circle distance between two points.

**Description:** Get great-circle distance between two points' positions defined as [latitude, logitude].

## Vertical separation

**Function name:** `vertical_separation`

**Parameters:**
- `from`: A string vector of aircraft IDs.
- `to`: An optional string vector of aircraft IDs. If not provided, `to`=`from`.

**Return value:** A structured array of doubles with `from` aircraft IDs as row names and `to` aircraft IDs as column names. The values are the vertical distance in metres between the positions of the aircraft pair at each [`from`, `to`] index.

**Description:** Get vertical separation in metres between the positions of all `from` and `to` pairs of aircraft. 

## Vertical distance

**Function name:** `vertical_distance`

**Parameters:**
- `from_alt`: A non-negatige double. The `from` point's altitude in metres.
- `to_alt`: A non-negatige double. The `to` point's altitude in metres.

**Return value:** A double, verticle distance between two points.

**Description:** Get vertical distance between two points' positions defined in altitude.

## Euclidean separation

**Function name:** `euclidean_separation`

**Parameters:**
- `from`: A string vector of aircraft IDs.
- `to`: An optional string vector of aircraft IDs. If not provided, `to`=`from`.

**Return value:** A structured array of doubles with `from` aircraft IDs as row names and `to` aircraft IDs as column names. The values are the euclidean distance in metres between the positions of the aircraft pair at each [`from`, `to`] index.

**Description:** Get euclidean separation in metres between the positions of all `from` and `to` pairs of aircraft. 

## Euclidean distance

**Function name:** `euclidean_distance`

**Parameters:**
- `from_lat`: A double in the range [-90, 90]. The `from` point's latitude.
- `from_long`: A double in the range [-180, 180). The `from` point's longitude.
- `from_alt`: A non-negatige double. The `from` point's altitude in metres.
- `to_lat`: A double in the range [-90, 90]. The `to` point's latitude.
- `to_long`: A double in the range [-180, 180). The `to` point's longitude.
- `to_alt`: A non-negatige double. The `to` point's altitude in metres.

**Return value:** A double, euclidean distance between two points.

**Description:** Get euclidean distance between two points' positions defined as [latitude, logitude, altitude].
