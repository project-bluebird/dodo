#' Make a call to the aircraft position endpoint
#'
#' @param aircraft_id
#' A scalar aircraft identifier (string), or NULL (the default).
#'
#' @return
#' A list of lists, each element named by a \code{aircraft_id} and each sublist
#' containing aircraft position information. If the \code{aircraft_id} was not
#' found in the simulation, the sublist will be empty. Returns an empty list if
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
  url <- construct_endpoint_url(endpoint, query = query)

  response <- tryCatch({
    httr::GET(url)
  },
  error=function(cond) {
    stop(paste(conditionMessage(cond)))
  })

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
  jsonlite::fromJSON(httr::content(response, "text"), simplifyVector = FALSE)
}

# Process the list of parsed position JSONs (for multiple aircraft) and return a
# data frame containing a row for each of them, named by the aircraft ID.
process_parsed_positions <- function(parsed_list) {

  # Handle the case that parsed_list is empty, indicating the call came from the
  # all_positions function and no aircraft were found. In this case return an
  # empty dataframe.
  if (length(parsed_list) == 0)
    return(process_parsed_position(list(), aircraft_id = "DUMMY")[-1, ])

  # Pull out the simulator time attribute.
  sim_t <- parsed_list[[config_param("simulator_time")]]
  parsed_list[[config_param("simulator_time")]] <- NULL

  # Process each position sublist and bind the rows of the resulting data frames.
  dfs <- purrr::map2(parsed_list, names(parsed_list), .f = process_parsed_position)
  ret <- Reduce(f = rbind, x = dfs)

  # Add the simulator time attribute
  attr(ret, config_param("simulator_time")) <- sim_t
  ret
}

# Process the parsed position JSON for a single aircraft and return a data
# frame containing a single row, named by the aircraft ID. If `parsed` is
# empty, indicating the given aircraft_id was not found in the simulation,
# return a data frame containing a row of NA values for the given aircraft_id.
process_parsed_position <- function(parsed, aircraft_id) {

  stopifnot(is.list(parsed))
  validate_aircraft_id(aircraft_id)

  # TODO: replace string literals with config parameters from Bluebird.
  expected_names <- c("actype", "alt", "gs", "lat", "lon", "vs")
  new_names <- c(config_param("aircraft_type"),
                 config_param("altitude"),
                 config_param("ground_speed"),
                 config_param("latitude"),
                 config_param("longitude"),
                 config_param("vertical_speed"))

  # Handle the case that the parsed list is empty. In that case return a
  # data frame with a single row of NA values for the given aircraft_id.
  if (length(parsed) == 0) {
    parsed <- as.list(rep(NA, times = length(expected_names)))
    names(parsed) <- expected_names
  }

  stopifnot(all(expected_names %in% names(parsed)))

  # Rename the elements.
  parsed <- parsed[expected_names]
  names(parsed) <- new_names

  # Convert to a data frame.
  ret <- as.data.frame(parsed[new_names], stringsAsFactors = FALSE)
  rownames(ret) <- aircraft_id

  ret %>% normalise_positions_units
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
