#' Get the URL of the bluebird API
#'
#' @return A string.
#'
#' @examples
#' get_bluebird_url()
#'
#' @import config
#' @export
get_bluebird_url <- function() {

  paste(config::get("host"), config::get("port"), sep = ":")
}
