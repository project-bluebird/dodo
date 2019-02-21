#' Check communication with BlueBird
#'
#' @return A boolean, \code{TRUE} indicates a valid response was received from
#' the BlueBird API.
#'
#' @examples
#' \dontrun{
#' found_bluebird()
#' }
#'
#' @export
found_bluebird <- function() {

  tryCatch({
      # TODO:
      # Temporary use of the reset command to check communication
      # (to be replaced with a "ping" endpoint when available).
      reset_simulation()
    },
    error=function(cond) {
      message(paste(cond))
      return(FALSE)
    }
  )
}
