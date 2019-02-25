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

  endpoint <- config::get("endpoint_reset_simulation")
  response <- tryCatch({
    httr::POST(url = construct_endpoint_url(endpoint = endpoint))
  },
  error=function(cond) {
    stop(paste(conditionMessage(cond)))
  })

  validate_response(response)
  TRUE
}
