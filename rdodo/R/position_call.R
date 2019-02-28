#' Make a call to the aircraft position endpoint
#'
#' @param aircraft_id
#' A scalar string aircraft identifier, or the special string \code{all}.
#'
#' @return
#' A list of aircraft position information, or an empty list if the given
#' \code{aircraft_id} did not match any aircraft in the simulation (this includes
#' the case that \code{aircraft_id} was the special string \code{all} but there
#' were no existing aircraft).
#'
#' @examples
#' \dontrun{
#' position_call('ABC123')
#' }
#'
#' @import httr
#' @importFrom jsonlite fromJSON
#' @export
position_call <- function(aircraft_id) {

  validate_aircraft_id(aircraft_id)

  endpoint <- config_param("endpoint_aircraft_position")
  query <- list(aircraft_id)
  names(query) <- config_param("query_aircraft_id")
  response <- tryCatch({
    httr::GET(url = construct_endpoint_url(endpoint, query = query))
  },
  error=function(cond) {
    stop(paste(conditionMessage(cond)))
  })

  # Status code 404 indicates that the aircraft_id was not matched to an
  # aircraft in the simulation. In that case return an empty list.
  if (httr::status_code(response) == config_param("status_code_aircraft_id_not_found"))
    return(list())

  validate_response(response)
  jsonlite::fromJSON(httr::content(response, "text"), simplifyVector = FALSE)
}

# Process the parsed position JSON for a single aircraft and return a data
# frame containing a single row, named by the aircraft ID.
process_parsed_position <- function(parsed, aircraft_id) {

  stopifnot(is.list(parsed))
  validate_aircraft_id(aircraft_id)

  # TODO: replace string literals with config parameters from Bluebird.
  expected_names <- c("alt", "gs", "lat", "lon", "vs")
  new_names <- c(config_param("altitude"),
                 config_param("ground_speed"),
                 config_param("latitude"),
                 config_param("longitude"),
                 config_param("vertical_speed"))

  # Handle the case that the aircraft_id was not found.
  if (length(parsed) == 0) {
    parsed <- as.list(rep(NA, times = length(expected_names)))
    names(parsed) <- expected_names
  }

  stopifnot(all(expected_names %in% names(parsed)))

  # Rename the elements.
  parsed <- parsed[expected_names]
  names(parsed) <- new_names

  # Convert to a data frame.
  ret <- as.data.frame(parsed[new_names])
  rownames(ret) <- aircraft_id

  ret %>% normalise_positions_units
}

# Process the list of parsed position JSONs (for multiple aircraft) and return a
# data frame containing a row for each of them, named by the aircraft ID.
process_parsed_positions <- function(parsed_list) {

  # Handle the case that parsed_list is empty (*not* a list of empty lists),
  # indicating the call came from the all_positions function (and no aircraft
  # were found). In this case return an empty dataframe.
  if (length(parsed_list) == 0) {
    ret <- process_parsed_position(list(), aircraft_id = "DUMMY")
    return(ret[-1, ])
  }

  # Process each position list and bind the rows of the resulting data frames.
  Reduce(f = rbind,
         x = purrr::map2(parsed_list, names(parsed_list), .f = process_parsed_position))
}

# Normalise units of measurement in the positions data.
normalise_positions_units <- function(df) {

  SCALE_METRES_TO_FEET <- 3.280839895

  # Bluesky returns altitude in metres, not feet.
  if (config_param("simulator") == config_param("bluesky_simulator"))
    df[, config_param("altitude")] <-
      SCALE_METRES_TO_FEET * df[, config_param("altitude")]

  df
}
