#' Geodesic distance
#'
#' Compute the geodesic distance in metres between two latitude/longitude
#' positions.
#'
#' @param from_lat
#' A double in the range [-90, 90].
#' @param from_lon
#' A double in the range [-180, 180).
#' @param to_lat
#' A double in the range [-90, 90].
#' @param to_lon
#' A double in the range [-180, 180).
#'
#' @return
#' A double, the geodesic distance between the two points.
#'
#' @import geosphere
#' @export
geodesic_distance <- function(from_lat, from_lon, to_lat, to_lon) {

  validate_latitude(from_lat)
  validate_longitude(from_lon)
  validate_latitude(to_lat)
  validate_longitude(to_lon)

  # Note that coordinates in geosphere are given as longitude/latitude.
  geosphere::distGeo(p1 = c(from_lon, from_lat), p2 = c(to_lon, to_lat))
}
