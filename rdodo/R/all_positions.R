#' Get all aircraft positions
#'
#' @return
#' A data frame of aircraft positions with one row per aircraft. The
#' row names are aircraft IDs.
#'
#' @examples
#' \dontrun{
#' all_positions()
#' }
#'
#' @import purrr
#'
#' @export
all_positions <- function() {

  process_parsed_positions(position_call(aircraft_id = "all"))
}
