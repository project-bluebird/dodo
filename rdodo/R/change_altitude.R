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
#' A double in the range [0, 6000]. The aircraft's new altitude in feet.
#' For altitudes in excess of 6000ft a flight level should be specified instead.
#' @param flight_level
#' A integer of 60 or more. The aircraft's flight level.
#' @param vertical_speed
#' A non-negative double. The requested vertical speed in feet/min.
#'
#' @return
#' \code{TRUE} if successful. Otherwise \code{FALSE} and an error is thrown.
#'
#' @examples
#' \dontrun{
#' change_altitude("test1234", flight_level = 450)
#' change_altitude("test1234", altitude = 5000)
#' }
#' @import httr
#' @export
change_altitude <- function(aircraft_id,
                            altitude = NULL,
                            flight_level = NULL,
                            vertical_speed = NULL) {

  stopifnot(is.character(aircraft_id), length(aircraft_id) == 1)

  if (!is.null(vertical_speed))
    validate_speed(vertical_speed)

  # TODO: move to validate_flight_level and validate_altitude functions.

  # Either altitude or flight_level must be NULL, but not both.
  stopifnot(is.null(altitude) || is.null(flight_level))
  if (is.null(altitude)) {
    flight_level <- validate_flight_level(flight_level)

    # Flight level unit corresponds to hundreds of feet.
    altitude <- flight_level * 100
  }
  if (is.null(flight_level))
    validate_altitude(altitude)

  # TODO: replace string literals with config parameters from Bluebird.
  body <- list(
    "acid" = aircraft_id,
    "alt" = altitude
  )

  if (!is.null(vertical_speed)) {
    l <- list("vs" = vertical_speed)
    body <- c(body, l)
  }

  post_call(endpoint = config_param("endpoint_change_altitude"), body = body)
}
