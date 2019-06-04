#' Wait for a command to take effect
#'
#' @param aircraft_id
#' The aircraft ID.
#' @param property
#' The name of the aircraft property to which the change is expected. This must
#' be one of the column names in the data frame returned by the
#' \code{\link{aircraft_position}} function (e.g. altitude).
#' @param operator
#' A binary operator for testing whether the aircraft property has changed.
#' Defaults to \code{`!=`}, meaning that the function will return only when the
#' value of the given property is not equal to its initial (or the timeout is
#' reached). If an asymmetric operator is used (e.g. \code{`<`}), the initial
#' value appears on the right-hand side.
#' @param initial_value
#' (Optional) The initial value of the property. If omitted, the initial value
#' is obtained via a call to the \code{\link{aircraft_position}} function.
#' @param timeout
#' A timeout after which the function will return even if the expected change
#' has not been observed.
#'
#' @return
#' Returns \code{TRUE}, invisibly, unless the timeout was reached, in which case
#' \code{FALSE}.
#'
#' @export
wait <- function(aircraft_id, property, operator = `!=`, initial_value = NULL,
                 timeout = 10) {

  # Get the start time and initial aircraft position.
  t <- Sys.time()
  position <- aircraft_position(aircraft_id)

  stopifnot(property %in% colnames(position))

  # If necessary, set the initial value.
  if (is.null(initial_value))
    initial_value <- position[aircraft_id, property]

  # Wait until the property value has changed from the initial value.
  while(!operator(position[aircraft_id, property], initial_value)) {
    if (Sys.time() - t > timeout)
      return(FALSE)
    position <- aircraft_position(aircraft_id)
  }

  invisible(TRUE)
}
