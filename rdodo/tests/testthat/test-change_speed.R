require(testthat)
context("change_speed function")

skip_if_not(found_bluebird(), message = "BlueBird not found: tests skipped.")

# Reset the simulation to ensure no aircraft exist initially.
reset_simulation()

test_that("the change_speed function works", {

  aircraft_id <- "test-change-speed"
  type <- "B744"
  latitude <- 0
  longitude <- 0
  heading <- 0
  flight_level <- 250
  speed <- 265

  # Create an aircraft.
  expect_true(create_aircraft(aircraft_id = aircraft_id,
                              type = type,
                              latitude = latitude,
                              longitude = longitude,
                              heading = heading,
                              flight_level = flight_level,
                              speed = speed))

  # TODO: replace hard-coded string "speed" with config parameter (see also
  # other list elements in aircraft_position):

  # Check the speed.
  position <- aircraft_position(aircraft_id)

  # In the returned data frame aircraft_id is uppercase.
  aircraft_id <- toupper(aircraft_id)

  # Aircaft initial speed differs from specified speed.
  expect_true(position[aircraft_id, "ground_speed"] < 198)

  # Test with an invalid speed.
  invalid_speed <- -1
  expect_error(change_speed(aircraft_id = aircraft_id, speed = invalid_speed))

  expect_true(position[aircraft_id, "ground_speed"] < 198)

  # Give the command to change speed.
  new_speed <- 400
  expect_true(change_speed(aircraft_id = aircraft_id, speed = new_speed))

  # Wait for the ground speed to increase.
  Sys.sleep(0.5)

  # Check that the speed has changed.
  new_position <- aircraft_position(aircraft_id)
  expect_true(new_position[aircraft_id, "ground_speed"] > 198)
})