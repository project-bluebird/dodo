#' Get the URL of the bluebird API
#'
#' @return A string.
#'
#' @examples
#' bluebird_url()
#'
#' @import config httr
#' @export
bluebird_url <- function() {

  httr::modify_url(url = "",
                   scheme = "http",
                   hostname = config::get("host"),
                   port = config::get("port"))
}
