require(testthat)
context("aircraft_position function")

skip_if_not(found_bluebird(), message = "BlueBird not found: tests skipped.")

# Reset the simulation to ensure no aircraft exist initially.
reset_simulation()

test_that("the aircraft_position function works with invalid aircraft ID", {

  invalid_id <- "NoSuchAircraft"

  # Get its position.
  result <- aircraft_position(invalid_id)

  # In the returned data frame aircraft_id is uppercase.
  invalid_id <- toupper(invalid_id)

  expect_true(is.data.frame(result))
  expect_identical(object = nrow(result), expected = 1L)
  expect_identical(object = rownames(result), invalid_id)
  expected <- c(config_param("aircraft_type"),
                config_param("current_flight_level"),
                config_param("cleared_flight_level"),
                config_param("requested_flight_level"),
                config_param("ground_speed"),
                config_param("heading"),
                config_param("latitude"),
                config_param("longitude"),
                config_param("vertical_speed"))
  expect_identical(object = colnames(result), expected = expected)

  # Expect a row of NAs in the data frame.
  expect_true(is.na(result[invalid_id, config_param("aircraft_type")]))
  expect_true(is.na(result[invalid_id, config_param("current_flight_level")]))
  expect_true(is.na(result[invalid_id, config_param("cleared_flight_level")]))
  expect_true(is.na(result[invalid_id, config_param("requested_flight_level")]))
  expect_true(is.na(result[invalid_id, config_param("ground_speed")]))
  expect_true(is.na(result[invalid_id, config_param("latitude")]))
  expect_true(is.na(result[invalid_id, config_param("longitude")]))
  expect_true(is.na(result[invalid_id, config_param("vertical_speed")]))

  # Check the simulator time attribute doesn't exist.
  expect_true(is.na(attr(result, which = config_param("simulator_time"))))

  # Expect appropriate units (according to the Dodo specification).
  expect_true(inherits(result[, config_param("ground_speed")], "units"))
  expect_equal(units(result[, config_param("ground_speed")])[["numerator"]],
               expected = "knot")
  expect_equal(units(result[, config_param("ground_speed")])[["denominator"]],
               expected = character(0))

  expect_true(inherits(result[, config_param("vertical_speed")], "units"))
  expect_equal(units(result[, config_param("vertical_speed")])[["numerator"]],
               expected = "ft")
  expect_equal(units(result[, config_param("vertical_speed")])[["denominator"]],
               expected = "min")
})

test_that("the aircraft_position function works with scalar argument", {

  aircraft_id <- "testAircraftPosition"
  type <- "B744"
  latitude <- 0
  longitude <- 0
  heading <- 0
  flight_level <- 250
  speed <- 200

  # Create an aircraft.
  expect_true(create_aircraft(aircraft_id = aircraft_id,
                              type = type,
                              latitude = latitude,
                              longitude = longitude,
                              heading = heading,
                              flight_level = flight_level,
                              speed = speed))

  # In the returned data frame aircraft_id is uppercase.
  aircraft_id <- toupper(aircraft_id)

  # Get its position.
  result <- aircraft_position(aircraft_id)

  expect_true(is.data.frame(result))
  expect_identical(object = nrow(result), expected = 1L)
  expect_identical(object = rownames(result), expected = aircraft_id)
  expected <- c(config_param("aircraft_type"),
                config_param("current_flight_level"),
                config_param("cleared_flight_level"),
                config_param("requested_flight_level"),
                config_param("ground_speed"),
                config_param("heading"),
                config_param("latitude"),
                config_param("longitude"),
                config_param("vertical_speed"))
  expect_identical(object = colnames(result), expected = expected)

  # Aircaft initial speed may differ from specified speed.
  expect_true(result[aircraft_id, config_param("ground_speed")] >
                units::set_units(150, m/s))

  expect_true(object = result[aircraft_id, config_param("latitude")] > 0)
  expect_equal(object = result[aircraft_id, config_param("longitude")],
                   expected = 0)
  expect_equal(object = result[aircraft_id, config_param("vertical_speed")],
                   expected = 0)

  # Check the simulator time attribute exists.
  sim_time <- attr(result, which = config_param("simulator_time"))
  expect_true(!is.null(sim_time))
  expect_true(is.numeric(sim_time))
  expect_true(sim_time >= units::set_units(0, s))

  # Expect appropriate units (according to the Dodo specification).
  expect_true(inherits(result[, config_param("ground_speed")], "units"))
  expect_equal(units(result[, config_param("ground_speed")])[["numerator"]],
               expected = "knot")
  expect_equal(units(result[, config_param("ground_speed")])[["denominator"]],
               expected = character(0))

  expect_true(inherits(result[, config_param("vertical_speed")], "units"))
  expect_equal(units(result[, config_param("vertical_speed")])[["numerator"]],
               expected = "ft")
  expect_equal(units(result[, config_param("vertical_speed")])[["denominator"]],
               expected = "min")

  expect_true(inherits(sim_time, "units"))
  expect_equal(units(sim_time)[["numerator"]], expected = "s")
  expect_equal(units(sim_time)[["denominator"]], expected = character(0))
})

test_that("the aircraft_position function works with a vector argument", {

  # Create two aircraft.
  aircraft_id_1 <- "testAircraftPosition1"
  type_1 <- "B744"
  latitude_1 <- 0
  longitude_1 <- 0
  heading_1 <- 0
  flight_level_1 <- 250
  speed_1 <- 200

  expect_true(create_aircraft(aircraft_id = aircraft_id_1,
                              type = type_1,
                              latitude = latitude_1,
                              longitude = longitude_1,
                              heading = heading_1,
                              flight_level = flight_level_1,
                              speed = speed_1))

  aircraft_id_2 <- "testAircraftPosition2"
  type_2 <- "C744"
  latitude_2 <- 0
  longitude_2 <- 0
  heading_2 <- 180
  flight_level_2 <- 300
  speed_2 <- 220

  expect_true(create_aircraft(aircraft_id = aircraft_id_2,
                              type = type_2,
                              latitude = latitude_2,
                              longitude = longitude_2,
                              heading = heading_2,
                              flight_level = flight_level_2,
                              speed = speed_2))

  # Get their positions.
  result <- aircraft_position(c(aircraft_id_1, aircraft_id_2))

  # In the returned data frame aircraft_ids are uppercase.
  aircraft_id_1 <- toupper(aircraft_id_1)
  aircraft_id_2 <- toupper(aircraft_id_2)

  expect_true(is.data.frame(result))
  expect_identical(object = nrow(result), expected = 2L)
  expect_identical(object = rownames(result),
                   expected = c(aircraft_id_1, aircraft_id_2))
  expected <- c(config_param("aircraft_type"),
                config_param("current_flight_level"),
                config_param("cleared_flight_level"),
                config_param("requested_flight_level"),
                config_param("ground_speed"),
                config_param("heading"),
                config_param("latitude"),
                config_param("longitude"),
                config_param("vertical_speed"))
  expect_identical(object = colnames(result), expected = expected)

  # Check aircraft_id_1 entries.
  # Aircaft initial speed may differ from specified speed.
  expect_true(result[aircraft_id_1, config_param("ground_speed")] >
                units::set_units(150, m/s))

  expect_true(object = result[aircraft_id_1, config_param("latitude")] > 0)
  expect_equal(object = result[aircraft_id_1, config_param("longitude")],
                   expected = 0)
  expect_equal(object = result[aircraft_id_1, config_param("vertical_speed")],
                   expected = 0)

  # Check aircraft_id_2 entries.
  # Aircaft initial speed may differ from specified speed.
  expect_true(result[aircraft_id_2, config_param("ground_speed")] >
                units::set_units(150, m/s))

  expect_true(object = result[aircraft_id_2, config_param("latitude")] < 0)
  expect_equal(object = result[aircraft_id_2, config_param("longitude")],
               expected = 0, tolerance = 10^(-10))
  expect_equal(object = result[aircraft_id_2, config_param("vertical_speed")],
                   expected = 0)

  # Check the simulator time attribute exists.
  sim_time <- attr(result, which = config_param("simulator_time"))
  expect_true(!is.null(sim_time))
  expect_true(is.numeric(sim_time))
  expect_true(sim_time >= units::set_units(0, s))

  # Expect appropriate units (according to the Dodo specification).
  expect_true(inherits(result[, config_param("ground_speed")], "units"))
  expect_equal(units(result[, config_param("ground_speed")])[["numerator"]],
               expected = "knot")
  expect_equal(units(result[, config_param("ground_speed")])[["denominator"]],
               expected = character(0))

  expect_true(inherits(result[, config_param("vertical_speed")], "units"))
  expect_equal(units(result[, config_param("vertical_speed")])[["numerator"]],
               expected = "ft")
  expect_equal(units(result[, config_param("vertical_speed")])[["denominator"]],
               expected = "min")

  expect_true(inherits(sim_time, "units"))
  expect_equal(units(sim_time)[["numerator"]], expected = "s")
  expect_equal(units(sim_time)[["denominator"]], expected = character(0))

  ###
  ### Test with a vector argument including both valid and only invalid IDs.
  ###
  invalid_id <- "NoSuchAircraft"
  aircraft_id <- c(aircraft_id_1, invalid_id, aircraft_id_2)
  result <- aircraft_position(aircraft_id)

  # In the returned data frame aircraft_id is uppercase.
  invalid_id <- toupper(invalid_id)

  expect_true(is.data.frame(result))
  expect_identical(object = nrow(result), expected = 3L)
  expect_identical(object = rownames(result),
                   expected = c(aircraft_id_1, invalid_id, aircraft_id_2))
  expected <- c(config_param("aircraft_type"),
                config_param("current_flight_level"),
                config_param("cleared_flight_level"),
                config_param("requested_flight_level"),
                config_param("ground_speed"),
                config_param("heading"),
                config_param("latitude"),
                config_param("longitude"),
                config_param("vertical_speed"))
  expect_identical(object = colnames(result), expected = expected)

  # Expect a row of NAs in the data frame for the invalid ID only.
  expect_true(is.na(result[invalid_id, config_param("aircraft_type")]))
  expect_true(is.na(result[invalid_id, config_param("current_flight_level")]))
  expect_true(is.na(result[invalid_id, config_param("cleared_flight_level")]))
  expect_true(is.na(result[invalid_id, config_param("requested_flight_level")]))
  expect_true(is.na(result[invalid_id, config_param("ground_speed")]))
  expect_true(is.na(result[invalid_id, config_param("latitude")]))
  expect_true(is.na(result[invalid_id, config_param("longitude")]))
  expect_true(is.na(result[invalid_id, config_param("vertical_speed")]))

  # Expect NAs only in the cleared and requested flight level columns for the
  # valid aircraft IDs.
  expect_false(is.na(result[aircraft_id_1, config_param("aircraft_type")]))
  expect_false(is.na(result[aircraft_id_1, config_param("current_flight_level")]))

  expect_true(is.na(result[aircraft_id_1, config_param("cleared_flight_level")]))
  expect_true(is.na(result[aircraft_id_1, config_param("requested_flight_level")]))

  expect_false(is.na(result[aircraft_id_1, config_param("ground_speed")]))
  expect_false(is.na(result[aircraft_id_1, config_param("heading")]))
  expect_false(is.na(result[aircraft_id_1, config_param("latitude")]))
  expect_false(is.na(result[aircraft_id_1, config_param("longitude")]))
  expect_false(is.na(result[aircraft_id_1, config_param("vertical_speed")]))

  expect_false(is.na(result[aircraft_id_2, config_param("aircraft_type")]))
  expect_false(is.na(result[aircraft_id_2, config_param("current_flight_level")]))

  expect_true(is.na(result[aircraft_id_2, config_param("cleared_flight_level")]))
  expect_true(is.na(result[aircraft_id_2, config_param("requested_flight_level")]))

  expect_false(is.na(result[aircraft_id_2, config_param("ground_speed")]))
  expect_false(is.na(result[aircraft_id_1, config_param("heading")]))
  expect_false(is.na(result[aircraft_id_2, config_param("latitude")]))
  expect_false(is.na(result[aircraft_id_2, config_param("longitude")]))
  expect_false(is.na(result[aircraft_id_2, config_param("vertical_speed")]))

  # Check the simulator time attribute exists.
  sim_time <- attr(result, which = config_param("simulator_time"))
  expect_true(!is.null(sim_time))
  expect_true(is.numeric(sim_time))
  expect_true(sim_time >= units::set_units(0, s))

  # Expect appropriate units (according to the Dodo specification).
  expect_true(inherits(result[, config_param("ground_speed")], "units"))
  expect_equal(units(result[, config_param("ground_speed")])[["numerator"]],
               expected = "knot")
  expect_equal(units(result[, config_param("ground_speed")])[["denominator"]],
               expected = character(0))

  expect_true(inherits(result[, config_param("vertical_speed")], "units"))
  expect_equal(units(result[, config_param("vertical_speed")])[["numerator"]],
               expected = "ft")
  expect_equal(units(result[, config_param("vertical_speed")])[["denominator"]],
               expected = "min")

  expect_true(inherits(sim_time, "units"))
  expect_equal(units(sim_time)[["numerator"]], expected = "s")
  expect_equal(units(sim_time)[["denominator"]], expected = character(0))
})

# Reset the simulation to ensure no aircraft exist initially.
reset_simulation()

test_that("the aircraft_position function works with no argument", {

  # Get all aircraft positions.
  result <- aircraft_position()

  # Check that the result is an empty data frame with the expected columns.
  expect_true(is.data.frame(result))
  expect_identical(object = nrow(result), expected = 0L)
  expected <- c(config_param("aircraft_type"),
                config_param("current_flight_level"),
                config_param("cleared_flight_level"),
                config_param("requested_flight_level"),
                config_param("ground_speed"),
                config_param("heading"),
                config_param("latitude"),
                config_param("longitude"),
                config_param("vertical_speed"))
  expect_identical(object = colnames(result), expected = expected)

  # Create an aircraft.
  aircraft_id_1 <- "testAircraftPositionAll1"
  type_1 <- "B744"
  latitude_1 <- 0
  longitude_1 <- 0
  heading_1 <- 0
  flight_level_1 <- 250
  speed_1 <- 200

  expect_true(create_aircraft(aircraft_id = aircraft_id_1,
                              type = type_1,
                              latitude = latitude_1,
                              longitude = longitude_1,
                              heading = heading_1,
                              flight_level = flight_level_1,
                              speed = speed_1))

  # Get all aircraft positions.
  result <- aircraft_position()

  # In the returned data frame aircraft_id is uppercase.
  aircraft_id_1 <- toupper(aircraft_id_1)

  expect_true(is.data.frame(result))
  expect_identical(object = nrow(result), expected = 1L)
  expect_identical(object = rownames(result), expected = aircraft_id_1)
  expected <- c(config_param("aircraft_type"),
                config_param("current_flight_level"),
                config_param("cleared_flight_level"),
                config_param("requested_flight_level"),
                config_param("ground_speed"),
                config_param("heading"),
                config_param("latitude"),
                config_param("longitude"),
                config_param("vertical_speed"))
  expect_identical(object = colnames(result), expected = expected)

  # Create a second aircraft.
  aircraft_id_2 <- "testAircraftPositionAll2"
  type_2 <- "C744"
  latitude_2 <- 0
  longitude_2 <- 0
  heading_2 <- 180
  flight_level_2 <- 300
  speed_2 <- 220

  expect_true(create_aircraft(aircraft_id = aircraft_id_2,
                              type = type_2,
                              latitude = latitude_2,
                              longitude = longitude_2,
                              heading = heading_2,
                              flight_level = flight_level_2,
                              speed = speed_2))

  # Get all aircraft positions.
  result <- aircraft_position()

  # In the returned data frame aircraft_ids are uppercase.
  aircraft_id_1 <- toupper(aircraft_id_1)
  aircraft_id_2 <- toupper(aircraft_id_2)

  expect_true(is.data.frame(result))
  expect_identical(object = nrow(result), expected = 2L)
  expect_identical(object = rownames(result),
                   expected = c(aircraft_id_1, aircraft_id_2))
  expected <- c(config_param("aircraft_type"),
                config_param("current_flight_level"),
                config_param("cleared_flight_level"),
                config_param("requested_flight_level"),
                config_param("ground_speed"),
                config_param("heading"),
                config_param("latitude"),
                config_param("longitude"),
                config_param("vertical_speed"))
  expect_identical(object = colnames(result), expected = expected)

  # Check the simulator time attribute exists.
  sim_time <- attr(result, which = config_param("simulator_time"))
  expect_true(!is.null(sim_time))
  expect_true(is.numeric(sim_time))
  expect_true(sim_time >= units::set_units(0, s))

  # Expect appropriate units (according to the Dodo specification).
  expect_true(inherits(result[, config_param("ground_speed")], "units"))
  expect_equal(units(result[, config_param("ground_speed")])[["numerator"]],
               expected = "knot")
  expect_equal(units(result[, config_param("ground_speed")])[["denominator"]],
               expected = character(0))

  expect_true(inherits(result[, config_param("vertical_speed")], "units"))
  expect_equal(units(result[, config_param("vertical_speed")])[["numerator"]],
               expected = "ft")
  expect_equal(units(result[, config_param("vertical_speed")])[["denominator"]],
               expected = "min")

  expect_true(inherits(sim_time, "units"))
  expect_equal(units(sim_time)[["numerator"]], expected = "s")
  expect_equal(units(sim_time)[["denominator"]], expected = character(0))
})

