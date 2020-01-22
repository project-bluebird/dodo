#' Create an aircraft
#'
#' Either the \code{altitude} or \code{flight_level} argument must be given,
#' but not both.
#'
#' If an aircraft with the given \code{aircraft_id} already exists an error is
#' thrown.
#'
#' @param aircraft_id
#' A string aircraft identifier
#' @param type
#' A string ICAO aircraft type designator
#' @param latitude
#' A double in the range [-90, 90]. The aircraft's latitude.
#' @param longitude
#' A double in the range [-180, 180). The aircraft's longitude.
#' @param heading
#' An integer in the range [0, 360). The aircraft's heading in degrees.
#' @param altitude
#' The aircraft's altitude in feet expressed as a double in the range [0, 6000]
#' or a quantity whose units can be converted to feet. For altitudes in excess
#' of 6000ft a flight level should be specified instead.
#' @param flight_level
#' A integer of 60 or more. The aircraft's flight level.
#' @param speed
#' The aircraft's speed in knots (KCAS) expressed as a non-negative double or
#' a quantity whose units can be converted to knots.
#'
#' @return
#' \code{TRUE} if successful. Otherwise \code{FALSE} and an error is thrown.
#'
#' @examples
#' \dontrun{
#' create_aircraft("test1234", "B744", 0, 0, 0, flight_level = 250, speed = 200)
#' }
#' @import httr units
#' @export
create_aircraft <- function(aircraft_id,
                            type,
                            latitude,
                            longitude,
                            heading,
                            altitude = NULL,
                            flight_level = NULL,
                            speed) {

  validate_aircraft_id(aircraft_id)
  validate_aircraft_type(type)
  validate_latitude(latitude)
  validate_longitude(longitude)
  validate_heading(heading)
  validate_speed(speed)

  # Either altitude or flight_level must be NULL, but not both.
  stopifnot(is.null(altitude) || is.null(flight_level))

  if (is.null(altitude)) {
    flight_level <- validate_flight_level(flight_level)
    alt <- paste0("FL", flight_level)
  }
  if (is.null(flight_level)) {
    validate_altitude(altitude)
    units(altitude) <- with(units::ud_units, ft)
    alt <- as.double(altitude)
  }

  # Assign/convert units as necessary.
  units(speed) <- with(units::ud_units, "knots")

  # TODO: replace string literals with config parameters from Bluebird.
  body <- list(
    "callsign" = aircraft_id,
    "type" = type,
    "lat" = latitude,
    "lon" = longitude,
    "hdg" = heading,
    "alt" = alt,
    "gspd" = as.double(speed)
  )

  post_call(endpoint = config_param("endpoint_create_aircraft"), body = body)
}

# Validate a *scalar* aircraft ID.
validate_aircraft_id <- function(aircraft_id) {

  stopifnot(is.character(aircraft_id), length(aircraft_id) == 1)
  if (config_param("simulator") == config_param("bluesky_simulator"))
    stopifnot(nchar(aircraft_id) >= 3)
}

validate_aircraft_type <- function(type) {

  stopifnot(is.character(type), length(type) == 1)
}

validate_latitude <- function(latitude) {

  stopifnot(is.double(latitude), length(latitude) == 1,
            latitude >= -90, latitude <= 90)
}

validate_longitude <- function(longitude) {

  stopifnot(is.double(longitude), length(longitude) == 1,
            longitude >= -180, longitude < 180)
}

validate_heading <- function(heading) {

  # Check that heading is an integer value, without requiring is.integer.
  if (!is.integer(heading))
    stopifnot(heading %% 1 == 0)

  stopifnot(is.double(heading), length(heading) == 1,
            heading >= 0, heading < 360)
}

#' @import units
validate_speed <- function(speed) {

  # If the given speed has no units, check its valid.
  if (!inherits(speed, "units"))
    stopifnot(is.double(speed), length(speed) == 1, speed >= 0)

  # Check that the given speed can be converted to knots (o/w raise an error).
  units(speed) <- with(units::ud_units, "knots")
}

validate_altitude <- function(altitude) {

  # If the given altitude has no units, check its valid.
  if (!inherits(altitude, "units"))
    stopifnot(is.double(altitude),
              length(altitude) == 1,
              altitude >= 0,
              altitude <= config_param("feet_altitude_upper_limit"))

  # Check that the given altitude can be converted to feet (o/w raise an error).
  units(altitude) <- with(units::ud_units, ft)
}

validate_flight_level <- function(flight_level) {

  stopifnot(length(flight_level) == 1, is.numeric(flight_level),
            flight_level >= config_param("flight_level_lower_limit"))

  # Check that flight_level is an integer value, without requiring is.integer.
  if (!is.integer(flight_level))
    stopifnot(flight_level %% 1 == 0)

  # Return the integer flight level.
  as.integer(flight_level)
}
