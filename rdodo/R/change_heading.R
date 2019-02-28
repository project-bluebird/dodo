#' Send a "change heading" command
#'
#' Request an aircraft to change heading.
#'
#' @param aircraft_id
#' A string aircraft identifier
#' @param heading
#' A double in the range [0, 360). The aircraft's new heading in degrees.
#'
#' @return
#' \code{TRUE} if successful. Otherwise \code{FALSE} and an error is thrown.
#'
#' @examples
#' \dontrun{
#' change_heading("test1234", heading = 90)
#' }
#' @import httr
#' @export
change_heading <- function(aircraft_id, heading) {

  stopifnot(is.character(aircraft_id), length(aircraft_id) == 1)

  # TODO: move to validate_heading function.
  stopifnot(is.double(heading), length(heading) == 1,
            heading >= 0, heading < 360)

  body <- list(
    "acid" = aircraft_id,
    "hdg" = heading
  )
  post_call(endpoint = config_param("endpoint_change_heading"), body = body)
}
