#' Construct a Bluebird API endpoint URL
#'
#' @param endpoint
#' A string specifying the API endpoint.
#' @param query
#' A list of HTTP query parameters.
#'
#' @return A string.
#'
#' @examples
#' construct_endpoint_url(endpoint = "ic")
#'
#' @import httr
#' @export
construct_endpoint_url <- function(endpoint, query = NULL) {

  path <- paste(config::get("api_path"), config::get("api_version"), endpoint,
                sep = "/")

  httr::modify_url(bluebird_url(), path = path, query = query)
}
