#' Send a "change speed" command
#'
#' Request an aircraft to change speed.
#'
#' @param aircraft_id
#' A string aircraft identifier
#' @param speed
#' A non-negative double. The aircraft's new speed in knots.
#'
#' @return
#' \code{TRUE} if successful. Otherwise \code{FALSE} and an error is thrown.
#'
#' @examples
#' \dontrun{
#' change_speed("test1234", speed = 90)
#' }
#' @import httr
#' @export
change_speed <- function(aircraft_id, speed) {

  validate_aircraft_id(aircraft_id)
  validate_speed(speed)

  # TODO: replace string literals with config parameters from Bluebird.
  body <- list(
    "acid" = aircraft_id,
    "spd" = speed
  )
  post_call(endpoint = config_param("endpoint_change_speed"), body = body)
}
