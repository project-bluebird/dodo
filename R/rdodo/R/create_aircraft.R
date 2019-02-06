#' Create an aircraft
#'
#' Either the \code{altitude} or \code{flight_level} argument must be given,
#' but not both.
#'
#' @param aircraft_id
#' A string aircraft identifier
#' @param type
#' A string ICAO aircraft type designator
#' @param lat
#' A double in the range [-180, 180). The aircraft's latitude.
#' @param lon
#' A double in the range [-90, 90]. The aircraft's longitude.
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
#' create_aircraft("test1234", "B744", 0, 0, 0, flight_level = 250, speed = 200)
#'
#' @export
create_aircraft <- function(aircraft_id,
                            type,
                            lat,
                            lon,
                            heading,
                            altitude = NULL,
                            flight_level = NULL,
                            speed) {

  FALSE
}
