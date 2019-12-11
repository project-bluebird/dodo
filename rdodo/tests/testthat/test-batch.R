require(testthat)
context("batch function")

skip_if_not(found_bluebird(), message = "BlueBird not found: tests skipped.")

# Reset the simulation to ensure no aircraft exist initially.
reset_simulation()

test_that("the batch function works", {

  aircraft_id <- "test-batch"
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

  # Execute several commands in series.
  t_start_series <- as.numeric(Sys.time())

  expect_true(change_altitude(aircraft_id, flight_level = 220))
  expect_true(change_altitude(aircraft_id, flight_level = 240))
  expect_true(change_altitude(aircraft_id, flight_level = 260))
  expect_true(change_altitude(aircraft_id, flight_level = 280))
  expect_true(change_altitude(aircraft_id, flight_level = 300))

  dt_series <- as.numeric(Sys.time()) - t_start_series

  # Execute the same commands synchronously using the batch function.
  t_start_sync <- as.numeric(Sys.time())

  result <- batch(
    change_altitude(aircraft_id = aircraft_id, flight_level = 220),
    change_altitude(aircraft_id = aircraft_id, flight_level = 240),
    change_altitude(aircraft_id = aircraft_id, flight_level = 260),
    change_altitude(aircraft_id = aircraft_id, flight_level = 280),
    change_altitude(aircraft_id = aircraft_id, flight_level = 300),
    async = FALSE)

  dt_sync <- as.numeric(Sys.time()) - t_start_sync
  expect_true(all(unlist(result)))

  # Execute the same commands asynchronously using the batch function.
  t_start_async <- as.numeric(Sys.time())

  result <- batch(
    change_altitude(aircraft_id = aircraft_id, flight_level = 220),
    change_altitude(aircraft_id = aircraft_id, flight_level = 240),
    change_altitude(aircraft_id = aircraft_id, flight_level = 260),
    change_altitude(aircraft_id = aircraft_id, flight_level = 280),
    change_altitude(aircraft_id = aircraft_id, flight_level = 300),
    async = TRUE)

  dt_async <- as.numeric(Sys.time()) - t_start_async
  expect_true(all(unlist(result)))

  # Test that the time taken to execute the calls made in series is approximately
  # equal to the time taken to execute the synchronous calls.
  expect_equal(dt_series, expected = dt_sync, tolerance = 0.1, scale = dt_sync)

  # Test that the time taken to execute the asynchronous calls is less than
  # half that for the synchronous calls.
  expect_true(dt_async < dt_sync)
})

test_that("the batch function handles errors correctly", {

  aircraft_id <- "test-batch-errors"
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

  # Execute a batch of commands asynchronously.
  result <- batch(
    change_altitude(aircraft_id = aircraft_id, flight_level = 220),
    change_altitude(aircraft_id = aircraft_id, flight_level = 240),
    change_altitude(aircraft_id = aircraft_id, flight_level = 260),
    change_altitude(aircraft_id = aircraft_id, flight_level = 280),
    change_altitude(aircraft_id = aircraft_id, flight_level = 300),
    async = TRUE)

  expect_true(all(unlist(result)))

  # Expect an error if a command has an invalid parameter.
  expect_error(result <<- batch(
    change_altitude(aircraft_id = aircraft_id, flight_level = 220),
    change_altitude(aircraft_id = aircraft_id, flight_level = 240),
    change_altitude(aircraft_id = aircraft_id, flight_level = 260),
    change_altitude(aircraft_id = aircraft_id, flight_level = -10),
    change_altitude(aircraft_id = aircraft_id, flight_level = 300),
    async = TRUE), regexp = "flight_level_lower_limit")

  expect_error(result <<- batch(
    change_altitude(aircraft_id = aircraft_id, flight_level = 220),
    change_altitude(aircraft_id = "INVALID_ID", flight_level = 240),
    change_altitude(aircraft_id = aircraft_id, flight_level = 260),
    change_altitude(aircraft_id = aircraft_id, flight_level = 280),
    change_altitude(aircraft_id = aircraft_id, flight_level = 300),
    async = TRUE), regexp = "INVALID_ID not found")

  # Expect an error if two commands have an invalid parameter.
  expect_error(result <<- batch(
    change_altitude(aircraft_id = aircraft_id, flight_level = 220),
    change_altitude(aircraft_id = "INVALID_ID", flight_level = 240),
    change_altitude(aircraft_id = aircraft_id, flight_level = 260),
    change_altitude(aircraft_id = aircraft_id, flight_level = -10),
    change_altitude(aircraft_id = aircraft_id, flight_level = 300),
    async = TRUE), regexp = "INVALID_ID not found.*;.*flight_level_lower_limit")
})
