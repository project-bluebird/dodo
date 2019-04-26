#' Resume the simulation after a pause
#'
#' @return
#' \code{TRUE} if successful. Otherwise \code{FALSE} and an error is thrown.
#'
#' @examples
#' \dontrun{
#' resume_simulation()
#' }
#'
#' @export
resume_simulation <- function() {

  post_call(endpoint = config_param("endpoint_resume_simulation"))
}
