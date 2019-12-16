#' Vertical distance
#'
#' Compute the vertical distance in metres between two altitudes. This is a
#' trivial helper function for \code{\link{vertical_separation}}.
#'
#' @param from_alt
#' A vector of non-negative doubles, interpreted as an altitude in feet, or a
#' vector of double values with a distance unit.
#' @param to_alt
#' A vector of non-negative doubles, interpreted as an altitude in feet, or a
#' vector of double values with a distance unit.
#'
#' @return
#' A matrix of doubles, with units, with one row for each element in
#' \code{from_alt} and one column for each element in \code{to_alt}. The
#' \code{(i,j)}th entry is the vertical distance \code{to_alt[j] - from_alt[i]},
#' in metres.
#'
#' @import units
#' @export
vertical_distance <- function(from_alt, to_alt) {

  stopifnot(all(as.double(from_alt) >= 0))
  stopifnot(all(as.double(to_alt) >= 0))

  # If the from_alt is unitless, add "ft" units.
  if (!inherits(from_alt, "units"))
    units(from_alt) <- with(units::ud_units, ft)

  # If the to_alt is unitless, add "ft" units.
  if (!inherits(to_alt, "units"))
    units(to_alt) <- with(units::ud_units, ft)

  # Convert to_alt to metres.
  units(to_alt) <- with(units::ud_units, m)

  # Return the result (automatically in metres, because to_alt is).
  t(outer(to_alt, from_alt, FUN = "-"))
}
