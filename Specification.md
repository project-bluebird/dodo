# Dodo specification

## Create scenario simulation

**Function name:** `create_simulation`

**Parameters:**
- `filename`: A string indicating path to scenario file.

**Return value:** A boolean, `TRUE` indicates success.

**Description:** Load scenario file and begin simulation.

## Reset the simulation

**Function name:** `reset_simulation`

**Parameters:**

**Return value:** A boolean, `TRUE` indicates success.

**Description:** Reset simulation to the start of the currently running scenario.

## Create aircraft

**Function name:** `create_aircraft`

**Parameters:**
- `aircraft_id`: A string aircraft identifier.
- `type`: A string ICAO aircraft type designator.
- `latitude`: A double in the range [-90, 90]. The aircraft's latitude.
- `longitude`: A double in the range [-180, 180). The aircraft's longitude.
- `heading`: A double in the range [0, 360). The aircraft's heading in degrees.
- `altitude`: A double in the range [0, 6000]. The aircraft's altitude in feet. For altitudes in excess of 6000ft a flight level should be specified instead.
- `flight_level`: A integer of 60 or more. The aircraft's flight level.
- `speed`: A non-negative double. The aircraft's speed in knots (KCAS).

Either the `altitude` or `flight_level` argument must be given, but not both.

**Return value:** A boolean, `TRUE` indicates success.

**Description:** Inititate a new aircraft in the simulation at the given position, heading and speed.

## Get aircraft position

**Function name:** `aircraft_position`

**Parameters:**
- `aircraft_id`: Optional string or vector of strings indicating aircraft IDs. Can also pass string `all`.

**Return value:** Dataframe indexed by aircraft ID with columns:
  - `aircraft_id`: A string aircraft identifier.
  - `altitude`: A double in the range [0, 6000]. The aircraft's altitude in feet.
  - `ground_speed`: A non-negative double. The aircraft's ground speed in knots.
  - `latitude`: A double in the range [-90, 90]. The aircraft's latitude.
  - `longitude`: A double in the range [-180, 180). The aircraft's longitude.
  - `vertical_speed`: A double. The aircraft's vertical speed in feet/min (units according to BlueSky docs).

If aircraft ID does not exist, returns row with NULLs for that aircraft ID.

**Description:** Get position information for a single or multiple aircrafts in the simulation. Can request specific aircraft IDs or all aircraft in the simulation.

## Change aircraft altitude

**Function name:** `change_aircraft_altitude`

**Parameters:**
- `aircraft_id`: A string aircraft identifier
- `altitude`: A double in the range [0, 6000]. The aircraft's altitude in feet.
- `vertical_speed`: A optional double. The aircraft's vertical speed in feet/min (units according to BlueSky docs).

**Return value:** A boolean, `TRUE` indicates success.

**Description:** Request change to aircraft altitude.

## Change aircraft heading

**Function name:** `change_aircraft_heading`

**Parameters:**
- `aircraft_id`: A string aircraft identifier.
- `heading`: A double in the range [0, 360). The aircraft's heading in degrees.

**Return value:** A boolean, `TRUE` indicates success.

**Description:** Request change to aircraft heading.

## Change aircraft vertical speed

**Function name:** `change_aircraft_vertical_speed`

**Parameters:**
- `aircraft_id`: A string aircraft identifier.
- `vertical_speed`: A double. The aircraft's vertical speed in feet/min (units according to BlueSky docs).

**Return value:** A boolean, `TRUE` indicates success.

**Description:** Request change to aircraft vertical speed.

## Change aircraft speed

**Function name:** `change_aircraft_speed`

**Parameters:**
- `aircraft_id`: A string aircraft identifier.
- `speed`: A non-negative double. The aircraft's speed in knots.

**Return value:** A boolean, `TRUE` indicates success.

**Description:** Request change to aircraft speed.
