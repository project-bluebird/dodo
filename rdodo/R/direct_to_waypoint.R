#' Send a "go directly to a waypoint" command
#'
#' Request aircraft to change heading toward a given waypoint. The waypoint must
#' exist on the aircraft route.
#'
#' @param aircraft_id
#' A string aircraft identifier.
#' @param waypoint_name
#' The name of the waypoint.
#'
#' @return
#' \code{TRUE} if successful. Otherwise \code{FALSE} and an error is thrown.
#'
#' @examples
#' \dontrun{
#' direct_to_waypoint("TST1000", waypoint_name = "TESTWPT")
#' }
#' @export
direct_to_waypoint <- function(aircraft_id, waypoint_name) {

  validate_aircraft_id(aircraft_id)
  stopifnot(is.character(waypoint_name), length(waypoint_name) == 1)

  # TODO: replace string literals with config parameters from Bluebird.
  body <- list(
    "acid" = aircraft_id,
    "waypoint" = waypoint_name
  )

  post_call(endpoint = config_param("endpoint_direct_to_waypoint"), body = body)
}
