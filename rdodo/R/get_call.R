#' Make a GET request to the Bluebird API
#'
#' @param endpoint
#' The Bluebird API endpoing to call.
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
get_call <- function(endpoint, query = NULL) {

  response <- tryCatch({
    httr::GET(url = construct_endpoint_url(endpoint = endpoint, query = query))
  },
  error=function(cond) {
    stop(paste(conditionMessage(cond)))
  })

  validate_response(response)
  response
}
