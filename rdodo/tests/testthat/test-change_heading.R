require(testthat)
context("change_heading function")

skip_if_not(found_bluebird(), message = "BlueBird not found: tests skipped.")

# Reset the simulation to ensure no aircraft exist initially.
reset_simulation()

test_that("the change_heading function works", {

  aircraft_id <- "test-change-heading"
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

  # Check the heading.
  position <- aircraft_position(aircraft_id)
  h_longitude <- config_param("longitude")

  # Test with an invalid heading.
  invalid_heading <- 400
  expect_error(change_heading(aircraft_id = aircraft_id, heading = invalid_heading))

  # Confirm the longitude hasn't changed (implying no change of heading yet).
  expect_equal(object = position[aircraft_id, h_longitude], expected = 0)

  # Give the command to change heading.
  new_heading <- 90
  expect_true(change_heading(aircraft_id = aircraft_id, heading = new_heading))

  # Wait for the aircraft's longitude to change.
  expect_true(wait(aircraft_id, property = h_longitude, operator = `>`,
                   initial_value = 0))

  # Check that the londitude has changed (implying a change of heading).
  new_position <- aircraft_position(aircraft_id)
  expect_true(new_position[aircraft_id, h_longitude] > 0)
})
