#' Separation
#'
#' Compute the separation between the positions of pairs of aircraft under a
#' given distance measure.
#'
#' @param from_aircraft_id
#' A string vector of aircraft IDs.
#' @param to_aircraft_id
#' (Optional) A string vector of aircraft IDs. Defaults to
#' \code{from_aircraft_id}.
#' @param f_distance
#' A distance function such as\link{geodesic_distance} or
#' \link{great_circle_distance}.
#'
#' @return
#' A dataframe, with \code{from_aircraft_id} as row names and
#' \code{to_aircraft_id} as column names, containing the separation between the
#' positions of the corresponding pair of aircraft.
#'
#' @export
separation <- function(from_aircraft_id, to_aircraft_id = from_aircraft_id,
                       f_distance) {

  # Get aircraft positions.
  pos <- aircraft_position(unique(c(from_aircraft_id, to_aircraft_id)))
  lat <- config_param("latitude"); lon <- config_param("longitude")

  # Construct a matrix to contain the results.
  m <- matrix(NA, nrow = length(from_aircraft_id), ncol = length(to_aircraft_id),
              dimnames = list(from_aircraft_id, to_aircraft_id))

  # Fill the matrix.
  sink <- sapply(from_aircraft_id, FUN = function(i) {
    sapply(to_aircraft_id, FUN = function(j) {
      m[i, j] <<- f_distance(from_lat = pos[i, lat], from_lon = pos[i, lon],
                             to_lat = pos[j, lat], to_lon = pos[j, lon])
    })
  })

  as.data.frame(m)
}
