#' Create an aircraft
#'
#' Either the \code{altitude} or \code{flight_level} argument must be given,
#' but not both.
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
#' A double in the range [0, 360). The aircraft's heading in degrees.
#' @param altitude
#' A double in the range [0, 6000]. The aircraft's altitude in feet.
#' For altitudes in excess of 6000ft a flight level should be specified instead.
#' @param flight_level
#' A integer of 60 or more. The aircraft's flight level.
#' @param speed
#' A double. The aircraft's speed in knots (KCAS).
#'
#' @return A boolean, \code{TRUE} indicates success.
#'
#' @examples
#' \dontrun{
#' create_aircraft("test1234", "B744", 0, 0, 0, flight_level = 250, speed = 200)
#' }
#'
#' @export
create_aircraft <- function(aircraft_id,
                            type,
                            latitude,
                            longitude,
                            heading,
                            altitude = NULL,
                            flight_level = NULL,
                            speed) {

  stopifnot(is.character(aircraft_id), length(aircraft_id) == 1)
  stopifnot(is.character(type), length(type) == 1)

  stopifnot(is.double(latitude), length(latitude) == 1,
            latitude >= -90, latitude <= 90)
  stopifnot(is.double(longitude), length(longitude) == 1,
            longitude >= -180, longitude < 180)
  stopifnot(is.double(heading), length(heading) == 1,
            heading >= 0, heading < 360)
  stopifnot(is.double(speed), length(speed) == 1)

  # Either altitude or flight_level must be NULL, but not both.
  stopifnot(is.null(altitude) || is.null(flight_level))
  if (is.null(altitude)) {

    # Check that flight_level is an integer value, without requiring is.integer.
    if (!is.integer(flight_level)) {
      stopifnot(is.numeric(flight_level), flight_level %% 1 == 0)
      flight_level <- as.integer(flight_level)
    }
    stopifnot(is.integer(flight_level), length(flight_level) == 1,
              flight_level >= 60)

    # Flight level unit corresponds to hundreds of feet.
    altitude <- flight_level * 100
  }
  if (is.null(flight_level)) {
    stopifnot(is.double(altitude), length(altitude) == 1,
              altitude >= 0, altitude <= 6000)
  }

  body <- list(
    "acid" = aircraft_id,
    "type" = type,
    "lat" = latitude,
    "lon" = longitude,
    "hdg" = heading,
    "alt" = altitude,
    "spd" = speed
  )

  # TODO: hard-coded endpoint.
  response <- httr::POST(url = construct_endpoint_url(endpoint = "cre"),
                         body = body, encode = "json")

  if (httr::status_code(response) == 200)
    return(TRUE)

  FALSE
}
