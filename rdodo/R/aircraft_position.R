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
#' aircraft_position(c('ABC123', 'DEF456'))
#' aircraft_position()
#' }
#'
#' @import purrr
#'
#' @export
aircraft_position <- function(aircraft_id = NULL) {

  # Keep track of the requested (uppercase) aircraft ID(s).
  aircraft_ids <- toupper(aircraft_id)

  # If aircraft_id is a vector, get all aircraft positions and filter.
  if (length(aircraft_id) > 1)
    aircraft_id <- NULL

  parsed_list <- position_call(aircraft_id)
  ret <- process_parsed_positions(parsed_list)

  # If no particular aircraft_ids were specified, return all aircraft positions.
  if (length(aircraft_ids) == 0)
    return(ret)

  # Add a row of NAs for any missing aircraft_ids.
  missing_ids <- setdiff(aircraft_ids, rownames(ret))
  if (length(missing_ids) != 0)
    sink <- purrr::map(missing_ids, .f = function(id) {
      ret[id, ] <<- NA
    })

  # Filter the data frame to include only the requested aircraft IDs.
  ret[aircraft_ids, ]
}
