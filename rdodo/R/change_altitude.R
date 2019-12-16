#' Send a "change altitude" command
#'
#' Request an aircraft to change altitude.
#'
#' Either the \code{altitude} or \code{flight_level} argument must be given,
#' but not both.
#'
#' @param aircraft_id
#' A string aircraft identifier
#' @param altitude
#' The aircraft's new altitude in feet expressed as a double in the range
#' [0, 6000] or as a quantity whose units can be converted to feet. For
#' altitudes in excess of 6000ft a flight level should be specified instead.
#' @param flight_level
#' A integer of 60 or more. The aircraft's flight level.
#' @param vertical_speed
#' The vertical speed expressed as a non-negative double or as a quantity whose
#' units can be converted to feet/min.
#'
#' @return
#' \code{TRUE} if successful. Otherwise \code{FALSE} and an error is thrown.
#'
#' @examples
#' \dontrun{
#' change_altitude("test1234", flight_level = 450)
#' change_altitude("test1234", altitude = 5000)
#' }
#'
#' @import units
#' @export
change_altitude <- function(aircraft_id,
                            altitude = NULL,
                            flight_level = NULL,
                            vertical_speed = NULL) {

  validate_aircraft_id(aircraft_id)

  # Validate vertical speed argument & assign/convert units as necessary.
  if (!is.null(vertical_speed)) {
    validate_speed(vertical_speed)
    units(vertical_speed) <- with(units::ud_units, ft/min)
  }

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

  # TODO: replace string literals with config parameters from Bluebird.
  body <- list(
    "acid" = aircraft_id,
    "alt" = alt
  )

  if (!is.null(vertical_speed)) {
    l <- list("vs" = as.double(vertical_speed))
    body <- c(body, l)
  }

  post_call(endpoint = config_param("endpoint_change_altitude"), body = body)
}
