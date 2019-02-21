#' Reset the simulation
#'
#' @return A boolean, \code{TRUE} indicates success.
#'
#' @examples
#' \dontrun{
#' reset_simulation()
#' }
#'
#' @import httr
#' @export
reset_simulation <- function() {

  # TODO: hard-coded endpoint.
  response <- httr::POST(url = construct_endpoint_url(endpoint = "reset"))

  if (httr::status_code(response) == 200)
    return(TRUE)

  stop(paste("Response status unsuccessful:", httr::status_code(response)))
}
