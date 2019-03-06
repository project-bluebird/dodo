require(testthat)
context("position_call function")

skip_if_not(found_bluebird(), message = "BlueBird not found: tests skipped.")

# Reset the simulation to ensure no aircraft exist initially.
reset_simulation()

test_that("the position_call function works with an invalid aircraft ID", {

  # Missing aircraft_id (i.e. not found in the simulation).
  invalid_id <- "NoSuchAircraft"

  # Expect an empty list.
  expect_identical(position_call(invalid_id), expected = list())
})

test_that("the position_call function works with a valid aircraft ID", {

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

  # Get its position.
  result <- position_call(aircraft_id)

  expect_true(is.list(result))
  expected <- c("alt", "gs", "lat", "lon", "vs")
  expect_true(all(expected %in% names(result)))

  expect_true(object = result[["lat"]] > 0)
  expect_identical(object = result[["lon"]], expected = 0)
  expect_identical(object = result[["vs"]], expected = 0)
})
