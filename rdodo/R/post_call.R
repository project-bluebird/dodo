#' Make a POST request to the Bluebird API
#'
#' @param endpoint
#' The Bluebird API endpoing to call.
#' @param body
#' A named list.
#'
#' @return
#' \code{TRUE} if successful. Otherwise \code{FALSE} and an error is thrown.
#'
#' @import httr
#'
post_call <- function(endpoint, body = NULL) {

  response <- tryCatch({
    httr::POST(url = construct_endpoint_url(endpoint = endpoint), body = body,
               encode = "json")
  },
  error=function(cond) {
    stop(paste(conditionMessage(cond)))
  })

  validate_response(response)
  TRUE
}
