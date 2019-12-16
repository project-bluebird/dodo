#' Make a call to the aircraft position endpoint
#'
#' @param aircraft_id
#' A scalar aircraft identifier (string), or NULL (the default).
#'
#' @return
#' A list of lists, each element named by a \code{aircraft_id} and each sublist
#' containing aircraft position information, plus an element for the
#' \code{simulator_time}. If the \code{aircraft_id} was not found in the
#' simulation, the sublist will be empty. Returns an empty list if
#' \code{aircraft_id} was NULL but there were no existing aircraft.
#'
#' @examples
#' \dontrun{
#' position_call('ABC123')
#' position_call()
#' }
#'
#' @import httr
#' @importFrom jsonlite fromJSON
#' @export
position_call <- function(aircraft_id = NULL) {

  if (is.null(aircraft_id))
    aircraft_id <- "all" # TODO: replace hardcoded string literal.

  validate_aircraft_id(aircraft_id)

  # Construct the API call URL
  endpoint <- config_param("endpoint_aircraft_position")
  query <- list(aircraft_id)
  names(query) <- config_param("query_aircraft_id")

  response <- get_call(endpoint = endpoint, query = query, validate = FALSE)

  # Status code 404 indicates that the aircraft_id was not matched to an
  # aircraft in the simulation. In that case return a list containing an empty
  # list.
  if (httr::status_code(response) == config_param("status_code_aircraft_id_not_found")) {
    ret <- list(list()); names(ret) <- aircraft_id
    return(ret)
  }

  # Status code 400 indicates that all positions were requested but there were
  # no aircraft in the simulation, or that an invalid aircraft_id was sent.
  # In that case return an empty list.
  if (httr::status_code(response) == config_param("status_code_no_aircraft_found"))
    return(list())

  validate_response(response)
  jsonlite::fromJSON(httr::content(response, as = "text", encoding = "UTF-8"),
                     simplifyVector = FALSE)
}
