#' Get aircraft position
#'
#' Get the position of a single or multiple aircraft based on their IDs, or
#' positions of all aircraft in the simulation.
#'
#' @param aircraft_id
#' (Optional) Single aircraft ID, or a vector of aircraft IDs. If no ID is
#' supplied, returns positions of all aircraft in the simulation. Each aircraft
#' ID is a string.
#'
#' @return
#' A list of aircraft positions as a data frame with one row per aircraft. The
#' row names are aircraft IDs. If any of the given aircraft IDs does not exist
#' in the simulation, the returned dataframe contains a row of missing (NA)
#' values for that ID. If \code{aircraft_id} is NULL (or omitted) and no
#' aircraft exist in the simulation, an empty data frame is returned.
#'
#' @examples
#' \dontrun{
#' aircraft_position('ABC123')
#' aircraft_position(c('ABC123', 'DEF456'))
#' aircraft_position()
#' }
#'
#' @import purrr
#'
#' @export
aircraft_position <- function(aircraft_id = NULL) {

  # Keep track of the requested (uppercase) aircraft ID(s).
  aircraft_ids <- toupper(aircraft_id)

  # If aircraft_id is a vector, get all aircraft positions and filter.
  if (length(aircraft_id) > 1)
    aircraft_id <- NULL

  parsed_list <- position_call(aircraft_id)
  ret <- process_parsed_positions(parsed_list)

  # If no particular aircraft_ids were specified, return all aircraft positions.
  if (length(aircraft_ids) == 0)
    return(ret)

  # Add a row of NAs for any missing aircraft_ids.
  missing_ids <- setdiff(aircraft_ids, rownames(ret))
  if (length(missing_ids) != 0)
    sink <- purrr::map(missing_ids, .f = function(id) {
      ret[id, ] <<- NA
    })

  # Filter the data frame to include only the requested aircraft IDs.
  ret[aircraft_ids, ]
}

# Process the list of parsed position JSONs (for multiple aircraft) and return a
# data frame containing a row for each of them, named by the aircraft ID.
#' @import units
process_parsed_positions <- function(parsed_list) {

  # TODO: the simulator_time attribute is lost in this case:
  # Handle the case that parsed_list is empty, indicating the call came from the
  # all_positions function and no aircraft were found. In this case return an
  # empty dataframe.
  if (length(parsed_list) == 0)
    return(process_parsed_position(list(), aircraft_id = "DUMMY")[-1, ])

  # Pull out the simulator time attribute, then remove it from the list.
  sim_t <- parsed_list[[config_param("simulator_time")]]
  if (is.null(sim_t))
    sim_t <- NA
  parsed_list[[config_param("simulator_time")]] <- NULL

  # Process each position sublist and bind the rows of the resulting data frames.
  dfs <- purrr::map2(parsed_list, names(parsed_list), .f = process_parsed_position)
  ret <- Reduce(f = rbind, x = dfs)

  # Assign units (according to the Bluebird specification).
  ret <- assign_position_units(ret)

  # Normalise units (according to the Dodo specification).
  ret <- normalise_position_units(ret)

  # Add the simulator time attribute (with units).
  units(sim_t) <- with(units::ud_units, s)
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
  expected_names <- c("actype", "current_fl", "cleared_fl", "requested_fl",
                "gs", "hdg", "lat", "lon", "vs")
  new_names <- c(config_param("aircraft_type"),
                 config_param("current_flight_level"),
                 config_param("cleared_flight_level"),
                 config_param("requested_flight_level"),
                 config_param("ground_speed"),
                 config_param("heading"),
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

  # Replace any NULL flight level values with NA.
  if (is.null(parsed[[config_param("cleared_flight_level")]]))
    parsed[[config_param("cleared_flight_level")]] <- NA
  if (is.null(parsed[[config_param("requested_flight_level")]]))
    parsed[[config_param("requested_flight_level")]] <- NA

  # Convert to a data frame.
  ret <- as.data.frame(parsed[new_names], stringsAsFactors = FALSE)
  rownames(ret) <- aircraft_id

  ret
}

# Assign appropriate units to a data frame of aircraft position information
# received from Bluebird. These are the units specified in the Bluebird API
# (see API.md) at https://github.com/alan-turing-institute/bluebird/.
#' @import units
assign_position_units <- function(df) {

  stopifnot(is.data.frame(df))

  # Assign ground speed units (m/s).
  units(df[, config_param("ground_speed")]) <- with(units::ud_units, m/s)

  # Assign vertical speed units (ft/min).
  units(df[, config_param("vertical_speed")]) <- with(units::ud_units, ft/min)

  df
}

# Normalise units of measurement in the positions data.
#' @import units
normalise_position_units <- function(df) {

  # Check that the relevants columns already have units assigned.
  stopifnot(inherits(df[, config_param("ground_speed")], "units"))
  stopifnot(inherits(df[, config_param("vertical_speed")], "units"))

  # Convert units as necessary
  units(df[, config_param("ground_speed")]) <- with(units::ud_units, "knot")
  units(df[, config_param("vertical_speed")]) <- with(units::ud_units, ft/min)

  df
}

