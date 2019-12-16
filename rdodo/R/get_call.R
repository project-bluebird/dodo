#' Make a GET request to the Bluebird API
#'
#' @param endpoint
#' The Bluebird API endpoing to call.
#' @param query
#' A list of HTTP query parameters.
#' @param validate
#' A boolean flag. If \code{TRUE} (the default), the HTTP response will be
#' validated before being returned.
#'
#' @return
#' A \code{\link{response}} object, if successful. Otherwise an error is thrown.
#'
#' @examples
#' \dontrun{
#' endpoint <- config_param("endpoint_simulation_time")
#' get_call(endpoint = endpoint)
#' }
#'
#' @import httr
#' @export
get_call <- function(endpoint, query = NULL, validate = TRUE) {

  response <- tryCatch({
    httr::GET(url = construct_endpoint_url(endpoint = endpoint, query = query))
  },
  error=function(cond) {
    stop(paste(conditionMessage(cond)))
  })

  if (validate)
    validate_response(response)
  response
}
