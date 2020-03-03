#' Validate a response from the Bluebird API
#'
#' Generates an error in case the response is invalid.
#'
#' @param response An \code{httr} response object.
#'
#' @examples
#' \dontrun{
#' response <- httr::POST(construct_endpoint_url(config_param("endpoint_reset_simulation")))
#' validate_response(response)
#' }
#'
#' @import httr
#' @export
#'
validate_response <- function(response) {
  if (httr::http_error(response)) {
    stop(
      sprintf(
        "Bluebird API request failed [%s]\nurl: %s\nmsg: %s",
        httr::status_code(response),
        response$url,
        httr::content(response)
      )
    )
  }

  if (length(httr::content(response)) != 0) {
    if (httr::http_type(response) != "application/json")
      stop("Bluebird API did not return json")
  }
}
