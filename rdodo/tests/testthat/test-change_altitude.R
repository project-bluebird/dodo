require(testthat)
context("change_altitude function")

skip_if_not(found_bluebird(), message = "BlueBird not found: tests skipped.")

# Reset the simulation to ensure no aircraft exist initially.
reset_simulation()

test_that("the change_altitude function works", {

  aircraft_id <- "test-change-altitude"
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

  # Check the altitude.
  position <- aircraft_position(aircraft_id)
  h_altitude <- config_param("altitude")

  expect_equal(object = position[aircraft_id, h_altitude],
               expected = flight_level * 100)

  # Give the command to ascend.
  new_flight_level <- 450
  expect_true(change_altitude(aircraft_id = aircraft_id,
                              flight_level = new_flight_level))

  # Wait for the altitude to increase.
  expect_true(wait(aircraft_id, property = h_altitude, operator = `>`,
       initial_value = flight_level * 100))

  # Check that the new altitude exceeds the original one.
  new_position <- aircraft_position(aircraft_id)
  expect_true(new_position[aircraft_id, h_altitude] > flight_level * 100)
})

test_that("the change_altitude function's altitude/flight level guard clause works", {

  aircraft_id <- "test-change-altitude"
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

  # Give the command to ascend with both a flight level and an altitude.
  new_flight_level <- 450
  new_altitude <- 30000
  expect_error(change_altitude(aircraft_id = aircraft_id,
                               altitude = new_altitude,
                               flight_level = new_flight_level))
})
