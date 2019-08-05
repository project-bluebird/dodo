#' Submit a batch of calls to the Bluebird API asynchronously.
#'
#' This function mitigates the problem of unresponsiveness when submitting
#' multiple API calls in quick succession. By wrapping the calls in the
#' \code{batch} function they are dispatched asynchronous to minimise blocking.
#'
#' @param ...
#' One or more API function calls.
#' @param async
#' A boolean flag. Defaults to \code{TRUE}, in which case the calls are
#' dispatched asynchronously.
#'
#' @return
#' A list of return values, one for each of the given function calls, if all are
#' successful. Otherwise an error is thrown containing the conconcated error
#' messages from all of the failed function calls, separated by a semicolon.
#'
#' @examples
#' \dontrun{
#' reset_simulation()
#' create_aircraft("ABC",type="B741",latitude=0,longitude=0,heading=0,flight_level=200,speed=250)
#' create_aircraft("XYZ",type="B744",latitude=0,longitude=0,heading=0,flight_level=300,speed=350)
#' batch(
#'   change_heading("ABC", heading = 350),
#'   change_altitude("ABC", flight_level = 450),
#'   change_heading("XYZ", heading = 10),
#'   change_altitude("XYZ", flight_level = 250)
#' )
#' }
#'
#' @import purrr future
#' @export
batch <- function(..., async = TRUE) {

  # Capture all of the unevaluated expressions in the ellipsis argument (...).
  calls <- eval(substitute(alist(...)))

  # Get the calling environment (i.e. the environment from which this function
  # was called). This will be needed to evaluate the expressions.
  calling_env <- parent.frame()

  # If async is false just evaluate all of the function calls *in the calling
  # environment*.
  if (!async) {
    return(purrr::map(calls, .f = function(x) {
      eval(as.expression(x), envir = calling_env)
    }))
  }

  # Evaluate the calls asynchronously, *in the calling environment*, obtaining a
  # promise for each of them.
  future::plan(future::multiprocess)
  promises <- purrr::map(calls, .f = function(x) {
    future::future(eval(as.expression(x), envir = calling_env))
  })

  # Wait until all promises are resolved.
  while(!all(is_resolved <- purrr::map_lgl(promises, .f = future::resolved)))
    message(paste("Waiting for", sum(is_resolved), "of", length(promises), "promises..."))

  # Get the values of the promises, or their error messages.
  ret <- purrr::map(promises, .f = function(p) {
    tryCatch({
      future::value(p)
    },
    error=function(cond) {
      paste(conditionMessage(cond))
    })
  })

  # If any of the calls failed, throw an error containing the concatenated error
  # messages, separated by a semicolon.
  if (any(purrr::map_lgl(ret, .f = is.character)))
    stop(paste(unlist(purrr::keep(ret, .p = is.character)), collapse = ";"))

  ret
}
