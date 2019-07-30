#' Get the current simulation time
#'
#' @return
#' A \code{POSIXct} date-time object, if successful. Otherwise an error is thrown.
#'
#' @examples
#' \dontrun{
#' simulation_time()
#' }
#'
#' @import httr
#' @importFrom jsonlite fromJSON
#' @export
simulation_time <- function() {

  endpoint <- config_param("endpoint_simulation_time")
  response <- get_call(endpoint)

  l <- jsonlite::fromJSON(httr::content(response, "text"), simplifyVector = FALSE)

  stopifnot(is.list(l), length(l) == 1)

  # Identify the timezone.
  name <- "sim_utc"
  stopifnot(identical(names(l), name))
  tz <- toupper(substring(name, first = nchar(name) - 2, last = nchar(name)))

  as.POSIXct(l[[name]], tz = tz)
}
