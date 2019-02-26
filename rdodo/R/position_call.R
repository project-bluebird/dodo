#' Make a call to the aircraft position endpoint
#'
#' @param aircraft_id
#' A string aircraft identifier. If this aircraft does not exist an exception
#' will be thrown.
#'
#' @return
#' A list of aircraft position information.
#'
#' @examples
#' \dontrun{
#' position_call('ABC123')
#' }
#'
#' @import config httr jsonlite
#' @export
position_call <- function(aircraft_id) {

  stopifnot(is.character(aircraft_id), length(aircraft_id) == 1)

  endpoint <- config::get("endpoint_aircraft_position")
  query <- list(aircraft_id)
  names(query) <- config::get("query_aircraft_id")
  response <- tryCatch({
    response <- httr::GET(url = construct_endpoint_url(endpoint, query = query))
  },
  error=function(cond) {
    stop(paste(conditionMessage(cond)))
  })

  validate_response(response)
  jsonlite::fromJSON(httr::content(response, "text"), simplifyVector = FALSE)
}

# Process the parsed position JSON for a single aircraft and return a data
# frame containing a single row, named by the aircraft ID.
process_parsed_position <- function(parsed, aircraft_id) {

  stopifnot(is.list(parsed))

  # TODO: hard-coded element names.
  expected_names <- c("alt", "gs", "lat", "lon", "vs")
  new_names <- c("altitude", "ground_speed", "latitude", "longitude", "vertical_speed")

  stopifnot(all(expected_names %in% names(parsed)))

  # Rename the elements.
  parsed <- parsed[expected_names]
  names(parsed) <- new_names

  # Convert to a data frame.
  ret <- as.data.frame(parsed[new_names])
  rownames(ret) <- aircraft_id
  ret
}

# Process the parsed position JSON for multiple aircraft and return a data
# frame containing a row for each of them, named by the aircraft ID.
process_parsed_positions <- function(parsed) {

  # Process each position list and bind the rows of the resulting data frames.
  Reduce(f = rbind,
         x = purrr::map2(parsed, names(parsed), .f = process_parsed_position))
}
