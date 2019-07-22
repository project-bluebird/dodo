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

  # Construct a matrix to contain the results.
  m <- matrix(NA, nrow = length(from_aircraft_id), ncol = length(to_aircraft_id),
              dimnames = list(from_aircraft_id, to_aircraft_id))

  # Fill the matrix.
  sink <- sapply(from_aircraft_id, FUN = function(i) {
    sapply(to_aircraft_id, FUN = function(j) {
      m[i, j] <<- vertical_distance(from_alt = pos[i, alt], to_alt = pos[j, alt])
    })
  })

  as.data.frame(m)
}
