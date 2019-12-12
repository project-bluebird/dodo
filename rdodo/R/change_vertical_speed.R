#' Send a "change vertical speed" command
#'
#' Request an aircraft to change vertical speed.
#'
#' @param aircraft_id
#' A string aircraft identifier
#' @param vertical_speed
#' The aircraft's new vertical speed in feet/min expressed as a non-negative
#' double or a quantity whose units can be converted to feet/min.
#'
#' @return
#' \code{TRUE} if successful. Otherwise \code{FALSE} and an error is thrown.
#'
#' @examples
#' \dontrun{
#' change_vertical_speed("test1234", vertical_speed = 10)
#' }
#' @import config httr
#' @export
change_vertical_speed <- function(aircraft_id, vertical_speed) {

  validate_aircraft_id(aircraft_id)
  validate_speed(vertical_speed)

  # Convert the given speed to feet/min
  units(vertical_speed) <- with(units::ud_units, ft/min)

  # TODO: replace string literals with config parameters from Bluebird.
  body <- list(
    "acid" = aircraft_id,
    "vspd" = as.double(vertical_speed)
  )
  post_call(endpoint = config_param("endpoint_change_vertical_speed"), body = body)
}
