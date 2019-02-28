#' Get the URL of the bluebird API
#'
#' @return A string.
#'
#' @examples
#' bluebird_url()
#'
#' @import httr
#' @export
bluebird_url <- function() {

  httr::modify_url(url = "",
                   scheme = "http",
                   hostname = config_param("host"),
                   port = config_param("port"))
}
