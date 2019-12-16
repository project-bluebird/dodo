#' Vertical separation
#'
#' Compute the vertical separation in metres between the positions of pairs of
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
#' \code{to_aircraft_id} as column names, containing the vertical distance in
#' metres between the positions of the corresponding pair of aircraft.
#'
#' @export
vertical_separation <- function(from_aircraft_id,
                                to_aircraft_id = from_aircraft_id) {

  # Get aircraft positions.
  pos <- aircraft_position(unique(c(from_aircraft_id, to_aircraft_id)))
  alt <- config_param("altitude")

  # Extract the vectors of "from" and "to" altitudes.
  from_alt <- pos[from_aircraft_id, alt]
  to_alt <- pos[to_aircraft_id, alt]

  ret <- as.data.frame(vertical_distance(from_alt, to_alt))
  rownames(ret) <- from_aircraft_id
  colnames(ret) <- to_aircraft_id

  ret
}
