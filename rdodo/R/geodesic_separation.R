#' Geodesic separation
#'
#' Compute the geodesic separation in metres between the positions of pairs of
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
#' \code{to_aircraft_id} as column names, containing the geodesic distance in
#' metres between the positions of the corresponding pair of aircraft.
#'
#' @import geosphere
#' @export
geodesic_separation <- function(from_aircraft_id,
                                to_aircraft_id = from_aircraft_id) {

  #TODO:
  # - Get aircraft positions
  # - Call geodesic_distance with mapply to obtain a matrix
  # - Add colnames/rownames
  # - Convert to data frame


  0
}
