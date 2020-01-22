#' Check communication with BlueBird
#'
#' @param verbose
#' A boolean flag. If \code{TRUE} then an error message is printed to the
#' console in case Bluebird is not found.
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
found_bluebird <- function(verbose = FALSE) {

  # Use the simulation info endpoint to check for a response from Bluebird.
  endpoint <- config_param("endpoint_simulation_info")
  tryCatch({
    !httr::http_error(construct_endpoint_url(endpoint = endpoint))
  },
  error=function(cond) {
    if (verbose)
      message(paste(cond))
    return(FALSE)
  })
}
