#' Reset the simulation
#'
#' @return \code{TRUE} if successful. Otherwise \code{FALSE} and an error is thrown.
#'
#' @examples
#' \dontrun{
#' reset_simulation()
#' }
#'
#' @import httr config
#' @export
reset_simulation <- function() {

  post_call(endpoint = config::get("endpoint_reset_simulation"))
}
