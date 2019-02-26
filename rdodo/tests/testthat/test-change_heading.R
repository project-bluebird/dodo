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

  # TODO: replace hard-coded string "heading" with config parameter (see also
  # other list elements in aircraft_position):

  # Check the heading.
  position <- aircraft_position(aircraft_id)
  expect_identical(object = position[aircraft_id, "longitude"], expected = 0)

  # Give the command to change heading.
  new_heading <- 90
  expect_true(change_heading(aircraft_id = aircraft_id, heading = new_heading))

  # Check that the heading has changed.
  new_position <- aircraft_position(aircraft_id)
  expect_true(new_position[aircraft_id, "longitude"] > 0)
})
