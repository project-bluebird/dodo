#' Get aircraft position
#'
#' Get the position of a single or multiple aircraft based on their IDs, or
#' positions of all aircraft in the simulation.
#'
#' @param aircraft_id
#' (Optional) Single aircraft ID, or a vector of aircraft IDs. If no ID is
#' supplied, returns positions of all aircraft in the simulation. Each aircraft
#' ID is a string.
#'
#' @return
#' A list of aircraft positions as a data frame with one row per aircraft. The
#' row names are aircraft IDs. If any of the given aircraft IDs does not exist
#' in the simulation, the returned dataframe contains a row of missing (NA)
#' values for that ID.
#'
#' @examples
#' \dontrun{
#' aircraft_position('ABC123')
#'
#' aircraft_position(c('ABC123', 'DEF456'))
#' }
#'
#' @import purrr
#'
#' @export
aircraft_position <- function(aircraft_id) {

  parsed_list <- purrr::map(aircraft_id, .f = position_call)
  names(parsed_list) <- toupper(aircraft_id)

  process_parsed_positions(parsed_list)
}
