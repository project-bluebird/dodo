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

  parsed <- position_call(aircraft_id = "all")

  if (length(parsed) == 0)
    return(process_parsed_position(parsed))

  process_parsed_positions(parsed)
}
