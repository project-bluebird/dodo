#' Get all aircraft positions
#'
#' @return
#' A data frame of aircraft positions with one row per aircraft. The
#' row names are aircraft IDs. Returns an empty data frame if there are no
#' aircraft in the simulation.
#'
#' @examples
#' \dontrun{
#' all_positions()
#' }
#'
#' @export
all_positions <- function() {
  aircraft_position(aircraft_id = NULL)
}
