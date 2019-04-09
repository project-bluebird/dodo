#' Make a POST request to the Bluebird API
#'
#' @param endpoint
#' The Bluebird API endpoing to call.
#' @param body
#' A named list.
#'
#' @return
#' \code{TRUE} if successful. Otherwise \code{FALSE} and an error is thrown.
#'
#' @examples
#' \dontrun{
#' body <- list("acid" = "ABC100", "type" = "B744", "lat" = 0, "lon" = 0, "hdg" = 0, "alt" = 20000, "spd" = 240)
#' endpoint <- config_param("endpoint_create_aircraft")
#' post_call(endpoint = endpoint, body = body)
#' }
#'
#' @import httr
#' @export
post_call <- function(endpoint, body = NULL) {

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
