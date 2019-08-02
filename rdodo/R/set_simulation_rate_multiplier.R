#' Set the simulation rate multiplier.
#'
#' Sets the simulation rate multiplier for the current simulation. By default
#' this multiplier is equal to one (real-time operation). If set to another
#' value, the simulation will run faster (or slower) than real-time, with a
#' fixed multiplier as provided. For example, a multiplier of 2 would cause the
#' simulation to run twice as fast: 60 simulation minutes take 30 actual minutes.
#'
#' @param multiplier
#' A position double
#'
#' @return
#' \code{TRUE} if successful. Otherwise \code{FALSE} and an error is thrown.
#'
#' @examples
#' \dontrun{
#' set_simulation_rate_multiplier(2)
#' set_simulation_rate_multiplier(0.5)
#' }
#' @export
set_simulation_rate_multiplier <- function(multiplier) {

  stopifnot(is.double(multiplier), length(multiplier) == 1, multiplier > 0)

  # TODO: replace string literal with config parameter from Bluebird.
  body <- list("multiplier" = multiplier)

  post_call(endpoint = config_param("endpoint_set_simulation_rate_multiplier"),
            body = body)
}
