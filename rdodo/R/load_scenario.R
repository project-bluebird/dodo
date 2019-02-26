#' Load a scenario
#'
#' @return
#' \code{TRUE} if successful. Otherwise \code{FALSE} and an error is thrown.
#'
#' @params filename
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

  endpoint <- config::get("endpoint_load_scenario")
  body <- list("filename" = filename)

  response <- tryCatch({
    httr::POST(url = construct_endpoint_url(endpoint = endpoint), body = body,
               encode = "json")
  },
  error=function(cond) {
    stop(paste(conditionMessage(cond)))
  })

  validate_response(response)
  TRUE
}
