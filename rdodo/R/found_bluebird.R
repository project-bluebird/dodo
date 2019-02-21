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

  tryCatch({
    !httr::http_error(get_bluebird_url())
  },
  error=function(cond) {
    message(paste(cond))
    return(FALSE)
  })
}
