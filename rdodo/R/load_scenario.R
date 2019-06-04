#' Load a scenario
#'
#' @return
#' \code{TRUE} if successful. Otherwise \code{FALSE} and an error is thrown.
#'
#' @param filename
#' The relative path to a scenario file.
#' @param multiplier
#' (Optional) A positive number specifying the simulation rate multiplier. If
#' omitted, the rate multiplier will be 1.
#'
#' @examples
#' \dontrun{
#' load_scenario("scenario/8.SCN")
#' }
#'
#' @export
load_scenario <- function(filename, multiplier = NULL) {

  stopifnot(is.character(filename), length(filename) == 1)

  # TODO: replace string literals with config parameters from Bluebird.
  body <- list("filename" = filename)
  if (!is.null(multiplier)) {
    stopifnot(is.numeric(multiplier), multiplier > 0)
    body <- c(body, list("multiplier" = multiplier))
  }
  post_call(endpoint = config_param("endpoint_load_scenario"), body = body)
}
