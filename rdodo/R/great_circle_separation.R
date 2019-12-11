#' Great circle separation
#'
#' Compute the great circle separation in metres between the positions of pairs of
#' aircraft.
#'
#' @param from_aircraft_id
#' A string vector of aircraft IDs.
#' @param to_aircraft_id
#' (Optional) A string vector of aircraft IDs. Defaults to
#' \code{from_aircraft_id}.
#'
#' @return
#' A dataframe, with \code{from_aircraft_id} as row names and
#' \code{to_aircraft_id} as column names, containing the great circle distance in
#' metres between the positions of the corresponding pair of aircraft.
#'
#' @export
great_circle_separation <- function(from_aircraft_id,
                                to_aircraft_id = from_aircraft_id) {

  separation(from_aircraft_id = from_aircraft_id,
             to_aircraft_id = to_aircraft_id,
             f_distance = great_circle_distance)
}
