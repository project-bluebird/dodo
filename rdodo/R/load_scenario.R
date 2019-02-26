#' Load a scenario
#'
#' @return
#' \code{TRUE} if successful. Otherwise \code{FALSE} and an error is thrown.
#'
#' @param filename
#' A string indicating the relative path to a scenario file.
#'
#' @examples
#' \dontrun{
#' load_scenario("scenario/8.SCN")
#' }
#'
#' @import httr config
#' @export
load_scenario <- function(filename) {

  stopifnot(is.character(filename), length(filename) == 1)

  body <- list("filename" = filename)
  post_call(endpoint = config::get("endpoint_load_scenario"), body = body)
}
