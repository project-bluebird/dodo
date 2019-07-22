#' Vertical distance
#'
#' Compute the vertical distance in metres between two altitudes. This is a
#' trivial helper function for \code{\link{vertical_separation}}.
#'
#' @param from_alt
#' A non-negative double.
#' @param to_alt
#' A non-negative double.
#'
#' @return
#' A double, the vertical distance between the two altitudes.
#'
#' @export
vertical_distance <- function(from_alt, to_alt) {

  stopifnot(from_alt >= 0)
  stopifnot(to_alt >= 0)

  # Convert feet to metres.
  (to_alt - from_alt)/3.2808
}
