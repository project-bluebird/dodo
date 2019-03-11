#' Pause the simulation
#'
#' @return
#' \code{TRUE} if successful. Otherwise \code{FALSE} and an error is thrown.
#'
#' @examples
#' \dontrun{
#' pause_simulation()
#' }
#'
#' @export
pause_simulation <- function() {

  post_call(endpoint = config_param("endpoint_pause_simulation"))
}
