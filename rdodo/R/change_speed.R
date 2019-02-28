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

  stopifnot(is.character(aircraft_id), length(aircraft_id) == 1)

  # TODO: move to validate_speed function.
  stopifnot(is.double(speed), length(speed) == 1, speed >= 0)

  body <- list(
    "acid" = aircraft_id,
    "spd" = speed
  )
  post_call(endpoint = config_param("endpoint_change_speed"), body = body)
}
