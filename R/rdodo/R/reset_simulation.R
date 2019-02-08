#' Reset the simulation
#'
#' @return A boolean, \code{TRUE} indicates success.
#'
#' @examples
#' \dontrun{
#' reset_simulation()
#' }
#'
#' @export
reset_simulation <- function() {

  # TODO: hard-coded endpoint.
  response <- httr::POST(url = construct_endpoint_url(endpoint = "ic"))

  # TODO: Temporary:
  if (httr::status_code(response) == 418)
    return(TRUE)

  # 202 status code: Accepted for processing.
  if (httr::status_code(response) == 202)
    return(TRUE)

  FALSE
}
