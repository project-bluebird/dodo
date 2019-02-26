#' Send a "change vertical speed" command
#'
#' Request an aircraft to change vertical speed.
#'
#' @param aircraft_id
#' A string aircraft identifier
#' @param vertical_speed
#' A non-negative double. The aircraft's new vertical speed in feet/min.
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

  stopifnot(is.character(aircraft_id), length(aircraft_id) == 1)

  # TODO: move to validate_vertical_speed function.
  stopifnot(is.double(vertical_speed), length(vertical_speed) == 1,
            vertical_speed >= 0)

  body <- list(
    "acid" = aircraft_id,
    "vspd" = vertical_speed
  )
  post_call(endpoint = config::get("endpoint_change_vertical_speed"), body = body)
}
