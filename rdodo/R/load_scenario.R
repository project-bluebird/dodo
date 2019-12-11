#' Load a scenario
#'
#' @param scenario
#' The name of the scenario, which must exist on the simulator host.
#' @param multiplier
#' (Optional) A positive number specifying the simulation rate multiplier. If
#' omitted, the rate multiplier will be 1.
#' @return
#' \code{TRUE} if successful. Otherwise \code{FALSE} and an error is thrown.
#'
#' @examples
#' \dontrun{
#' load_scenario("test-scenario")
#' }
#'
#' @export
load_scenario <- function(scenario, multiplier = NULL) {

  stopifnot(is.character(scenario), length(scenario) == 1)

  # TODO: replace string literals with config parameters from Bluebird.
  body <- list("filename" = scenario)
  if (!is.null(multiplier)) {
    stopifnot(is.numeric(multiplier), multiplier > 0)
    body <- c(body, list("multiplier" = multiplier))
  }
  post_call(endpoint = config_param("endpoint_load_scenario"), body = body)
}
