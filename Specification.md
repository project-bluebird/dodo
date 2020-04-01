# Dodo specification

# Overview

Dodo is a scaffold for air traffic control (ATC) agents implemented in Python and R (PyDodo and rdodo respectively). It provides a set of commands for communicating with [BlueBird](https://github.com/alan-turing-institute/bluebird).

Dodo commands allow one to control [BlueBird](#bluebird-commands), the [simulation](#simulation-commands) or [aircraft in the simultion](#aircraft-commands). Dodo also provides [aircraft information](#aircraft-information), [distance measures](#distance-measures) and performance [metrics](#metrics).

A shared `config.yml` file exists for both rdodo and PyDodo, specifying common required parameters and settings.

## Contents

### BlueBird commands

- [Bluebird config](#bluebird-config)
- [Episode log](#episode-log)

### Simulation commands

- [Upload sector](#create-scenario)
- [Upload scenario](#load-scenario)
- [Create aircraft](#create-aircraft)
- [Reset simulation](#reset-the-simulation)
- [Pause simulation](#pause-the-simulation)
- [Resume simulation](#resume-the-simulation)
- [Set the simulation rate multiplier](#set-the-simulation-rate-multiplier)
- [Simulation step](#simulation-step)

### Aircraft information

- [Get aircraft position](#get-aircraft-position)
- [Get all aircraft positions](#get-all-aircraft-positions)
- [Get aircraft route](#list-aircraft-route)
- [Get current flight level](#current-flight-level)
- [Get requested flight level](#requested-flight-level)
- [Get cleared flight level](#cleared-flight-level)

### Aircraft control

- [Change altitude](#change-aircraft-altitude)
- [Change heading](#change-aircraft-heading)
- [Change speed](#change-aircraft-speed)
- [Change vertical speed](#change-aircraft-vertical-speed)
- [Direct to waypoint](#direct-aircaft-to-waypoint)
- [Batch](#batch)

### Distance measures

- [Geodesic separation](#geodesic-separation)
- [Geodesic distance](#geodesic-distance)
- [Great-circle separation](#great-circle-separation)
- [Great-circle distance](#great-circle-distance)
- [Vertical separation](#vertical-separation)
- [Vertical distance](#vertical-distance)
- [Euclidean separation](#euclidean-separation)
- [Euclidean distance](#euclidean-distance)

### Metrics

- [Loss of separation](#loss-of-separation)
- [Sector exit](#sector-exit)
- [Fuel efficiency](#fuel-efficiency)

---

# Commands

## Bluebird config

**Function name:** `bluebird_config`

**Parameters:**
- `host`: An optional string. The Bluebird host.
- `port`: An optional double. The Bluebird port.
- `version`: An optional string. The Bluebird version.

**Description:** Set Bluebird host, port and version parameters. Default values are taken from the config file.

## Episode log

**Function name:** `episode_log`

**Parameters:** None

**Return value:** A string, the relative path to the log file. An exception is thrown if an error occurs.

**Description:** Get the episode log and save to file in the working directory in a `logs` subdirectory.

## Upload sector

**Function name:** `upload_sector`

**Parameters:**
- `filename`: A string indicating path to sector GeoJSON file on the local machine.
- `sector_name`: A string indicating name to store sector under.

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Load a sector definition and begin the simulation. The sector data format is defined in [Aviary](https://github.com/alan-turing-institute/aviary/blob/master/README.md)

## Upload scenario

**Function name:** `upload_scenario`

**Parameters:**
- `filename`: A string indicating path to scenario JSON file on the local machine.
- `sector_name`: A string indicating name to store scenario under.

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Upload a scenario definition. It requires that a sector definition has already been uploaded. The scenario data format is defined in [Aviary](https://github.com/alan-turing-institute/aviary/blob/master/README.md)

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

## Reset the simulation

**Function name:** `reset_simulation`

**Parameters:** None

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Reset the simulation. If used with the BlueSky simulator, this leads to a clean reset (as if launched from fresh) which means a scenario needs to be reloaded. 

## Pause the simulation

**Function name:** `pause_simulation`

**Parameters:** None

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Pause the simulation. This is only possible if the simulator is run in `sandbox` mode.

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

**Description:** Sets the simulation rate multiplier for the current simulation. By default this multiplier is equal to one (real-time operation). If set to another value, the simulation will run faster (or slower) than real-time, with a fixed multiplier as provided. If in **agent** mode (the BlueBird default), this corresponds to the number of seconds which are progressed during a [simulation step](#simulation-step) command. In **sandbox** mode, a multiplier of 2 would cause the simulation to run twice as fast: 60 simulation minutes take 30 actual minutes. 

## Simulation step

**Function name:** `simulation_step`

**Parameters:** None

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Step forward through the simulation. Step size is based on the [simulation rate multiplier](#set-the-simulation-rate-multiplier). Can only be used if simulator is in [agent mode](#set-simulator-mode), otherwise an exception is thrown.

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

## List aircraft route

**Function name:** `list_route`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.

**Return value:** Dictionary of route information with keys:
- `aircraft_id`:  A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.
- `next_waypoint`: A string. Name of waypoint the aircraft is currently headed toward.
- `route_name`: A string name of the route.
- `route_waypoints`: A list of strings. All the waypoints on the route.

If no aircraft exists with the given ID, or the ID is invalid, an exception is thrown.

If the corresponding aircraft has no route information, a dictionary with just the aircraft_id is returned.

If any other error occurs (e.g. a failure to parse the route information), an exception is thrown.

**Description:** Get a dictionary of waypoints on an aircraft's route.

## Current flight level

**Function name:** `current_flight_level`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.

**Return value:** A non-negative double. The aircraft's current flight level in meters. If an invalid ID is given, or the call to Bluebird fails, an exception is thrown.

**Description:** Get the aircraft's current flight level (in meters).

## Requested flight level

**Function name:** `requested_flight_level`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.

**Return value:** A non-negative double. The aircraft's requested flight level in meters. If an invalid ID is given, or the call to Bluebird fails, an exception is thrown.

**Description:** Get the aircraft's requested flight level (in meters). Can only be returned if the aircraft has a defined route.

## Cleared flight level

**Function name:** `cleared_flight_level`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.

**Return value:** A non-negative double. The aircraft's cleared flight level in meters. If an invalid ID is given, or the call to Bluebird fails, an exception is thrown.

**Description:** Get the aircraft's cleared flight level (in meters). The initial cleared flight level is set to the initial altitude when a scenario is loaded.

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

## Direct aircraft to waypoint

**Function name:** `direct_to_waypoint`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.
- `waypoint_name`: A string waypoint identifier. The waypoint to direct the aircraft to.

**Return value:** `TRUE` if successful. Otherwise an exception is thrown.

**Description:** Request aircraft to change heading toward the waypoint. The waypoint must exist on the aircraft route.

## Batch

**Function name:** `batch`

**Parameters:**
- A list of aircraft control commands. In PyDodo, these need an `async_` prefix. For example, `batch([async_change_speed(...), async_change_altitude(...)]`.

**Return value:** `TRUE` if all commands were successful. Otherwise an exception is thrown.

**Description:** Send a batch of aircraft control commands and dispatch them asynchronously to Bluebird.

## Geodesic separation

**Function name:** `geodesic_separation`

**Parameters:**
- `from_aircraft_id`: A string vector of aircraft IDs.
- `to_aircraft_id`: An optional string vector of aircraft IDs. If not provided, `to_aircraft_id`=`from_aircraft_id`.
- `major_semiaxis`: An optional double. The major (equatorial) radius of the ellipsoid. The default value is for WGS84.
- `flattening`: An optional double. Ellipsoid flattening. The default value is for WGS84.

**Return value:** A dataframe of doubles with `from_aircraft_id` as row names and `to_aircraft_id` as column names. The values are the geodesic distance in metres between the positions of the aircraft pair at each [`from_aircraft_id`, `to_aircraft_id`] index.

If any of the given aircraft IDs does not exist in the simulation, the returned dataframe contains a row or column of missing values for that ID.

**Description:** Get geodesic separation in metres between the positions of all `from_aircraft_id` and `to_aircraft_id` pairs of aircraft.

## Geodesic distance

**Function name:** `geodesic_distance`

**Parameters:**
- `from_lat`: A double in the range [-90, 90]. The `from` point's latitude.
- `from_lon`: A double in the range [-180, 180). The `from` point's longitude.
- `to_lat`: A double in the range [-90, 90]. The `to` point's latitude.
- `to_lon`: A double in the range [-180, 180). The `to` point's longitude.
- `major_semiaxis`: An optional double. The major (equatorial) radius of the ellipsoid. The default value is for WGS84.
- `flattening`: An optional double. Ellipsoid flattening. The default value is for WGS84.

**Return value:** A double, geodesic distance between two points.

**Description:** Get geodesic distance in metres between two points defined in terms of [latitude, longitude].

## Great-circle separation

**Function name:** `great_circle_separation`

**Parameters:**
- `from_aircraft_id`: A string vector of aircraft IDs.
- `to_aircraft_id`: An optional string vector of aircraft IDs. If not provided, `to_aircraft_id`=`from_aircraft_id`.
- `radius`: An optional double. The radius of the earth in metres. The default value is 6378137 m.

**Return value:** A dataframe of doubles with `from_aircraft_id` as row names and `to_aircraft_id` as column names. The values are the great-circle distance in metres between the positions of the aircraft pair at each [`from_aircraft_id`, `to_aircraft_id`] index.

If any of the given aircraft IDs does not exist in the simulation, the returned dataframe contains a row or column of missing values for that ID.

**Description:** Get great-circle separation in metres between the positions of all `from_aircraft_id` and `to_aircraft_id` pairs of aircraft.

## Great-circle distance

**Function name:** `great_circle_distance`

**Parameters:**
- `from_lat`: A double in the range [-90, 90]. The `from` point's latitude.
- `from_lon`: A double in the range [-180, 180). The `from` point's longitude.
- `to_lat`: A double in the range [-90, 90]. The `to` point's latitude.
- `to_lon`: A double in the range [-180, 180). The `to` point's longitude.
- `radius`: An optional double. The radius of the earth in metres. The default value is 6378137 m.

**Return value:** A double, the great-circle distance between two points.

**Description:** Get great-circle distance in metres between two points' positions defined as [latitude, logitude].

## Vertical separation

**Function name:** `vertical_separation`

**Parameters:**
- `from_aircraft_id`: A string vector of aircraft IDs.
- `to_aircraft_id`: An optional string vector of aircraft IDs. If not provided, `to_aircraft_id`=`from_aircraft_id`.

**Return value:** A dataframe of doubles with `from_aircraft_id` as row names and `to` as column names. The values are the vertical distance in metres between the positions of the aircraft pair at each [`from_aircraft_id`, `to_aircraft_id`] index.

If any of the given aircraft IDs does not exist in the simulation, the returned dataframe contains a row or column of missing values for that ID.

**Description:** Get vertical separation in metres between the positions of all `from_aircraft_id` and `to_aircraft_id` pairs of aircraft.

## Vertical distance

**Function name:** `vertical_distance`

**Parameters:**
- `from_alt`: A non-negatige double. The `from` point's altitude in metres.
- `to_alt`: A non-negatige double. The `to` point's altitude in metres.

**Return value:** A double, verticle distance between two points.

**Description:** Get vertical distance in metres between two points' positions defined in altitude.

## Euclidean separation

**Function name:** `euclidean_separation`

**Parameters:**
- `from_aircraft_id`: A string vector of aircraft IDs.
- `to_aircraft_id`: An optional string vector of aircraft IDs. If not provided, `to_aircraft_id`=`from_aircraft_id`.
- `major_semiaxis`: An optional double. The major (equatorial) radius of the ellipsoid. The default value is for WGS84.
- `flattening`: An optional double. Ellipsoid flattening. The default value is for WGS84.

**Return value:** A dataframe of doubles with `from_aircraft_id` as row names and `to_aircraft_id` as column names. The values are the euclidean distance in metres between the positions of the aircraft pair at each [`from_aircraft_id`, `to_aircraft_id`] index.

If any of the given aircraft IDs does not exist in the simulation, the returned dataframe contains a row or column of missing values for that ID.

**Description:** Get euclidean separation in metres between the positions of all `from_aircraft_id` and `to_aircraft_id` pairs of aircraft. The aircraft positions are converted to [ECEF](https://en.wikipedia.org/wiki/ECEF) coordinates to calculate separation.

## Euclidean distance

**Function name:** `euclidean_distance`

**Parameters:**
- `from_lat`: A double in the range [-90, 90]. The `from` point's latitude.
- `from_lon`: A double in the range [-180, 180). The `from` point's longitude.
- `from_alt`: A non-negatige double. The `from` point's altitude in metres.
- `to_lat`: A double in the range [-90, 90]. The `to` point's latitude.
- `to_lon`: A double in the range [-180, 180). The `to` point's longitude.
- `to_alt`: A non-negatige double. The `to` point's altitude in metres.
- `major_semiaxis`: An optional double. The major (equatorial) radius of the ellipsoid. The default value is for WGS84.
- `flattening`: An optional double. Ellipsoid flattening. The default value is for WGS84.

**Return value:** A double, euclidean distance between two points.

**Description:** Get euclidean distance in metres between two points' positions defined as [latitude, logitude, altitude]. The points are converted to [ECEF](https://en.wikipedia.org/wiki/ECEF) coordinates to calculate distance.

## Loss of separation

**Function name:** `loss_of_separation`

**Parameters:**
- `from_aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.
- `to_aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.

**Return value:** A double, the loss of separation score between `from_aircraft_id` and `to_aircraft_id`. If any of the given aircraft IDs does not exist in the simulation, returns missing value.

**Description:** The metric comes from [Aviary](https://github.com/alan-turing-institute/aviary/blob/master/README.md).

## Sector exit

**Function name:** `sector_exit`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.

**Return value:** A double, the sector exit score for `aircraft_id`. If the aircraft does not exist in the simulation or has not exited the sector yet, returns missing value.

**Description:** The metric comes from [Aviary](https://github.com/alan-turing-institute/aviary/blob/master/README.md).

## Fuel efficiency

**Function name:** `fuel_efficiency`

**Parameters:**
- `aircraft_id`: A string aircraft identifier. For the BlueSky simulator, this has to be at least three characters.

**Return value:** A double, the fuel efficiency score for `aircraft_id`.

**Description:** The metric comes from [Aviary](https://github.com/alan-turing-institute/aviary/blob/master/README.md).
