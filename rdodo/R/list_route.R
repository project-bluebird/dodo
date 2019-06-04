#' List an aircraft's route information
#'
#' Get the route information of an aircraft as a data frame whose row names are
#' waypoint names.
#'
#' @param aircraft_id
#' An aircraft ID.
#'
#' @return
#' A list of aircraft route information as a data frame with one row per waypoint
#' on the route. The row names are waypoint names. If the specified aircraft has
#' no route, an empty data frame is returned. If the given aircraft ID does
#' not exist in the simulation, an exception is thrown.
#'
#' @examples
#' \dontrun{
#' list_route('ABC123')
#' }
#'
#' @import purrr
#'
#' @export
list_route <- function(aircraft_id) {

  parsed_list <- route_call(aircraft_id)
  ret <- process_parsed_route(parsed_list)
  attr(ret, which = 'aircraft_id') <- aircraft_id
  ret
}
