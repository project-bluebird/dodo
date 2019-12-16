#' Check communication with BlueBird
#'
#' @return A boolean, \code{TRUE} indicates that a request to the BlueBird URL
#' was successful.
#'
#' @examples
#' \dontrun{
#' found_bluebird()
#' }
#'
#' @import httr
#' @export
found_bluebird <- function() {

  # Use the simulation time endpoint to check for a response from Bluebird.
  endpoint <- config_param("endpoint_simulation_time")
  tryCatch({
    !httr::http_error(construct_endpoint_url(endpoint = endpoint))
  },
  error=function(cond) {
    message(paste(cond))
    return(FALSE)
  })
}
