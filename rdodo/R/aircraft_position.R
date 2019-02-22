#' Get aircraft position
#'
#' Get position of a single or multiple aircraft based on their IDs, or
#' positions of all aircraft in the simulation.
#'
#' @param aircraft_id (Optional) Single aircraft ID, or a vector of aircraft IDs.
#'                    If no ID is supplied, returns positions of all aircraft in the simulation.
#'                    Aircraft ID is a string with at least three characters.
#'
#' @return A list of aircraft positions as a named list. Position is NULL if aircraft not found.
#'
#' @examples
#' \dontrun{
#' aircraft_position()
#'
#' aircraft_position('ABC123')
#'
#' aircraft_position(c('ABC123', 'DEF456'))
#' }
#'
#' @import magrittr
#'
#' @export
aircraft_position <- function(aircraft_id = NULL) {

  if (is.null(aircraft_id)) {
    # Get position for all aircraft
    get_all()
  } else if (is.vector(aircraft_id)) {
    # Loop over aircraft and return their positions
    result <-
      aircraft_id %>%
      purrr::map(get_aircraft_request) %>%
      set_names(aircraft_id)
    return(result)
  } else {
    return(get_aircraft_request(aircraft_id))
  }
}

position_call <- function(query_body) {
  endpoint <- config::get("endpoint_aircraft_position")
  response <- httr::GET(url = construct_endpoint_url(endpoint = endpoint),
              query = list(arcid = query_body))

  if (httr::http_type(response) != "application/json") {
    warning("API did not return json")
    return(NULL)
  }

  parsed <- jsonlite::fromJSON(httr::content(response, "text"), simplifyVector = FALSE)

  if (httr::http_error(response)) {
    warning(
      sprintf(
        "Bluebird API request failed [%s]\n%s\n<%s>",
        httr::status_code(response),
        parsed$message
      ))
    return(NULL)
  }
  return(parsed)
}

process_response <- function(parsed) {

  # TODO: include time (timestamp?)

  list(
    "altitude" = parsed$alt,
    "ground_speed" = parsed$gs,
    "latitude" = parsed$lat,
    "longitude" = parsed$lon,
    "vertical_speed" = parsed$vs
  )
}

# Helper function - get position of a single aircraft
get_aircraft_request <- function(aircraft_id) {

  if (is.character(aircraft_id) && (nchar(aircraft_id) >= 3)) {
    body <- list("acid" = aircraft_id)
  } else {
    warning("Aircraft ID must be a string with at least three characters")
    return(NULL)
  }

  position_call(body) %>%
    process_response() %>%
    list() %>%
    set_names(aircraft_id) %>%
    return
}

get_all <- function() {
  body <- list("acid" = "ALL")
  parsed <- position_call(body)

  parsed %>%
    purrr::map(process_response) %>%
    set_names(names(parsed)) %>%
    return
}
