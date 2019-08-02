#' Make a call to the aircraft route endpoint
#'
#' @param aircraft_id
#' A scalar aircraft identifier (string).
#'
#' @return
#' A list with three elements: 1. the aircraft ID, 2. route information (a list
#' of lists) 3. the simulator  time. If the \code{aircraft_id} was not found in the
#' simulation, the 'route' element will contain a single \code{NA} value. If the
#' \code{aircraft_id} was found, but the aircraft has no route, the 'route'
#' element will be an empty list.
#'
#' @examples
#' \dontrun{
#' route_call('ABC123')
#' }
#'
#' @import httr purrr stringr
#' @importFrom jsonlite fromJSON
#' @export
route_call <- function(aircraft_id) {

  validate_aircraft_id(aircraft_id)

  # Construct the API call URL
  endpoint <- config_param("endpoint_list_route")
  query <- list(aircraft_id)
  names(query) <- config_param("query_aircraft_id")
  url <- construct_endpoint_url(endpoint, query = query)

  response <- tryCatch({
    httr::GET(url)
  },
  error=function(cond) {
    stop(paste(conditionMessage(cond)))
  })

  # Status code 400 indicates that the aircraft_id was invalid.
  # In that case return an empty list. Note that this case is caught earlier.
  if (httr::status_code(response) == 400)
    stop(paste("Invalid aircraft ID:", aircraft_id))

  # Status code 404 indicates that the aircraft_id was not matched to an
  # aircraft in the simulation. In that case return a list with an 'acid'
  # element and a 'route' element containing an NA value.
  if (httr::status_code(response) == config_param("status_code_aircraft_id_not_found")) {
    ret <- list(aircraft_id, NA); names(ret) <- c('acid', 'route')
    return(ret)
  }

  # Status code 500 indicates that route data could not be parsed, or the
  # specified aircraft has no route. In the latter case, return a list with an
  # 'acid' element and a 'route' element containing an empty list. Otherwise
  # throw an exception.
  if (httr::status_code(response) == 500) {
    content <- httr::content(response)
    if (!stringr::str_detect(content, config_param("err_msg_aircraft_has_no_route")))
      stop(content)
    ret <- list(aircraft_id, list()); names(ret) <- c('acid', 'route')
    return(ret)
  }

  validate_response(response)
  jsonlite::fromJSON(httr::content(response, "text"), simplifyVector = FALSE)
}

# Process the parsed route JSON and return a data frame containing a row for
# each waypoint. If the 'route' element is NA, indicating that the aircraft
# was not found in the simulation, throw an exception. If the 'route' element
# is an empty list, indicating that the corresponding aircraft has no route,
# return an empty data frame.
process_parsed_route <- function(parsed_list) {

  # Get the aircraft ID.
  stopifnot('acid' %in% names(parsed_list))
  aircraft_id <- parsed_list[[config_param("query_aircraft_id")]]

  # Handle the case that 'route' element is NA (aircraft ID not found).
  if (length(parsed_list[['route']]) == 1 && is.na(parsed_list[['route']]))
    stop(paste("aircraft not found:", aircraft_id))

  # Handle the case that the 'route' element is an empty list (aircraft has no
  # route). Note that no simulator time information is returned in this case.
  if (length(parsed_list[['route']]) == 0)
    return(process_parsed_waypoint(list()))

  # Pull out the simulator time attribute.
  sim_t <- parsed_list[[config_param("simulator_time")]]

  # Process each waypoint sublist and bind the rows of the resulting data frames.
  dfs <- purrr::map(parsed_list[['route']], .f = process_parsed_waypoint)
  ret <- Reduce(f = rbind, x = dfs)

  # Add the simulator time attribute
  attr(ret, which = config_param("simulator_time")) <- sim_t
  ret
}

# Process the parsed route JSON for a single waypoint and return a data
# frame containing a single row, named by the waypoint name.
process_parsed_waypoint <- function(parsed) {

  stopifnot(is.list(parsed))

  # TODO: replace string literals with config parameters from Bluebird.
  expected_names <- c("wpt_name", "req_alt", "req_spd", "is_current")
  new_names <- c("waypoint_name", "requested_altitude", "requested_speed", "current")
  ret_names <- setdiff(new_names, 'waypoint_name')

  # Handle the case that parsed is empty. In that case return an empty data
  # frame, with the expected column names.
  if (length(parsed) == 0)
    return(data.frame(matrix(nrow = 0, ncol = length(ret_names),
                             dimnames = list(c(), ret_names))))

  stopifnot(all(expected_names %in% names(parsed)))
  #stopifnot(!any(purrr::map_lgl(parsed, .f = is.null)))

  # Rename the elements.
  parsed <- parsed[expected_names]
  names(parsed) <- new_names

  # Replace any NULL values with NAs.
  sink <- purrr::map(names(parsed), .f = function(x) {
    if (is.null(parsed[[x]]))
      parsed[[x]] <<- NA
  })

  # Get the waypoint name.
  waypoint_name <- parsed[['waypoint_name']]

  # Convert to a data frame, omitting the waypoint_name.
  ret <- as.data.frame(parsed[ret_names], stringsAsFactors = FALSE)
  rownames(ret) <- waypoint_name
  ret
}

