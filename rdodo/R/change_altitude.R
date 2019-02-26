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
#' A double in the range [0, 6000]. The aircraft's altitude in feet.
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
#' @import config httr
#' @export
change_altitude <- function(aircraft_id,
                            altitude = NULL,
                            flight_level = NULL,
                            vertical_speed = NULL) {

  stopifnot(is.character(aircraft_id), length(aircraft_id) == 1)

  if (!is.null(vertical_speed))
    stopifnot(is.double(vertical_speed), length(vertical_speed) == 1,
              vertical_speed >= 0)

  # TODO: move to validate_flight_level and validate_altitude functions.

  # Either altitude or flight_level must be NULL, but not both.
  stopifnot(is.null(altitude) || is.null(flight_level))
  if (is.null(altitude)) {

    # Check that flight_level is an integer value, without requiring is.integer.
    if (!is.integer(flight_level)) {
      stopifnot(is.numeric(flight_level), flight_level %% 1 == 0)
      flight_level <- as.integer(flight_level)
    }
    stopifnot(is.integer(flight_level), length(flight_level) == 1,
              flight_level >= config::get("flight_level_lower_limit"))

    # Flight level unit corresponds to hundreds of feet.
    altitude <- flight_level * 100
  }
  if (is.null(flight_level)) {
    stopifnot(is.double(altitude), length(altitude) == 1,
              altitude >= 0, altitude <= config::get("feet_altitude_upper_limit"))
  }

  body <- list(
    "acid" = aircraft_id,
    "alt" = altitude
  )

  if (!is.null(vertical_speed)) {
    l <- list("vs" = vertical_speed)
    body <- c(body, l)
  }

  endpoint <- config::get("endpoint_change_altitude")
  response <- httr::POST(url = construct_endpoint_url(endpoint = endpoint),
                         body = body, encode = "json")

  validate_response(response)
  TRUE
}
