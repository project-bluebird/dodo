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
  tryCatch({
    !httr::http_error(simulation_time_url())
  },
  error=function(cond) {
    message(paste(cond))
    return(FALSE)
  })
}
