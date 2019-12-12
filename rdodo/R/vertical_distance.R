#' Vertical distance
#'
#' Compute the vertical distance in metres between two altitudes. This is a
#' trivial helper function for \code{\link{vertical_separation}}.
#'
#' @param from_alt
#' A non-negative double, interpreted as an altitude in feet, or a double value
#' with a distance unit.
#' @param to_alt
#' A non-negative double, interpreted as an altitude in feet, or a double value
#' with a distance unit.
#'
#' @return
#' A double with units, the vertical distance between the two altitudes in metres.
#'
#' @import units
#' @export
vertical_distance <- function(from_alt, to_alt) {

  stopifnot(as.double(from_alt) >= 0)
  stopifnot(as.double(to_alt) >= 0)

  # If the from_alt is unitless, add "ft" units.
  if (!inherits(from_alt, "units"))
    units(from_alt) <- with(units::ud_units, ft)

  # If the to_alt is unitless, add "ft" units.
  if (!inherits(to_alt, "units"))
    units(to_alt) <- with(units::ud_units, ft)

  # Convert to_alt to metres.
  units(to_alt) <- with(units::ud_units, m)

  # Return the result (automatically in metres, because to_alt is).
  to_alt - from_alt
}
