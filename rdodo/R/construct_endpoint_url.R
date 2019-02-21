#' Construct a Bluebird API endpoint URL
#'
#' @param endpoint A string
#'
#' @return A string.
#'
#' @examples
#' construct_endpoint_url(endpoint = "ic")
#'
#' @export
construct_endpoint_url <- function(endpoint) {

  # TODO: hard-coded API version number.
  paste0(get_bluebird_url(), "/api/v1/", endpoint)
}
